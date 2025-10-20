import logging
from aiogram.filters import CommandStart
from aiogram.filters.command import Command
from aiogram.types import LabeledPrice
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_API_KEY, ADMIN_ID, START_IMAGE
from languages import get_texts, get_images, get_caption
from languages.desc import DESCRIPTIONS, SHORT_DESCRIPTIONS, NAMES
from aiogram.client.default import DefaultBotProperties
from buttons import *
from ydb_connect import DonateCompanyClient, DonateCompany, PaymentClient, Payment, Cache, CacheClient, loading_animation
from config import YDB_ENDPOINT, YDB_PATH, YDB_TOKEN
import re
import asyncio


# ------------------------------------------------------------------- Настройки -------------------------------------------------------------


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


# установка описания
@dp.message(Command("set_description"))
async def cmd_set_description(message: types.Message):
    user_id = message.from_user.id
    if user_id == ADMIN_ID:
        # установка описания для бота на разных языках
        for lang, text in DESCRIPTIONS.items():
            try:
                await bot.set_my_description(description=text, language_code=lang)
            except Exception as e:
                print(f"Ошбика установки описания для языка {lang} - {e}")
            else:
                print("Описание для бота установлено ✅")

        # установка короткого описания для бота на разных языках
        for lang, text in SHORT_DESCRIPTIONS.items():
            try:
                await bot.set_my_short_description(short_description=text, language_code=lang)
            except Exception as e:
                print(f"Ошбика установки короткого описания для языка {lang} - {e}")
            else:
                print("Короткое описание для бота установлено ✅")

        # установка имени бота на разных языках
        for lang, name in NAMES.items():
            try:
                await bot.set_my_name(name=name, language_code=lang)
            except Exception as e:
                print(f"Ошбика установки имени для языка {lang} - {e}")
            else:
                print("Название бота установлено ✅")


# ------------------------------------------------------------------- Донат компания -------------------------------------------------------


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    user_lang = message.from_user.language_code

    text = await get_texts(user_lang)

    message_id = await loading_animation(bot, message, text["TEXT"]["loading"])
    await bot.delete_message(chat_id=message.chat.id, message_id=message_id.message_id)

    async with CacheClient() as client:
        user_cache = await client.get_cache_by_telegram_id(user_id)
    
    ref_id = int(user_cache.get("referal")) if user_cache.get("referal") else None
    print(f"ref_id={ref_id}")

    # логика донатеров
    if ref_id:
        async with DonateCompanyClient() as donate_client, CacheClient() as cache_client:
            company = await donate_client.get_company_by_id(ref_id)
            amounts = list(map(int, company.prices.split()))
            await message.answer_photo(photo=company.photo_id, caption=company.about_company,
                                                   reply_markup=await get_payment_buttons(text, amounts, company.telegram_id))
        

            await cache_client.delete_cache_by_telegram_id_and_parameter(user_id, "referal")

    # логика creators
    else:
        start_message = await message.answer_photo(photo=START_IMAGE, caption=text['TEXT']['start'].format(first_name=first_name),
                                                   reply_markup=await donate_company_begin_button(text))
        async with CacheClient() as cache_client:
            new_cache = Cache(telegram_id=user_id, parameter="start_message_id", value=start_message.message_id)
            await cache_client.insert_cache(new_cache)


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
    
    async with CacheClient() as cache_client:
        await cache_client.insert_cache(Cache(telegram_id=user_id, parameter="step", value=1))


    # msg_id = user_cache.get("start_message_id")
    photo = images['IMAGE']['step_1']
    caption = text['TEXT']['step_1']
    await callback.message.edit_media(media=types.InputMediaPhoto(media=photo, caption=caption))


# обработка фото
@dp.message(F.photo)
async def handle_photo(message: types.Message):
    user_id = message.from_user.id
    user_lang = message.from_user.language_code

    async with CacheClient() as cache_client:
        user_cache = await cache_client.get_cache_by_telegram_id(user_id)

    step_number = int(user_cache.get("step")) if user_cache.get("step") else None

    await message.delete()

    photo = message.photo[-1]
    file_id = photo.file_id

    # await message.answer(file_id)
    # return

    if step_number != 1:
        return

    text = await get_texts(user_lang)
    images = await get_images(user_lang)

    async with DonateCompanyClient(YDB_ENDPOINT, YDB_PATH, YDB_TOKEN) as donate_client, CacheClient() as cache_client:
        await asyncio.gather(
            donate_client.update_company_fields(user_id, photo_id=file_id),
            cache_client.insert_cache(Cache(telegram_id=user_id, parameter="step", value=2))
            )
    
    msg_id = user_cache.get("start_message_id")
    photo = images['IMAGE']['step_2']
    caption = text['TEXT']['step_2']
    await bot.edit_message_media(chat_id=message.chat.id, message_id=msg_id, media=types.InputMediaPhoto(media=photo, caption=caption))


@dp.message(F.text)
async def handle_text(message: types.Message):
    user_id = message.from_user.id
    user_lang = message.from_user.language_code
    user_text = message.text

    async with CacheClient() as cache_client:
        user_cache = await cache_client.get_cache_by_telegram_id(user_id)

    step_number = int(user_cache.get("step")) if user_cache.get("step") else None
    msg_id = user_cache.get("start_message_id")

    await message.delete()

    if not step_number:
        return
    
    text = await get_texts(user_lang)
    images = await get_images(user_lang)

    if step_number == 2:
        async with DonateCompanyClient(YDB_ENDPOINT, YDB_PATH, YDB_TOKEN) as donate_client, CacheClient() as cache_client:
            await asyncio.gather(
                donate_client.update_company_fields(user_id, about_company=user_text),
                cache_client.insert_cache(Cache(telegram_id=user_id, parameter="step", value=3))
                )
        await bot.edit_message_media(chat_id=message.chat.id, message_id=msg_id,
                                     media=types.InputMediaPhoto(media=images['IMAGE']['step_3'], caption=text['TEXT']['step_3']))

    elif step_number == 3:
        async with DonateCompanyClient(YDB_ENDPOINT, YDB_PATH, YDB_TOKEN) as donate_client, CacheClient() as cache_client:
            await asyncio.gather(
                donate_client.update_company_fields(user_id, link_text=user_text),
                cache_client.insert_cache(Cache(telegram_id=user_id, parameter="step", value=4))
                )
        await bot.edit_message_media(chat_id=message.chat.id, message_id=msg_id,
                                     media=types.InputMediaPhoto(media=images['IMAGE']['step_4'], caption=text['TEXT']['step_4']))
        
    elif step_number == 4:
        link_pattern = re.compile(r"^https://t\.me/DonateCampaignBot\?start=[\w\d_-]+$")

        if not link_pattern.match(user_text.strip()):
            return
        
        ref_code = user_text.split("=")[-1]

        async with DonateCompanyClient(YDB_ENDPOINT, YDB_PATH, YDB_TOKEN) as donate_client, CacheClient() as cache_client:
            await asyncio.gather(
                donate_client.update_company_fields(user_id, ref_code=ref_code),
                cache_client.insert_cache(Cache(telegram_id=user_id, parameter="step", value=5))
                )
        await bot.edit_message_media(chat_id=message.chat.id, message_id=msg_id,
                                     media=types.InputMediaPhoto(media=images['IMAGE']['step_5'], caption=text['TEXT']['step_5']))
    
    elif step_number == 5:
        number_pattern = re.compile(r"^\d+(?:\s+\d+){1,8}$")

        if not number_pattern.match(user_text.strip()):
            return

        async with DonateCompanyClient(YDB_ENDPOINT, YDB_PATH, YDB_TOKEN) as donate_client, CacheClient() as cache_client:
            await asyncio.gather(
                donate_client.update_company_fields(user_id, prices=user_text.strip()),
                cache_client.insert_cache(Cache(telegram_id=user_id, parameter="step", value=6))
                )
        await bot.edit_message_media(chat_id=message.chat.id, message_id=msg_id,
                                     media=types.InputMediaPhoto(media=images['IMAGE']['end'], caption=text['TEXT']['end']))
        
        async with DonateCompanyClient(YDB_ENDPOINT, YDB_PATH, YDB_TOKEN) as donate_client:
            company = await donate_client.get_company_by_id(user_id)
        
        await bot.send_photo(chat_id=message.chat.id,
                             photo=company.photo_id,
                             caption=await get_caption(company.about_company, company.link_text, company.ref_code))


# ------------------------------------------------------------------- ОПЛАТА -------------------------------------------------------


# обработка колбека оплаты
@dp.callback_query(lambda c: c.data.startswith("pay_intentions"))
async def handle_intentions_pay(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_lang = callback.from_user.language_code
    
    _, amount_str, telegram_id = callback.data.split("|")
    amount = int(amount_str)
    telegram_id = int(telegram_id)

    texts = await get_texts(user_lang)

    async with DonateCompanyClient() as donate_client:
        company = await donate_client.get_company_by_id(telegram_id)

    label = company.link_text
    title = company.link_text
    description = texts["TEXT"]["payment"]["description"].format(amount=amount)


    prices = [LabeledPrice(label=label, amount=amount)]

    sent_invoice = await callback.message.answer_invoice(
        title=title,
        description=description,
        payload=f"payment|{amount}|{company.ref_code}",
        provider_token="",
        currency="XTR",
        prices=prices,
        reply_markup=payment_button(texts)
    )

    # сохраняем в Кэш
    async with CacheClient() as cache_client:
        new_cache = Cache(user_id, "payment_message_id", sent_invoice.message_id)
        await cache_client.insert_cache(new_cache)

    await callback.answer(texts["TEXT"]["notifications"]["payment_sent"])


@dp.pre_checkout_query()
async def pre_checkout(pre_checkout_query: types.PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@dp.message(lambda message: message.successful_payment is not None)
async def on_successful_payment(message: types.Message):
    payload = message.successful_payment.invoice_payload
    user_id = message.from_user.id
    user_lang = message.from_user.language_code

    # получение текста на языке пользователя
    texts = await get_texts(user_lang)
    
    _, amount, ref_code = payload.split("|")

    async with PaymentClient() as payment_client:
        new_payment = Payment(user_id, int(amount), ref_code)
        await payment_client.insert_payment(new_payment)

    await message.answer(texts["TEXT"]["payment"]["payment_accepted"])

    # удаление старого сообщения
    async with CacheClient() as cache_client:
        cached_messages = await cache_client.get_cache_by_telegram_id(user_id)
        payment_message_id = cached_messages.get("payment_message_id")
    await bot.delete_message(chat_id=message.chat.id, message_id=payment_message_id)
    await bot.send_message(chat_id=message.chat.id, text=texts["TEXT"]["ad"])


# ------------------------------------------------------------------- Обработка других форматов -------------------------------------------------------


@dp.message(~(F.text | F.photo))
async def delete_unwanted(message: types.Message):
    try:
        await message.delete()
    except Exception as e:
        print(f"⚠️ Не удалось удалить сообщение: {e}")


# ------------------------------------------------------------------------ Запуск -------------------------------------------------------------


async def main():
    # Запуск бота
    await dp.start_polling(bot)


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())