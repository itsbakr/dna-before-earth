"""The unobserved interval before the oldest data point.

Any straight-line extrapolation to 1 bp equals
    origin = t_first + (y_first - y0) / (m * b)
where b is the fitted rate and m is the ratio of the (unobserved) early rate to b.
The data constrain b but say nothing about m, so the origin date is set by the
assumption about m.
"""

import numpy as np


def origin_given_multiplier(t_first, y_first, b, m, y0=0.0):
    return t_first + (y_first - y0) / (np.asarray(m, float) * b)


def required_multiplier(t_first, y_first, b, origin_age, y0=0.0):
    """Early-rate multiplier needed for the origin to fall at ``origin_age``."""
    return (y_first - y0) / ((origin_age - t_first) * b)


def doubling_time_myr(rate_log10_per_gyr):
    return np.log10(2) / np.asarray(rate_log10_per_gyr, float) * 1000
