import logging
from aiogram.filters import CommandStart
from aiogram.filters.command import Command
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_API_KEY, ADMIN_ID, START_IMAGE
from languages import get_texts, get_images
from aiogram.client.default import DefaultBotProperties
from buttons import *
from ydb_connect import DonateCompanyClient, DonateCompany, PaymentClient, Payment
from config import YDB_ENDPOINT, YDB_PATH, YDB_TOKEN


# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Инициализация бота и диспетчера
bot = Bot(token=BOT_API_KEY, default=DefaultBotProperties(parse_mode="HTML"))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


@dp.message(Command('test'))
async def cmd_test(message: types.Message, ):
    caption = "Друзья, нужна ваша помощь! 🐾 \nНаш любимый котик Марсик оказался в беде — врачи диагностировали у него серьезное заболевание, и без срочной операции он не сможет жить.\nУ нас нет возможности собрать всю сумму самостоятельно, поэтому обращаемся к вам за поддержкой.\n\n<a href='https://t.me/pdd_good_bot?start=_tgr_3O1Yb4A4MDJi'>❤️ Помочь Марсику</a>"
    await message.answer_photo(photo='AgACAgIAAxkBAAMeaNvHX1PBgnIyTHonRxADYB4HDKkAAq70MRvkkeFKjKA0At8sHiQBAAMCAAN4AAM2BA', caption=caption)


@dp.message(CommandStart())
async def cmd_start(message: types.Message, command: CommandStart):
    first_name = message.from_user.first_name
    user_lang = message.from_user.language_code

    text = await get_texts(user_lang)

    payload = command.args   # значение после /start

    # логика донатеров
    if payload:
        pass
    
    # логика creators
    else:
        await message.answer_photo(photo=START_IMAGE, caption=text['TEXT']['start'].format(first_name=first_name),
                                   reply_markup=await donate_company_begin_button(text))


@dp.callback_query(F.data == "step_1")
async def query_get_text(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    first_name = callback.from_user.first_name
    user_lang = callback.from_user.language_code

    await callback.message.edit_reply_markup(reply_markup=None)

    text = await get_texts(user_lang)
    images = await get_images(user_lang)

    new_company = DonateCompany(
        telegram_id=user_id,
        first_name=first_name
    )
    async with DonateCompanyClient(YDB_ENDPOINT, YDB_PATH, YDB_TOKEN) as client:
        await client.insert_company(new_company)

    await callback.message.edit_media()
    # answer_photo(photo=images['IMAGE']['step_1'], caption=text['TEXT']['step_1'])


# обработка фото
@dp.message(F.photo)
async def handle_photo(message: types.Message):
    user_id = message.from_user.id
    user_lang = message.from_user.language_code

    photo = message.photo[-1]
    file_id = photo.file_id
    print(file_id)

    # await message.delete()

    text = await get_texts(user_lang)
    images = await get_images(user_lang)

    async with DonateCompanyClient(YDB_ENDPOINT, YDB_PATH, YDB_TOKEN) as client:
        await client.update_company_fields(user_id, photo_id=file_id)
    

    await message.answer_photo(photo=images['IMAGE']['step_2'], caption=text['TEXT']['step_2'])


async def main():
    # Запуск бота
    await dp.start_polling(bot)


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())