import asyncio
import ydb
import ydb.aio
from enum import Enum
from typing import Optional, Dict, Any, List
from config import YDB_ENDPOINT, YDB_PATH, YDB_TOKEN
from dataclasses import dataclass
from datetime import datetime, timezone


# yc iam create-token   (12 часов действует)


# ------------------------------------------------------------ Базовый класс -----------------------------------------------------------


class YDBClient:
    def __init__(self, endpoint: str = YDB_ENDPOINT, database: str = YDB_PATH, token: str = YDB_TOKEN):
        """
        Инициализация клиента YDB
        """
        self.endpoint = endpoint
        self.database = database
        self.token = token
        self.driver = None
        self.pool = None
        self.credentials = ydb.AccessTokenCredentials(self.token) # ydb.iam.MetadataUrlCredentials()
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
    
    async def connect(self):
        """
        Создание соединения с YDB и инициализация пула сессий
        """
        if self.driver is not None:
            return  # уже подключены
            
        driver_config = ydb.DriverConfig(
            self.endpoint, 
            self.database,
            credentials=self.credentials,
            root_certificates=ydb.load_ydb_root_certificate(),
        )
        
        self.driver = ydb.aio.Driver(driver_config)
        
        try:
            await self.driver.wait(timeout=5)
            self.pool = ydb.aio.QuerySessionPool(self.driver)
            print("Successfully connected to YDB")
        except TimeoutError:
            print("Connect failed to YDB")
            print("Last reported errors by discovery:")
            print(self.driver.discovery_debug_details())
            await self.driver.stop()
            self.driver = None
            raise
    
    async def close(self):
        """
        Закрытие соединения с YDB
        """
        if self.pool:
            await self.pool.stop()
            self.pool = None
        
        if self.driver:
            await self.driver.stop()
            self.driver = None
            print("YDB connection closed")
    
    def _ensure_connected(self):
        """
        Проверка, что соединение установлено
        """
        if self.driver is None or self.pool is None:
            raise RuntimeError("YDB client is not connected. Call connect() first or use as async context manager.")
    
    async def table_exists(self, table_name: str) -> bool:
        """
        Проверка существования таблицы
        """
        self._ensure_connected()
        try:
            await self.pool.execute_with_retries(f"SELECT 1 FROM `{table_name}` LIMIT 0;")
            return True
        except ydb.GenericError:
            return False
    
    async def create_table(self, table_name: str, schema: str):
        """
        Создание таблицы с заданной схемой (если она не существует)
        """
        self._ensure_connected()
        print(f"\nChecking if table {table_name} exists...")
        try:
            await self.pool.execute_with_retries(schema)
            print(f"Table {table_name} created successfully!")
        except ydb.GenericError as e:
            if "path exist" in str(e):
                print(f"Table {table_name} already exists, skipping creation.")
            else:
                raise e
    
    async def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None):
        """
        Выполнение произвольного запроса
        """
        self._ensure_connected()
        return await self.pool.execute_with_retries(query, params)
    
    async def clear_all_tables(self):
        """Удаляет все записи во всех таблицах"""
        self._ensure_connected()

        tables = [
            "donate_companies",
            "payments",
            "cache"
        ]

        for table in tables:
            try:
                await self.execute_query(f"DELETE FROM `{table}`;")
                print(f"Таблица {table} очищена.")
            except Exception as e:
                print(f"Ошибка при очистке {table}: {e}")


# ------------------------------------------------------------ ДОНАТ КОМПАНИЯ -----------------------------------------------------------


@dataclass
class DonateCompany:
    telegram_id: int
    first_name: Optional[str] = None
    photo_id: Optional[str] = None
    about_company: Optional[str] = None
    link_text: Optional[str] = None
    link: Optional[str] = None
    prices: Optional[str] = None


class DonateCompanyClient(YDBClient):
    def __init__(self, endpoint: str = YDB_ENDPOINT, database: str = YDB_PATH, token: str = YDB_TOKEN):
        super().__init__(endpoint, database, token)
        self.table_name = "donate_companies"
        self.table_schema = """
            CREATE TABLE `donate_companies` (
                `telegram_id` Uint64 NOT NULL,
                `first_name` Utf8,
                `photo_id` Utf8,
                `about_company` Utf8,
                `link_text` Utf8,
                `link` Utf8,
                `prices` Utf8,
                PRIMARY KEY (`telegram_id`)
            )
        """
    
    async def create_companies_table(self):
        """Создание таблицы donate_companies"""
        await self.create_table(self.table_name, self.table_schema)
    
    async def insert_company(self, donate_company: DonateCompany) -> DonateCompany:
        """Вставка или обновление донат компании (UPSERT) и возврат объекта DonateCompany"""
        await self.execute_query(
            """
            DECLARE $telegram_id AS Uint64;
            DECLARE $first_name AS Utf8?;
            DECLARE $photo_id AS Utf8?;
            DECLARE $about_company AS Utf8?;
            DECLARE $link_text AS Utf8?;
            DECLARE $link AS Utf8?;
            DECLARE $prices AS Utf8?;

            UPSERT INTO donate_companies (
                telegram_id, first_name, photo_id, about_company, link_text, link, prices
            ) VALUES (
                $telegram_id, $first_name, $photo_id, $about_company, $link_text, $link, $prices
            );
            """,
            self._to_params(donate_company)
        )
        return await self.get_company_by_id(donate_company.telegram_id)

    async def get_company_by_id(self, telegram_id: int) -> Optional[DonateCompany]:
        """Получение донат компании по telegram_id"""
        result = await self.execute_query(
            """
            DECLARE $telegram_id AS Uint64;

            SELECT telegram_id, first_name, photo_id, about_company, link_text, link, prices
            FROM donate_companies
            WHERE telegram_id = $telegram_id;
            """,
            {"$telegram_id": (telegram_id, ydb.PrimitiveType.Uint64)}
        )

        rows = result[0].rows
        if not rows:
            return None

        return self._row_to_company(rows[0])

    async def update_company(self, donate_company: DonateCompany) -> DonateCompany:
        """Обновление данных донат компании по объекту DonateCompany"""
        await self.execute_query(
            """
            DECLARE $telegram_id AS Uint64;
            DECLARE $first_name AS Utf8?;
            DECLARE $photo_id AS Utf8?;
            DECLARE $about_company AS Utf8?;
            DECLARE $link_text AS Utf8?;
            DECLARE $link AS Utf8?;
            DECLARE $prices AS Utf8?;

            UPDATE donate_companies SET
                first_name = $first_name,
                photo_id = $photo_id,
                about_company = $about_company,
                link_text = $link_text,
                link = $link,
                prices = $prices
            WHERE telegram_id = $telegram_id;
            """,
            self._to_params(donate_company)
        )
        return await self.get_company_by_id(donate_company.telegram_id)
    
    async def update_company_fields(self, user_id: int, **fields: Any) -> bool:
        """Обновление выбранных полей по telegram_id"""
        if not fields:
            return False

        # Фильтруем только поля, которые относятся к таблице users
        company_fields = {k: v for k, v in fields.items() 
                      if k in ['first_name', 'photo_id', 'about_company', 'link_text', 'link', 'prices']}
        
        if not company_fields:
            return False

        set_clauses = []
        params = {"$telegram_id": (user_id, ydb.PrimitiveType.Uint64)}

        for field, value in company_fields.items():
            param_name = f"${field}"
            set_clauses.append(f"{field} = {param_name}")
            params[param_name] = (value, ydb.OptionalType(ydb.PrimitiveType.Utf8))

        set_query = ", ".join(set_clauses)
        declare_params = "\n".join([f"DECLARE {p} AS Utf8?;" for p in params.keys() if p != "$telegram_id"])

        query = f"""
            DECLARE $telegram_id AS Uint64;
            {declare_params}

            UPDATE donate_companies
            SET {set_query}
            WHERE telegram_id = $telegram_id;
        """

        await self.execute_query(query, params)
        return True

    async def delete_company(self, telegram_id: int) -> None:
        """Удаление компании по telegram_id"""
        await self.execute_query(
            """
            DECLARE $telegram_id AS Uint64;
            DELETE FROM donate_companies WHERE telegram_id = $telegram_id;
            """,
            {"$telegram_id": (telegram_id, ydb.PrimitiveType.Uint64)}
        )

    def _row_to_company(self, row) -> DonateCompany:
        return DonateCompany(
            telegram_id=row["telegram_id"],
            first_name=row.get("first_name"),
            photo_id=row.get("photo_id"),
            about_company=row.get("about_company"),
            link_text=row.get("link_text"),
            link=row.get("link"),
            prices=row.get("prices"),
        )

    def _to_params(self, donate_company: DonateCompany) -> dict:
        return {
            "$telegram_id": (donate_company.telegram_id, ydb.PrimitiveType.Uint64),
            "$first_name": (donate_company.first_name, ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            "$photo_id": (donate_company.photo_id, ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            "$about_company": (donate_company.about_company, ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            "$link_text": (donate_company.link_text, ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            "$link": (donate_company.link, ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            "$prices": (donate_company.prices, ydb.OptionalType(ydb.PrimitiveType.Utf8))
        }
    

# --------------------------------------------------------------- ПЛАТЕЖИ -----------------------------------------------------------------


@dataclass
class Payment:
    telegram_id: int
    amount: int
    link: str
    created_at: Optional[int] = None  # Храним как timestamp (секунды с эпохи)


class PaymentClient(YDBClient):
    def __init__(self, endpoint: str = YDB_ENDPOINT, database: str = YDB_PATH, token: str = YDB_TOKEN):
        super().__init__(endpoint, database, token)
        self.table_name = "payments"
        self.table_schema = """
            CREATE TABLE `payments` (
                `telegram_id` Uint64 NOT NULL,
                `amount` Uint32 NOT NULL,
                `link` Utf8 NOT NULL,
                `created_at` Uint64 NOT NULL,
                PRIMARY KEY (`created_at`)
            )
        """
    
    async def create_payments_table(self):
        """
        Создание таблицы payments
        """
        await self.create_table(self.table_name, self.table_schema)
    
    async def insert_payment(self, payment: Payment) -> Payment:
        """
        Вставка нового платежа
        """
        if payment.created_at is None:
            payment.created_at = int(datetime.now(timezone.utc).timestamp() * 1000)
        
        await self.execute_query(
            """
            DECLARE $telegram_id AS Uint64;
            DECLARE $amount AS Uint32;
            DECLARE $link AS Utf8;
            DECLARE $created_at AS Uint64;

            INSERT INTO payments (telegram_id, amount, link, created_at)
            VALUES ($telegram_id, $amount, $link, $created_at);
            """,
            self._to_params(payment)
        )

    async def delete_payment(self, created_at: int) -> None:
        """
        Удаление платежа по ID
        """
        await self.execute_query(
            """
            DECLARE $created_at AS Uint64;
            DELETE FROM payments WHERE created_at = $created_at;
            """,
            {"$created_at": (created_at, ydb.PrimitiveType.Uint64)}
        )

    # --- helpers ---
    def _row_to_payment(self, row) -> Payment:
        return Payment(
            telegram_id=row["telegram_id"],
            amount=row["amount"],
            link=row["link"],
            created_at=row["created_at"],
        )
    
    @staticmethod
    def timestamp_to_datetime(timestamp: int) -> datetime:
        """Конвертация timestamp в datetime объект"""
        return datetime.fromtimestamp(timestamp, tz=timezone.utc)
    
    @staticmethod
    def datetime_to_timestamp(dt: datetime) -> int:
        """Конвертация datetime в timestamp"""
        return int(dt.timestamp())

    def _to_params(self, payment: Payment) -> dict:
        return {
            "$telegram_id": (payment.telegram_id, ydb.PrimitiveType.Uint64),
            "$amount": (payment.amount, ydb.PrimitiveType.Uint32),
            "$link": (payment.link, ydb.PrimitiveType.Utf8),
            "$created_at": (payment.created_at, ydb.PrimitiveType.Uint64),
        }
    

# ------------------------------------------------------------ КЭШ -----------------------------------------------------------


@dataclass
class Cache:
    telegram_id: int = None
    parameter: Optional[str] = None
    message_id: Optional[int] = None


class CacheClient(YDBClient):
    def __init__(self, endpoint: str = YDB_ENDPOINT, database: str = YDB_PATH, token: str = YDB_TOKEN):
        super().__init__(endpoint, database, token)
        self.table_name = "cache"
        self.table_schema = """
            CREATE TABLE `cache` (
                `telegram_id` Uint64 NOT NULL,
                `parameter` Utf8,
                `message_id` Int32,
                PRIMARY KEY (`telegram_id`, `parameter`)
            )
        """
        
    async def create_cache_table(self):
        """
        Создание таблицы cache
        """
        await self.create_table(self.table_name, self.table_schema)
    
    async def insert_cache(self, cache: Cache) -> Cache:
        """
        Вставка записи в кэш
        """
        await self.execute_query(
            """
            DECLARE $telegram_id AS Uint64;
            DECLARE $parameter AS Utf8?;
            DECLARE $message_id AS Int32?;

            UPSERT INTO cache (telegram_id, parameter, message_id)
            VALUES ($telegram_id, $parameter, $message_id);
            """,
            self._to_params(cache)
        )

    async def get_cache_by_telegram_id(self, telegram_id: int) -> dict[str, int]:
        """
        Получение всех записей кэша для пользователя в виде словаря:
        {parameter: message_id}
        """
        result = await self.execute_query(
            """
            DECLARE $telegram_id AS Uint64;

            SELECT parameter, message_id
            FROM cache
            WHERE telegram_id = $telegram_id
            ORDER BY parameter;
            """,
            {"$telegram_id": (telegram_id, ydb.PrimitiveType.Uint64)}
        )

        rows = result[0].rows
        return {row["parameter"]: row["message_id"] for row in rows}

    async def delete_cache_by_telegram_id(self, telegram_id: int) -> None:
        """
        Удаление всех записей кэша для пользователя
        """
        await self.execute_query(
            """
            DECLARE $telegram_id AS Uint64;
            DELETE FROM cache WHERE telegram_id = $telegram_id;
            """,
            {"$telegram_id": (telegram_id, ydb.PrimitiveType.Uint64)}
        )

    async def delete_cache_by_telegram_id_and_parameter(self, telegram_id: int, parameter: str) -> None:
        """
        Удаление записи кэша по telegram_id и параметру
        """
        await self.execute_query(
            """
            DECLARE $telegram_id AS Uint64;
            DECLARE $parameter AS Utf8;
            DELETE FROM cache WHERE telegram_id = $telegram_id AND parameter = $parameter;
            """,
            {
                "$telegram_id": (telegram_id, ydb.PrimitiveType.Uint64),
                "$parameter": (parameter, ydb.PrimitiveType.Utf8)
            }
        )

    # --- helpers ---
    def _row_to_cache(self, row) -> Cache:
        return Cache(
            telegram_id=row["telegram_id"],
            parameter=row.get("parameter"),
            message_id=row.get("message_id"),
        )

    def _to_params(self, cache: Cache) -> dict:
        return {
            "$telegram_id": (cache.telegram_id, ydb.PrimitiveType.Uint64),
            "$parameter": (cache.parameter, ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            "$message_id": (cache.message_id, ydb.OptionalType(ydb.PrimitiveType.Int32)),
        }


# --------------------------------------------------------- СОЗДАНИЕ ТАБЛИЦ -------------------------------------------------------


async def create_tables_on_ydb():
    # Создание всех таблиц в базе
    async with DonateCompanyClient() as client:
        await client.create_companies_table()
        print("Table 'DONATE_COMPANIES' created successfully!")

    async with PaymentClient() as client:
        await client.create_payments_table()
        print("Table 'PAYMENTS' created successfully!")

    
    async with CacheClient() as client:
        await client.create_cache_table()
        print("Table 'CACHE' created successfully!")


# --------------------------------------------------------- ЗАПУСК -------------------------------------------------------


if __name__ == "__main__":
    asyncio.run(create_tables_on_ydb())
