import logging
from aiogram.filters import CommandStart
from aiogram.filters.command import Command
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_API_KEY, ADMIN_ID
from languages import get_texts
from aiogram.client.default import DefaultBotProperties


# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Инициализация бота и диспетчера
bot = Bot(token=BOT_API_KEY, default=DefaultBotProperties(parse_mode="HTML"))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


@dp.message(CommandStart())
async def cmd_start(message: types.Message, command: CommandStart):
    first_name = message.from_user.first_name
    user_id = message.from_user.id
    user_lang = message.from_user.language_code

    payload = command.args   # значение после /start

    text = await get_texts(user_lang)

    # логика донатеров
    if payload:
        pass
    
    # логика creators
    else:
        await message.answer(text["TEXT"]['start'].format(first_name=first_name))


async def main():
    # Запуск бота
    await dp.start_polling(bot)


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())