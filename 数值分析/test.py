import sympy

x = sympy.Symbol('x')
s = "x**2-115"
es = eval(s)
esd = sympy.diff(es, x)
print(esd)
