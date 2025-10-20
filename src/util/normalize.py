import math

def normalize_sigmoid(n, center=0, width=1):
    return 1 / (1 + math.exp(-(n - center) / width))


def to_zero_point(n):
    n_abs = abs(n)
    if n_abs >= 1:
        num_digits = len(str(int(n_abs)))
        return n / (10 ** num_digits)
    else:
        return n

def normalize(n):
    n_zeroed = to_zero_point(n)
    return normalize_sigmoid(n_zeroed)