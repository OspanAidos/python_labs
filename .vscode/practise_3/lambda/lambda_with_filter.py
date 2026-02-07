#1
numbers = [1, 2, 3, 4, 5, 6]
evens = filter(lambda x: x % 2 == 0, numbers)
print(list(evens))

#2
words = ["hi", "hello", "python", "a"]
long_words = filter(lambda s: len(s) > 3, words)
print(list(long_words))

#3
ages = [5, 12, 17, 18, 24, 32]
adults = filter(lambda x: x >= 18, ages)
print(list(adults))

#4
nums = [-1, 0, 1, 2]
positives = filter(lambda x: x > 0, nums)
print(list(positives))

#5
mixed = [True, False, True, True]
truthy = filter(lambda x: x is True, mixed)
print(list(truthy))