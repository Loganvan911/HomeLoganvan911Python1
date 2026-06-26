# ============================================================
# ТАНКОВИЙ ЧАТ-БОТ — від Першої світової до сьогодні
# Використовує Google Gemini AI для генерації відповідей
# Інтерфейс: tkinter (вбудований у Python, не потребує встановлення)
# ============================================================

# --- Подавлення попередження з Google плагіна ---
# --- Подавлення попередження з Google плагіна ---
import os
import sys
import logging
import warnings

# Встановлюємо змінні середовища ДО будь-яких імпортів Google
os.environ['GRPC_VERBOSITY'] = 'NONE'        # ← було 'ERROR', стало 'NONE'
os.environ['GRPC_TRACE'] = ''                # ← нове
os.environ['GCLOUD_DISABLE_GRPC'] = 'true'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['PYTHONWARNINGS'] = 'ignore'
os.environ['GOOGLE_API_USE_GRPC_WEB'] = '0' # ← нове

# Пригнічуємо stderr на рівні OS (перехоплює навіть C++ gRPC логи)
_old_fd = os.dup(2)
_devnull_fd = os.open(os.devnull, os.O_WRONLY)
os.dup2(_devnull_fd, 2)

# Перенаправляємо stderr для подавлення системних повідомлень з Google плагінів
_stderr_backup = sys.stderr

class _FilteredStderr:
    def __init__(self, original_stderr):
        self.original_stderr = original_stderr
    
    def write(self, msg):
        # Список ключових слів помилок Google, які треба приховати
        blocked_keywords = [
            'plugin_credentials',
            'validate_metadata',
            'Plugin added',
            'INTERNAL:Illegal',
            'invalid metadata',
            'gRPC',
            'E0613',  # Формат повідомлення Google
            'E0616',  # Додаємо для поточної помилки
        ]
        
        # Якщо це одна з заблокованих помилок - не виводимо
        if any(keyword in msg for keyword in blocked_keywords):
            return
        
        # Інші повідомлення виводимо нормально
        self.original_stderr.write(msg)
    
    def flush(self):
        self.original_stderr.flush()
    
    def isatty(self):
        return self.original_stderr.isatty()

sys.stderr = _FilteredStderr(_stderr_backup)

# Отримуємо логгер Google та встановлюємо рівень WARNING
logging.getLogger('google.generativeai').setLevel(logging.WARNING)
logging.getLogger('google.genai').setLevel(logging.WARNING)
logging.getLogger('google.auth').setLevel(logging.WARNING)
logging.getLogger('grpc').setLevel(logging.WARNING)

# --- Імпорт стандартних бібліотек ---
import tkinter as tk                          # Основна бібліотека для GUI (графічний інтерфейс)
from tkinter import scrolledtext, ttk        # scrolledtext — текстове поле зі скролом; ttk — сучасні віджети
import threading                              # Для запуску запитів до AI у фоновому потоці (щоб GUI не зависав)
import datetime                               # Для відображення часу повідомлень

## --- Імпорт бібліотеки Google Gemini AI ---
# Встановити командою: pip install google-genai
try:
    from google import genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
except Exception:
    GEMINI_AVAILABLE = False

# Повертаємо нормальний stderr після імпорту Google бібліотек
os.dup2(_old_fd, 2)
os.close(_devnull_fd)
os.close(_old_fd)


# ============================================================
# КЛАС ТАНКОВОГО ЧАТ-БОТА
# Містить всю логіку: налаштування AI, обробку повідомлень, GUI
# ============================================================
class TankChatBot:
    def __init__(self, root):
        # root — головне вікно tkinter, яке передається при створенні об'єкта
        self.root = root
        self.root.title("⚔️  ВІЙСЬКОВИЙ КОМАНДНИЙ ЦЕНТР | Танковий Чат-Бот ⚔️ ")  # Заголовок вікна
        self.root.geometry("900x700")                                   # Розмір вікна: 900x700 пікселів
        
        # --- Кольорова палітра Cyberpunk / Sci-Fi ---
        self.COLOR_BG = "#0f081d"            # Темно-фіолетовий (майже чорний) фон
        self.COLOR_PANEL_BG = "#1d1136"      # Фіолетовий фон панелей
        self.COLOR_TEXT_MAIN = "#ffffff"     # Головний білий текст
        self.COLOR_NEON_PINK = "#ff007f"     # Неоновий рожевий (акценти, кнопки, користувач)
        self.COLOR_NEON_CYAN = "#00f0ff"     # Неоновий бірюзовий (боти, рамки, другорядні акценти)
        self.COLOR_MUTED_PURPLE = "#8f70c6"  # Приглушений фіолетовий (часові мітки, другорядні написи)
        self.COLOR_CHAT_BG = "#090412"       # Глибокий чорно-фіолетовий для поля чату
        self.COLOR_SEPARATOR = "#3d225a"     # Роздільник повідомлень
        
        self.root.configure(bg=self.COLOR_BG)                            # Темно-фіолетовий фон
        self.root.minsize(700, 500)                                     # Мінімальний розмір вікна

        # --- Налаштування Gemini AI ---
        self.client = None                    # Об'єкт клієнта для нової бібліотеки
        self.system_instruction = ""          # Зберігаємо інструкцію для перезапуску сесії
        self.model = None                     # Змінна для зберігання моделі Gemini (спочатку None)
        self.chat_session = None              # Змінна для сесії чату (зберігає історію розмови)
        self.setup_gemini()                   # Викликаємо метод налаштування Gemini

        # --- Будуємо інтерфейс ---
        self.setup_gui()                      # Викликаємо метод побудови GUI

        # --- Вітальне повідомлення від бота ---
        self.show_welcome()                   # Показуємо привітання при запуску


    # --------------------------------------------------------
    # МЕТОД: Налаштування Google Gemini AI
    # --------------------------------------------------------
    def setup_gemini(self):
        if not GEMINI_AVAILABLE:
            print("❌ google-generativeai не встановлена. Встанови: pip install google-generativeai")
            print("❌ google-genai не встановлена. Встанови: pip install google-genai")
            return

        # Якщо ви не хочете використовувати змінні середовища, вставте ваш API ключ тут:
        api_key = ""
       
        
         # Читаємо ключ з змінної середовища
        if not api_key or api_key == "":
            print("❌ GEMINI_API_KEY не встановлена!")
            print("   1. Отримай ключ тут: https://makersuite.google.com/app/apikey")
            print("   2. Встанови в Windows (PowerShell): $env:GEMINI_API_KEY='твій_ключ'")
            print("   3. Чи встав прямо в код (після цього рядка)")
            self.model = None
            return

        try:
            self.client = genai.Client(api_key=api_key)
            print("✅ Gemini API ключ встановлено успішно")

            self.system_instruction = "Ти — експерт з танків від 1916 до сьогодні. Відповідай УКРАЇНСЬКОЮ, коротко й точно."
            
            # Список моделей для спроби (в порядку переваги)
            models_to_try = [
                        "gemini-3.5-flash",       # Найновіша модель для автономних та агентних задач (Травень 2026)
                        "gemini-3.1-pro",         # Найпотужніша модель для складних логічних задач та кодингу
                        "gemini-3.1-flash-lite",  # Найновіша оптимізована за швидкістю та вартістю модель
                        "gemini-2.5-pro",         # Стабільна робоча конячка для глибокого аналізу
                        "gemini-2.5-flash"        # Стандартна збалансована модель попереднього покоління
                        ]
            
            for model_name in models_to_try:
                try:
                    self.model = model_name
                    self.chat_session = self.client.chats.create(
                        model=self.model,
                        config={'system_instruction': self.system_instruction}
                    )
                    print(f"✅ Модель {model_name} завантажена")
                    break
                except Exception as e:
                    print(f"⚠️  {model_name} недоступна: {type(e).__name__}: {str(e)}")
                    continue
            
            if self.model is None:
                print("❌ Жодна модель не доступна")
                return
            print("✅ Сесія чату ініціалізована")

        except Exception as e:
            print(f"❌ Помилка при налаштуванні Gemini: {str(e)}")
            print(f"   Тип помилки: {type(e).__name__}")
            self.model = None


    # --------------------------------------------------------
    # МЕТОД: Побудова графічного інтерфейсу (GUI)
    # --------------------------------------------------------
    def setup_gui(self):

        # === ВЕРХНЯ ПАНЕЛЬ (шапка програми) ===
        header_frame = tk.Frame(self.root, bg=self.COLOR_PANEL_BG, height=90)   # Фіолетовий фон
        header_frame.pack(fill=tk.X, padx=0, pady=0)                  # Розтягуємо по ширині
        header_frame.pack_propagate(False)                             # Фіксуємо висоту (не стискається)

        # Іконка танка та назва програми
        tk.Label(
            header_frame,
            text="⚔️  ВІЙСЬКОВИЙ КОМАНДНИЙ ЦЕНТР ⚔️ ",          # Текст заголовку
            font=("Arial", 20, "bold"),             # Великий жирний шрифт
            bg=self.COLOR_PANEL_BG,
            fg=self.COLOR_NEON_PINK                 # Неоновий рожевий акцент
        ).pack(side=tk.LEFT, padx=20, pady=15)     # Розміщуємо ліворуч з відступами

        # Підзаголовок з роками
        tk.Label(
            header_frame,
            text="🛡️  WWI — Сьогодні 🛡️  • Генерація відповідей AI",
            font=("Arial", 10, "bold"),                    # Менший шрифт
            bg=self.COLOR_PANEL_BG,
            fg=self.COLOR_MUTED_PURPLE              # Приглушений фіолетовий
        ).pack(side=tk.LEFT, padx=5, pady=20)

        # Статус підключення Gemini (праворуч у шапці)
        status_text = "🔓 AI АКТИВНА" if (self.model is not None) else "⚠️  ЛОКАЛЬНА БД"
        status_color = self.COLOR_NEON_CYAN if (self.model is not None) else self.COLOR_NEON_PINK
        self.status_label = tk.Label(
            header_frame,
            text=status_text,
            font=("Arial", 10, "bold"),
            bg=self.COLOR_PANEL_BG,
            fg=status_color
        )
        self.status_label.pack(side=tk.RIGHT, padx=20)   # Розміщуємо праворуч


        # === ПАНЕЛЬ ШВИДКИХ КНОПОК (категорії танків) ===
        buttons_frame = tk.Frame(self.root, bg=self.COLOR_BG, pady=10)      # Темно-фіолетовий фон
        buttons_frame.pack(fill=tk.X, padx=0)                          # Розтягуємо по ширині

        # Підпис до кнопок
        tk.Label(
            buttons_frame,
            text="⚡ БОЄВІ ЗАВДАННЯ:",
            font=("Arial", 10, "bold"),
            bg=self.COLOR_BG,
            fg=self.COLOR_NEON_PINK
        ).pack(side=tk.LEFT, padx=10)

        # Список швидких запитань для кнопок-ярликів
        quick_buttons = [
            ("🌍 WWI танки", "Розкажи про перші танки Першої світової війни"),
            ("⚔️ WWII СРСР", "Які найкращі радянські танки Другої світової?"),
            ("🦁 Tiger I", "Розкажи про танк Tiger I: характеристики і бойове застосування"),
            ("⭐ Т-34", "Чому Т-34 вважається найкращим танком WWII? Характеристики"),
            ("🦅 Abrams", "M1 Abrams: характеристики та чому він вважається одним з найкращих"),
            ("🇺🇦 Укр танки", "Які танки є на озброєнні України? Оплот, Булат"),
            ("📊 Порівняння", "Порівняй Leopard 2 та T-90 за основними характеристиками"),
            ("🔬 Сучасні", "Назви топ-5 найкращих сучасних танків у світі"),
        ]

        # Створюємо кожну кнопку в циклі
        for btn_text, query in quick_buttons:
            # lambda з default аргументом q=query — важливо! Без q=query всі кнопки мали б один запит
            btn = tk.Button(
                buttons_frame,
                text=btn_text,                           # Текст на кнопці
                font=("Arial", 8, "bold"),
                bg=self.COLOR_PANEL_BG,                  # Фіолетова кнопка
                fg=self.COLOR_NEON_CYAN,                  # Неоновий бірюзовий текст
                activebackground=self.COLOR_NEON_PINK,    # Неоновий рожевий при натисканні
                activeforeground="#ffffff",
                relief=tk.FLAT,                          # Плоска сучасна кнопка (більш кіберпанкова)
                padx=8, pady=4,
                cursor="hand2",                          # Курсор-рука при наведенні
                command=lambda q=query: self.quick_ask(q)  # Функція при натисканні
            )
            btn.pack(side=tk.LEFT, padx=3)              # Розміщуємо кнопки горизонтально


        # === ГОЛОВНА ОБЛАСТЬ ЧАТУо ===
        # Рамка для чату — займає весь доступний простір між кнопками і полем вводу
        chat_frame = tk.Frame(self.root, bg=self.COLOR_BG)
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        # Текстове поле зі скролом для відображення повідомлень
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,                       # Перенос по словах (не розриває слова)
            font=("Consolas", 11),              # Моноширний шрифт для чату
            bg=self.COLOR_CHAT_BG,              # Темно-фіолетовий фон чату
            fg=self.COLOR_TEXT_MAIN,            # Світлий текст
            insertbackground=self.COLOR_NEON_PINK, # Рожевий курсор вводу
            relief=tk.FLAT,                     # Сучасна плоска рамка
            padx=10, pady=10,
            spacing3=4,                          # Відстань між рядками
            bd=1                                 # Тонка рамка
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)

        # --- Налаштування кольорових тегів для різних типів повідомлень ---
        # Кожен тег задає стиль для певного виду тексту в чаті

        self.chat_display.tag_configure(
            "user_name",                        # Тег для імені користувача
            foreground=self.COLOR_NEON_PINK,    # Неоновий рожевий
            font=("Consolas", 10, "bold")       # Жирний шрифт
        )
        self.chat_display.tag_configure(
            "user_msg",                         # Тег для тексту повідомлення користувача
            foreground=self.COLOR_NEON_CYAN,    # Неоновий бірюзовий
            font=("Consolas", 11)
        )
        self.chat_display.tag_configure(
            "bot_name",                         # Тег для імені бота
            foreground=self.COLOR_NEON_CYAN,    # Неоновий бірюзовий
            font=("Consolas", 10, "bold")
        )
        self.chat_display.tag_configure(
            "bot_msg",                          # Тег для відповіді бота
            foreground=self.COLOR_TEXT_MAIN,    # Білий текст
            font=("Consolas", 11)
        )
        self.chat_display.tag_configure(
            "system_msg",                       # Тег для системних повідомлень
            foreground=self.COLOR_MUTED_PURPLE, # Фіолетовий
            font=("Consolas", 10, "italic")
        )
        self.chat_display.tag_configure(
            "time_tag",                         # Тег для часу повідомлення
            foreground=self.COLOR_MUTED_PURPLE, # Фіолетовий
            font=("Consolas", 9)
        )
        self.chat_display.tag_configure(
            "separator",                        # Тег для роздільника між повідомленнями
            foreground=self.COLOR_SEPARATOR,
            font=("Consolas", 6)
        )

        # Робимо поле тільки для читання — користувач не може редагувати чат напряму
        self.chat_display.configure(state=tk.DISABLED)


        # === НИЖНЯ ПАНЕЛЬ ВВОДУ ===
        input_frame = tk.Frame(self.root, bg=self.COLOR_BG, pady=12)       # Рамка для поля вводу
        input_frame.pack(fill=tk.X, padx=15, pady=(0, 15))            # Прилягає до низу

        # Поле текстового вводу (однорядкове)
        self.input_field = tk.Entry(
            input_frame,
            font=("Arial", 12, "bold"),
            bg=self.COLOR_CHAT_BG,              # Темний фон
            fg=self.COLOR_NEON_CYAN,            # Бірюзовий текст
            insertbackground=self.COLOR_NEON_PINK, # Рожевий курсор
            relief=tk.FLAT,
            bd=1,
            disabledbackground=self.COLOR_PANEL_BG,
            disabledforeground=self.COLOR_MUTED_PURPLE
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)  # Розтягуємо по ширині

        # Прив'язуємо клавішу Enter до відправки повідомлення
        self.input_field.bind("<Return>", lambda event: self.send_message())   # Enter — відправити
        self.input_field.bind("<Shift-Return>", lambda e: None)                # Shift+Enter — нічого

        # Кнопка відправки
        self.send_button = tk.Button(
            input_frame,
            text="🔥 ВОГОНЬ! 🔫",
            font=("Arial", 11, "bold"),
            bg=self.COLOR_NEON_PINK,            # Рожева кнопка
            fg="#ffffff",
            activebackground="#ff3399",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=20, pady=8,
            cursor="hand2",
            bd=0,
            command=self.send_message           # Виклик методу відправки
        )
        self.send_button.pack(side=tk.RIGHT, padx=(10, 0))  # Кнопка праворуч

        # Кнопка очищення чату
        clear_button = tk.Button(
            input_frame,
            text="⚠️  ПЕРЕЗАГРУЗКА ⚠️ ",
            font=("Arial", 10, "bold"),
            bg=self.COLOR_PANEL_BG,
            fg=self.COLOR_NEON_CYAN,
            activebackground=self.COLOR_NEON_PINK,
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=15, pady=8,
            cursor="hand2",
            bd=0,
            command=self.clear_chat             # Виклик методу очищення
        )
        clear_button.pack(side=tk.RIGHT, padx=(10, 0))


        # === РЯДОК СТАТУСУ (внизу вікна) ===
        self.status_bar = tk.Label(
            self.root,
            text="⚔️  КОМАНДНИЙ ЦЕНТР ГОТОВИЙ | Передайте команду про танки ⚔️ ",
            font=("Arial", 9, "bold"),
            bg=self.COLOR_PANEL_BG,
            fg=self.COLOR_NEON_CYAN,
            anchor=tk.W,                        # Вирівнювання тексту ліворуч
            padx=10,
            relief=tk.FLAT,
            bd=0
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)  # Прилягає до самого низу

        # Фокус на полі вводу — одразу можна друкувати
        self.input_field.focus_set()


    # --------------------------------------------------------
    # МЕТОД: Показати вітальне повідомлення при запуску
    # --------------------------------------------------------
    def show_welcome(self):
        welcome_text = (
            "╔═══════════════════════════════════════════════════════════════╗\n"
            "║        ⚔️  ВІЙСЬКОВИЙ КОМАНДНИЙ ЦЕНТР — АКТИВОВАНО ⚔️         ║\n"
            "║           ТАНКОВИЙ ІНТЕЛЕКТУАЛЬНИЙ АНАЛІЗ СИСТЕМИ             ║\n"
            "╚═══════════════════════════════════════════════════════════════╝\n\n"
            "[СИСТЕМА] ТАНКОВА БД ІНІЦІАЛІЗОВАНА | ВСІ ПАРАМЕТРИ НОРМА\n\n"
            "ДОСТУПНІ КОМАНДИ РОЗВІДКИ:\n"
            "  🔫 ВОГНЕВІ ХАРАКТЕРИСТИКИ — технічні параметри броні та озброєння\n"
            "  ⚔️  БОЙОВІ ОПЕРАЦІЇ — застосування на фронтах світових войн\n"
            "  📊 ПОРІВНЯЛЬНИЙ АНАЛІЗ — тактико-технічна невідповідність\n"
            "  🌍 МІЖНАРОДНА СЛУЖБА — танки різних армій та епох\n"
            "  🔬 ПЕРЕДОВІ РОЗРОБКИ — експериментальні та найновіші системи\n\n"
        )

        # Додаємо різну підказку залежно від режиму роботи
        if self.model and self.chat_session:
            welcome_text += "[СТАТУС] 🟢 GEMINI AI СИСТЕМА АКТИВНА\n"
            welcome_text += "[РЕЖИМ] 🔓 НЕЙРОМЕРЕЖЕВА ГЕНЕРАЦІЯ УВІМКНЕНА\n"
            welcome_text += "[КОМАНДА] 🎯 Використовуй БОЄВІ ЗАВДАННЯ вгорі для швидкого запуску\n"
            welcome_text += "[СИСТЕМА] 🚀 Режим: Live AI — відповіді генеруються в реальному часі\n"
        else:
            welcome_text += "[СТАТУС] 🔴 GEMINI AI СИСТЕМА НЕАКТИВНА\n\n"
            if not GEMINI_AVAILABLE:
                welcome_text += "[ПОМИЛКА] ❌ Модуль google-generativeai НЕ ВСТАНОВЛЕНО\n"
                welcome_text += "[ПОМИЛКА] ❌ Модуль google-genai НЕ ВСТАНОВЛЕНО\n"
                welcome_text += "[ВИПРАВЛЕННЯ]\n"
                welcome_text += "  1️⃣  Відкрий PowerShell (адміністратор)\n"
                welcome_text += "  2️⃣  Виконай: pip install google-generativeai\n"
                welcome_text += "  2️⃣  Виконай: pip install google-genai\n"
                welcome_text += "  3️⃣  Перезапусти цю програму\n"
            else:
                welcome_text += "[ПОМИЛКА] ❌ GEMINI_API_KEY НЕ ВСТАНОВЛЕНА\n\n"
                welcome_text += "[ВИПРАВЛЕННЯ]\n"
                welcome_text += "  1️⃣  Отримай ключ на https://makersuite.google.com/app/apikey\n"
                welcome_text += "  2️⃣  У PowerShell встанови: $env:GEMINI_API_KEY='твій_ключ'\n"
                welcome_text += "  3️⃣  Запусти програму знову\n\n"
                welcome_text += "[АЛЬТЕРНАТИВА] 💾 Встав ключ прямо у код\n"
                welcome_text += "  Рядок: api_key = os.environ.get(\"GEMINI_API_KEY\", \"\")\n"
                welcome_text += "  Змінити на: api_key = \"sk-...(твій ключ)\"\n"

            welcome_text += "\n[БАЗА] 🔹 ЛОКАЛЬНА БАЗА ДАНИХ ТАНКІВ: ДОСТУПНА\n"

        welcome_text += "═══════════════════════════════════════════════════════════════\n"

        # Відображаємо вітання в чаті
        self.append_to_chat(welcome_text, "system_msg")


    # --------------------------------------------------------
    # МЕТОД: Додати текст до поля чату
    # tag — рядок з назвою тегу форматування (user_msg, bot_msg тощо)
    # --------------------------------------------------------
    def append_to_chat(self, text, tag="user_msg"):
        self.chat_display.configure(state=tk.NORMAL)   # Дозволяємо редагування (щоб додати текст)
        self.chat_display.insert(tk.END, text, tag)    # Вставляємо текст в кінець з заданим тегом
        self.chat_display.configure(state=tk.DISABLED) # Знову забороняємо редагування
        self.chat_display.see(tk.END)                  # Прокручуємо до кінця (щоб видно останнє)


    # --------------------------------------------------------
    # МЕТОД: Відправити повідомлення (викликається кнопкою або Enter)
    # --------------------------------------------------------
    def send_message(self):
        user_text = self.input_field.get().strip()     # Зчитуємо текст з поля вводу, видаляємо пробіли

        if not user_text:                              # Якщо порожньо — нічого не робимо
            return

        self.input_field.delete(0, tk.END)             # Очищаємо поле вводу після зчитування

        # Отримуємо поточний час для відображення
        now = datetime.datetime.now().strftime("%H:%M")

        # Відображаємо повідомлення користувача в чаті
        self.append_to_chat(f"\n[{now}] ", "time_tag")          # Час
        self.append_to_chat("👤 Ти: ", "user_name")             # Ім'я
        self.append_to_chat(f"{user_text}\n", "user_msg")       # Текст

        # Показуємо заголовок відповіді бота заздалегідь
        self.append_to_chat(f"\n[{now}] ", "time_tag")
        self.append_to_chat("🤖 Бот: ", "bot_name")

        # Блокуємо кнопку та поле вводу, поки бот "думає"
        self.send_button.configure(state=tk.DISABLED, text="⏳ Генерую...")
        self.input_field.configure(state=tk.DISABLED)
        self.status_bar.configure(text="🤖 Отримую відповідь від Gemini...")

        # Запускаємо отримання відповіді у ФОНОВОМУ ПОТОЦІ
        # Це критично важливо! Без threading — GUI зависне поки AI думає
        thread = threading.Thread(
            target=self.get_ai_response,           # Функція яку запускаємо у фоні
            args=(user_text,),                     # Аргументи для функції
            daemon=True                            # Daemon=True — потік завершиться разом з програмою
        )
        thread.start()                             # Запускаємо потік


    # --------------------------------------------------------
    # МЕТОД: Отримати відповідь від AI (виконується у фоновому потоці)
    # --------------------------------------------------------
    def get_ai_response(self, user_text):
        try:
            if not self.model or not self.chat_session:
                local_answer = self.get_local_response(user_text)
                self.root.after(0, self.display_response, local_answer)
                return

        # Очищаємо поле відповіді бота, якщо хочете
            self.chat_display.configure(state=tk.NORMAL)
            self.chat_display.insert(tk.END, "\n", "bot_msg")
            self.chat_display.configure(state=tk.DISABLED)

        # Отримуємо потокову відповідь від Gemini AI
            response_stream = self.chat_session.send_message_stream(message=user_text)
            for chunk in response_stream:
                text_chunk = chunk.text or ""
                self.root.after(0, self.append_streaming_chunk, text_chunk)

            self.root.after(0, self.finalize_streaming)

        except Exception as error:
            error_msg = str(error)
            if "429" in error_msg:
                local_answer = "⚠️ [ЛІМІТ ВИЧЕРПАНО] Спробуйте через хвилину.\n\n" + self.get_local_response(user_text)
            else:
                local_answer = f"⚠️ [ПОМИЛКА API] {error_msg}\n\n" + self.get_local_response(user_text)
            self.root.after(0, self.display_response, local_answer)

    # --------------------------------------------------------
    # МЕТОД: Додати кусок текста при потоковій генерації
    # --------------------------------------------------------
    def append_streaming_chunk(self, chunk):
        """Додавати текст поступово при надходженні від API"""
        self.chat_display.configure(state=tk.NORMAL)
        self.chat_display.insert(tk.END, chunk, "bot_msg")
        self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.see(tk.END)  # Автоматично прокручуємо вниз


    # --------------------------------------------------------
    # МЕТОД: Завершити потокову генерацію і розблокувати UI
    # --------------------------------------------------------
    def finalize_streaming(self):
        """Завершити отримання відповіді і повернути контроль користувачу"""
        self.chat_display.configure(state=tk.NORMAL)
        self.chat_display.insert(tk.END, "\n", "bot_msg")
        self.chat_display.insert(tk.END, "─" * 58 + "\n", "separator")
        self.chat_display.configure(state=tk.DISABLED)

        # Розблоковуємо кнопку та поле вводу
        self.send_button.configure(state=tk.NORMAL, text="🔥 ВОГОНЬ! 🔫")
        self.input_field.configure(state=tk.NORMAL)
        self.input_field.focus_set()

        # Оновлюємо статус-бар
        self.status_bar.configure(text="Готовий | Введіть наступне питання")


    # --------------------------------------------------------
    # МЕТОД: Відобразити відповідь бота в чаті
    # (для локального режиму без AI)
    # --------------------------------------------------------
    def display_response(self, answer):
        """Показати повну відповідь (для локального режиму)"""
        now = datetime.datetime.now().strftime("%H:%M")   # Поточний час

        # Відображаємо відповідь бота
        self.chat_display.configure(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"\n[{now}] ", "time_tag")
        self.chat_display.insert(tk.END, "🤖 Бот: ", "bot_name")
        self.chat_display.insert(tk.END, f"{answer}\n", "bot_msg")
        self.chat_display.insert(tk.END, "─" * 58 + "\n", "separator")
        self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.see(tk.END)

        # Розблоковуємо кнопку та поле вводу
        self.send_button.configure(state=tk.NORMAL, text=" ВОГОНЬ! 🔫")
        self.input_field.configure(state=tk.NORMAL)
        self.input_field.focus_set()                      # Повертаємо фокус на поле вводу

        # Оновлюємо статус-бар
        self.status_bar.configure(text="Готовий | Введіть наступне питання")


    # --------------------------------------------------------
    # МЕТОД: Локальна база знань (якщо немає Gemini)
    # Містить базові факти про відомі танки
    # --------------------------------------------------------
    def get_local_response(self, text):
        text_lower = text.lower()   # Переводимо в нижній регістр для пошуку

        # Словник: ключові слова → відповідь
        # Перевіряємо чи є ключові слова у питанні користувача
        knowledge_base = {
            # Перша світова
            ("mark i", "mark 1", "перший танк", "wwi", "перша світова"): (
                "🌍 Mark I (1916) — перший бойовий танк у світовій історії!\n"
                "⚙️ Маса: 28 тонн | Екіпаж: 8 осіб\n"
                "🔫 Озброєння: 2x гармати Hotchkiss (57мм) + кулемети\n"
                "💨 Швидкість: 6 км/год | Двигун: Daimler 105 к.с.\n"
                "📖 Вперше застосований 15 вересня 1916 на Соммі. Революція у війні!"
            ),
            # Т-34
            ("т-34", "t-34", "т34"): (
                "⭐ Т-34 — легенда Другої світової!\n"
                "⚙️ Маса: 26-32 тонни | Екіпаж: 4-5 осіб\n"
                "🔫 Гармата: 76мм (Т-34/76) або 85мм (Т-34/85)\n"
                "💨 Швидкість: 55 км/год | Двигун: В-2 (500 к.с.)\n"
                "🛡 Броня: 45-90мм нахилена під 60° — революційне рішення!\n"
                "📊 Вироблено: ~65 000 одиниць. Переломив хід WWII!"
            ),
            # Tiger I
            ("tiger i", "тигр", "tiger 1"): (
                "🦁 Panzerkampfwagen VI Tiger I (1942)\n"
                "⚙️ Маса: 57 тонн | Екіпаж: 5 осіб\n"
                "🔫 Гармата: KwK 36 (88мм) — пробивала броню з 2км!\n"
                "🛡 Броня: 25-120мм лобова\n"
                "💨 Швидкість: 45 км/год | Двигун: Maybach HL230 (700 к.с.)\n"
                "📖 Вироблено лише 1347 шт. Нищив Sherman та Т-34 з великих дистанцій."
            ),
            # M1 Abrams
            ("abrams", "абрамс", "m1"): (
                "🦅 M1 Abrams — основний бойовий танк США\n"
                "⚙️ Маса: 62-73 тонни | Екіпаж: 4 особи\n"
                "🔫 Гармата: M256 (120мм гладкоствольна)\n"
                "🛡 Броня: Chobham/Burlington + DU (збіднений уран)\n"
                "💨 Швидкість: 68 км/год | Двигун: газова турбіна AGT-1500 (1500 к.с.)\n"
                "📊 На озброєнні з 1980. Найпотужніший танк НАТО!"
            ),
            # Leopard 2
            ("leopard 2", "леопард"): (
                "🇩🇪 Leopard 2 — найпоширеніший танк НАТО\n"
                "⚙️ Маса: 62-68 тонн | Екіпаж: 4 особи\n"
                "🔫 Гармата: Rheinmetall 120мм (L/44 або L/55)\n"
                "💨 Швидкість: 72 км/год | Двигун: MTU MB 873 (1500 к.с.)\n"
                "🌍 Експлуатується 18+ країнами. Версія A7 — найсучасніша!"
            ),
            # Т-90
            ("т-90", "t-90"): (
                "🇷🇺 Т-90 — основний танк Росії\n"
                "⚙️ Маса: 46.5 тонни | Екіпаж: 3 особи (автозаряджання!)\n"
                "🔫 Гармата: 2А46М (125мм) — стріляє ракетами через ствол!\n"
                "🛡 КДЗ «Контакт-5» + система «Штора» (захист від ПТРК)\n"
                "💨 Швидкість: 65 км/год | Двигун: В-92С2 (1000 к.с.)\n"
                "📖 Прийнятий на озброєння 1992. Модернізована версія Т-72."
            ),
            # Армата
            ("армата", "т-14", "armata"): (
                "🔬 Т-14 Армата — найновіший російський танк (2015)\n"
                "⚙️ Маса: ~55 тонн | Екіпаж: 3 особи (ІЗОЛЬОВАНА КАПСУЛА!)\n"
                "🔫 Гармата: 2А82-1М (125мм) або 152мм (перспективна)\n"
                "🛡 КАЗ 'Афганіт' (збиває снаряди і ракети в польоті!)\n"
                "💨 Швидкість: 80-90 км/год | Двигун: 12Н360 (1200 к.с.)\n"
                "⚠️ Масове виробництво затримується через санкції та складність."
            ),
            # Оплот / Україна
            ("оплот", "булат", "україн", "bm oplot"): (
                "🇺🇦 Українські танки:\n\n"
                "БМ Оплот (на базі Т-84):\n"
                "🔫 Гармата: КБА3 (125мм) | Маса: 51 тонна\n"
                "🛡 КДЗ 'Дуплет' | 💨 Швидкість: 70 км/год\n"
                "📖 Найсучасніший вітчизняний розробок. Поставлявся Таїланду!\n\n"
                "БМ Булат (модернізований Т-64):\n"
                "🛡 Посилена броня + КДЗ | 🔫 Гармата 125мм\n"
                "📖 Масова модернізація старих Т-64 для ЗСУ"
            ),
            # Merkava
            ("merkava", "меркава"): (
                "✡️ Merkava — танк-фортеця Ізраїлю\n"
                "⚙️ Маса: 65-70 тонн | Екіпаж: 4 особи\n"
                "🔫 Гармата: MG253 (120мм) | + 60мм міномет!\n"
                "🛡 Унікальність: двигун СПЕРЕДУ захищає екіпаж!\n"
                "💨 Швидкість: 64 км/год | КАЗ Trophy (активний захист)\n"
                "📖 Розроблений після важких втрат у Судній війні 1973р."
            ),
        }

        # Шукаємо відповідність у базі знань
        for keywords, response in knowledge_base.items():
            if any(keyword in text_lower for keyword in keywords):   # Перевіряємо всі ключові слова
                return response

        # Якщо нічого не знайдено — загальна відповідь
        return (
            "🔍 Я знаю багато про танки, але ця інформація не знайдена в локальній базі.\n\n"
            "💡 Щоб отримати детальну відповідь:\n"
            "   1. Підключи Gemini AI (встанови ключ API)\n"
            "   2. Або спробуй запитати про: Mark I, Т-34, Tiger I, M1 Abrams,\n"
            "      Leopard 2, Т-90, Т-14 Армата, Оплот, Merkava"
        )


    # --------------------------------------------------------
    # МЕТОД: Швидке питання (викликається кнопками-ярликами)
    # --------------------------------------------------------
    def quick_ask(self, query):
        self.input_field.delete(0, tk.END)        # Очищаємо поле вводу
        self.input_field.insert(0, query)         # Вставляємо готовий запит
        self.send_message()                       # Відправляємо


    # --------------------------------------------------------
    # МЕТОД: Очистити чат і скинути сесію
    # --------------------------------------------------------
    def clear_chat(self):
        self.chat_display.configure(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.configure(state=tk.DISABLED)

    # Тільки новий API:
        if self.client and self.model:
            self.chat_session = self.client.chats.create(
            model=self.model,
            config={'system_instruction': self.system_instruction}
        )

        self.show_welcome()
        self.status_bar.configure(text="Чат очищено | Нова сесія розпочата")


# ============================================================
# ТОЧКА ВХОДУ В ПРОГРАМУ
# Цей блок виконується тільки якщо запускаємо файл напряму
# (не при імпорті як модуль)
# ============================================================
if __name__ == "__main__":
    # Перевіряємо наявність необхідної бібліотеки Gemini
    if not GEMINI_AVAILABLE:
        print("=" * 60)
        print("⚠️  ПОПЕРЕДЖЕННЯ: бібліотека google-generativeai не встановлена!")
        print("   Встанови командою: pip install google-generativeai")
        print("   Програма запуститься в ЛОКАЛЬНОМУ РЕЖИМІ (без AI)")
        print("=" * 60)

    root = tk.Tk()                    # Створюємо головне вікно програми

    # Встановлюємо іконку вікна (якщо є файл icon.ico, інакше пропускаємо)
    try:
        root.iconbitmap("tank_icon.ico")
    except:
        pass                          # Якщо іконки немає — ігноруємо помилку

    app = TankChatBot(root)           # Створюємо об'єкт нашого чат-бота, передаємо вікно

    # Обробник закриття вікна (коли користувач натискає X)
    root.protocol("WM_DELETE_WINDOW", root.destroy)   # Коректне закриття програми

    root.mainloop()                   # Запускаємо головний цикл подій tkinter

    # Повертаємо нормальний stderr після закриття програми
    sys.stderr = _stderr_backup
                                      # Програма "живе" тут доки вікно відкрите
