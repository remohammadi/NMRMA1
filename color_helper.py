import matplotlib.colors as mc
import colorsys


def shade_color(color, amount=0.5):
    """
    Lightens/Darkens the given color by multiplying (1-luminosity) by
    the given amount.
    Input can be matplotlib color string, hex string, or RGB tuple.

    Examples:
    >>> shade_color('g', 0.3)
    (0.5500000000000002, 0.9999999999999999, 0.5500000000000002)
    >>> shade_color('#F034A3', 0.6)
    (0.9647058823529411, 0.5223529411764707, 0.783529411764706)
    >>> shade_color((.3,.55,.1), 0.5)
    (0.6365384615384615, 0.8961538461538462, 0.42884615384615377)
    >>> shade_color('#0a3050', 1.5)
    (0.0, 0.0, 0.0)
    """
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], max(0, 1 - amount * (1 - c[1])), c[2])

if __name__ == "__main__":
    import doctest
    doctest.testmod()
