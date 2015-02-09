#!/usr/bin/python

#
# Script: metrochrome.py
# Author: Michael Stockman
#
# Purpose: A command line based tool for exploration and manipulation of color 
# values.
#

import sys

class InvalidColorError(Exception):
    def __init__(self):
        self.value = "Invalid color error"
    def __str__(self):
        return repr(self.value)

class RgbValue:
    """A red, green, or blue value as an integer 0 through 255"""
    def __init__(self, inValue):
        if isinstance(inValue, int):
            self.value = inValue
        elif isinstance(inValue, str) and inValue.isdigit():
            self.value = int(inValue)
        else:
            raise InvalidColorError()

        if self.value < 0 or self.value > 255:
            raise InvalidColorError()

class RgbColor:
    """A color represented in RGB color space by RgbValues of red green and blue"""
    def __init__(self, red, green, blue):
        self.red = RgbValue(red).value
        self.green = RgbValue(green).value
        self.blue = RgbValue(blue).value
    def __str__(self):
        return "%i %i %i" % (self.red, self.green, self.blue)

class RgbHexColor:
    def __init__(self, value):
        # *** Should be more complex eventually
        self.value = value
    def __str__(self):
        return "#%0.6X" % self.value

class CmykColor:
    def __init__(self, cyan, magenta, yellow, key):
        # *** Should be more complex eventually
        self.cyan = cyan
        self.magenta = magenta
        self.yellow = yellow
        self.key = key
    def __str__(self):
        return "(%.3g, %.3g, %.3g, %.3g)" % (self.cyan, self.magenta, self.yellow, self.key)

def printHelp():
    print("""
metrochrome.py - a command line tool for exploring color

++ Convert color representations from one color space to another: RGB, RGB (hexadecimal), CMYK, etc.
++ Find variations on a color tint, hue, shade 

    Usage Options 
--------------------------------

* Display this help screen *
    metrochrome.py -help   OR   metrochrome.py -h

* Convert color space *
    metrochrome.py <in_color_space> <in_color> <out_color_space>

    color space flags:
    -rgb = RGB color space written as three numbers 0-255 separted by spaces
    -rgbh = RGB in hexadecimal format with a leading hash mark (e.g. #00FF30)
    -cmyk = CMYK color space 4 comma separated ratio values 0 to 1 written between parenthesis such as (0, 1, 0.955, 0.827)
    -cmykp = CMYK in percent format 4 space separated percent values 0 to 100 such as 0 100 95.5 82.7

    examples:
    metrochrome.py -rgb 0 0 0 -cmyk        # converts RGB to CMYK and prints (0, 0, 0, 1)
    metrochrome.py -rgb 255 255 255 -rgbh  # converts RGB to hexadecimal and prints #FFFFFF
    metrochrome.py -cmyk (0, 1, 0.955, 0.827) -rgb  # converts CMYK to RGB and prints #FFFFFF
""")

def exitWithError():
    """If the inputs are unusable explain how to print the help screen"""
    print("Unusable parameters...\nRun 'python metrochrome.py -help' to display the help screen.")
    sys.exit(1)

def RGB_to_RGBhex(inputRgb):
    total = inputRgb.red*65536 + inputRgb.green*256 + inputRgb.blue
    return RgbHexColor(total)

def RGB_to_CMYK(inputRgb):
    redRatio = inputRgb.red / 255.0
    greenRatio = inputRgb.green / 255.0
    blueRatio = inputRgb.blue / 255.0

    key = 1.0 - max(redRatio, greenRatio, blueRatio)

    if key == 1.0:
        cyan = 0.0
        magenta = 0.0
        yellow = 0.0
    else:
        cyan = (1.0 - redRatio - key) / (1.0 - key)
        magenta = (1.0 - greenRatio - key) / (1.0 - key)
        yellow = (1.0 - blueRatio - key) / (1.0 - key)

    return CmykColor(cyan, magenta, yellow, key)

def RGB_to_CMYKpercent(red, green, blue):
    return "RGB_to_CMYKpercent(): not implimented yet"
 
def RGBhex_to_RGB():
    return "RGBhex_to_RGB(): not implimented yet"

def RGBhex_to_CMYK():
    return "RGBhex_to_CMYK(): not implimented yet"

def CMYK_to_RGB():
    return "CMYK_to_RGB(): not implimented yet"

def CMYK_to_RGBhex():
    return "CMYK_to_RGBhex(): not implimented yet"

def main():

    #print("argv: " + str(sys.argv))

    if len(sys.argv) == 2 and (sys.argv[1] == "-h" or sys.argv[1] == "-help"):
        printHelp()

    elif len(sys.argv) == 6 and sys.argv[1] == "-rgb":
        try:
            rgb = RgbColor(sys.argv[2], sys.argv[3], sys.argv[4])
        except InvalidColorError:
            exitWithError()

        if sys.argv[5] == "-rgbh":
            print(RGB_to_RGBhex(rgb))
        elif sys.argv[5] == "-cmyk":
            print(RGB_to_CMYK(rgb))
        else:
            exitWithError()
    else:
        exitWithError()

if __name__ == "__main__":
    main()
