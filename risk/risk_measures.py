"""
(1) Dispersion measuures
(2) Downside measures
"""





def get_mean_absolute_deviation(data, start, end):
    return data['alpha'][start:end].mad()


def get_standard_deviation(data, start, end):
    "unbiased standard deviation"
    return data['alpha'][start:end].std()


def get_skewness(data, start, end):
    "unbiased skewness"
    return data['alpha'][start:end].skew()


def get_kurtosis(data, start, end):
    "unbiased kurtosis"
    return data['alpha'][start:end].kurt()


