#1
for x in ["apple", "banana", "cherry"]:
  if x == "banana":
    continue
  print(x)

#2
for i in range(6):
  if i == 3:
    continue
  print(i)

#3
for x in "banana":
  if x == "a":
    continue
  print(x)

#4
for n in range(10):
  if n % 2 != 0:
    continue
  print(n)

#5
for i in range(1, 5):
  if i == 2:
    continue
  print("Iteration", i)