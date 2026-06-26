#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔══════════════════════════════════════════════════════════════════════════╗
║           ТЕЛЕГРАМ БОТ "МІНИ СВІТУ" — ІНФОРМАЦІЙНИЙ ДОВІДНИК            ║
║                                                                          ║
║  Мета: освітній бот про протипіхотні та протитанкові міни,               ║
║        їх ознаки, дії при виявленні та заходи безпеки.                   ║
╚══════════════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  КРОК 1 — ВСТАНОВЛЕННЯ PYTHON
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Windows:
    Завантажте з https://www.python.org/downloads/
    Під час встановлення поставте ✓ "Add Python to PATH"
    Перевірка: відкрийте CMD → python --version

  Linux / macOS:
    sudo apt install python3 python3-pip   # Ubuntu/Debian
    brew install python                    # macOS (Homebrew)
    Перевірка: python3 --version

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  КРОК 2 — ВСТАНОВЛЕННЯ БІБЛІОТЕКИ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Відкрийте термінал (CMD / PowerShell / Terminal) і виконайте:

    pip install pyTelegramBotAPI

  Або для Python 3 на Linux/macOS:
    pip3 install pyTelegramBotAPI

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  КРОК 3 — СТВОРЕННЯ БОТА В ТЕЛЕГРАМ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. Відкрийте Telegram і знайдіть @BotFather
  2. Надішліть команду: /newbot
  3. Введіть ім'я бота, наприклад: Mine Info Bot
  4. Введіть username, наприклад: mine_info_ukraine_bot
  5. BotFather надасть вам TOKEN — скопіюйте його
  6. Вставте токен у змінну BOT_TOKEN нижче

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  КРОК 4 — ЗАПУСК БОТА
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Збережіть цей файл як mine_info_bot.py, потім:

    python mine_info_bot.py          # Windows
    python3 mine_info_bot.py         # Linux/macOS

  Бот працює, поки термінал відкритий.
  Для постійної роботи використайте сервер або:
    nohup python3 mine_info_bot.py &   # фоновий режим Linux

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import telebot
from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

# ─────────────────────────────────────────────────────────────
#  !! ЗАМІНІТЬ НА СВІЙ ТОКЕН ВІД @BotFather !!
# ─────────────────────────────────────────────────────────────
BOT_TOKEN = "ВАШ_ТОКЕН_ТУТ"
# ─────────────────────────────────────────────────────────────

bot = telebot.TeleBot(BOT_TOKEN)


# ═══════════════════════════════════════════════════════════════
#  БАЗА ЗНАНЬ — ДАНІ ПРО МІНИ
# ═══════════════════════════════════════════════════════════════

MINES_DATA = {
    # ── ПРОТИПІХОТНІ МІНИ ──────────────────────────────────────
    "pfm1": {
        "name": "ПФМ-1 «Метелик»",
        "type": "Протипіхотна розкидна",
        "country": "🇷🇺 СРСР / Росія",
        "description": (
            "Невелика пластикова міна у формі метелика або крила.\n"
            "Розкидається з літаків, гелікоптерів та артилерійських снарядів.\n"
            "Не має механізму самознешкодження в старих версіях — залишається небезпечною роками."
        ),
        "appearance": (
            "🔸 Розмір: ~6 × 4 × 2 см\n"
            "🔸 Колір: зелений, коричневий або темно-зелений (камуфляжний)\n"
            "🔸 Форма: схожа на крило метелика або листок\n"
            "🔸 Матеріал: пластик"
        ),
        "danger": "⚠️ Спрацьовує від мінімального натискання (~0,5 кг). Відриває стопу або кілька пальців ніг.",
        "action": (
            "🚫 НЕ ТОРКАТИСЯ!\n"
            "📍 Запам'ятайте місце та позначте його.\n"
            "📞 Повідомте ДСНС: 101 або Нацполіцію: 102\n"
            "🏃 Відійдіть тим самим шляхом, яким прийшли."
        ),
        "emoji": "🦋",
    },
    "tm62": {
        "name": "ТМ-62 (серія)",
        "type": "Протитанкова протиднищева",
        "country": "🇷🇺 СРСР / Росія",
        "description": (
            "Одна з найпоширеніших протитанкових мін у світі. "
            "Існує у версіях ТМ-62М, ТМ-62П, ТМ-62Т тощо.\n"
            "Масово застосовується в зонах конфліктів."
        ),
        "appearance": (
            "🔸 Діаметр: ~32 см, висота ~12 см\n"
            "🔸 Форма: циліндрична або прямокутна\n"
            "🔸 Матеріал: метал або пластик (залежно від версії)\n"
            "🔸 Колір: зелений, іржавий або камуфляжний\n"
            "🔸 Маса вибухівки: ~7–7,5 кг"
        ),
        "danger": "⚠️ Спрацьовує від тиску 150–500 кг. Знищує легкоброньовану техніку, смертельна для людей поруч.",
        "action": (
            "🚫 КАТЕГОРИЧНО НЕ ТОРКАТИСЯ!\n"
            "📍 Позначте район, попередьте інших.\n"
            "📞 ДСНС: 101 | Поліція: 102 | HALO Trust: +380 800 50 51 01\n"
            "🏃 Евакуюйтесь на відстань мінімум 300 метрів."
        ),
        "emoji": "💣",
    },
    "vs50": {
        "name": "VS-50",
        "type": "Протипіхотна натискна",
        "country": "🇮🇹 Італія",
        "description": (
            "Кругла пластикова протипіхотна міна. "
            "Широко використовувалась у конфліктах Африки, Балкан та Близького Сходу. "
            "Через мінімальний вміст металу важко виявляється детекторами."
        ),
        "appearance": (
            "🔸 Діаметр: ~9 см, висота ~4 см\n"
            "🔸 Форма: кругла, плоска\n"
            "🔸 Матеріал: зелений або сірий пластик\n"
            "🔸 На верхній кришці — невеликий виступ (кнопка тиску)"
        ),
        "danger": "⚠️ Спрацьовує від ~5 кг. Серйозне травмування стопи та гомілки.",
        "action": (
            "🚫 НЕ ТОРКАТИСЯ!\n"
            "📍 Позначте місце підручними засобами (гілки, каміння).\n"
            "📞 Повідомте саперів або ДСНС: 101\n"
            "🏃 Відійдіть обережно назад по своїх слідах."
        ),
        "emoji": "🔴",
    },
    "mon50": {
        "name": "МОН-50 / МОН-90 / МОН-100",
        "type": "Протипіхотна спрямованої дії (осколкова)",
        "country": "🇷🇺 СРСР / Росія",
        "description": (
            "Міна спрямованої дії — аналог американської M18 Claymore.\n"
            "Випускає 540 металевих кульок у секторі 54° на відстань до 50 метрів.\n"
            "Може встановлюватись у режимі дистанційного підриву або натяжної дії."
        ),
        "appearance": (
            "🔸 Розмір: ~22 × 15 × 6 см\n"
            "🔸 Форма: прямокутна, вигнута (увігнута сторона — до ворога)\n"
            "🔸 Матеріал: зелений пластик\n"
            "🔸 На корпусі написи і стрілки напрямку ураження\n"
            "🔸 Часто встановлена на ніжках-підпорках"
        ),
        "danger": "⚠️ Смертельна у секторі ураження до 50 м. Небезпечні осколки до 150 м.",
        "action": (
            "🚫 НЕ ПІДХОДИТИ до підозрілих предметів на ніжках!\n"
            "🔍 Слідкуйте за натяжними дротами або мотузками.\n"
            "📞 ДСНС: 101\n"
            "🏃 Відійдіть убік від напрямку, куди «дивиться» увігнута сторона."
        ),
        "emoji": "📡",
    },
    "pomz2": {
        "name": "ПОМЗ-2 / ПОМЗ-2М",
        "type": "Протипіхотна осколкова натяжна",
        "country": "🇷🇺 СРСР / Росія",
        "description": (
            "Міна на металевому кілочку з натяжним дротом-розтяжкою.\n"
            "Одна з найдавніших і найпоширеніших мін у світі.\n"
            "Масово застосовується в Україні та інших зонах конфліктів."
        ),
        "appearance": (
            "🔸 Висота над землею: 10–15 см\n"
            "🔸 Форма: циліндр із нарізним корпусом на кілочку\n"
            "🔸 Матеріал: чавун або сталь\n"
            "🔸 Колір: іржавий або темно-зелений\n"
            "🔸 Від неї відходить тонкий дріт (розтяжка) на рівні ніг"
        ),
        "danger": "⚠️ Осколкове ураження в радіусі 4–6 метрів. Смертельна на відстані до 2 метрів.",
        "action": (
            "🚫 НЕ ЧІПАТИ ДРІТ! Будь-яке натягування або обрив — підрив.\n"
            "👀 ЗАВЖДИ дивіться під ноги в зонах бойових дій.\n"
            "📞 ДСНС: 101 | Поліція: 102\n"
            "🏃 Якщо побачили дріт — зупиніться, обережно перестрибніть або поверніться назад."
        ),
        "emoji": "⚙️",
    },
    "at2": {
        "name": "AT2 / STABO",
        "type": "Протитанкова розкидна самоліквідуюча",
        "country": "🇩🇪 Німеччина",
        "description": (
            "Артилерійська суббоєприпасна міна стандарту НАТО.\n"
            "Розкидається касетними боєприпасами. "
            "Має таймер самоліквідації (зазвичай 4–12 годин або 2–7 діб залежно від версії), "
            "але механізм може відмовити."
        ),
        "appearance": (
            "🔸 Розмір: ~13 × 13 × 4 см\n"
            "🔸 Форма: квадратна плоска 'шайба'\n"
            "🔸 Матеріал: хакі або оливковий пластик\n"
            "🔸 Після розкидання можуть бути частково в ґрунті або траві"
        ),
        "danger": "⚠️ Спрацьовує від тиску техніки. Навіть 'прострочена' (після таймера) може залишатись активною.",
        "action": (
            "🚫 НЕ ТОРКАТИСЯ — таймер може дати збій!\n"
            "📞 ДСНС: 101\n"
            "🏃 Позначте площу і евакуюйте людей з зони."
        ),
        "emoji": "🟫",
    },
    "dm31": {
        "name": "DM31 / PARM",
        "type": "Протипіхотна осколкова натяжна/сейсмічна",
        "country": "🇩🇪 Німеччина",
        "description": (
            "Сучасна протипіхотна міна з розтяжкою або датчиком наближення.\n"
            "Використовується країнами НАТО. "
            "Дозволяє дистанційне встановлення та має режим самоліквідації."
        ),
        "appearance": (
            "🔸 Форма: циліндрична або конічна\n"
            "🔸 Матеріал: зелений або камуфляжний пластик\n"
            "🔸 Може мати антену або дроти-розтяжки"
        ),
        "danger": "⚠️ Осколкове ураження до 25 метрів.",
        "action": (
            "🚫 НЕ ПІДХОДИТИ!\n"
            "📞 Зверніться до саперів або ДСНС: 101"
        ),
        "emoji": "🔵",
    },
    "m14": {
        "name": "M14 «Toe Popper»",
        "type": "Протипіхотна натискна мінімальна",
        "country": "🇺🇸 США",
        "description": (
            "Одна з найменших протипіхотних мін у світі. "
            "Розроблена у 1950-х, широко поширена по всьому світу.\n"
            "Майже повністю пластикова — вкрай важко виявити."
        ),
        "appearance": (
            "🔸 Діаметр: ~5,5 см, висота ~4 см\n"
            "🔸 Форма: маленький зелений або коричневий циліндр\n"
            "🔸 Майже не містить металу\n"
            "🔸 Часто повністю прикрита ґрунтом або листям"
        ),
        "danger": "⚠️ Невелика заряд (~30 г вибухівки) — але гарантовано відриває пальці або стопу.",
        "action": (
            "🚫 НІКОЛИ не ходити по незнайомій траві/листю в зонах конфліктів!\n"
            "📞 ДСНС: 101\n"
            "👟 Ходіть тільки по відомих безпечних маршрутах."
        ),
        "emoji": "🟢",
    },
}

# Корисні контакти
CONTACTS = {
    "ukraine": {
        "title": "🇺🇦 Україна — Екстрені служби",
        "info": (
            "📞 *ДСНС (пожежна/сапери):* 101\n"
            "📞 *Поліція:* 102\n"
            "📞 *Екстрена:* 112\n\n"
            "🌐 *Гаряча лінія розмінування HALO Trust:*\n"
            "+380 800 505 101 (безкоштовно)\n\n"
            "🌐 *Міжнародна протимінна служба (UNMAS):*\n"
            "ukraine@unmas.org\n\n"
            "📍 *Позначте місце на карті та сфотографуйте здалеку* "
            "(мінімум 50 м) — це допоможе саперам."
        ),
    },
    "international": {
        "title": "🌍 Міжнародні організації",
        "info": (
            "🔵 *HALO Trust:* www.halotrust.org\n"
            "   Одна з найбільших організацій з розмінування.\n\n"
            "🟡 *MAG (Mines Advisory Group):* www.maginternational.org\n"
            "   Допомога жертвам та розмінування.\n\n"
            "🟢 *UNMAS:* www.unmas.org\n"
            "   Координаційний центр ООН з протимінної діяльності.\n\n"
            "🔴 *ICBL:* www.icbl.org\n"
            "   Міжнародна кампанія за заборону протипіхотних мін."
        ),
    },
}

# Правила безпеки
SAFETY_RULES = """
🛡️ *ЗОЛОТІ ПРАВИЛА БЕЗПЕКИ В МІНОНЕБЕЗПЕЧНИХ РАЙОНАХ*

━━━━━━━━━━━━━━━━━━━━━━

*НІКОЛИ:*
🚫 Не торкайтесь невідомих предметів
🚫 Не піднімайте нічого незнайомого з землі
🚫 Не ходіть по незнайомій місцевості без підтвердження безпеки
🚫 Не тягніть дроти, мотузки або нитки
🚫 Не відхиляйтесь від перевірених маршрутів

━━━━━━━━━━━━━━━━━━━━━━

*ЗАВЖДИ:*
✅ Дивіться під ноги та навколо
✅ Звертайте увагу на незвичні предмети
✅ Запитуйте місцевих жителів про безпечні маршрути
✅ Повідомляйте про знахідки за 101 або 102
✅ Позначайте небезпечні місця підручними засобами

━━━━━━━━━━━━━━━━━━━━━━

*ОЗНАКИ МІННОГО ПОЛЯ:*
⚠️ Таблички «Небезпека мін» / «MINES»
⚠️ Мертві тварини поруч зі стежкою
⚠️ Підозрілі горбки або виїмки в землі
⚠️ Тонкі дроти на рівні ніг
⚠️ Предмети незвичної форми в траві або ґрунті
⚠️ Покинута техніка або будівлі без людей навколо

━━━━━━━━━━━━━━━━━━━━━━

*ЩО РОБИТИ ПРИ ВИЯВЛЕННІ ПІДОЗРІЛОГО ПРЕДМЕТА:*
1️⃣ Зупиніться. Не рухайтесь різко.
2️⃣ Повільно відступіть своїм же шляхом.
3️⃣ Попередьте оточуючих.
4️⃣ Позначте місце (якщо безпечно).
5️⃣ Зателефонуйте 101 або 102.
6️⃣ Залишайтесь поряд (на безпечній відстані) для вказівок.
"""


# ═══════════════════════════════════════════════════════════════
#  КЛАВІАТУРИ
# ═══════════════════════════════════════════════════════════════

def main_menu_keyboard():
    """Головне меню бота."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("💣 Протитанкові міни"),
        KeyboardButton("🚶 Протипіхотні міни"),
        KeyboardButton("🛡️ Правила безпеки"),
        KeyboardButton("📞 Екстрені контакти"),
        KeyboardButton("ℹ️ Про бота"),
    )
    return markup


def mines_inline_keyboard(mine_type: str):
    """Inline-кнопки для вибору конкретної міни."""
    markup = InlineKeyboardMarkup(row_width=1)

    if mine_type == "anti_tank":
        markup.add(
            InlineKeyboardButton("💣 ТМ-62 (СРСР/Росія)", callback_data="mine_tm62"),
            InlineKeyboardButton("🟫 AT2/STABO (Німеччина)", callback_data="mine_at2"),
        )
    elif mine_type == "anti_personnel":
        markup.add(
            InlineKeyboardButton("🦋 ПФМ-1 «Метелик» (СРСР)", callback_data="mine_pfm1"),
            InlineKeyboardButton("🔴 VS-50 (Італія)", callback_data="mine_vs50"),
            InlineKeyboardButton("📡 МОН-50/90/100 (СРСР)", callback_data="mine_mon50"),
            InlineKeyboardButton("⚙️ ПОМЗ-2 (СРСР)", callback_data="mine_pomz2"),
            InlineKeyboardButton("🔵 DM31/PARM (Німеччина)", callback_data="mine_dm31"),
            InlineKeyboardButton("🟢 M14 (США)", callback_data="mine_m14"),
        )

    markup.add(InlineKeyboardButton("🏠 Головне меню", callback_data="main_menu"))
    return markup


def mine_detail_keyboard(mine_id: str):
    """Кнопки деталей міни."""
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("👁️ Зовнішній вигляд", callback_data=f"look_{mine_id}"),
        InlineKeyboardButton("⚠️ Небезпека", callback_data=f"danger_{mine_id}"),
        InlineKeyboardButton("🆘 Що робити", callback_data=f"action_{mine_id}"),
        InlineKeyboardButton("◀️ Назад", callback_data="back_to_list"),
        InlineKeyboardButton("🏠 Меню", callback_data="main_menu"),
    )
    return markup


# ═══════════════════════════════════════════════════════════════
#  ОБРОБНИКИ КОМАНД
# ═══════════════════════════════════════════════════════════════

@bot.message_handler(commands=["start"])
def cmd_start(message):
    """Вітання при старті бота."""
    name = message.from_user.first_name or "друже"
    text = (
        f"👋 Вітаю, *{name}*!\n\n"
        "Я — інформаційний бот про *протипіхотні та протитанкові міни* у світі.\n\n"
        "🎯 *Що вмію:*\n"
        "• Надавати інформацію про різні типи мін\n"
        "• Описувати зовнішній вигляд та ознаки мін\n"
        "• Пояснювати правила безпеки\n"
        "• Давати контакти екстрених служб\n\n"
        "⚠️ *ВАЖЛИВО:* Бот несе виключно *освітню функцію*.\n"
        "При виявленні підозрілого предмета — *НЕ ТОРКАТИСЯ* "
        "та одразу дзвонити *101*.\n\n"
        "Оберіть розділ у меню нижче 👇"
    )
    bot.send_message(
        message.chat.id,
        text,
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(),
    )


@bot.message_handler(commands=["help"])
def cmd_help(message):
    """Довідка по командах."""
    text = (
        "*Доступні команди:*\n\n"
        "/start — Запустити бота\n"
        "/help — Показати довідку\n"
        "/safety — Правила безпеки\n"
        "/contacts — Екстрені контакти\n"
        "/antitank — Протитанкові міни\n"
        "/antipersonnel — Протипіхотні міни\n"
        "/about — Про бота\n\n"
        "Або скористайтесь кнопками меню 👇"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")


@bot.message_handler(commands=["safety"])
def cmd_safety(message):
    bot.send_message(
        message.chat.id,
        SAFETY_RULES,
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(),
    )


@bot.message_handler(commands=["contacts"])
def cmd_contacts(message):
    send_contacts(message.chat.id)


@bot.message_handler(commands=["antitank"])
def cmd_antitank(message):
    bot.send_message(
        message.chat.id,
        "💣 *Протитанкові міни*\n\nОберіть міну для детальної інформації:",
        parse_mode="Markdown",
        reply_markup=mines_inline_keyboard("anti_tank"),
    )


@bot.message_handler(commands=["antipersonnel"])
def cmd_antipersonnel(message):
    bot.send_message(
        message.chat.id,
        "🚶 *Протипіхотні міни*\n\nОберіть міну для детальної інформації:",
        parse_mode="Markdown",
        reply_markup=mines_inline_keyboard("anti_personnel"),
    )


@bot.message_handler(commands=["about"])
def cmd_about(message):
    send_about(message.chat.id)


# ═══════════════════════════════════════════════════════════════
#  ОБРОБНИКИ ТЕКСТОВИХ ПОВІДОМЛЕНЬ (КНОПКИ МЕНЮ)
# ═══════════════════════════════════════════════════════════════

@bot.message_handler(func=lambda m: m.text == "💣 Протитанкові міни")
def text_antitank(message):
    bot.send_message(
        message.chat.id,
        "💣 *Протитанкові міни*\n\nОберіть міну для детальної інформації:",
        parse_mode="Markdown",
        reply_markup=mines_inline_keyboard("anti_tank"),
    )


@bot.message_handler(func=lambda m: m.text == "🚶 Протипіхотні міни")
def text_antipersonnel(message):
    bot.send_message(
        message.chat.id,
        "🚶 *Протипіхотні міни*\n\nОберіть міну для детальної інформації:",
        parse_mode="Markdown",
        reply_markup=mines_inline_keyboard("anti_personnel"),
    )


@bot.message_handler(func=lambda m: m.text == "🛡️ Правила безпеки")
def text_safety(message):
    bot.send_message(
        message.chat.id,
        SAFETY_RULES,
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(),
    )


@bot.message_handler(func=lambda m: m.text == "📞 Екстрені контакти")
def text_contacts(message):
    send_contacts(message.chat.id)


@bot.message_handler(func=lambda m: m.text == "ℹ️ Про бота")
def text_about(message):
    send_about(message.chat.id)


# ═══════════════════════════════════════════════════════════════
#  ДОПОМІЖНІ ФУНКЦІЇ ВІДПРАВКИ
# ═══════════════════════════════════════════════════════════════

def send_contacts(chat_id: int):
    """Відправити контакти екстрених служб."""
    ua = CONTACTS["ukraine"]
    intl = CONTACTS["international"]

    bot.send_message(
        chat_id,
        f"*{ua['title']}*\n\n{ua['info']}",
        parse_mode="Markdown",
    )
    bot.send_message(
        chat_id,
        f"*{intl['title']}*\n\n{intl['info']}",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(),
    )


def send_about(chat_id: int):
    """Інформація про бота."""
    text = (
        "ℹ️ *Про цей бот*\n\n"
        "Цей бот створено з метою *підвищення обізнаності* "
        "населення про небезпеку мін.\n\n"
        "🎓 *Для кого:*\n"
        "• Мирні жителі в зонах конфліктів\n"
        "• Волонтери та рятувальники\n"
        "• Журналісти та медики\n"
        "• Всі, хто хоче знати, як уберегти себе\n\n"
        "⚖️ *Важлива примітка:*\n"
        "Інформація носить виключно *освітній характер*. "
        "Ніколи не намагайтеся самостійно знешкоджувати вибухонебезпечні предмети!\n\n"
        "📊 *У базі даних:*\n"
        f"• {len(MINES_DATA)} типів мін\n"
        "• Інформація про зовнішній вигляд\n"
        "• Рівні небезпеки\n"
        "• Правила безпеки\n"
        "• Контакти служб розмінування"
    )
    bot.send_message(
        chat_id,
        text,
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(),
    )


def send_mine_info(chat_id: int, mine_id: str):
    """Відправити загальну інформацію про міну."""
    mine = MINES_DATA.get(mine_id)
    if not mine:
        bot.send_message(chat_id, "❌ Міну не знайдено.")
        return

    text = (
        f"{mine['emoji']} *{mine['name']}*\n\n"
        f"🏷️ *Тип:* {mine['type']}\n"
        f"🌍 *Країна виробник:* {mine['country']}\n\n"
        f"📖 *Опис:*\n{mine['description']}"
    )
    bot.send_message(
        chat_id,
        text,
        parse_mode="Markdown",
        reply_markup=mine_detail_keyboard(mine_id),
    )


# ═══════════════════════════════════════════════════════════════
#  ОБРОБНИКИ INLINE CALLBACK
# ═══════════════════════════════════════════════════════════════

@bot.callback_query_handler(func=lambda call: call.data.startswith("mine_"))
def cb_mine_info(call):
    """Показати інформацію про конкретну міну."""
    mine_id = call.data.replace("mine_", "")
    mine = MINES_DATA.get(mine_id)
    if not mine:
        bot.answer_callback_query(call.id, "Міну не знайдено")
        return

    bot.answer_callback_query(call.id)
    send_mine_info(call.message.chat.id, mine_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("look_"))
def cb_look(call):
    """Показати зовнішній вигляд міни."""
    mine_id = call.data.replace("look_", "")
    mine = MINES_DATA.get(mine_id)
    if not mine:
        return

    bot.answer_callback_query(call.id)
    text = (
        f"👁️ *Зовнішній вигляд — {mine['name']}*\n\n"
        f"{mine['appearance']}"
    )
    bot.send_message(
        call.message.chat.id,
        text,
        parse_mode="Markdown",
        reply_markup=mine_detail_keyboard(mine_id),
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("danger_"))
def cb_danger(call):
    """Показати рівень небезпеки міни."""
    mine_id = call.data.replace("danger_", "")
    mine = MINES_DATA.get(mine_id)
    if not mine:
        return

    bot.answer_callback_query(call.id)
    text = (
        f"⚠️ *Рівень небезпеки — {mine['name']}*\n\n"
        f"{mine['danger']}"
    )
    bot.send_message(
        call.message.chat.id,
        text,
        parse_mode="Markdown",
        reply_markup=mine_detail_keyboard(mine_id),
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("action_"))
def cb_action(call):
    """Показати, що робити при виявленні міни."""
    mine_id = call.data.replace("action_", "")
    mine = MINES_DATA.get(mine_id)
    if not mine:
        return

    bot.answer_callback_query(call.id)
    text = (
        f"🆘 *Що робити при виявленні — {mine['name']}*\n\n"
        f"{mine['action']}\n\n"
        "⚡ *Пам'ятайте:* Ваше життя важливіше за будь-який предмет!"
    )
    bot.send_message(
        call.message.chat.id,
        text,
        parse_mode="Markdown",
        reply_markup=mine_detail_keyboard(mine_id),
    )


@bot.callback_query_handler(func=lambda call: call.data == "back_to_list")
def cb_back_to_list(call):
    """Повернутись до списку мін."""
    bot.answer_callback_query(call.id)
    # Показуємо обидва типи
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("💣 Протитанкові міни", callback_data="show_antitank"),
        InlineKeyboardButton("🚶 Протипіхотні міни", callback_data="show_antipersonnel"),
        InlineKeyboardButton("🏠 Головне меню", callback_data="main_menu"),
    )
    bot.send_message(
        call.message.chat.id,
        "📋 *Оберіть категорію:*",
        parse_mode="Markdown",
        reply_markup=markup,
    )


@bot.callback_query_handler(func=lambda call: call.data == "show_antitank")
def cb_show_antitank(call):
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        "💣 *Протитанкові міни*\n\nОберіть міну:",
        parse_mode="Markdown",
        reply_markup=mines_inline_keyboard("anti_tank"),
    )


@bot.callback_query_handler(func=lambda call: call.data == "show_antipersonnel")
def cb_show_antipersonnel(call):
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        "🚶 *Протипіхотні міни*\n\nОберіть міну:",
        parse_mode="Markdown",
        reply_markup=mines_inline_keyboard("anti_personnel"),
    )


@bot.callback_query_handler(func=lambda call: call.data == "main_menu")
def cb_main_menu(call):
    """Повернутись до головного меню."""
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        "🏠 *Головне меню*\n\nОберіть розділ:",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(),
    )


# ═══════════════════════════════════════════════════════════════
#  ОБРОБНИК НЕВІДОМИХ ПОВІДОМЛЕНЬ
# ═══════════════════════════════════════════════════════════════

@bot.message_handler(func=lambda m: True)
def fallback_handler(message):
    """Відповідь на невідомі повідомлення."""
    bot.send_message(
        message.chat.id,
        "🤔 Я не розумію цієї команди.\n\n"
        "Скористайтесь кнопками меню нижче або введіть /help для довідки.",
        reply_markup=main_menu_keyboard(),
    )


# ═══════════════════════════════════════════════════════════════
#  ЗАПУСК БОТА
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("━" * 50)
    print("  🤖 БОТ «МІНИ СВІТУ» ЗАПУСКАЄТЬСЯ...")
    print("━" * 50)
    print(f"  📌 Версія: 1.0")
    print(f"  📦 Мін у базі: {len(MINES_DATA)}")
    print("━" * 50)
    print("  ✅ Бот запущено! Натисніть Ctrl+C для зупинки.")
    print("━" * 50)

    # none_stop=True — автоматично відновлює з'єднання при помилках мережі
    bot.infinity_polling(none_stop=True, interval=1)