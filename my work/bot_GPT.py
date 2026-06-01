import tkinter as tk

def send_message():
    user = entry.get().lower()
    chat.insert(tk.END, f"Ти: {user}\n")

    if user == "привіт":
        answer = "Привіт 👋"
    elif user == "як справи":
        answer = "У мене все добре, я ж програма :)"

    elif user == "що ти вмієш":
        answer = "Можу відповідати на прості питання."
    elif user == "хто тебе створив":
        answer = "Мене створив Іван на Python 😎" 

    elif user == "яка сьогодні погода":
        answer = "Я не можу перевірити погоду, але сподіваюся, що вона гарна! ☀️"

    elif user == "який сьогодні день":
        answer = "Сьогодні чудовий день для навчання! 📚" 

    elif user == "який твій улюблений колір":
        answer = "Мій улюблений колір - синій! 💙" 

    else:
        answer = "Я поки не знаю, що відповісти."

    chat.insert(tk.END, f"Бот: {answer}\n\n")
    entry.delete(0, tk.END)

window = tk.Tk()
window.title("🤖 Мій AI Чат-Бот")

chat = tk.Text(window, width=100, height=40)
chat.pack()

entry = tk.Entry(window, width=100) 
entry.pack()

button = tk.Button(window, text="Надіслати", command=send_message)
button.pack()

window.mainloop()