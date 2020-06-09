"""
The Dichotomy Algorithm :
Given a function f : x -> f(x) && interval [a, b]
Find x such that: a < x < b && f(x) = 0
"""
def dichtomy(f, a, b, e):
  """ The Dichotomy Algorithm
  dichotomy(
  f: represenst the function: can be written as an anonymous function
  a: first boundary
  b: second boundary
  e: the exponential precision
  )
  """
  while (b - a) > e:
    m = (a + b) / 2
    if (f(a) * f(m)) > 0: a = m
    else: b = m
  return m

print(dichtomy(lambda x: x**3 - 2*x, 1, 2, 1e-15))
print(dichtomy(lambda x: x**3 + 2*x -1, 0, 1, 1e-15))
print(dichtomy(lambda x: x**4 + 5*x - 1, 0, 1, 1e-15))

