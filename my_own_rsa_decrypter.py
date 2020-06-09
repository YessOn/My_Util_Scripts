from my_own_rsa_encrypter import encrypter, e_key, phi

# How It Works?

# Text Decryption
# Char == CharCode**decryption_key mod[n]

# The Decryption Key
def d_key(phi, e):
	""" The Decryption Key Generator """
	for d in range(1, phi):
		if d*e % phi == 1: return d

# The Decrypter Function
def decrypter(p, q, code):
	""" The Decrypter Function Generator """
	n = p * q
	code = code.split(",")
	dec = ""
	for i in code:
		dec += chr(int(i)**d_key(phi(n), e_key(phi(n))) % n)
	return dec

# Examples:
# print(decrypter(89, 97, encrypter(89, 97, "yess.mapss@gmail.com")))