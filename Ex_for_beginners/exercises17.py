def merge_lists(list1, list2):
    rezult = []
    for num in list1:
        if num % 2 != 0:
            rezult.append(num)
    for num in list2:
        if num % 2 == 0:
            rezult.append(num)
    return rezult

list1 = [10, 20, 25, 30, 35]
list2 = [40, 45, 60, 75, 90]
print("rezult: ", merge_lists(list1, list2))