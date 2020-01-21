
"""More math functions
"""

def lerp(a, b, t):
    """Unclamped Linear interpolation
    
    Arguments:
        a {int/float} -- from
        b {int/float} -- to
        t {int/float} -- time
    
    Returns:
        float -- if time is between 0 and 1 return a value between a and b
    """
    return a + ((b - a) * t)

def inverse_lerp(a, b, c):
    """Calculates the linear parameter t that produces the interpolant value within the range [a, b].
    
    Arguments:
        a {int/float} -- from
        b {int/float} -- to
        c {int/float} -- value between a and b
    
    Returns:
        int/float -- percentage of value between a and b
    """
    return (c - a) / (b - a)