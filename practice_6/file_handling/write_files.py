#1
f = open("out.txt", "w")
f.write("top text")
f.close()

#2
with open("out.txt", "a") as f:
    f.write("\nadded line")

#3
a = ["one\n", "two\n", "three\n"]
with open("out.txt", "w") as f:
    f.writelines(a)

#4
with open("new.txt", "x") as f:
    f.write("unique")

#5
with open("out.txt", "w+") as f:
    f.write("reset")
    f.seek(0)
    print(f.read())