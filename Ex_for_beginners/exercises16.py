def polindrom(number):
    print("original number", number)
    original_str = str(number)
    reversed_str = original_str[::-1]

    if original_str == reversed_str:
        print("The number is a palindrome.")
    else:
        print("The number is not a palindrome.")

polindrom(121)
polindrom(125)