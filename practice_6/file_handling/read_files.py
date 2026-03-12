#1
f = open("data.txt", "r")
print(f.read())
f.close()

#2
f = open("data.txt", "r")
print(f.readline())
f.close()

#3
with open("data.txt", "r") as f:
    a = f.readlines()
    print(a)

#4
with open("data.txt", "r") as f:
    for l in f:
        print(l.strip())

#5
with open("data.txt", "r") as f:
    print(f.read(10))