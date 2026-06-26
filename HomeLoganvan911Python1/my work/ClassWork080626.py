
# завдання 1 Парне чи непарне число
# Початок завдання1
# def is_even(number):
#     if number % 2 == 0:
#         return "Парне число"
#     else:
#         return "Непарне число"
# user_input = input("Будь ласка, введіть число: ")
# num = int(user_input)
# print(is_even(num))
# Кінець завдання1

# завдання 2 Понолітній Неповнолітній 
# def check_age(age):
#     if age >= 18:
#         return "Повнолітній"
#     else:
#         return "Неповнолітній"
# user_input = input("Будь ласка, введіть Ваш вік: ")
# user_age = int(user_input)
# print(check_age(user_age))
# Кінець завдання2

#  завдання 3 Більше з двох чисел   
# def max_number(num1, num2):
#     if num1 > num2:
#         return num1
#     elif num2 > num1:
#         return num2
#     else:
#         return "Числа рівні"
# user_input1 = input("Будь ласка, введіть перше число: ")
# user_input2 = input("Будь ласка, введіть друге число: ")
# number1 = int(user_input1) 
# number2 = int(user_input2)
# print(max_number(number1, number2))
# кінець завдання3

# завдання 4 Позитивні чи негативні числа
# def check_number(num):
#     if num > 0:
#         return "Позитивне число"
#     elif num < 0:
#         return "Негативне число"
#     else:
#         return "Нуль"
# user_input = input("Будь ласка, введіть число: ")
# num = int(user_input)
# print(check_number(num))   
# кінець завдання 4

# завдання 5 оцінка учня
# def student_grade(rating):
#     if rating >= 60:
#         return "Склав"
#     else:        
#         return "Не склав"
# user_input = input("Будь ласка, введіть оцінку учня: ")
# rating = int(user_input)
# print(student_grade(rating))
# кінець завдання 5

# завдання 6 Привітання
# def greet(name):
#     if name == "Іван":
#         return f"Привіт, Іван!"
#     else:
#         return f"Привіт, користувач!"
# user_input = input("Будь ласка, введіть ваше ім'я: ") 
# print(greet(user_input))
# кінець завдання 6

# завдання 7 Температура
# def temperatyre(temp):
#     if temp < 0:
#         return "мороз"
#     else:
#         return "не мороз"
# user_input = input("Будь ласка, введіть температуру: ")
# temp = int(user_input)
# print(temperatyre(temp))
# кінець завдання 7

# завдання 8 
# def discount(price):
#     if price > 1000:
#         return price * 0.9
#     else:
#         return price
# user_input = input("Будь ласка, введіть ціну товару: ")
# price = float(user_input)
# print(f"Ціна зі знижкою: {discount(price)}")
# кінець завдання 8

#  завдання 9
def login(username):
    if username == "admin":
        return "Вхід дозволено"
    else:
        return "Невірне ім'я користувача"
user_input = input("Будь ласка, введіть ім'я користувача: ")
print(login(user_input))
# кінець завдання 9







