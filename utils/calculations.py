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
