def cdf(y):
  return sorted(y), [float(i) / len(y) for i in range(len(y))]
  