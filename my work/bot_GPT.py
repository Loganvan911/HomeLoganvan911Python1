import os
import tkinter as tk

try:
    import openai
except ImportError:
    openai = None

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if openai and OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY


def ask_ai(prompt: str) -> str:
    if not openai:
        return "AI-модуль не встановлено. Встановіть пакет openai через pip."
    if not OPENAI_API_KEY:
        return "OpenAI API ключ не знайдено. Задайте змінну середовища OPENAI_API_KEY."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as error:
        return f"Помилка AI: {error}"


def clear_chat():
    chat.delete("1.0", tk.END)
    chat.insert(tk.END, "Чат очищено. Напишіть повідомлення, щоб продовжити.\n")


def send_message():
    user = entry.get().strip()
    if not user:
        return

    chat.insert(tk.END, f"Ти: {user}\n")

    command = user.lower()
    if command == "привіт":
        answer = "Привіт 👋"
    elif command == "як справи":
        answer = "У мене все добре, я ж програма :)"
    elif command == "що ти вмієш":
        answer = "Можу відповідати на прості питання та використовувати AI для нових відповідей."
    elif command == "хто тебе створив":
        answer = "Мене створив Іван на Python 😎"
    elif command == "яка сьогодні погода":
        answer = "Я не можу перевірити погоду, але сподіваюся, що вона гарна! ☀️"
    elif command == "який сьогодні день":
        answer = "Сьогодні чудовий день для навчання! 📚"
    elif command == "який твій улюблений колір":
        answer = "Мій улюблений колір - синій! 💙"
    elif command in ["очистити чат", "clear chat", "сброс"]:
        clear_chat()
        entry.delete(0, tk.END)
        return
    else:
        answer = ask_ai(user)

    chat.insert(tk.END, f"Бот: {answer}\n\n")
    entry.delete(0, tk.END)


window = tk.Tk()
window.title("🤖 Мій AI Чат-Бот")

status_text = "AI готовий." if openai and OPENAI_API_KEY else "AI не налаштовано. Введіть OPENAI_API_KEY або встановіть openai."
status_label = tk.Label(window, text=status_text, fg="blue")
status_label.pack(pady=(5, 0))

chat = tk.Text(window, width=100, height=30)
chat.pack(padx=10, pady=5)

entry = tk.Entry(window, width=100)
entry.pack(padx=10)

button_frame = tk.Frame(window)
button_frame.pack(pady=10)

send_button = tk.Button(button_frame, text="Надіслати", command=send_message)
send_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(button_frame, text="Очистити чат", command=clear_chat)
clear_button.pack(side=tk.LEFT, padx=5)

window.mainloop()