import logging
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_API_KEY, ADMIN_ID
from aiogram.filters import CommandStart


# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Инициализация бота и диспетчера
bot = Bot(token=BOT_API_KEY)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


@dp.message(CommandStart())
async def cmd_start(message: types.Message, command: CommandStart):
    user_name = message.from_user.full_name
    user_id = message.from_user.id

    payload = command.args   # <-- тут сразу "secret_code"

    await message.answer(
        f"Привет, {user_name}! Я бот. Твой ID: {user_id}, текст: {payload}"
    )


async def main():
    # Запуск бота
    await dp.start_polling(bot)


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())