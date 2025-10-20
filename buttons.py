from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def donate_company_begin_button(texts: dict):
    # Кнопка 18+ и согласие с политикой и соглашением
    button = InlineKeyboardButton(text=texts["BUTTONS_TEXT"]["begin"], callback_data="step_1")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button]])
    
    return markup


def payment_button(texts: dict):
    # кнопка оплатить
    builder = InlineKeyboardBuilder()
    builder.button(text=texts["BUTTONS_TEXT"]["pay"], pay=True)
    
    return builder.as_markup()


async def get_payment_buttons(texts: dict, amounts: list, telegram_id: int):
    buttons = []
    # получить кнопки для 
    for amount in amounts:
        button = InlineKeyboardButton(text=texts["BUTTONS_TEXT"]["amount"].format(amount=amount), callback_data=f"pay_intentions|{amount}|{telegram_id}", pay=True)
        buttons.append([button])

    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    return markup
