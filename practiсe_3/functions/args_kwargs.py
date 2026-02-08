#1
def my_function(*kids):
  print("The youngest child is " + kids[2])
my_function("Emil", "Tobias", "Linus")

#2
def my_function(**kid):
  print("His last name is " + kid["lname"])
my_function(fname = "Tobias", lname = "Refsnes")

#3
def sum_all(*nums):
  return sum(nums)
print(sum_all(1, 2, 3, 4))

#4
def print_info(**data):
  for key, value in data.items():
    print(f"{key}: {value}")
print_info(name="Alice", age=25)

#5
def combine(*args, **kwargs):
  print(args, kwargs)
combine(1, 2, a=3, b=4)