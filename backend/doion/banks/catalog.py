"""Initial bank catalog rows (spec §3.1). Colors are approximate #RRGGBB."""

from __future__ import annotations

from typing import TypedDict


class CatalogBank(TypedDict):
    code: str
    display_name: str
    aliases: list[str]
    brand_color_light: str
    brand_color_dark: str


INITIAL_BANKS: tuple[CatalogBank, ...] = (
    {
        "code": "mellat",
        "display_name": "بانک ملت",
        "aliases": ["بانک ملت"],
        "brand_color_light": "#E21836",
        "brand_color_dark": "#C4112C",
    },
    {
        "code": "melli",
        "display_name": "بانک ملی ایران",
        "aliases": ["بانک ملی ایران", "بانک ملی"],
        "brand_color_light": "#0057A0",
        "brand_color_dark": "#004080",
    },
    {
        "code": "saderat",
        "display_name": "بانک صادرات ایران",
        "aliases": ["بانک صادرات ایران", "بانک صادرات"],
        "brand_color_light": "#1A7A3A",
        "brand_color_dark": "#14622E",
    },
    {
        "code": "pasargad",
        "display_name": "بانک پاسارگاد",
        "aliases": ["بانک پاسارگاد"],
        "brand_color_light": "#F5A623",
        "brand_color_dark": "#C48412",
    },
    {
        "code": "tejarat",
        "display_name": "بانک تجارت",
        "aliases": ["بانک تجارت"],
        "brand_color_light": "#003DA5",
        "brand_color_dark": "#002D7A",
    },
    {
        "code": "saman",
        "display_name": "بانک سامان",
        "aliases": ["بانک سامان"],
        "brand_color_light": "#00A0E3",
        "brand_color_dark": "#007FB5",
    },
    {
        "code": "parsian",
        "display_name": "بانک پارسیان",
        "aliases": ["بانک پارسیان"],
        "brand_color_light": "#8B1E3F",
        "brand_color_dark": "#6E1832",
    },
    {
        "code": "sepah",
        "display_name": "بانک سپه",
        "aliases": ["بانک سپه"],
        "brand_color_light": "#1B4F72",
        "brand_color_dark": "#153D59",
    },
    {
        "code": "ayandeh",
        "display_name": "بانک آینده",
        "aliases": ["بانک آینده"],
        "brand_color_light": "#E67E22",
        "brand_color_dark": "#B85F14",
    },
    {
        "code": "maskan",
        "display_name": "بانک مسکن",
        "aliases": ["بانک مسکن"],
        "brand_color_light": "#27AE60",
        "brand_color_dark": "#1E8449",
    },
    {
        "code": "shahr",
        "display_name": "بانک شهر",
        "aliases": ["بانک شهر"],
        "brand_color_light": "#8E44AD",
        "brand_color_dark": "#6C3483",
    },
    {
        "code": "keshavarzi",
        "display_name": "بانک کشاورزی",
        "aliases": ["بانک کشاورزی"],
        "brand_color_light": "#229954",
        "brand_color_dark": "#1A7439",
    },
    {
        "code": "refah",
        "display_name": "بانک رفاه کارگران",
        "aliases": ["بانک رفاه کارگران"],
        "brand_color_light": "#16A085",
        "brand_color_dark": "#117A65",
    },
    {
        "code": "sina",
        "display_name": "بانک سینا",
        "aliases": ["بانک سینا"],
        "brand_color_light": "#2C3E50",
        "brand_color_dark": "#1A252F",
    },
)
