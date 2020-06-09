# Absolute Value Or Module(Math: radius in Complex) Z=r*e^(ix)
print(abs(3+5j))

# Convert Numbers to Binary
print(bin(8))

# Convert Single Characters to Binary
rint(bin(ord("M")))
# Convert a Whole Plain Text to Binary
# First Hard and Quick Way
print(' '.join(bin(x)[2:].zfill(8) for x in 'Hello you'.encode('UTF-8')))
# Second Standard and Long Way
y = []
for x in 'Hello you'.encode('UTF-8'):
    y.append(bin(x)[2:].zfill(8))
print(" ".join(y))

# Converst ASCII Decimals into Characters
print(chr(65)) # Print A

# Attribute Family: delattr, setattr, hasattr, getattr
class Person:
    name = "mYName"
    age = 29
delattr(Person, 'age') # Delete a Class Attribute
setattr(Person, 'age', 30) # Set a Class Attribute
print(hasattr(Person, 'age')) # Check Boolean Of a Class Attribute
print(getattr(Person, 'name')) # Get a Class Attribute

# Division & Remainder
print(divmod(7, 2)) # 7/2 Returns (Quotient: 3, Remainder: 1)

# Enumerate An Iterable Object
mytuple = ("apple", "banana", "appricot")
x = enumerate(mytuple, 1)
print(list(x)) # Print element by order of enumeration

# Filter through an object
ages = [12, 78, 45, 25, 11, 32]
def filering(x):
    if x < 18:
        return False
    else:
        return True
adults = filter(filering, ages)
newages = []
for x in adults:
    newages.append(x)
print(newages)

# Convert a Decimal to HexaDecimal
print(hex(200)[2:].upper())

# Convert Hex2Dec
print(int("FFA", 16))
# Convert Bin2Dec
print(int("1111", 2))
