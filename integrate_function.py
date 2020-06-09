# The Integration function
def integrate(f, a, b, n):
	""" Calculate the Area Under Any Curve
	integrate(
	f: represenst the function: can be written as an anonymous function
	a: first boundary
	b: second boundary
	n: reperesnt the number of squares it must be huge
	)
	"""
	area = 0
	dx = (b - a) / n
	for i in range(int(n)):
		area += dx * f(a + dx * i)
	return area

print(integrate(lambda x: x**3 - 2*x, -1, 5, 1e6))
print(integrate(lambda x: x**3 + 2*x -1, 0, 15, 1e6))
print(integrate(lambda x: x**4 + 5*x - 1, -1, 1, 1e6))

