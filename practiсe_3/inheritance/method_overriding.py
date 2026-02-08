#1
class Animal:
  def speak(self):
    print("Animal speaks")
class Dog(Animal):
  def speak(self):
    print("Bark")
d = Dog()
d.speak()

#2
class Parent:
  def show(self):
    print("Inside Parent")
class Child(Parent):
  def show(self):
    print("Inside Child")

#3
class Bird:
  def fly(self):
    print("Flying")
class Penguin(Bird):
  def fly(self):
    print("Cannot fly")

#4
class Shape:
  def area(self):
    return 0
class Square(Shape):
  def area(self):
    return 100

#5
class Human:
  def greet(self):
    print("Hello")
class Student(Human):
  def greet(self):
    print("Hi teacher")