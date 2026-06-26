# не скачена бібліотека
import os  # імпорт модуля для роботи з системними змінними та шляхами
import tkinter as tk  # імпорт графічного інтерфейсу tkinter як tk

# спробуємо підключити бібліотеку Gemini (Google Generative AI)
try:
    import google.generativeai as genai
except ImportError:
    genai = None

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if genai and GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        chat_session = model.start_chat(history=[])
    except Exception:
        chat_session = None
else:
    chat_session = None


def ask_ai(prompt: str) -> str:
    if not chat_session:
        return "AI-модуль не налаштовано. Перевірте ключ API та підключення."

    try:
        response = chat_session.send_message(prompt)
        if response.text:
            return response.text.strip()
            
        return "AI не повернув відповіді."
    except Exception as error:
        return f"Помилка AI: {error}"  # повідомлення про помилку при зверненні до Gemini


def clear_chat():
    chat.delete("1.0", tk.END)  # очищаємо текстове поле чату
    chat.insert(tk.END, "Чат очищено. Напишіть повідомлення, щоб продовжити.\n")  # вставляємо повідомлення про очищення


def send_message():
    user = entry.get().strip()  # читаємо текст з поля вводу та видаляємо зайві пробіли
    if not user:
        return  # якщо ввід порожній, нічого не робимо

    chat.insert(tk.END, f"Ти: {user}\n")  # додаємо введене повідомлення до чату

    command = user.lower()  # приводимо команду до нижнього регістру
    if command == "привіт":
        answer = "Привіт 👋"  # відповідаємо привітанням
    elif command == "як справи":
        answer = "У мене все добре, я ж програма :)"  # відповідаємо на питання про стан
    elif command == "що ти вмієш":
        answer = "Можу відповідати на прості питання та використовувати AI для нових відповідей."  # розповідаємо про можливості
    elif command == "хто тебе створив":
        answer = "Мене створив Іван на Python 😎"  # відповідаємо, хто автор
    elif command == "яка сьогодні погода":
        answer = "Я не можу перевірити погоду, але сподіваюся, що вона гарна! ☀️"  # відповідаємо про погоду
    elif command == "який сьогодні день":
        answer = "Сьогодні чудовий день для навчання! 📚"  # відповідаємо про день
    elif command == "який твій улюблений колір":
        answer = "Мій улюблений колір - синій! 💙"  # відповідь про улюблений колір
    elif command in ["очистити чат", "clear chat", "сброс"]:
        clear_chat()  # очищаємо чат, якщо команда відповідна
        entry.delete(0, tk.END)  # очищаємо поле вводу
        return  # припиняємо обробку повідомлення
    else:
        answer = ask_ai(user)  # передаємо повідомлення в AI, якщо команда невідома

    chat.insert(tk.END, f"Бот: {answer}\n\n")  # виводимо відповідь бота в чат
    entry.delete(0, tk.END)  # очищаємо поле вводу після відправки


window = tk.Tk()  # створюємо головне вікно програми
window.title("🤖 Мій AI Чат-Бот")  # задаємо заголовок вікна

status_text = "AI готовий." if genai and GEMINI_API_KEY else "AI не налаштовано. Встановіть google-generative-ai і GEMINI_API_KEY."  # текст стану AI
status_label = tk.Label(window, text=status_text, fg="blue")  # створюємо мітку стану
status_label.pack(pady=(5, 0))  # розміщуємо мітку зверху з відступом

chat = tk.Text(window, width=100, height=30)  # створюємо текстове поле для чату
chat.pack(padx=10, pady=5)  # розміщуємо поле з відступами

entry = tk.Entry(window, width=100)  # створюємо поле вводу користувача
entry.pack(padx=10)  # розміщуємо поле вводу з відступом

button_frame = tk.Frame(window)  # створюємо контейнер для кнопок
button_frame.pack(pady=10)  # розміщуємо контейнер з вертикальним відступом

send_button = tk.Button(button_frame, text="Надіслати", command=send_message)  # кнопка для відправки повідомлення
send_button.pack(side=tk.LEFT, padx=5)  # розміщуємо кнопку з невеликим відступом

clear_button = tk.Button(button_frame, text="Очистити чат", command=clear_chat)  # кнопка для очищення чату
clear_button.pack(side=tk.LEFT, padx=5)  # розміщуємо кнопку поруч з іншою

window.mainloop()  # запускаємо головний цикл обробки подій
