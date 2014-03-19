import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np


def mean_test(event_list, attribute, length):
    series = [e.concat_data.series_after(attribute, lag=2, length=length)
              for e in event_list]
    returns = [s.sum() for s in series]
    print('Mean:', np.mean(returns))
    # t-test
    # null hypothesis: expected value = 0
    t_statistic, p_value = stats.ttest_1samp(returns, 0)
    print('p_value:', p_value)


def plot_histogram_of_alphas(event_list):
    attribute, length = 'alpha', 20
    series = [e.concat_data.series_after(attribute, lag=2, length=length)
              for e in event_list]
    returns = [s.sum() for s in series]
    plt.hist(returns, bins=50, normed=True, alpha=0.6, color='g')
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    mu, std = stats.norm.fit(returns)
    p = stats.norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    title = "Fit results: mu = %.2f,  std = %.2f" % (mu, std)
    plt.title(title)
