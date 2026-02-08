#1
x = lambda a : a + 10
print(x(5))

#2
x = lambda a, b : a * b
print(x(5, 6))

#3
x = lambda a, b, c : a + b + c
print(x(5, 6, 2))

#4
square = lambda x: x**2
print(square(9))

#5
is_positive = lambda x: x > 0
print(is_positive(-1))