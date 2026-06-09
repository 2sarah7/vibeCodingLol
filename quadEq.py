import math

# inputs
a = float(input("a = "))
b = float(input("b = "))
c = float(input("c = "))

# discriminant
D = b**2 - 4*a*c

if a == 0:
    print("Not quadratic (a ≠ 0 required).")

elif D > 0:
    x1 = (-b + math.sqrt(D)) / (2*a)
    x2 = (-b - math.sqrt(D)) / (2*a)
    print("Two real solutions:", x1, x2)

elif D == 0:
    x = -b / (2*a)
    print("One real solution:", x)

else:
    real = -b / (2*a)
    imag = math.sqrt(-D) / (2*a)
    print("Complex solutions:", complex(real, imag), complex(real, -imag))

