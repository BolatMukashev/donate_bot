from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from uuid import uuid4


async def donate_company_begin_button(texts: dict):
    # Кнопка 18+ и согласие с политикой и соглашением
    button = InlineKeyboardButton(text=texts["BUTTONS_TEXT"]["begin"], callback_data="begin")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button]])
    
    return markup


#TODO получать список?
def payment_keyboard(texts: dict):
    builder = InlineKeyboardBuilder()
    builder.button(text=texts["BUTTONS_TEXT"]["pay"], pay=True)
    
    return builder.as_markup()
