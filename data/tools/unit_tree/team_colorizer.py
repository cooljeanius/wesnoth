import sys, subprocess

MAGICK_CMD = "convert"


# Note: Luminance formula taken from the Wikipedia article on luminance:
#   http://en.wikipedia.org/wiki/Luminance_(colorimetry)
def rgb2lum(r, g, b):
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


max_color = 255
default_color = {
    "mid": {"r": 255, "g": 0, "b": 0},
    "max": {"r": 0xFF, "g": 0xFF, "b": 0xFF},
    "min": {"r": 0x00, "g": 0x00, "b": 0x00},
}

team_colors = {
    "magenta": {
        "mid": {"r": 0xF4, "g": 0x9A, "b": 0xC1},
        "max": {"r": 0xFF, "g": 0xFF, "b": 0xFF},
        "min": {"r": 0x00, "g": 0x00, "b": 0x00},
    },
    "red": {
        "mid": {"r": 0xFF, "g": 0x00, "b": 0x00},
        "max": {"r": 0xFF, "g": 0xFF, "b": 0xFF},
        "min": {"r": 0x00, "g": 0x00, "b": 0x00},
    },
    "lightred": {
        "mid": {"r": 0xD1, "g": 0x62, "b": 0x0D},
        "max": {"r": 0xFF, "g": 0xFF, "b": 0xFF},
        "min": {"r": 0x00, "g": 0x00, "b": 0x00},
    },
    "darkred": {
        "mid": {"r": 0x8A, "g": 0x08, "b": 0x08},
        "max": {"r": 0xFF, "g": 0xFF, "b": 0xFF},
        "min": {"r": 0x00, "g": 0x00, "b": 0x00},
    },
    "blue": {
        "mid": {"r": 0x2E, "g": 0x41, "b": 0x9B},
        "max": {"r": 0xFF, "g": 0xFF, "b": 0xFF},
        "min": {"r": 0x0F, "g": 0x0F, "b": 0x0F},
    },
    "lightblue": {
        "mid": {"r": 0x00, "g": 0xA4, "b": 0xFF},
        "max": {"r": 0xFF, "g": 0xFF, "b": 0xFF},
        "min": {"r": 0x00, "g": 0x0A, "b": 0x21},
    },
    "green": {
        "mid": {"r": 0x62, "g": 0xB6, "b": 0x64},
        "max": {"r": 0xFF, "g": 0xFF, "b": 0xFF},
        "min": {"r": 0x00, "g": 0x00, "b": 0x00},
    },
    "brightgreen": {
        "mid": {"r": 0x8C, "g": 0xFF, "b": 0x00},
        "max": {"r": 0xEB, "g": 0xFF, "b": 0xBF},
        "min": {"r": 0x2D, "g": 0x40, "b": 0x01},
    },
    "purple": {
        "mid": {"r": 0x93, "g": 0x00, "b": 0x9D},
        "max": {"r": 0xFF, "g": 0xFF, "b": 0xFF},
        "min": {"r": 0x00, "g": 0x00, "b": 0x00},
    },
    "orange": {
        "mid": {"r": 0xFF, "g": 0x7E, "b": 0x00},
        "max": {"r": 0xFF, "g": 0xFF, "b": 0xFF},
        "min": {"r": 0x0F, "g": 0x0F, "b": 0x0F},
    },
    "brightorange": {
        "mid": {"r": 0xFF, "g": 0xC6, "b": 0x00},
        "max": {"r": 0xFF, "g": 0xF7, "b": 0xE6},
        "min": {"r": 0x79, "g": 0x2A, "b": 0x00},
    },
    "black": {
        "mid": {"r": 0x5A, "g": 0x5A, "b": 0x5A},
        "max": {"r": 0xFF, "g": 0xFF, "b": 0xFF},
        "min": {"r": 0x00, "g": 0x00, "b": 0x00},
    },
    "white": {
        "mid": {"r": 0xE1, "g": 0xE1, "b": 0xE1},
        "max": {"r": 0xFF, "g": 0xFF, "b": 0xFF},
        "min": {"r": 0x1E, "g": 0x1E, "b": 0x1E},
    },
    "brown": {
        "mid": {"r": 0x94, "g": 0x50, "b": 0x27},
        "max": {"r": 0xFF, "g": 0xFF, "b": 0xFF},
        "min": {"r": 0x00, "g": 0x00, "b": 0x00},
    },
    "teal": {
        "mid": {"r": 0x30, "g": 0xCB, "b": 0xC0},
        "max": {"r": 0xFF, "g": 0xFF, "b": 0xFF},
        "min": {"r": 0x00, "g": 0x00, "b": 0x00},
    },
    "gold": {
        "mid": {"r": 0xFF, "g": 0xF3, "b": 0x5A},
        "max": {"r": 0xFF, "g": 0xF8, "b": 0xD2},
        "min": {"r": 0x99, "g": 0x4F, "b": 0x13},
    },
    "cyan": {
        "mid": {"r": 0x00, "g": 0xBE, "b": 0xBE},
        "max": {"r": 0x00, "g": 0xEE, "b": 0xEE},
        "min": {"r": 0x33, "g": 0x33, "b": 0x33},
    },
    "yellow": {
        "mid": {"r": 0xEE, "g": 0xE0, "b": 0x00},
        "max": {"r": 0xFF, "g": 0xFF, "b": 0xFF},
        "min": {"r": 0x10, "g": 0x0F, "b": 0x00},
    },
    "pink": {
        "mid": {"r": 0xFF, "g": 0xAA, "b": 0xFF},
        "max": {"r": 0xFF, "g": 0xEE, "b": 0xFF},
        "min": {"r": 0x50, "g": 0x37, "b": 0x50},
    },
}

flag_rgb = (
    (244, 154, 193),
    (63, 0, 22),
    (85, 0, 42),
    (105, 0, 57),
    (123, 0, 69),
    (140, 0, 81),
    (158, 0, 93),
    (177, 0, 105),
    (195, 0, 116),
    (214, 0, 127),
    (236, 0, 140),
    (238, 61, 150),
    (239, 91, 161),
    (241, 114, 172),
    (242, 135, 182),
    (246, 173, 205),
    (248, 193, 217),
    (250, 213, 229),
    (253, 233, 241),
)

base_red = team_colors["magenta"]["mid"]["r"]
base_green = team_colors["magenta"]["mid"]["g"]
base_blue = team_colors["magenta"]["mid"]["b"]
base_avg = (base_red + base_green + base_blue) / 3


def convert_color(color, hex=False):
    """
    Takes a dictionary containing 'r', 'g', and 'b' keys in one of various
    formats, and optionally a boolean specifying whether hexidecimal or base 10
    should be used (default is False, which implies base 10). If the keys are
    integers, they're left as-is, but if they're strings, they're converted
    into integers, using either base 10 or 16 as directed. This returns a new
    dictionary, leaving the old one unmodified. Optionally, a string may be
    given instead of a dictionary. In this case, the string is looked up in the
    internal table, and the resulting values are used. A failed table lookup
    results in an error message.
    """
    if isinstance(color, str):
        if color in team_colors:
            return team_colors[color]
        else:
            print("Couldn't find color '%s'." % color, file=sys.stderr)
            sys.exit(1)
    new = {}
    base = 16 if hex else 10
    for c in "rgb":
        if isinstance(color["mid"][c], str):
            try:
                new[c] = int(color["mid"][c], base)
            except ValueError:
                print(
                    "Couldn't convert color value %s='%s' using "
                    "base %d. Did you forget -x?" % (c, color["mid"][c], base),
                    file=sys.stderr,
                )
                sys.exit(1)
        else:
            new[c] = color["mid"][c]
        if new[c] not in range(256):
            print(
                "Value %s='%s' is out-of-range! Color values "
                "should be in the range [0, 255]." % (c, new[c]),
                file=sys.stderr,
            )
            sys.exit(1)
    return {
        "mid": new,
        "max": {"r": 0xFF, "g": 0xFF, "b": 0xFF},
        "min": {"r": 0x00, "g": 0x00, "b": 0x00},
    }


def get_convert_options(color, method):
    """
    Takes a dictionary containing 'r', 'g', and 'b' keys each with an integer
    value in the range [0, 255]. Returns a list containing all of the arguments
    to ImageMagick 'convert' necessary to teamcolor a unit to this color.
    """
    options = []

    new_red = color["mid"]["r"]
    new_green = color["mid"]["g"]
    new_blue = color["mid"]["b"]

    min_red = color["min"]["r"]
    min_green = color["min"]["g"]
    min_blue = color["min"]["b"]

    max_red = color["max"]["r"]
    max_green = color["max"]["g"]
    max_blue = color["max"]["b"]

    for old_r, old_g, old_b in flag_rgb:
        if method == "average":
            old_avg = (old_r + old_g + old_b) / 3
            reference_avg = base_avg
        elif method == "luminance":
            old_avg = rgb2lum(old_r, old_g, old_b)
            reference_avg = rgb2lum(base_red, base_green, base_blue)
        if old_avg <= reference_avg:
            old_rat = old_avg / float(reference_avg)
            new_r = int(old_rat * new_red + (1 - old_rat) * min_red)
            new_g = int(old_rat * new_green + (1 - old_rat) * min_green)
            new_b = int(old_rat * new_blue + (1 - old_rat) * min_blue)
        else:
            old_rat = (255 - old_avg) / float(255 - reference_avg)
            new_r = int(old_rat * new_red + (1 - old_rat) * max_red)
            new_g = int(old_rat * new_green + (1 - old_rat) * max_green)
            new_b = int(old_rat * new_blue + (1 - old_rat) * max_blue)

        if new_r > 255:
            new_r = 255
        if new_g > 255:
            new_g = 255
        if new_b > 255:
            new_b = 255

        options += [
            "-fill",
            "#%02x%02x%02x" % (new_r, new_g, new_b),
            "-opaque",
            "#%02x%02x%02x" % (old_r, old_g, old_b),
        ]
    return options


def colorize(
    color,
    in_file,
    out_file,
    magick=MAGICK_CMD,
    method="average",
    hex=False,
    namespace=None,
):
    if not color:
        r = 255 if namespace is None or namespace.red is None else namespace.red
        g = 0 if namespace is None or namespace.green is None else namespace.green
        b = 0 if namespace is None or namespace.blue is None else namespace.blue
        color = {
            "mid": {"r": r, "g": g, "b": b},
            "max": {"r": 0xFF, "g": 0xFF, "b": 0xFF},
            "min": {"r": 0x00, "g": 0x00, "b": 0x00},
        }

    color = convert_color(color, hex)
    options = get_convert_options(color, method)
    command = magick.split(" ") + options + [in_file, out_file]

    if namespace and namespace.verbose:
        print(" ".join(command))
    if not namespace or not namespace.dryrun:
        ret = subprocess.call(command)
        if ret != 0:
            print(
                "Error: Conversion command exited with error " "code %d." % ret,
                file=sys.stderr,
            )
        return ret
