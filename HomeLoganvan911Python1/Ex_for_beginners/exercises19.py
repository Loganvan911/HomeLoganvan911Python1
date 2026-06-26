income = 45000
tax = 0
if income <= 10000:
    tax = 0
elif income <= 20000:
    tax = (income - 10000) * 0.1
else:
    tax = (10000 * 0.1) + ((income - 20000) * 0.2)

print(f"Tax to be paid:  {int(tax)}")