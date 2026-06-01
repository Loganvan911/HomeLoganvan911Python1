def first_last_same(number_list):

    print("Given list:", number_list)

    first = number_list[0]
    last = number_list[-1]

    if first == last:
        return True
    else:
        return False

numbers_x = [10, 20, 30, 40, 10]
print("result is", first_last_same(numbers_x))

numbers_y = [75, 65, 35, 75, 30]
print("result is", first_last_same(numbers_y))
