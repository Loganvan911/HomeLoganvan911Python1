import random

txt = ["Ivan", "Petro", "Oleksandr", "Mykola", "Andrii",
    "Vasyl", "Dmytro", "Serhii", "Oleh", "Yurii",
    "Volodymyr", "Maksym", "Roman", "Bohdan", "Taras",
    "Artem", "Vitalii", "Ruslan", "Yevhen", "Stepan",
    "Mariia", "Olena", "Anna", "Iryna", "Nataliia",
    "Tetiana", "Kateryna", "Yuliia", "Oksana", "Liudmyla",
    "Sofiia", "Daryna", "Viktoriia", "Alina", "Polina",
    "Khrystyna", "Zoriana", "Marta", "Solomiia", "Veronika",
    "Denys", "Ihor", "Anastasiia", "Valeriia", "Yeva",
    "Emiliia", "Milana", "Arsen", "Nazar","Davyd",
   "Hlib","Mark","Eduard","Stanislav","Vladyslav",
    "Anton", "Illia", "Svitlana", "Nina", "Halyna",
    "Alla", "Liubov", "Uliana", "Liliia", "Karina",
    "Elina", "Myroslava", "Ostap", "Myroslav", "Orest",
    "Sviatoslav", "Liubomyr", "Adam", "Luka", "Mykhailo",
    "Valentyn", "Heorhii", "Zlata", "Anhelina", "Kira",
    "Diana", "Melaniia", "Yana", "Inna", "Taisiia",
    "Eleonora", "Bohdana"]

for i in range(10):
    winner = random.choice(txt)

winner = random.choice(txt)

print("Winner:", winner)
