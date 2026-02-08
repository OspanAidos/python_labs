#1
class Dog:
  species = "Canine"
  def __init__(self, name):
    self.name = name
d1 = Dog("Rex")
print(d1.species)

#2
class Robot:
  count = 0
  def __init__(self):
    Robot.count += 1

#3
class Car:
  wheels = 4
  def __init__(self, color):
    self.color = color

#4
class Employee:
  company = "Google"

#5
class Planet:
  system = "Solar"