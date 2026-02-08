#1
class Engine:
  def start(self): print("Engine start")
class Wheels:
  def roll(self): print("Rolling")
class Car(Engine, Wheels):
  pass
c = Car()
c.start()
c.roll()

#2
class A:
  def method_a(self): pass
class B:
  def method_b(self): pass
class C(A, B):
  pass

#3
class Father:
  hair = "Black"
class Mother:
  eyes = "Blue"
class Child(Father, Mother):
  pass

#4
class Flyer:
  def fly(self): print("Flying")
class Swimmer:
  def swim(self): print("Swimming")
class Duck(Flyer, Swimmer):
  pass

#5
class Log1:
  def log1(self): print("Log 1")
class Log2:
  def log2(self): print("Log 2")
class Logger(Log1, Log2):
  pass