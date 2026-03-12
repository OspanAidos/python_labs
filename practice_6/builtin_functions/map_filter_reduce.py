#1
a = [1, 2, 3]
b = list(map(lambda x: x * 10, a))

#2
a = ["apple", "banana"]
b = list(map(str.upper, a))

#3
a = range(10)
b = list(filter(lambda x: x % 2 == 0, a))

#4
a = ["hi", "", "bye"]
b = list(filter(None, a))

#5
from functools import reduce
a = [1, 2, 3, 4]
b = reduce(lambda x, y: x + y, a)