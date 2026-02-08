#1
class Person:
  def __init__(self, name):
    self.name = name
class Student(Person):
  def __init__(self, name, year):
    super().__init__(name)
    self.graduationyear = year

#2
class A:
  def __init__(self):
    print("A init")
class B(A):
  def __init__(self):
    super().__init__()
    print("B init")
b = B()

#3
class Parent:
  def msg(self):
    print("Parent")
class Child(Parent):
  def msg(self):
    super().msg()
    print("Child")

#4
class Base:
  def __init__(self, val):
    self.val = val
class Sub(Base):
  def __init__(self, val):
    super().__init__(val)

#5
class Shape:
  def __init__(self, color):
    self.color = color
class Square(Shape):
  def __init__(self, color, side):
    super().__init__(color)
    self.side = side