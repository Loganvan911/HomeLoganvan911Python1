previous_num = 0

for current_num in range(10):
    total = previous_num + current_num
    print("Поточне число:", current_num,
          "Попереднє число:", previous_num,
          "Сума:", total)

    previous_num = current_num