#1
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age
p1 = Person("John", 36)
print(p1.name)

#2
class Car:
  def __init__(self, model):
    self.model = model
c1 = Car("Ford")
print(c1.model)

#3
class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

#4
class Book:
  def __init__(self, title):
    self.title = title

#5
class User:
  def __init__(self, id):
    self.id = id