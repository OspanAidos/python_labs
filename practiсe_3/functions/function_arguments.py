#1
def my_function(fname):
  print(fname + " Refsnes")
my_function("Emil")

#2
def my_function(fname, lname):
  print(fname + " " + lname)
my_function("Emil", "Refsnes")

#3
def my_function(country = "Norway"):
  print("I am from " + country)
my_function("Sweden")

#4
def multiply(a, b):
  print(a * b)
multiply(3, 5)

#5
def check_age(age):
  if age >= 18:
    print("Adult")
check_age(20)