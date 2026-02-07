#1
class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname
class Student(Person):
  pass
x = Student("Mike", "Olsen")
print(x.firstname)

#2
class Animal:
  def eat(self):
    print("Eating...")
class Cat(Animal):
  pass
c = Cat()
c.eat()

#3
class Vehicle:
  pass
class Truck(Vehicle):
  pass

#4
class Device:
  brand = "Universal"
class Phone(Device):
  pass

#5
class Parent:
  pass
class Child(Parent):
  pass