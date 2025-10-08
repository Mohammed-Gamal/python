import sympy as sp

def inverse_function(func, x):
  # Solve y = f(x) for x
  y = sp.symbols('y')
  sols = sp.solve(sp.Eq(y, func), x)  # x expressed in terms of y

  if not sols:
    raise ValueError("No inverse found.")
  
  inv_expr = sols[0].subs(y, x)  # make it a function of x
  return sp.simplify(inv_expr)


# Example Usage
x = sp.symbols('x')
f = 2*x - 7

f_inv = inverse_function(f, x)

print(f"f(x) = {f}")
print(f"f^-1(x) = {f_inv}")

sp.plot(
  f, f_inv,
  (x, -10, 10),
  legend=True,
  title='Function and Its Inverse'
)
