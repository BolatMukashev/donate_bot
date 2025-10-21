# переведи на немецкий язык
# учитывай особенности языка, чтобы носители легко понимали смысл написанного 
# нативный перевод — адаптированный так, чтобы звучал естественно и понятно для пользователей 
# учти стиль Telegram, дружелюбный тон и культурные особенности


TEXT = {'start': 'Привет, {first_name}!\n'
                 'Здесь ты можешь создать свою донат-компанию и собирать донаты в Звёздах ⭐️ (Telegram Stars)\n'
                 'Условия:\n'
                 '• Комиссия - 20% (хотелось бы меньше, но Telegram не позволяет)\n'
                 '• Срок сбора - бессрочно\n'
                 '• Начисление - сразу после получения оплаты\n'
                 '• Ограничения — можно создать только 1 донат компанию\n'
                 '<i>При попытке создать новую донат-компанию старая будет удалена</i>\n'
                 'Подробнее о других ограничениях можно почитать в официальном <a href="https://telegram.org/tos/affiliate-program/ru">Соглашении</a>',
        'step_1': 'Начнём! Объявление для донат-компании состоит из 5 шагов\n\n'
                '<b>Шаг 1. Отправь ФОТО</b>\n'
                'Оно будет использоваться в объявлении вашей донат-компании\n'
                '<i>Это может быть фото человека, питомца, предмета или любое изображение, связанное с целью сбора</i>',
        'step_2': '<b>Шаг 2. Напиши ОПИСАНИЕ</b>\n'
                'Укажи, на что именно будут потрачены пожертвования <i>(лечение, помощь приюту, благотворительность, поддержка проекта и т.д.)</i>\n'
                'Постарайся написать искренне и понятно',
        'step_3': '<b>Шаг 3. Придумай КОРОТКИЙ ТЕКСТ для ссылки</b>\n'
                'На этот текст в посте будут нажимать подписчики, чтобы перейти в бота для оплаты (например: <i>«Сделать донат»</i> или <i>«Поддержать проект»</i>)',
        'step_4': '<b>Шаг 4. Отправьте партнёрскую ССЫЛКУ</b>.\n\n'
                '<i>Чтобы её получить нужно:\n'
                '• Открой описание бота\n'
                '• Нажми \"Партнерская программа\"\n'
                '• Нажми \"Участвовать\"\n'
                '• Нажми \"Копировать ссылку\"\n'
                '• Вернись к диалогу с ботом и отправь ссылку\n'
                'Вставь её полностью (например: https:\u200B//t.me/donate_company\u200B_bot?start=donate123)</i>',
        'step_5': '<b>Шаг 5. Напиши ВАРИАНТЫ донатов</b>\n'
                'Напиши суммы через пробел, от 2 до 9 вариантов\n'
                'Подписчики смогут выбрать одну из них <i>(например: 50 100 250 500)</i>\n'
                '<i>Учитывай, что цены представленны в Звездах ⭐️</i>',
        'end':  'Готово!\n'
                'Вот твоё объявление для публикации:\n'
                '<i>Опубликуй его у себя группе или телеграм канале.\n'
                'При переходе по ссылке будет отображаться объявление с суммами донатов</i>',
        "payment": {"label": "{purpose}",
                    "title": "{purpose}",
                    "description": "Стоимость: ⭐️ {amount}",
                    "payment_accepted": "Ваш платёж принят. Спасибо ❤️"},

        "notifications": {"payment_sent": "Платёж отправлен. Ожидается оплата",
                          "payment_accepted": "Ваш платёж принят. Спасибо ❤️"},
        "ad": "Чтобы создать свою донат-компанию\nнажми 👉 /start",
        "loading": "Проверяем"
        }

BUTTONS_TEXT = {'begin': 'Создать донат-компанию',
                'pay': 'Оплатить',
                'amount': '⭐️ {amount}'}

IMAGE = {'step_1': 'AgACAgIAAxkBAAMOaPNv9s_YDyqZLLRlNmUzpBvC0DkAAlP4MRtVnqBLFBHrZtKvcN8BAAMCAAN3AAM2BA',
         'step_2': 'AgACAgIAAxkBAAMPaPNv_JFkXag-GpnUm-bSXa7aWNMAAlT4MRtVnqBLLrdjY1chDpcBAAMCAAN3AAM2BA',
         'step_3': 'AgACAgIAAxkBAAMQaPNwBVEVAUPa1PDMcekT8_fAiFoAAlX4MRtVnqBLdkRSBSbovrcBAAMCAAN3AAM2BA',
         'step_4': 'AgACAgIAAxkBAAMRaPNwCPwmYLhav-I3tl0N4mP8w4gAAlb4MRtVnqBLYAJSt-PZnXABAAMCAAN3AAM2BA',
         'step_5': 'AgACAgIAAxkBAAMSaPNwDLVQrj2gtmOgCzyvr8YbREoAAlf4MRtVnqBLnahmLnWHAYsBAAMCAAN3AAM2BA',
         'end':'AgACAgIAAxkBAAMTaPNwEBVTNXIpkVjkzhPwkv3JzdoAAlj4MRtVnqBL-MEHpvzfaTwBAAMCAAN3AAM2BA'
         }

"""
IMAGE = {'step_1': '',
         'step_2': '',
         'step_3': '',
         'step_4': '',
         'step_5': '',
         'end':''
         }

         
PRICES = {'en': {'name': 'английский', 'incognito': 100, 'add_to_collection': 40},
          'de': {'name': 'немецкий', 'incognito': 100, 'add_to_collection': 40},
          'fr': {'name': 'французский', 'incognito': 100, 'add_to_collection': 40},
          'it': {'name': 'итальянский', 'incognito': 100, 'add_to_collection': 40},
          'es': {'name': 'испанский', 'incognito': 100, 'add_to_collection': 40},
          'nl': {'name': 'нидерландский', 'incognito': 100, 'add_to_collection': 40},
          'sv': {'name': 'шведский', 'incognito': 100, 'add_to_collection': 40},
          'fi': {'name': 'финский', 'incognito': 100, 'add_to_collection': 40},
          'no': {'name': 'норвежский', 'incognito': 100, 'add_to_collection': 40},
          'he': {'name': 'иврит', 'incognito': 100, 'add_to_collection': 40},
          'ko': {'name': 'корейский', 'incognito': 100, 'add_to_collection': 40},
          'ja': {'name': 'японский', 'incognito': 100, 'add_to_collection': 40},
          'cs': {'name': 'чешский', 'incognito': 100, 'add_to_collection': 40},
          'sk': {'name': 'словацкий', 'incognito': 100, 'add_to_collection': 40},
          'sl': {'name': 'словенский', 'incognito': 100, 'add_to_collection': 40},
          'pl': {'name': 'польский', 'incognito': 100, 'add_to_collection': 40},
          'pt': {'name': 'португальский', 'incognito': 100, 'add_to_collection': 40},
          'hr': {'name': 'хорватский', 'incognito': 100, 'add_to_collection': 40},

          'ru': {'name': 'русский', 'incognito': 50, 'add_to_collection': 20},
          'ar': {'name': 'арабский', 'incognito': 50, 'add_to_collection': 20},
          'be': {'name': 'белорусский', 'incognito': 50, 'add_to_collection': 20},
          'ca': {'name': 'каталанский', 'incognito': 50, 'add_to_collection': 20},
          'hu': {'name': 'венгерский', 'incognito': 50, 'add_to_collection': 20},
          'id': {'name': 'индонезийский', 'incognito': 50, 'add_to_collection': 20},
          'kk': {'name': 'казахский', 'incognito': 50, 'add_to_collection': 20},
          'ms': {'name': 'малайский', 'incognito': 50, 'add_to_collection': 20},
          'fa': {'name': 'персидский', 'incognito': 50, 'add_to_collection': 20},
          'ro': {'name': 'румынский', 'incognito': 50, 'add_to_collection': 20},
          'sr': {'name': 'сербский', 'incognito': 50, 'add_to_collection': 20},
          'tr': {'name': 'турецкий', 'incognito': 50, 'add_to_collection': 20},
          'uk': {'name': 'украинский', 'incognito': 50, 'add_to_collection': 20},
          'uz': {'name': 'узбекский', 'incognito': 50, 'add_to_collection': 20},
          'hi': {'name': 'хинди', 'incognito': 50, 'add_to_collection': 20},
          'vi': {'name': 'вьетнамский', 'incognito': 50, 'add_to_collection': 20},
          'th': {'name': 'тайский', 'incognito': 50, 'add_to_collection': 20},
          'zh': {'name': 'китайский', 'incognito': 50, 'add_to_collection': 20},
          'el': {'name': 'греческий', 'incognito': 50, 'add_to_collection': 20},
          }

"""