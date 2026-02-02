#1
i = 0
while i < 6:
  i += 1
  if i == 3:
    continue
  print(i)

#2
x = 10
while x > 0:
  x -= 1
  if x % 2 == 0:
    continue
  print(x)

#3
i = 0
while i < 5:
  i += 1
  if i == 1:
    continue
  print("Step", i)

#4
n = 0
while n < 4:
  n += 1
  if n == 2:
    continue
  print(n * 10)

#5
i = 0
while i < 3:
  i += 1
  continue
  print("This won't print")