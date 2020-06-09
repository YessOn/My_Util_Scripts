import math

# How It Works?
# Two primes are needed p = 37, q= 41
# n = p * q

# The Euler Totient Function phi(n)

# The Encryption Key, gcd(e, phi(n)) = 1

# The Decryption Key, d= (1 mod[phi(n)]) / e

# Text Encryption
# Code = Char**encryption_key mod[n]

# The Euler Totient Function
def phi(n):
	""" The Euler Totient Function """
	result = 1
	for i in range(2, n):
		if math.gcd(i, n) == 1: result += 1
	return result

# The Encryption Key
def e_key(phi):
	""" The Encryption Key Generator """
	for e in range(2, phi):
		if math.gcd(e, phi) == 1: return e

# The Encrypter Function
def encrypter(p, q, text):
	""" The Encrypter Function Generator """
	enc = []
	n = p * q
	for i in text:
		enc.append(str((ord(i) ** e_key(phi(n))) %  n))
	return ", ".join(enc)

# Examples:
# print(encrypter(89, 97, "YASSINE"))
