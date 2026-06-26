"""
╔══════════════════════════════════════════════════════════════╗
║         ТАНКОВИЙ ЧАТ-БОТ | КОМАНДНИЙ ЦЕНТР v2.0             ║
║         Від Першої світової до сьогодні                      ║
║         API: Anthropic Claude | UI: tkinter                  ║
╚══════════════════════════════════════════════════════════════╝

ВСТАНОВЛЕННЯ:
  pip install anthropic

КЛЮЧ API:
  Встав свій ключ у змінну ANTHROPIC_API_KEY нижче
  або встанови змінну середовища ANTHROPIC_API_KEY
"""

import os
import sys
import threading
import datetime
import tkinter as tk
from tkinter import scrolledtext, font as tkfont


# ─────────────────────────────────────────────
#  НАЛАШТУВАННЯ — зміни тільки тут
# ─────────────────────────────────────────────
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")   # ← або встав ключ тут у лапках
MODEL_NAME        = "claude-sonnet-4-6"
MAX_TOKENS        = 1024

SYSTEM_PROMPT = """Ти — провідний військовий аналітик і експерт з бронетехніки.
Твоя спеціалізація: танки від 1916 року (WWI) до сучасності.

Відповідай ВИКЛЮЧНО УКРАЇНСЬКОЮ МОВОЮ.
Стиль: чіткий, технічний, структурований. Використовуй факти, цифри, порівняння.
Формат відповіді: коротко й точно — без зайвої «води».
Коли є технічні характеристики — наводь їх.
Якщо питання не стосується танків або бронетехніки — ввічливо відмов і поясни свою спеціалізацію."""


# ─────────────────────────────────────────────
#  ІМПОРТ ANTHROPIC
# ─────────────────────────────────────────────
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


# ─────────────────────────────────────────────
#  ПАЛІТРА КОЛЬОРІВ (військовий термінал)
# ─────────────────────────────────────────────
C = {
    "bg_dark":    "#0d0d0d",   # основний фон
    "bg_panel":   "#111111",   # фон панелей
    "bg_header":  "#0a1a0a",   # темно-зелена шапка
    "bg_input":   "#080808",   # фон поля вводу
    "bg_btn_red": "#1a0505",   # фон кнопки «вогонь»
    "bg_btn_grn": "#0a1a08",   # фон зелених кнопок

    "accent_gold":  "#c9a640",  # золотий акцент
    "accent_green": "#39ff14",  # phosphor green (термінальний)
    "accent_cyan":  "#00e5cc",  # блакитний для користувача
    "accent_red":   "#ff4040",  # червоний для кнопки
    "accent_amber": "#ffb300",  # бурштиновий для системи

    "text_dim":   "#4a5a4a",   # приглушений текст
    "text_mid":   "#708870",   # середній (час, роздільники)
    "text_light":  "#b0d0b0",  # світло-зелений (bot msg)
    "text_white":  "#e8f0e8",  # майже білий

    "border":     "#1e3a1e",   # рамки
}


# ─────────────────────────────────────────────
#  ШВИДКІ ЗАПИТИ (кнопки-ярлики)
# ─────────────────────────────────────────────
QUICK_QUERIES = [
    ("WWI",       "Розкажи про перші танки Першої світової: Mark I, A7V — характеристики та бойове застосування"),
    ("Т-34",      "Чому Т-34 вважається найкращим танком WWII? Порівняй Т-34/76 та Т-34/85"),
    ("Tiger I",   "Panzerkampfwagen VI Tiger I: характеристики, переваги та слабкі місця"),
    ("Abrams",    "M1 Abrams: еволюція від A1 до SEPv3, характеристики та бойові застосування"),
    ("Leopard 2", "Leopard 2: версії від A4 до A8, порівняй з Abrams"),
    ("🇺🇦 ЗСУ",    "Танковий парк України: Т-64, Оплот, Булат — стан та можливості"),
    ("Т-14",      "Т-14 Армата — революція чи блеф? Реальні можливості та проблеми"),
    ("TOP-5",     "Топ-5 найкращих основних бойових танків світу станом на 2024 рік з обґрунтуванням"),
]


# ═══════════════════════════════════════════════════════════════
#  ГОЛОВНИЙ КЛАС ДОДАТКУ
# ═══════════════════════════════════════════════════════════════
class TankCommandCenter:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.chat_history: list[dict] = []   # Зберігаємо всю розмову для контексту
        self.is_generating = False

        # Ініціалізація Anthropic
        self.client = self._init_client()

        # Будуємо UI
        self._configure_window()
        self._build_header()
        self._build_quick_panel()
        self._build_chat_area()
        self._build_input_area()
        self._build_statusbar()

        # Привітання
        self._show_welcome()


    # ──────────────────────────────────────────
    #  ІНІЦІАЛІЗАЦІЯ API
    # ──────────────────────────────────────────
    def _init_client(self):
        if not ANTHROPIC_AVAILABLE:
            return None
        key = ANTHROPIC_API_KEY.strip()
        if not key:
            return None
        try:
            client = anthropic.Anthropic(api_key=key)
            return client
        except Exception as e:
            print(f"[ERROR] Anthropic init: {e}")
            return None


    # ──────────────────────────────────────────
    #  НАЛАШТУВАННЯ ВІКНА
    # ──────────────────────────────────────────
    def _configure_window(self):
        self.root.title("⚔  TANK COMMAND CENTER  |  Танковий Аналітик v2.0")
        self.root.geometry("980x760")
        self.root.minsize(720, 540)
        self.root.configure(bg=C["bg_dark"])

        # Відцентрувати вікно
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth()  - 980) // 2
        y = (self.root.winfo_screenheight() - 760) // 2
        self.root.geometry(f"980x760+{x}+{y}")


    # ──────────────────────────────────────────
    #  ШАПКА (HEADER)
    # ──────────────────────────────────────────
    def _build_header(self):
        hdr = tk.Frame(self.root, bg=C["bg_header"], height=72)
        hdr.pack(fill=tk.X)
        hdr.pack_propagate(False)

        # Ліворуч — назва
        left = tk.Frame(hdr, bg=C["bg_header"])
        left.pack(side=tk.LEFT, padx=20, pady=8)

        tk.Label(
            left, text="⚔  TANK COMMAND CENTER",
            font=("Courier New", 18, "bold"),
            bg=C["bg_header"], fg=C["accent_gold"]
        ).pack(anchor=tk.W)

        tk.Label(
            left, text="Танковий Інтелектуальний Аналітик · WWI → XXI",
            font=("Courier New", 9),
            bg=C["bg_header"], fg=C["text_mid"]
        ).pack(anchor=tk.W)

        # Праворуч — індикатор статусу
        right = tk.Frame(hdr, bg=C["bg_header"])
        right.pack(side=tk.RIGHT, padx=20)

        if self.client:
            dot_color, status_txt, model_txt = C["accent_green"], "ONLINE", MODEL_NAME
        elif not ANTHROPIC_AVAILABLE:
            dot_color, status_txt, model_txt = C["accent_red"], "NO LIB", "pip install anthropic"
        else:
            dot_color, status_txt, model_txt = "#ff9900", "NO KEY", "Встав API ключ"

        tk.Label(
            right, text="●", font=("Arial", 14),
            bg=C["bg_header"], fg=dot_color
        ).pack(side=tk.LEFT, padx=(0, 6))

        info = tk.Frame(right, bg=C["bg_header"])
        info.pack(side=tk.LEFT)
        tk.Label(info, text=status_txt, font=("Courier New", 11, "bold"),
                 bg=C["bg_header"], fg=dot_color).pack(anchor=tk.W)
        tk.Label(info, text=model_txt, font=("Courier New", 8),
                 bg=C["bg_header"], fg=C["text_dim"]).pack(anchor=tk.W)

        # Горизонтальний роздільник під шапкою
        tk.Frame(self.root, bg=C["border"], height=1).pack(fill=tk.X)


    # ──────────────────────────────────────────
    #  ПАНЕЛЬ ШВИДКИХ КНОПОК
    # ──────────────────────────────────────────
    def _build_quick_panel(self):
        container = tk.Frame(self.root, bg=C["bg_panel"], pady=6)
        container.pack(fill=tk.X, padx=0)

        tk.Label(
            container, text="  ЗАВДАННЯ:",
            font=("Courier New", 8, "bold"),
            bg=C["bg_panel"], fg=C["text_dim"]
        ).pack(side=tk.LEFT)

        for label, query in QUICK_QUERIES:
            btn = tk.Button(
                container,
                text=label,
                font=("Courier New", 8, "bold"),
                bg=C["bg_btn_grn"],
                fg=C["accent_gold"],
                activebackground=C["border"],
                activeforeground=C["accent_gold"],
                relief=tk.FLAT,
                padx=10, pady=4,
                cursor="hand2",
                bd=0,
                command=lambda q=query: self._quick_ask(q)
            )
            btn.pack(side=tk.LEFT, padx=2)
            # Hover-ефект
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#152815"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=C["bg_btn_grn"]))

        tk.Frame(self.root, bg=C["border"], height=1).pack(fill=tk.X)


    # ──────────────────────────────────────────
    #  ОБЛАСТЬ ЧАТУ
    # ──────────────────────────────────────────
    def _build_chat_area(self):
        wrapper = tk.Frame(self.root, bg=C["bg_dark"])
        wrapper.pack(fill=tk.BOTH, expand=True, padx=12, pady=(10, 4))

        self.chat_display = scrolledtext.ScrolledText(
            wrapper,
            wrap=tk.WORD,
            font=("Courier New", 11),
            bg=C["bg_input"],
            fg=C["text_light"],
            insertbackground=C["accent_gold"],
            selectbackground="#1e3a1e",
            selectforeground=C["text_white"],
            relief=tk.FLAT,
            padx=16, pady=12,
            spacing1=2, spacing3=6,
            bd=0,
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)

        # Кастомний скролбар — темний
        self.chat_display.vbar.config(
            bg=C["bg_panel"],
            troughcolor=C["bg_dark"],
            width=8,
        )

        # ── Теги форматування ──
        self.chat_display.tag_configure("time",
            foreground=C["text_dim"],
            font=("Courier New", 8))

        self.chat_display.tag_configure("user_label",
            foreground=C["accent_cyan"],
            font=("Courier New", 10, "bold"))

        self.chat_display.tag_configure("user_text",
            foreground=C["text_white"],
            font=("Courier New", 11))

        self.chat_display.tag_configure("bot_label",
            foreground=C["accent_gold"],
            font=("Courier New", 10, "bold"))

        self.chat_display.tag_configure("bot_text",
            foreground=C["text_light"],
            font=("Courier New", 11))

        self.chat_display.tag_configure("system",
            foreground=C["accent_amber"],
            font=("Courier New", 10, "italic"))

        self.chat_display.tag_configure("error",
            foreground=C["accent_red"],
            font=("Courier New", 10, "bold"))

        self.chat_display.tag_configure("sep",
            foreground=C["text_dim"],
            font=("Courier New", 6))

        self.chat_display.tag_configure("header",
            foreground=C["accent_gold"],
            font=("Courier New", 10, "bold"))

        self.chat_display.configure(state=tk.DISABLED)


    # ──────────────────────────────────────────
    #  ПАНЕЛЬ ВВОДУ
    # ──────────────────────────────────────────
    def _build_input_area(self):
        panel = tk.Frame(self.root, bg=C["bg_dark"], pady=0)
        panel.pack(fill=tk.X, padx=12, pady=(4, 6))

        # Рамка навколо поля вводу
        entry_frame = tk.Frame(panel, bg=C["border"], padx=1, pady=1)
        entry_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        inner = tk.Frame(entry_frame, bg=C["bg_input"])
        inner.pack(fill=tk.X)

        # Префікс «>»
        tk.Label(
            inner, text=" > ",
            font=("Courier New", 13, "bold"),
            bg=C["bg_input"], fg=C["accent_green"]
        ).pack(side=tk.LEFT)

        self.input_field = tk.Entry(
            inner,
            font=("Courier New", 12),
            bg=C["bg_input"],
            fg=C["accent_green"],
            insertbackground=C["accent_green"],
            relief=tk.FLAT, bd=0,
            disabledbackground=C["bg_panel"],
            disabledforeground=C["text_dim"],
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=9)

        self.input_field.bind("<Return>",       lambda e: self._send_message())
        self.input_field.bind("<Shift-Return>", lambda e: None)
        self.input_field.focus_set()

        # Кнопки праворуч
        btn_frame = tk.Frame(panel, bg=C["bg_dark"])
        btn_frame.pack(side=tk.RIGHT, padx=(6, 0))

        self.send_btn = tk.Button(
            btn_frame,
            text="  ВОГОНЬ  ",
            font=("Courier New", 11, "bold"),
            bg=C["bg_btn_red"],
            fg=C["accent_red"],
            activebackground="#3a0000",
            activeforeground="#ff6060",
            relief=tk.FLAT, bd=0,
            padx=16, pady=10,
            cursor="hand2",
            command=self._send_message
        )
        self.send_btn.pack(side=tk.LEFT, padx=(0, 4))
        self.send_btn.bind("<Enter>", lambda e: self.send_btn.config(bg="#2a0808"))
        self.send_btn.bind("<Leave>", lambda e: self.send_btn.config(bg=C["bg_btn_red"]))

        clear_btn = tk.Button(
            btn_frame,
            text="  RESET  ",
            font=("Courier New", 10, "bold"),
            bg=C["bg_btn_grn"],
            fg=C["text_mid"],
            activebackground=C["border"],
            activeforeground=C["accent_gold"],
            relief=tk.FLAT, bd=0,
            padx=12, pady=10,
            cursor="hand2",
            command=self._clear_chat
        )
        clear_btn.pack(side=tk.LEFT)
        clear_btn.bind("<Enter>", lambda e: clear_btn.config(bg="#152815"))
        clear_btn.bind("<Leave>", lambda e: clear_btn.config(bg=C["bg_btn_grn"]))


    # ──────────────────────────────────────────
    #  РЯДОК СТАТУСУ
    # ──────────────────────────────────────────
    def _build_statusbar(self):
        tk.Frame(self.root, bg=C["border"], height=1).pack(fill=tk.X)

        bar = tk.Frame(self.root, bg=C["bg_header"], height=24)
        bar.pack(fill=tk.X)
        bar.pack_propagate(False)

        self.status_left = tk.Label(
            bar,
            text="⚡ СИСТЕМА ГОТОВА",
            font=("Courier New", 8),
            bg=C["bg_header"], fg=C["text_mid"],
            anchor=tk.W, padx=12
        )
        self.status_left.pack(side=tk.LEFT)

        self.status_right = tk.Label(
            bar,
            text="",
            font=("Courier New", 8),
            bg=C["bg_header"], fg=C["text_dim"],
            anchor=tk.E, padx=12
        )
        self.status_right.pack(side=tk.RIGHT)


    # ──────────────────────────────────────────
    #  ПРИВІТАННЯ
    # ──────────────────────────────────────────
    def _show_welcome(self):
        lines = [
            ("╔" + "═"*58 + "╗\n", "header"),
            ("║   ⚔  TANK COMMAND CENTER — СИСТЕМА АКТИВОВАНА  ⚔   ║\n", "header"),
            ("║        Танковий Інтелектуальний Аналітик v2.0        ║\n", "header"),
            ("╚" + "═"*58 + "╝\n\n", "header"),
        ]

        if self.client:
            lines += [
                (f"  СТАТУС   : ANTHROPIC API — ПІДКЛЮЧЕНО\n", "system"),
                (f"  МОДЕЛЬ   : {MODEL_NAME}\n", "system"),
                (f"  ЛІМІТИ   : Без обмежень на кількість запитів\n", "system"),
                (f"  КОНТЕКСТ : Зберігається протягом сесії\n\n", "system"),
            ]
        else:
            lines += [
                ("  [ПОПЕРЕДЖЕННЯ] ANTHROPIC API НЕДОСТУПНА\n", "error"),
            ]
            if not ANTHROPIC_AVAILABLE:
                lines.append(("  → Встанови: pip install anthropic\n", "system"))
            else:
                lines += [
                    ("  → Встав ключ у змінну ANTHROPIC_API_KEY у коді\n", "system"),
                    ("  → Або: set ANTHROPIC_API_KEY=sk-ant-...\n", "system"),
                    ("  → Отримай ключ: https://console.anthropic.com\n", "system"),
                ]
            lines.append(("\n  [РЕЖИМ] Локальна база даних (обмежено)\n\n", "system"))

        lines += [
            ("  ЗОНИ ЗНАНЬ:\n", "bot_label"),
            ("  · Перша та Друга світова — Mark I, Tiger, Пантера, Т-34\n", "bot_text"),
            ("  · Холодна війна — Т-54/55/62/64/72, Centurion, M60\n", "bot_text"),
            ("  · Сучасні ОБТ — Abrams, Leopard 2, Оплот, Т-90, Армата\n", "bot_text"),
            ("  · Порівняння, тактика, бронювання, озброєння\n\n", "bot_text"),
            ("  Використовуй кнопки ЗАВДАННЯ або вводи своє питання\n", "system"),
            ("─"*60 + "\n", "sep"),
        ]

        self.chat_display.configure(state=tk.NORMAL)
        for text, tag in lines:
            self.chat_display.insert(tk.END, text, tag)
        self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.see(tk.END)


    # ──────────────────────────────────────────
    #  ВІДПРАВКА ПОВІДОМЛЕННЯ
    # ──────────────────────────────────────────
    def _send_message(self):
        if self.is_generating:
            return

        user_text = self.input_field.get().strip()
        if not user_text:
            return

        self.input_field.delete(0, tk.END)
        now = datetime.datetime.now().strftime("%H:%M:%S")

        # Відображаємо питання користувача
        self._append("\n", "sep")
        self._append(f"  [{now}] ", "time")
        self._append("ОПЕРАТОР › ", "user_label")
        self._append(f"{user_text}\n", "user_text")

        # Заголовок відповіді
        self._append(f"\n  [{now}] ", "time")
        self._append("АНАЛІТИК › ", "bot_label")

        # Блокуємо UI
        self._set_ui_state(generating=True)
        self._set_status("⟳  Генерую відповідь...", f"[{MODEL_NAME}]")

        # Запускаємо в окремому потоці
        t = threading.Thread(
            target=self._ai_worker,
            args=(user_text,),
            daemon=True
        )
        t.start()


    # ──────────────────────────────────────────
    #  AI WORKER (фоновий поток)
    # ──────────────────────────────────────────
    def _ai_worker(self, user_text: str):
        # Додаємо повідомлення у历史
        self.chat_history.append({"role": "user", "content": user_text})

        if not self.client:
            answer = self._local_response(user_text)
            self.root.after(0, self._stream_chunk, answer)
            self.root.after(0, self._finalize_response, True)
            return

        try:
            # Потокова відповідь через Anthropic SDK
            with self.client.messages.stream(
                model=MODEL_NAME,
                max_tokens=MAX_TOKENS,
                system=SYSTEM_PROMPT,
                messages=self.chat_history,
            ) as stream:
                full_response = ""
                for text in stream.text_stream:
                    full_response += text
                    self.root.after(0, self._stream_chunk, text)

            # Зберігаємо відповідь асистента в历史
            self.chat_history.append({"role": "assistant", "content": full_response})
            self.root.after(0, self._finalize_response, True)

        except anthropic.AuthenticationError:
            self.root.after(0, self._stream_chunk,
                "\n[ПОМИЛКА] Невірний API ключ. Перевір ANTHROPIC_API_KEY.")
            self.root.after(0, self._finalize_response, False)

        except anthropic.RateLimitError:
            # Rate limit — чекаємо і повідомляємо
            self.root.after(0, self._stream_chunk,
                "\n[ЛІМІТ] Перевищено rate limit. Зачекай кілька секунд і спробуй знову.")
            self.root.after(0, self._finalize_response, False)

        except anthropic.APIConnectionError:
            self.root.after(0, self._stream_chunk,
                "\n[ПОМИЛКА] Немає з'єднання з API. Перевір інтернет.")
            self.root.after(0, self._finalize_response, False)

        except Exception as e:
            err = f"\n[ПОМИЛКА] {type(e).__name__}: {str(e)[:200]}"
            self.root.after(0, self._stream_chunk, err)
            self.root.after(0, self._finalize_response, False)


    # ──────────────────────────────────────────
    #  ПОТОКОВИЙ ВИВОДУ ТЕКСТУ
    # ──────────────────────────────────────────
    def _stream_chunk(self, chunk: str):
        self.chat_display.configure(state=tk.NORMAL)
        self.chat_display.insert(tk.END, chunk, "bot_text")
        self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.see(tk.END)


    def _finalize_response(self, success: bool):
        self._append("\n" + "─"*60 + "\n", "sep")
        self._set_ui_state(generating=False)
        msg = "⚡ ГОТОВО — Введіть наступне питання" if success else "⚠  Помилка відповіді"
        self._set_status(msg)


    # ──────────────────────────────────────────
    #  ЛОКАЛЬНА БАЗА (fallback без API)
    # ──────────────────────────────────────────
    def _local_response(self, text: str) -> str:
        t = text.lower()

        db = {
            ("mark i", "mark 1", "перший танк", "wwi", "перша світова"): (
                "Mark I (1916) — перший бойовий танк в історії\n"
                "  Маса: 28 тонн   Екіпаж: 8 осіб\n"
                "  Озброєння: 2× гармати Hotchkiss 57мм + кулемети\n"
                "  Швидкість: 6 км/год   Двигун: Daimler 105 к.с.\n"
                "  Вперше застосований 15 вересня 1916 на Соммі.\n"
                "  Існувало 2 варіанти: «самець» (гармати) і «самиця» (кулемети)."
            ),
            ("т-34", "t-34", "т34"): (
                "Т-34 — символ радянської бронетехніки WWII\n"
                "  Т-34/76: маса 26т, гармата 76мм, броня 45мм\n"
                "  Т-34/85: маса 32т, гармата 85мм, броня 75мм\n"
                "  Швидкість: 55 км/год   Двигун: В-2 (500 к.с.)\n"
                "  Нахилена броня 60° = ефективний захист без зайвої ваги.\n"
                "  Вироблено: ~65 000 од. Найбільша серія в WWII."
            ),
            ("tiger", "тигр"): (
                "Panzerkampfwagen VI Tiger I (1942)\n"
                "  Маса: 57 тонн   Екіпаж: 5 осіб\n"
                "  Гармата: KwK 36 L/56 (88мм) — пробивала 120мм броні з 1000м\n"
                "  Броня лобова: 102мм   бортова: 82мм\n"
                "  Швидкість: 45 км/год   Двигун: Maybach HL 230 (700 к.с.)\n"
                "  Вироблено: лише 1347 шт. Висока вартість і ненадійна трансмісія."
            ),
            ("abrams", "абрамс", "m1"): (
                "M1 Abrams — основний бойовий танк США\n"
                "  Маса: 62–73 тонни   Екіпаж: 4 особи\n"
                "  Гармата: M256 (120мм гладкоствольна, сумісна з NATO)\n"
                "  Броня: Chobham/Burlington + пластини зі збідненого урану\n"
                "  Швидкість: 68 км/год   Двигун: газова турбіна AGT-1500 (1500 к.с.)\n"
                "  Версії: M1A1, M1A2, M1A2 SEP, M1A2 SEPv3. На озброєнні з 1980."
            ),
            ("leopard 2", "леопард"): (
                "Leopard 2 — найпоширеніший танк НАТО\n"
                "  Маса: 62–68 тонн   Екіпаж: 4 особи\n"
                "  Гармата: Rheinmetall 120мм (L/44 або L/55 на A6+)\n"
                "  Швидкість: 72 км/год   Двигун: MTU MB 873 (1500 к.с.)\n"
                "  Версії A4–A8. Використовується 18+ країнами, у т.ч. Україною (A4, A6)."
            ),
            ("т-90", "t-90"): (
                "Т-90 — основний танк РФ (глибока модернізація Т-72)\n"
                "  Маса: 46–50 тонн   Екіпаж: 3 особи (автозаряджання)\n"
                "  Гармата: 2А46М (125мм) — стріляє ракетами через ствол\n"
                "  КДЗ «Контакт-5» + система «Штора» проти ПТРК\n"
                "  Швидкість: 65 км/год   Двигун: В-92С2 (1000 к.с.)\n"
                "  Версії: Т-90А, Т-90М «Прорив» (найсучасніша)."
            ),
            ("армата", "т-14", "armata"): (
                "Т-14 Армата (2015) — нова платформа РФ\n"
                "  Маса: ~55 тонн   Екіпаж: 3 особи (у ізольованій бронекапсулі!)\n"
                "  Гармата: 2А82-1М (125мм), перспективна — 152мм\n"
                "  КАЗ «Афганіт» — збиває снаряди і ракети в польоті\n"
                "  Швидкість: 80–90 км/год   Двигун: 12Н360 (1200–1500 к.с.)\n"
                "  Проблеми: затримки серійного виробництва через санкції та вартість."
            ),
            ("оплот", "булат", "україн", "зсу", "т-64"): (
                "Танковий парк ЗСУ:\n\n"
                "  Т-64БМ Булат: глибока модернізація Т-64\n"
                "  → КДЗ «Нож», посилена броня, гармата 125мм\n\n"
                "  БМ Оплот (Т-84У): найсучасніший вітчизняний\n"
                "  → Маса 51т, гармата 125мм, КДЗ «Дуплет», 70 км/год\n"
                "  → Постачався Таїланду (49 одиниць)\n\n"
                "  Також отримані від партнерів: Leopard 2A4/A6, M1A1 Abrams, T-72M"
            ),
        }

        for keys, answer in db.items():
            if any(k in t for k in keys):
                return answer

        return (
            "[ЛОКАЛЬНА БД] Інформація не знайдена.\n"
            "→ Підключи Anthropic API для повних відповідей.\n"
            "→ Або питай про: Mark I, Т-34, Tiger, Abrams, Leopard, Т-90, Армата, ЗСУ"
        )


    # ──────────────────────────────────────────
    #  ДОПОМІЖНІ МЕТОДИ
    # ──────────────────────────────────────────
    def _append(self, text: str, tag: str = "bot_text"):
        """Додати текст у чат (thread-safe тільки з головного потоку)."""
        self.chat_display.configure(state=tk.NORMAL)
        self.chat_display.insert(tk.END, text, tag)
        self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.see(tk.END)


    def _set_ui_state(self, generating: bool):
        self.is_generating = generating
        state = tk.DISABLED if generating else tk.NORMAL
        btn_text = "  ⟳ ГЕНЕРУЮ  " if generating else "  ВОГОНЬ  "
        self.send_btn.configure(state=state, text=btn_text)
        self.input_field.configure(state=state)
        if not generating:
            self.input_field.focus_set()


    def _set_status(self, left: str = "", right: str = ""):
        self.status_left.configure(text=f"  {left}")
        if right:
            self.status_right.configure(text=f"{right}  ")


    def _quick_ask(self, query: str):
        self.input_field.delete(0, tk.END)
        self.input_field.insert(0, query)
        self._send_message()


    def _clear_chat(self):
        self.chat_display.configure(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.configure(state=tk.DISABLED)
        self.chat_history.clear()
        self._show_welcome()
        self._set_status("⚡ Чат очищено — нова сесія")


# ═══════════════════════════════════════════════════════════════
#  ТОЧКА ВХОДУ
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    if not ANTHROPIC_AVAILABLE:
        print("=" * 60)
        print("⚠  ПОМИЛКА: бібліотека anthropic не встановлена!")
        print("   Встанови командою: pip install anthropic")
        print("   Програма запуститься в ЛОКАЛЬНОМУ РЕЖИМІ")
        print("=" * 60)
    elif not ANTHROPIC_API_KEY.strip():
        print("=" * 60)
        print("⚠  ПОПЕРЕДЖЕННЯ: ANTHROPIC_API_KEY не встановлена!")
        print("   Встав ключ у змінну ANTHROPIC_API_KEY у коді,")
        print("   або: set ANTHROPIC_API_KEY=sk-ant-...")
        print("   Ключ отримай на: https://console.anthropic.com")
        print("   Програма запуститься в ЛОКАЛЬНОМУ РЕЖИМІ")
        print("=" * 60)

    root = tk.Tk()

    try:
        root.iconbitmap("tank_icon.ico")
    except Exception:
        pass

    app = TankCommandCenter(root)
    root.protocol("WM_DELETE_WINDOW", root.destroy)
    root.mainloop()