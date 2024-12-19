import math


def rotate(l, reverse=False):
    if reverse:
        return l[1:] + l[:1]
    return l[-1:] + l[:-1]


def periodic_skewed_exponential(t, period=2 * math.pi, skew=0.5, steepness=10):
    t_mod = t % period
    if t_mod < period * skew:
        normalized_t = t_mod / (period * skew)
        return math.exp(-steepness * (1 - normalized_t) ** 2)
    else:
        normalized_t = (t_mod - period * skew) / (period * (1 - skew))
        return math.exp(-steepness * normalized_t**2)
