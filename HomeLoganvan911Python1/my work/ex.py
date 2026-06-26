# def my_function(fname):
#  print(fname + " Refsnes")

# my_function("Emil")
# my_function("Tobias")
# my_function("Linus")


# def my_function(fname, lname):
#  print(fname + " " + lname)

# my_function("Emil", "Refsnes")

# def my_function(animal, name):
# print("I have a", animal)
# print("My", animal + "'s name is", name)

# my_function("dog", "Buddy")

# x = lambda a : a + 10
# print(x(15))


# def hello():
#     return "Hello"
# # print(hello())

# rez = hello()
# rez += hello()
# print(rez)

# def add(a, b):
#     if a < 0 or b < 0:
#         return "negative numbers are not allowed"
#     else:
#         return a + b
    
# num1 = int(input("Введите первое число: "))
# num2 = int(input("Введите второе число: "))
# print("Результат:", add(num1, num2))


# # print(add(5, 3))
# # print(add(10, 20))

# operation(a, b, operator)

# def my_oper(a, b, operator):
#     if operator == 1:
#         return a + b
#     elif operator == 2:
#         return a - b
#     elif operator == 3:
#         return a * b
#     elif operator == 4:
#         return a / b
#     elif operator == 5:
#         return a ** b
#     else: 
#         return "There is not operation"

# num1 = int(input("Введіть перше число: "))
# num2 = int(input("Введіть друге число: "))
# operator = int(input("Виберіть операцію (1-6): "))
# result = my_oper(num1, num2, operator)
# print("Результат:", result)

# def say_hello():
#     return "Hello"

# result = say_hello() + " Gays"
# print(result)

# # print(say_hello())


# 22.06.2026
# # Exercise 1.
# class Student:
#     def __init__(self, name, age):
#         # Ініціалізація атрибутів класу
#         self.name = name
#         self.age = age

#     def show_info(self):
       
#         print(f"Студент: {self.name}, Вік: {self.age}")

# student1 = Student("Олексій", 20)
# student1.show_info()

# student2 = Student("Марія", 19)
# student2.show_info()

# student3 = Student("Іван", 21)
# student3.show_info()
# # end of Exercise 1.

# Exercise 2.

# from datetime import datetime

# class Car:
#     def __init__(self, brand, model, year):
#         self.brand = brand
#         self.model = model
#         self.year = year

#     def get_age(self):
#         current_year = datetime.now().year
#         return current_year - self.year 

# my_car = Car("Toyota", "Camry", 2026)
# car_age = my_car.get_age()

# print(f"Автомобіль: {my_car.brand} {my_car.model}")
# print(f"Рік випуску: {my_car.year}")
# print(f"Вік автомобіля: {car_age} років")
# # end of Exercise 2.


# # Exercise 3.
# class Rectangle:
#     def __init__(self, length, width):
#         self.length = length  
#         self.width = width    

#     def area(self):
#         "Метод для обчислення площі прямокутника"
#         return self.length * self.width

#     def perimeter(self):
#         "Метод для обчислення периметра прямокутника"
#         return 2 * (self.length + self.width)

# my_rectangle = Rectangle(6, 12)

# print(f"Площа прямокутника: {my_rectangle.area()}")          
# print(f"Периметр прямокутника: {my_rectangle.perimeter()}")  
# # end of Exercise 3.

# # Exercise 4.
# class BankAccount:
#     def __init__(self, owner, balance=0.0):
#         self.owner = owner          
#         self.balance = balance      

#     def deposit(self, amount):
#         if amount > 0:
#             self.balance += amount
#             print(f"Рахунок поповнено на {amount} грн. Поточний баланс: {self.balance} грн.")
#         else:
#             print("Сума поповнення має бути більшою за 0.")

#     def withdraw(self, amount):
#         if amount <= 0:
#             print("Сума зняття має бути більшою за 0.")
#         elif amount > self.balance:
#             print(f"Помилка: Недостатньо коштів! Спроба зняти {amount} грн, але на рахунку лише {self.balance} грн.")
#         else:
#             self.balance -= amount
#             print(f"Успішно знято {amount} грн. Залишок: {self.balance} грн.")

#     def show_balance(self):
#         print(f"Власник рахунку: {self.owner} | Баланс: {self.balance} грн.")

# account = BankAccount("ПЕТРО", 1000)

# account.show_balance()

# account.deposit(500)

# account.withdraw(2000)

# account.withdraw(300)

# account.show_balance()
# # end of Exercise 4.

# # Exercise 5.
# class Tank:
#     def __init__(self, name, ammo, armor):
#         self.name = name          
#         self.ammo = ammo          
#         self.armor = armor        

#     def fire(self):
#         if self.ammo > 0:
#             self.ammo -= 1
#             print(f"{self.name} здійснив постріл! Снарядів залишилось: {self.ammo}")
#         else:
#             print(f"{self.name} не може стріляти: закінчилися снаряди! Потрібна перезарядка.")

#     def reload(self, count):
#         if count > 0:
#             self.ammo += count
#             print(f"{self.name} перезаряджено на +{count} снарядів. Всього: {self.ammo}")
#         else:
#             print("Кількість снарядів для перезарядки має бути більшою за 0.")

#     def show_status(self):
#         print(f"\n--- Статус танка {self.name} ---")
#         print(f"Броня: {self.armor}")
#         print(f"Снаряди: {self.ammo}")
#         print("-----------------------------\n")

# my_tank = Tank("Leopard 2", 3, "100%")

# my_tank.show_status()

# my_tank.fire()
# my_tank.fire()
# my_tank.fire()

# my_tank.reload(5)

# my_tank.show_status()
# # end of Exercise 5.

# # Exercise 6.
# class Book:
#     def __init__(self, title, author, pages):
#         self.title = title       
#         self.author = author     
#         self.pages = pages        

#     def display_info(self):
#         print(f"Книга: '{self.title}' | Автор: {self.author} | Сторінок: {self.pages}")

# books_list = [
#     Book("Кобзар", "Тарас Шевченко", 480),
#     Book("Тигролови", "Іван Багряний", 320),
#     Book("Захар Беркут", "Іван Франко", 250)
# ]
# print("Список книг:")
# for book in books_list:
#     book.display_info()
# # end of Exercise 6.

# # Exercise 7.
# class Animal:
#     def make_sound(self):
#         pass
# class Dog(Animal):
#     def make_sound(self):
#         print("Гав!")
# class Cat(Animal):
#     def make_sound(self):
#         print("Няв!")

# dog = Dog()
# cat = Cat()

# dog.make_sound() 
# cat.make_sound() 
# # end of Exercise 7.


# # Exercise 8. 
# class MilitaryVehicle:
#     def __init__(self, name: str, speed: int):
#         self.name = name
#         self.speed = speed

#     def move(self):
#         print(f"{self.name} рухається зі швидкістю {self.speed} км/год.")
# class Tank(MilitaryVehicle):
#     def move(self):
#         print(f"Танк {self.name} їде крізь хащі зі швидкістю {self.speed} км/год.")
# class Drone(MilitaryVehicle):
#     def move(self):
#         print(f"Безпілотник {self.name} підймається в повітря і летить на швидкості {self.speed} км/год.")

# heavy_tank = Tank("Leopard 2", 70)
# recon_drone = Drone("Shark", 130)

# heavy_tank.move()
# recon_drone.move()
# end of Exercise 8.

# exercise 9









