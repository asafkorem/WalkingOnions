import numpy as np
import matplotlib.pyplot as plt

desired_min = 100
desired_max = 3.5 * 10**6

# Play with these values:
mean = 10.
sigma = 0.4

sample = np.random.lognormal(mean=mean, sigma=sigma, size=100000)
sample = sample - min(sample)
sample = sample / max(sample) * desired_max
sample = sample + desired_min


print("sample.avg: ", sum(sample)/len(sample))
print("sample.min:", min(sample))
print("sample.max:", max(sample))


plt.hist(sample, density=True, bins=100)  # `density=False` would make counts
plt.ylabel('Percentage')
plt.xlabel('Transaction Value')
plt.show()

