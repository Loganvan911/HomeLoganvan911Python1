# умови в пайтоні

#age = 10
# if умова є true:
#if age >= 18:
 #   print("age is greater than 18")
#else:
#    print("age is less than 18")
# if умова є False:

#age = int(input("enter ypur name:"))


#print("your age is", + age)

# if умова є true:
#if age > 18:
#    print("age is greater than 18")
#elif age < 18:
#    print("age is less than 18")
#else:
#    print("age is equal to 18")

age = int(input("enter ypur name:"))

if age >= 18 and age < 20:
    print("age of the young person")
elif age >= 20 and age <= 50:
    print("age of the adult person")
elif age < 18:
    print("age of the children person")
else:
    print("age of the old person")

