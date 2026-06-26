def my_function(number1, number2):
    product = number1 * number2

    if product <= 1000:
        return product
    else:
        return number1 + number2


print("Результат:", my_function(20, 30))
print("Результат:", my_function(40, 30))