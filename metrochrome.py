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

class CmykValue:
    """A CMYK value as a float 0 through 100"""
    def __init__(self, inValue):
        if isinstance(inValue, float):
            self.value = inValue
        elif isinstance(inValue, str) and inValue.isdigit():
            self.value = float(inValue)
        else:
            raise InvalidColorError()

        if self.value < 0.0 or self.value > 100.0:
            raise InvalidColorError()

class RgbColor:
    """A color represented in RGB color space by values of red green and blue"""
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue
        if self.invalid():
            raise InvalidColorError()

    def __str__(self):
        return "%i %i %i" % (self.red, self.green, self.blue)

    def parseString(self, red, green, blue):
        try:
            self.red = int(red)
            self.green = int(green)
            self.blue = int(blue)
        except:
            raise InvalidColorError()
        if self.invalid():
            raise InvalidColorError()

    def invalid(self):
        r = self.red
        g = self.green
        b = self.blue
        if r < 0 or r > 255 or g < 0 or g > 255 or b < 0 or b > 255:
            return True
        else:
            return False

class RgbHexColor:
    def __init__(self, invalue):
        self.value = invalue
        if self.invalid():
            raise InvalidColorError()

    def __str__(self):
        return "#%0.6X" % self.value

    def parseString(self, string):
        if string.startswith("#"):
            string = string[1:]
        if len(string) != 6:
            raise InvalidColorError()
        try:
            val = int(string, 16)
        except:
            raise InvalidColorError()
        self.value = val
        if self.invalid():
            raise InvalidColorError()

    def invalid(self):
        if self.value < 0 or self.value > 16777215:
            return True
        else:
            return False

class CmykColor:
    def __init__(self, cyan, magenta, yellow, key):
        self.cyan = CmykValue(cyan).value
        self.magenta = CmykValue(magenta).value
        self.yellow = CmykValue(yellow).value
        self.key = CmykValue(key).value

    def __str__(self):
        return "%.1f %.1f %.1f %.1f" % (self.cyan, self.magenta, self.yellow, self.key)

class CmykRatioColor:
    def __init__(self, cyan, magenta, yellow, key):
        # *** Should be more complex eventually
        self.cyan = cyan
        self.magenta = magenta
        self.yellow = yellow
        self.key = key

    def __str__(self):
        return "%.3g %.3g %.3g %.3g" % (self.cyan, self.magenta, self.yellow, self.key)

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
    -cmyk = CMYK color space 4 space separated percentages from 0 to 100 such as 0 100 95.5 82.7
    -cmykr = CMYK in percent format 4 space separated ratio values 0 to 1 such as 0 1 0.955 0.827

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

    return CmykColor(100.0*cyan, 100.0*magenta, 100.0*yellow, 100.0*key)

def RGB_to_CMYKpercent(red, green, blue):
    return "RGB_to_CMYKpercent(): not implimented yet"
 
def RGBhex_to_RGB(rgbHex):

    initial = int(rgbHex.value)
    red = initial / 65536
    green = (initial-red*65536) / 256
    blue = (initial-red*65536-green*256)

    return RgbColor(red, green, blue)

def RGBhex_to_CMYK():
    return "RGBhex_to_CMYK(): not implimented yet"

def CMYK_to_RGB(cmyk):
    cyanDiv = cmyk.cyan / 100.0
    magentaDiv = cmyk.magenta / 100.0
    yellowDiv = cmyk.yellow / 100.0
    keyDiv = cmyk.key / 100.0

    redRatio = -1 * ((cyanDiv * (1.0 - keyDiv)) - (1.0 - keyDiv))
    greenRatio = -1 * ((magentaDiv * (1.0 - keyDiv)) - (1.0 - keyDiv))
    blueRatio = -1 * ((yellowDiv * (1.0 - keyDiv)) - (1.0 - keyDiv))

    red = int(redRatio * 255)
    green = int(greenRatio * 255)
    blue = int(blueRatio * 255)

    return RgbColor(red, green, blue)

def CMYK_to_RGBhex(cmyk):
    return "CMYK_to_RGBhex(): not implimented yet"

def main():

    #print("argv: " + str(sys.argv))

    if len(sys.argv) == 2 and (sys.argv[1] == "-h" or sys.argv[1] == "-help"):
        printHelp()

    elif len(sys.argv) == 6 and sys.argv[1] == "-rgb":
        try:
            rgb = RgbColor(0,0,0)
            print(rgb)
            rgb.parseString(sys.argv[2], sys.argv[3], sys.argv[4])
            print(rgb)
        except InvalidColorError:
            exitWithError()

        if sys.argv[5] == "-rgbh":
            print(RGB_to_RGBhex(rgb))
        elif sys.argv[5] == "-cmyk":
            print(RGB_to_CMYK(rgb))
        else:
            exitWithError()
    elif len(sys.argv) == 4 and sys.argv[1] == "-rgbh":
        try:
            rgbHex = RgbHexColor(0)
            print(rgbHex)
            rgbHex.parseString(sys.argv[2])
            print(rgbHex)

        except InvalidColorError:
            exitWithError()

        if sys.argv[3] == "-rgb":
            print(RGBhex_to_RGB(rgbHex))
        elif sys.argv[3] == "-cmyk":
            print(RGBhex_to_CMYK())
        else:
            exitWithError()
    elif len(sys.argv) == 7 and sys.argv[1] == "-cmyk":
        try:
            cmyk = CmykColor(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
        except InvalidColorError:
            exitWithError()

        if sys.argv[6] == "-rgb":
            print(CMYK_to_RGB(cmyk))
        elif sys.argv[6] == "-rgbh":
            print(CMYK_to_RGBhex(cmyk))
        else:
            exitWithError()
    else:
        exitWithError()

if __name__ == "__main__":
    main()
