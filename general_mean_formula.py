from math import log, exp, inf, isfinite

def power_mean(values, p):
  if not values:
    raise ValueError("values must be non-empty")

  if p == inf:
    return max(values)
  if p == -inf:
    return min(values)

  n = len(values)

  if abs(p) < 1e-12:  # geometric mean limit
    if any(v <= 0 for v in values):
      raise ValueError("geometric mean requires all values > 0")
    return exp(sum(log(v) for v in values) / n)

  if p < 0 and any(v <= 0 for v in values):
    raise ValueError("p <= 0 requires all values > 0")

  return (sum(v ** p for v in values) / n) ** (1.0 / p)


# Example Usage
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

print("Values: ", values)
print("\np=-inf (min):        ", power_mean(values, -inf))
print("p=1    (arithmetic): ", power_mean(values, 1   ))
print("p=0    (geometric):  ", power_mean(values, 0   ))
print("p=-1   (harmonic):   ", power_mean(values, -1  ))
print("p=2    (RMS):        ", power_mean(values, 2   ))
print("p=inf  (max):        ", power_mean(values, inf ))
