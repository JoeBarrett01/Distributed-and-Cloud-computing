print("\n1-----------")
print("Hello World")

a = 5
b = 3
c = a+b
print("\n2------------")
print(c)

def sum(e,f):
    return (e+f)

e = 2
f = 3
print("\n3-------------")
print(sum(e,f))

squares = [i*i for i in range(10)]
print("\n4-------------")
print(squares)

print("\n5-------------")
del squares[0]
print(squares)
squares.append(0)
print(squares)

print("\n6-------------")
def greatest (x,y):
    if x > y:
        return ("x is greater than y")
    elif x == y:
        return ("x and y are equivalent")
    else:
        return ("x is less than y")

x = 6
y = 7
print(greatest(x,y))

print("\n7-------------")
class MyClass:
    x = 5
    y = 8

p1 = MyClass()
print(p1.x)
print(p1.y)

print("\n8-------------")
class MyClass:
    def __init__ (self, x, y):
        self.x = x
        self.y = y

p1 = MyClass(4, 65)
print(p1.x)
print(p1.y)

print("\n9--------------")
class MyClass:
    def __init__ (self, x, y):
        self.x = x
        self.y = y

    def soln (self):
        print(self.x)
        print(self.y)

p1 = MyClass(4, 65)
p1.soln()

print("\n10-------------")
class MyClass:
    def __init__ (self, x, y):
        self.x = x
        self.y = y

    def soln (self):
        print(self.x)
        print(self.y)

    def set_xy (self, x, y):
        self.x = x
        self.y = y
p1 = MyClass(4, 65)
p1.soln()

p1.set_xy(0,0)
p1.soln()