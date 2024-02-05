#input is a point and a parameter and b parameter of a line
#output is a boolean value that indicates if the point is on the line
#if not check the distance bettween the point and the line
#and return the distance
from math import sqrt
def check_for_point_on_linearF(x, y, a, b):
    if y == a * x + b:
        return True
    else:
        return abs(a*x - y + b)/sqrt(a**2 + 1)

# now with input from user
x = float(input('Enter x: '))
y = float(input('Enter y: '))
a = float(input('Enter a: '))
b = float(input('Enter b: '))
print(check_for_point_on_linearF(x, y, a, b))
print(check_for_point_on_linearF(x, y, a, b)/sqrt(2))