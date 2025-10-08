from urllib.parse import quote
from . import (
     ru_text, en_text,
)


"""
    kk_text, pt_br_text,
    de_text, fr_text, it_text, es_text, nl_text, sv_text, fi_text, no_text,
    he_text, ko_text, ja_text, cs_text, sk_text, sl_text, pl_text,
    pt_text, hr_text, ar_text, be_text, ca_text, hu_text, id_text,
    ms_text, fa_text, ro_text, sr_text, tr_text, uk_text, uz_text,
    hi_text, vi_text, th_text, zh_text, zh_hans_text, zh_hant_text, el_text
"""

LANGUAGES = {
    "ru": {"TEXT": ru_text.TEXT, "BUTTONS_TEXT": ru_text.BUTTONS_TEXT},
    "en": {"TEXT": en_text.TEXT, "BUTTONS_TEXT": en_text.BUTTONS_TEXT},

}

IMAGES = {
    "ru": {"IMAGE": ru_text.IMAGE},
    "en": {"IMAGE": en_text.IMAGE},
}


"""
    
    "kk": {"TEXT": kk_text.TEXT, "BUTTONS_TEXT": kk_text.BUTTONS_TEXT},
    "pt-br": {"TEXT": pt_br_text.TEXT, "BUTTONS_TEXT": pt_br_text.BUTTONS_TEXT},
    "de": {"TEXT": de_text.TEXT, "BUTTONS_TEXT": de_text.BUTTONS_TEXT},
    "fr": {"TEXT": fr_text.TEXT, "BUTTONS_TEXT": fr_text.BUTTONS_TEXT},
    "it": {"TEXT": it_text.TEXT, "BUTTONS_TEXT": it_text.BUTTONS_TEXT},
    "es": {"TEXT": es_text.TEXT, "BUTTONS_TEXT": es_text.BUTTONS_TEXT},
    "nl": {"TEXT": nl_text.TEXT, "BUTTONS_TEXT": nl_text.BUTTONS_TEXT},
    "sv": {"TEXT": sv_text.TEXT, "BUTTONS_TEXT": sv_text.BUTTONS_TEXT},
    "fi": {"TEXT": fi_text.TEXT, "BUTTONS_TEXT": fi_text.BUTTONS_TEXT},
    "no": {"TEXT": no_text.TEXT, "BUTTONS_TEXT": no_text.BUTTONS_TEXT},
    "he": {"TEXT": he_text.TEXT, "BUTTONS_TEXT": he_text.BUTTONS_TEXT},
    "ko": {"TEXT": ko_text.TEXT, "BUTTONS_TEXT": ko_text.BUTTONS_TEXT},
    "ja": {"TEXT": ja_text.TEXT, "BUTTONS_TEXT": ja_text.BUTTONS_TEXT},
    "cs": {"TEXT": cs_text.TEXT, "BUTTONS_TEXT": cs_text.BUTTONS_TEXT},
    "sk": {"TEXT": sk_text.TEXT, "BUTTONS_TEXT": sk_text.BUTTONS_TEXT},
    "sl": {"TEXT": sl_text.TEXT, "BUTTONS_TEXT": sl_text.BUTTONS_TEXT},
    "pl": {"TEXT": pl_text.TEXT, "BUTTONS_TEXT": pl_text.BUTTONS_TEXT},
    "pt": {"TEXT": pt_text.TEXT, "BUTTONS_TEXT": pt_text.BUTTONS_TEXT},
    "hr": {"TEXT": hr_text.TEXT, "BUTTONS_TEXT": hr_text.BUTTONS_TEXT},
    "ar": {"TEXT": ar_text.TEXT, "BUTTONS_TEXT": ar_text.BUTTONS_TEXT},
    "be": {"TEXT": be_text.TEXT, "BUTTONS_TEXT": be_text.BUTTONS_TEXT},
    "ca": {"TEXT": ca_text.TEXT, "BUTTONS_TEXT": ca_text.BUTTONS_TEXT},
    "hu": {"TEXT": hu_text.TEXT, "BUTTONS_TEXT": hu_text.BUTTONS_TEXT},
    "id": {"TEXT": id_text.TEXT, "BUTTONS_TEXT": id_text.BUTTONS_TEXT},
    "ms": {"TEXT": ms_text.TEXT, "BUTTONS_TEXT": ms_text.BUTTONS_TEXT},
    "fa": {"TEXT": fa_text.TEXT, "BUTTONS_TEXT": fa_text.BUTTONS_TEXT},
    "ro": {"TEXT": ro_text.TEXT, "BUTTONS_TEXT": ro_text.BUTTONS_TEXT},
    "sr": {"TEXT": sr_text.TEXT, "BUTTONS_TEXT": sr_text.BUTTONS_TEXT},
    "tr": {"TEXT": tr_text.TEXT, "BUTTONS_TEXT": tr_text.BUTTONS_TEXT},
    "uk": {"TEXT": uk_text.TEXT, "BUTTONS_TEXT": uk_text.BUTTONS_TEXT},
    "uz": {"TEXT": uz_text.TEXT, "BUTTONS_TEXT": uz_text.BUTTONS_TEXT},
    "hi": {"TEXT": hi_text.TEXT, "BUTTONS_TEXT": hi_text.BUTTONS_TEXT},
    "vi": {"TEXT": vi_text.TEXT, "BUTTONS_TEXT": vi_text.BUTTONS_TEXT},
    "th": {"TEXT": th_text.TEXT, "BUTTONS_TEXT": th_text.BUTTONS_TEXT},
    "zh": {"TEXT": zh_text.TEXT, "BUTTONS_TEXT": zh_text.BUTTONS_TEXT},
    "zh-hans": {"TEXT": zh_hans_text.TEXT, "BUTTONS_TEXT": zh_hans_text.BUTTONS_TEXT},
    "zh-hant": {"TEXT": zh_hant_text.TEXT, "BUTTONS_TEXT": zh_hant_text.BUTTONS_TEXT},
    "el": {"TEXT": el_text.TEXT, "BUTTONS_TEXT": el_text.BUTTONS_TEXT},
"""


async def get_texts(lang_code: str) -> dict:
    """Возвращает набор словарей по коду языка."""
    return LANGUAGES.get(lang_code, LANGUAGES["en"])


async def get_images(lang_code: str) -> dict:
    """Возвращает набор словарей по коду языка."""
    return IMAGES.get(lang_code, IMAGES["en"])


async def get_caption(caption, link_text, ref_code) -> str:
    """Возвращает описание объявления"""
    link = f"https://t.me/donate_company_bot/app?startapp={quote(ref_code)}"
    return f"{caption}\n\n<a href='{link}'>{link_text}</a>"

