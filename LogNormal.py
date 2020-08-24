import numpy as np
import matplotlib.pyplot as plt

DESIRED_MIN: float = 100
DESIRED_MAX: float = 3.5 * 10 ** 6

# Play with these values:
MEAN: float = 10.
SIGMA: float = 0.4


def test_plot(sample_size: int):
    """

    :param sample_size:
    :return:
    """
    sample = np.random.lognormal(mean=MEAN, sigma=SIGMA, size=sample_size)
    sample = sample - min(sample)
    sample = sample / max(sample) * DESIRED_MAX
    sample = sample + DESIRED_MIN

    print("sample.avg: ", sum(sample) / len(sample))
    print("sample.min:", min(sample))
    print("sample.max:", max(sample))

    plt.hist(sample, density=True, bins=100)  # `density=False` would make counts
    plt.ylabel('Percentage')
    plt.xlabel('Transaction Value')
    plt.show()


class LogNormal:
    def __init__(self, size: int,
                 mean: float = MEAN,
                 sigma: float = SIGMA,
                 desired_min: float = DESIRED_MIN,
                 desired_max: float = DESIRED_MAX):
        """

        :param size:
        :param mean:
        :param sigma:
        :param desired_min:
        :param desired_max:
        """
        samples = np.random.lognormal(mean=mean, sigma=sigma, size=size)
        samples = samples - min(samples)
        samples = samples / max(samples) * desired_max
        samples = samples + desired_min
        self.__samples = samples

    def get_samples(self):
        return self.__samples
