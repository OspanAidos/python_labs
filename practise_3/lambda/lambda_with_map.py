#1
numbers = [1, 2, 3, 4]
result = map(lambda x: x * 2, numbers)
print(list(result))

#2
words = ["apple", "banana"]
lengths = map(lambda s: len(s), words)
print(list(lengths))

#3
nums1 = [1, 2, 3]
nums2 = [4, 5, 6]
result = map(lambda x, y: x + y, nums1, nums2)
print(list(result))

#4
str_nums = ["1", "2", "3"]
ints = map(lambda x: int(x), str_nums)
print(list(ints))

#5
temps = [0, 10, 20]
f_temps = map(lambda c: (c * 9/5) + 32, temps)
print(list(f_temps))