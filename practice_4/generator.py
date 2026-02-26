#1
def square_generator(N):
    for i in range(N + 1):
        yield i ** 2
for sq in square_generator(5):
    print(sq) 


#2
def even_generator(n):
    for i in range(0, n + 1, 2):
        yield str(i)
n = int(input("Введите n: "))
gen = even_generator(n)
print(", ".join(gen))


#3
def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i
n = 50
for num in divisible_by_3_and_4(n):
    print(f"Число {num} делится на 3 и 4")


#4
def squares(a, b):
    for i in range(a, b + 1):
        yield i ** 2
a, b = 3, 7
print(f"Квадраты от {a} до {b}:")
for val in squares(a, b):
    print(val)


#5
def countdown(n):
    while n >= 0:
        yield n
        n -= 1
for x in countdown(5):
    print(x) # 5, 4, 3, 2, 1, 0