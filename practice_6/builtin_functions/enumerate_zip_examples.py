#1
a = ["gold", "silver", "bronze"]
for i, v in enumerate(a, 1):
    print(i, v)

#2
k = ["name", "age"]
v = ["Aidos", 18]
d = dict(zip(k, v))

#3
a = [1, 2]
b = [3, 4]
c = [5, 6]
for x, y, z in zip(a, b, c):
    print(x + y + z)

#4
a = "abc"
b = list(enumerate(a))

#5
a = [10, 20, 30]
b = ["a", "b"]
print(list(zip(a, b)))