import numpy as np


def box_cox_transformation(x, lambda_):
    """
    Source
    ------
    https://www.itl.nist.gov/div898/handbook/eda/section3/boxcox.htm

    Formula
    -------
    The Box-Cox transformation is defined as: T(X) = (X^λ - 1) / λ,
    where X is the response variable and λ is the transformation
    parameter. For λ = 0, the log of the data is taken instead of using
    the above formula.
    """
    if lambda_ == 0:
        return np.log(x) / np.log(10)
    else:
        return (x**lambda_ - 1) / lambda_


def normal_pdf(x, mean=0, std=1):
    """
    The probability density function of a normal distribution with a
    mean of mu and standard deviation of sigma is given by the following
    formula:
    f(x) = (1/sqrt(2*pi*sigma^2)) * e^(-(x-mu)^2 / (2*sigma^2))

    This function (normal_pdf) can take a number or a numpy array for
    argument x.
    """
    coef = 1/np.sqrt(2*np.pi*(std**2))
    power = -(x-mean)**2 / (2*(std**2))
    return coef * np.exp(power)
    
