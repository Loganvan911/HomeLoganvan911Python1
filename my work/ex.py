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

def my_oper(a, b, operator):
    if operator == 1:
        return a + b
    elif operator == 2:
        return a - b
    elif operator == 3:
        return a * b
    elif operator == 4:
        return a / b
    elif operator == 5:
        return a ** b
    elif operator == 6: 
        return a % b
    else: 
        return "There is not operation"

num1 = int(input("Введіть перше число: "))
num2 = int(input("Введіть друге число: "))
operator = int(input("Виберіть операцію (1-6): "))
result = my_oper(num1, num2, operator)
print("Результат:", result)









