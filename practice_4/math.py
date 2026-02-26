#1
import math
degree = 15
radian = math.radians(degree)
print(f'Input degree: {degree}')
print(f'Output radian: {radian:.6f}')


#2
height = 5
base_1 = 5
base_2 = 6
area = ((base_1 + base_2) / 2) * height
print(f"Height: {height}")
print(f"Base, first value: {base_1}")
print(f"Base, second value: {base_2}")
print(f"Expected Output: {area}")


#3
import math
n_sides = 4
side_length = 25
area = (n_sides * pow(side_length, 2)) / (4 * math.tan(math.pi / n_sides))
print(f"Input the length of a side: {side_length}")
print(f"The area of the polygon is: {int(area)}")


#4
base = 5
height = 6
area = float(base * height)
print(f"Length of base: {base}")
print(f"Height of parallelogram: {height}")
print(f"Expected Output: {area}")