#1
class Person:
  def __init__(self, name):
    self.name = name
  def myfunc(self):
    print("Hello my name is " + self.name)
p1 = Person("John")
p1.myfunc()

#2
class Calculator:
  def add(self, a, b):
    return a + b
calc = Calculator()
print(calc.add(2, 3))

#3
class Dog:
  def bark(self):
    print("Woof!")
d = Dog()
d.bark()

#4
class Circle:
  def set_radius(self, r):
    self.radius = r

#5
class Printer:
  def show(self, msg):
    print(msg)