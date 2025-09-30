import asyncio
from ydb_connect import DonateCompanyClient, DonateCompany, PaymentClient, Payment
from config import YDB_ENDPOINT, YDB_PATH, YDB_TOKEN


async def create_new_company():
    new_company = DonateCompany(
        telegram_id=123456789,
        first_name="John",
        about_company="Сбор средств на лечение кота",
        photo_id="photo123",
        prices="1 2 3 4 5",
        link="https://example.com"
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


async def create_new_payment():
    new_payment = Payment(
        telegram_id=123456789,
        amount=1000,
        link="https://example.com"
    )
    async with PaymentClient(YDB_ENDPOINT, YDB_PATH, YDB_TOKEN) as client:
        await client.insert_payment(new_payment)


if __name__ == "__main__":
    asyncio.run(create_new_payment())

