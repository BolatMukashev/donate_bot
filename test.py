import asyncio
from ydb_connect import DonateCompanyClient, DonateCompany, PaymentClient, Payment, YDBClient, CacheClient, Cache
from config import YDB_ENDPOINT, YDB_PATH, YDB_TOKEN


async def create_new_company():
    new_company = DonateCompany(
        telegram_id=123456789,
        first_name="John",
        about_company="Сбор средств на лечение кота",
        link_text="кнопка",
        photo_id="photo123",
        prices="1 2 3 4 5",
        ref_code="ff220"
    )
    async with DonateCompanyClient(YDB_ENDPOINT, YDB_PATH, YDB_TOKEN) as client:
        await client.insert_company(new_company)


async def create_empty_company():
    new_company = DonateCompany(
        telegram_id=24555554,
        first_name="John"
    )
    async with DonateCompanyClient(YDB_ENDPOINT, YDB_PATH, YDB_TOKEN) as client:
        await client.insert_company(new_company)


async def edit_company(telegram_id):
    async with DonateCompanyClient(YDB_ENDPOINT, YDB_PATH, YDB_TOKEN) as client:
        await client.update_company_fields(telegram_id, first_name="Lina", about_company="Сбор средств на лечение пса")

    
async def get_company_by_id(telegram_id):
    async with DonateCompanyClient(YDB_ENDPOINT, YDB_PATH, YDB_TOKEN) as client:
        res = await client.get_company_by_id(telegram_id)
        print(res)


async def get_id_by_ref_code(ref_code):
    async with DonateCompanyClient(YDB_ENDPOINT, YDB_PATH, YDB_TOKEN) as client:
        res = await client.get_id_by_ref_code(ref_code)
        print(res)


async def create_new_payment():
    new_payment = Payment(
        telegram_id=123456789,
        amount=1000,
        ref_code="https://example.com"
    )
    async with PaymentClient(YDB_ENDPOINT, YDB_PATH, YDB_TOKEN) as client:
        await client.insert_payment(new_payment)


async def reset_database():
    async with YDBClient() as cleaner:
        await cleaner.clear_all_tables()


async def cache_test():
    async with CacheClient(YDB_ENDPOINT, YDB_PATH, YDB_TOKEN) as client:
        new_cache = Cache(telegram_id=123456789000, parameter="referal", value=11223344556699)
        await client.insert_cache(new_cache)


if __name__ == "__main__":
    asyncio.run(create_new_payment())

