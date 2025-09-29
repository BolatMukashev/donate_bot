import asyncio
from ydb_connect import DonateCompanyClient, DonateCompany
from config import YDB_ENDPOINT, YDB_PATH, YDB_TOKEN


async def main():
    async with DonateCompanyClient(YDB_ENDPOINT, YDB_PATH, YDB_TOKEN) as client:
        await client.create_companies_table()


async def create_new_company():
    new_company = DonateCompany(
        telegram_id=123456789,
        first_name="John",
        about_company="Сбор средств на лечение кота",
        photo_id="photo123",
        prices="1 2 3 4 5"
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
        await client.update_company_fields(telegram_id, first_name="Bob", about_company="Сбор средств на лечение пса",)


if __name__ == "__main__":
    asyncio.run(edit_company(24555554))

