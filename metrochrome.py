#!/usr/bin/python

#
# Script: metrochrome.py
# Author: Michael Stockman
#
# Purpose: A command line based tool for exploration and manipulation of color 
# values.
#

import sys

class InvalidColorException(Exception):
    """Exception indicates inputs to a color class are out of range for the color space"""
    def __init__(self):
        self.value = "Invalid color error"
    def __str__(self):
        return repr(self.value)

class InexactColorConversionException(Exception):
    """Exception indicates color conversion required approximation to map onto new color space"""
    def __init__(self):
        self.value = "Inexact color conversion exception"
    def __str__(self):
        return repr(self.value)

class RGBColor:
    """A color represented in RGB color space by values of red green and blue"""
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue
        if self.invalid():
            raise InvalidColorException()

    def __str__(self):
        return "%i %i %i" % (self.red, self.green, self.blue)

    def parseString(self, red, green, blue):
        try:
            self.red = int(red)
            self.green = int(green)
            self.blue = int(blue)
        except:
            raise InvalidColorException()
        if self.invalid():
            raise InvalidColorException()

    def invalid(self):
        r = self.red
        g = self.green
        b = self.blue
        if r < 0 or r > 255 or g < 0 or g > 255 or b < 0 or b > 255:
            return True
        else:
            return False

class RGBHexColor:
    """A color represented in RGB color space by a single hexadecimal value"""
    def __init__(self, invalue):
        self.value = invalue
        if self.invalid():
            raise InvalidColorException()

    def __str__(self):
        return "#%0.6X" % self.value

    def parseString(self, string):
        if string.startswith("#"):
            string = string[1:]
        if len(string) != 6:
            raise InvalidColorException()
        try:
            val = int(string, 16)
        except:
            raise InvalidColorException()
        self.value = val
        if self.invalid():
            raise InvalidColorException()

    def invalid(self):
        if self.value < 0 or self.value > 16777215:
            return True
        else:
            return False

class CMYKColor:
    """A color represented in CMYK color space by four percentages between 0 and 100"""
    def __init__(self, cyan, magenta, yellow, key):
        self.cyan = cyan
        self.magenta = magenta
        self.yellow = yellow
        self.key = key
        if self.invalid():
            raise InvalidColorException()

    def __str__(self):
        return "%.1f %.1f %.1f %.1f" % (self.cyan, self.magenta, self.yellow, self.key)

    def parseString(self, cyan, magenta, yellow, key):
        try:
            self.cyan = float(cyan)
            self.magenta = float(magenta)
            self.yellow = float(yellow)
            self.key = float(key)
        except:
            raise InvalidColorException()
        if self.invalid():
            raise InvalidColorException()

    def invalid(self):
        c = self.cyan
        m = self.magenta
        y = self.yellow
        k = self.key
        if c < 0.0 or c > 100.0 or m < 0.0 or m > 100.0 or y < 0.0 or y > 100.0 or k < 0.0 or k > 100.0:
            return True
        else:
            return False

class CMYKRatioColor:
    """A color represented in CMYK color space by four ratios values between 0 and 1"""
    def __init__(self, cyan, magenta, yellow, key):
        self.cyan = cyan / 100.0
        self.magenta = magenta / 100.0
        self.yellow = yellow / 100.0
        self.key = key / 100.0
        if self.invalid():
            raise InvalidColorException()

    def __str__(self):
        return "%.3g %.3g %.3g %.3g" % (self.cyan, self.magenta, self.yellow, self.key)

    def parseString(self, cyan, magenta, yellow, key):
        try:
            self.cyan = float(cyan)
            self.magenta = float(magenta)
            self.yellow = float(yellow)
            self.key = float(key)
        except:
            raise InvalidColorException()
        if self.invalid():
            raise InvalidColorException()

    def invalid(self):
        c = self.cyan
        m = self.magenta
        y = self.yellow
        k = self.key
        if c < 0.0 or c > 1.0 or m < 0.0 or m > 1.0 or y < 0.0 or y > 1.0 or k < 0.0 or k > 1.0:
            return True
        else:
            return False

class HSVColor:
    """A color represented in HSV color space: hue, saturation, value"""
    def __init__(self, hue, saturation, value):
        self.hue = hue
        self.saturation = saturation
        self.value = value
        if self.invalid():
            raise InvalidColorException()

    def __str__(self):
        return "%.1f %.3f %.3f" % (self.hue, self.saturation, self.value)

    def parseString(self, hue, saturation, value):
        try:
            self.hue = float(hue)
            self.saturation = float(saturation)
            self.value = float(value)
        except:
            raise InvalidColorException()
        if self.invalid():
            raise InvalidColorException()

    def invalid(self):
        h = self.hue
        s = self.saturation
        v = self.value
        if h < 0.0 or h > 360.0 or s < 0.0 or s > 1.0 or v < 0.0 or v > 1.0:
            return True
        else:
            return False

class HSLColor:
    """A color represented in HSL color space: hue, saturation, lightness"""
    def __init__(self, hue, saturation, lightness):
        self.hue = hue
        self.saturation = saturation
        self.lightness = lightness
        if self.invalid():
            raise InvalidColorException()

    def __str__(self):
        return "%.1f %.3f %.3f" % (self.hue, self.saturation, self.lightness)

    def parseString(self, hue, saturation, lightness):
        try:
            self.hue = float(hue)
            self.saturation = float(saturation)
            self.lightness = float(lightness)
        except:
            raise InvalidColorException()
        if self.invalid():
            raise InvalidColorException()

    def invalid(self):
        h = self.hue
        s = self.saturation
        l = self.lightness
        if h < 0.0 or h > 360.0 or s < 0.0 or s > 1.0 or l < 0.0 or l > 1.0:
            return True
        else:
            return False

class CIEColor:
    """A color represented in CIE color space"""
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        if self.invalid():
            raise InvalidColorException()

    def __str__(self):
        return "%.3f %.3f %.3f" % (self.x, self.y, self.z)

    def parseString(self, x, y, z):
        try:
            self.x = float(x)
            self.y = float(y)
            self.z = float(z)
        except:
            raise InvalidColorException()
        if self.invalid():
            raise InvalidColorException()

    def invalid(self):
        x = self.x
        y = self.y
        z = self.z
        if x < 0.0 or x > 1.0 or y < 0.0 or y > 1.0 or z < 0.0 or z > 1.0:
            return True
        else:
            return False

class WavelengthColor:
    """A color represented as physical wavelength"""
    def __init__(self, nm):
        self.nm = nm
        if self.invalid():
            raise InvalidColorException()

    def __str__(self):
        return "%.3f" % (self.nm)

    def parseString(self, nm):
        try:
            self.nm = float(nm)
        except:
            raise InvalidColorException()
        if self.invalid():
            raise InvalidColorException()

    def invalid(self):
        nm = self.nm
        if nm < 380.0 or nm > 780.0:
            return True
        else:
            return False

class DegreeKelvinColor:
    """A color represented as a source of black body radiation at a given temperature"""
    def __init__(self, dk):
        self.dk = dk
        if self.invalid():
            raise InvalidColorException()

    def __str__(self):
        return "%.1f" % (self.dk)

    def parseString(self, dk):
        try:
            self.dk = float(dk)
        except:
            raise InvalidColorException()
        if self.invalid():
            raise InvalidColorException()

    def invalid(self):
        dk = self.dk
        if dk < 0.0:
            return True
        else:
            return False

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
    """Converts RGB colors to hexadecimal representation"""
    total = inputRgb.red*65536 + inputRgb.green*256 + inputRgb.blue
    return RGBHexColor(total)

def RGB_to_CMYK(inputRgb):
    """Converts colors in RGB color space to CMYK"""
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

    return CMYKColor(100.0*cyan, 100.0*magenta, 100.0*yellow, 100.0*key)

def RGB_to_CMYKratio(rgb):
    """Converts colors in RGB color space to CMYK with a ratio rather than percentage representation"""
    cmyk = RGB_to_CMYK(rgb)
    return CMYK_to_CMYKratio(cmyk)

def RGB_to_HSV(rgb):
    """Converts colors in RGB color space to HSV"""
    red = rgb.red / 255.0
    green = rgb.green / 255.0
    blue = rgb.blue / 255.0

    m = min(red, green, blue)
    M = max(red, green, blue)

    value = M
    chroma = M - m

    if value != 0.0:
        saturation = chroma/M
    else:
        saturation = 0.0
        hue = 0.0
        return HSVColor(hue, saturation, value)

    if chroma == 0:
        hue = 0.0
    elif red == M:
        hue = ((green - blue) / chroma) % 6
    elif green == M:
        hue = ((blue - red) / chroma) + 2
    elif blue == M:
		hue = ((red - green) / chroma) + 4;

    hue *= 60.0

    return HSVColor(hue, saturation, value)

def RGB_to_HSL(rgb):
    """Converts colors in RGB color space to HSL"""
    red = rgb.red / 255.0
    green = rgb.green / 255.0
    blue = rgb.blue / 255.0

    m = min(red, green, blue)
    M = max(red, green, blue)

    lightness = 0.5 * (M + m)
    chroma = M - m

    if lightness == 0.0 or lightness == 1.0:
        saturation = 0.0
    else:
        saturation = chroma / (1 - abs(2 * lightness - 1))

    if chroma == 0:
        hue = 0.0
    elif red == M:
        hue = ((green - blue) / chroma) % 6
    elif green == M:
        hue = ((blue - red) / chroma) + 2
    elif blue == M:
		hue = ((red - green) / chroma) + 4;

    hue *= 60.0

    return HSLColor(hue, saturation, lightness)

def RGB_to_CIE(rgb):
    return CIEColor(0.0, 0.0, 0.0)

def RGB_to_wavelength(rgb):
    return WavelengthColor(380.0)

def RGB_to_degreeKelvin(rgb):
    return DegreeKelvinColor(0.0)
 
def RGBhex_to_RGB(rgbHex):
    """Converts RGB hexadecimal representation to standard RGB"""

    initial = int(rgbHex.value)
    red = initial / 65536
    green = (initial-red*65536) / 256
    blue = (initial-red*65536-green*256)

    return RGBColor(red, green, blue)

def RGBhex_to_CMYK(rgbHex):
    """Converts RGB color space (hexadecimal representation) to CMYK"""
    rgb = RGBhex_to_RGB(rgbHex)
    return RGB_to_CMYK(rgb)

def RGBhex_to_CMYKratio(rgbHex):
    """Converts RGB color space (hexadecimal representation) to CMYK (ratio representation)"""
    rgb = RGBhex_to_RGB(rgbHex)
    return RGB_to_CMYKratio(rgb)

def RGBhex_to_HSV(rgbHex):
    """Converts RGB color space (hexadecimal representation) to HSV"""
    rgb = RGBhex_to_RGB(rgbHex)
    return RGB_to_HSV(rgb)

def RGBhex_to_HSL(rgbHex):
    """Converts RGB color space (hexadecimal representation) to HSL"""
    rgb = RGBhex_to_RGB(rgbHex)
    return RGB_to_HSL(rgb)

def RGBhex_to_CIE(rgbHex):
    """Converts RGB color space (hexadecimal representation) to CIE"""
    rgb = RGBhex_to_RGB(rgbHex)
    return RGB_to_CIE(rgb)

def CMYK_to_RGB(cmyk):
    """Converts CMYK color space to RGB"""
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

    return RGBColor(red, green, blue)

def CMYK_to_RGBhex(cmyk):
    """Converts CMYK color space to RGB (hexadecimal representation)"""
    rgb = CMYK_to_RGB(cmyk)
    return RGB_to_RGBhex(rgb)

def CMYK_to_CMYKratio(cmyk):
    """Converts CMYK color space to ratio representation"""
    return CMYKRatioColor(cmyk.cyan, cmyk.magenta, cmyk.yellow, cmyk.key)

def CMYK_to_HSV(cmyk):
    """Converts CMYK color space to HSV"""
    rgb = CMYK_to_RGB(cmyk)
    return RGB_to_HSV(rgb)

def CMYK_to_HSL(cmyk):
    """Converts CMYK color space to HSL"""
    rgb = CMYK_to_RGB(cmyk)
    return RGB_to_HSL(rgb)

def CMYK_to_CIE(cmyk):
    """Converts CMYK color space to HSL"""
    rgb = CMYK_to_RGB(cmyk)
    return RGB_to_CIE(rgb)

def CMYKratio_to_RGB(cmykr):
    """Converts CMYK color space (ratio representation) to RGB"""
    cmyk = CMYKratio_to_CMYK(cmykr)
    return CMYK_to_RGB(cmyk)

def CMYKratio_to_RGBhex(cmykr):
    """Converts CMYK color space (ratio representation) to RGB (hexadecimal representation)"""
    cmyk = CMYKratio_to_CMYK(cmykr)
    return CMYK_to_RGBhex(cmyk)

def CMYKratio_to_CMYK(cmykr):
    """Converts CMYK color space (ratio representation) to standard representation"""
    cyan = cmykr.cyan * 100.0
    magenta = cmykr.magenta * 100.0
    yellow = cmykr.yellow * 100.0
    key = cmykr.key * 100.0

    return CMYKColor(cyan, magenta, yellow, key)

def CMYKratio_to_HSV(cmykr):
    """Converts CMYK color space (ratio representation) to HSV"""
    rgb = CMYKratio_to_RGB(cmykr)
    return RGB_to_HSV(rgb)

def CMYKratio_to_HSL(cmykr):
    """Converts CMYK color space (ratio representation) to HSL"""
    rgb = CMYKratio_to_RGB(cmykr)
    return RGB_to_HSL(rgb)

def CMYKratio_to_CIE(cmykr):
    """Converts CMYK color space (ratio representation) to CIE"""
    rgb = CMYKratio_to_RGB(cmykr)
    return RGB_to_CIE(rgb)

def HSV_to_RGB(hsv):
    """Converts HSV color space to RGB"""

    hue = hsv.hue
    saturation = hsv.saturation
    value = hsv.value

    c = value * saturation
    x = c * ( 1 - abs( ((hue/60.0) % 2) - 1 ) )
    m = value - c

    if hue < 60:
        red = c
        green = x
        blue = 0
    elif hue < 120:
        red = x
        green = c
        blue = 0
    elif hue < 180:
        red = 0
        green = c
        blue = x
    elif hue < 240:
        red = 0
        green = x
        blue = c
    elif hue < 300:
        red = x
        green = 0
        blue = c
    else:
        red = c
        green = 0
        blue = x

    red = (red + m) * 255
    green = (green + m) * 255
    blue = (blue + m) * 255

    return RGBColor(red, green, blue)

def HSV_to_RGBhex(hsv):
    """Converts HSV color space to RGB (hexadecimal representation)"""
    rgb = HSV_to_RGB(hsv)
    return RGB_to_RGBhex(rgb)

def HSV_to_CMYK(hsv):
    """Converts HSV color space to CMYK"""
    rgb = HSV_to_RGB(hsv)
    return RGB_to_CMYK(rgb)

def HSV_to_CMYKratio(hsv):
    """Converts HSV color space to CMYK (ratio representation)"""
    rgb = HSV_to_RGB(hsv)
    return RGB_to_CMYKratio(rgb)

def HSV_to_HSL(hsv):
    """Converts HSV color space to HSL"""
    rgb = HSV_to_RGB(hsv)
    return RGB_to_HSL(rgb)

def HSV_to_CIE(hsv):
    """Converts HSV color space to CIE"""
    rgb = HSV_to_RGB(hsv)
    return RGB_to_CIE(rgb)

def HSL_to_RGB(hsl):
    """Converts HSL color space to RGB"""

    hue = hsl.hue
    saturation = hsl.saturation
    lightness = hsl.lightness

    c = (1 - abs(2*lightness - 1)) * saturation
    x = c * ( 1 - abs( ((hue/60.0) % 2) - 1 ) )
    m = lightness - (c/2)

    if hue < 60:
        red = c
        green = x
        blue = 0
    elif hue < 120:
        red = x
        green = c
        blue = 0
    elif hue < 180:
        red = 0
        green = c
        blue = x
    elif hue < 240:
        red = 0
        green = x
        blue = c
    elif hue < 300:
        red = x
        green = 0
        blue = c
    else:
        red = c
        green = 0
        blue = x

    red = (red + m) * 255
    green = (green + m) * 255
    blue = (blue + m) * 255

    return RGBColor(red, green, blue)

def HSL_to_RGBhex(hsl):
    """Converts HSL color space to RGB (hexadecimal representation)"""
    rgb = HSL_to_RGB(hsl)
    return RGB_to_RGBhex(rgb)

def HSL_to_CMYK(hsl):
    """Converts HSL color space to CMYK"""
    rgb = HSL_to_RGB(hsl)
    return RGB_to_CMYK(rgb)

def HSL_to_CMYKratio(hsl):
    """Converts HSL color space to CMYK (ratio representation)"""
    rgb = HSL_to_RGB(hsl)
    return RGB_to_CMYKratio(rgb)

def HSL_to_HSV(hsl):
    """Converts HSL color space to HSV"""
    rgb = HSL_to_RGB(hsl)
    return RGB_to_HSV(rgb)

def HSL_to_CIE(hsl):
    """Converts HSL color space to CIE"""
    rgb = HSL_to_RGB(hsl)
    return RGB_to_CIE(rgb)

def CIE_to_RGB(cie):
    """Converts CIE color space to RGB"""
    return RGBColor(0, 0, 0)

def CIE_to_RGBhex(cie):
    """Converts CIE color space to RGB (hexadecimal representation)"""
    rgb = CIE_to_RGB(cie)
    return RGB_to_RGBhex(rgb)

def CIE_to_CMYK(cie):
    """Converts HSL color space to CMYK"""
    rgb = CIE_to_RGB(cie)
    return RGB_to_CMYK(rgb)

def CIE_to_CMYKratio(cie):
    """Converts CIE color space to CMYK (ratio representation)"""
    rgb = CIE_to_RGB(cie)
    return RGB_to_CMYKratio(rgb)

def CIE_to_HSV(cie):
    """Converts CIE color space to HSV"""
    rgb = CIE_to_RGB(cie)
    return RGB_to_HSV(rgb)

def CIE_to_HSL(cie):
    """Converts CIE color space to HSL"""
    rgb = CIE_to_RGB(cie)
    return RGB_to_HSL(rgb)

def main():

    if len(sys.argv) == 2 and (sys.argv[1] == "-h" or sys.argv[1] == "-help"):
        printHelp()

    elif len(sys.argv) == 6 and sys.argv[1] == "-rgb":
        try:
            rgb = RGBColor(0,0,0)
            rgb.parseString(sys.argv[2], sys.argv[3], sys.argv[4])
        except InvalidColorException:
            exitWithError()

        if sys.argv[5] == "-rgb":
            print(rgb)
        elif sys.argv[5] == "-rgbh":
            print(RGB_to_RGBhex(rgb))
        elif sys.argv[5] == "-cmyk":
            print(RGB_to_CMYK(rgb))
        elif sys.argv[5] == "-cmykr":
            print(RGB_to_CMYKratio(rgb))
        elif sys.argv[5] == "-hsv":
            print(RGB_to_HSV(rgb))
        elif sys.argv[5] == "-hsl":
            print(RGB_to_HSL(rgb))
        elif sys.argv[5] == "-cie":
            print(RGB_to_CIE(rgb))
        elif sys.argv[5] == "-wave":
            print(RGB_to_wavelength(rgb))
        elif sys.argv[5] == "-kelvin":
            print(RGB_to_degreeKelvin(rgb))

        else:
            exitWithError()

    elif len(sys.argv) == 4 and sys.argv[1] == "-rgbh":
        try:
            rgbHex = RGBHexColor(0)
            rgbHex.parseString(sys.argv[2])
        except InvalidColorException:
            exitWithError()

        if sys.argv[3] == "-rgb":
            print(RGBhex_to_RGB(rgbHex))
        elif sys.argv[3] == "-rgbh":
            print(rgbHex)
        elif sys.argv[3] == "-cmyk":
            print(RGBhex_to_CMYK(rgbHex))
        elif sys.argv[3] == "-cmykr":
            print(RGBhex_to_CMYKratio(rgbHex))
        elif sys.argv[3] == "-hsv":
            print(RGBhex_to_HSV(rgbHex))
        elif sys.argv[3] == "-hsl":
            print(RGBhex_to_HSL(rgbHex))
        elif sys.argv[3] == "-cie":
            print(RGBhex_to_CIE(rgbHex))
        else:
            exitWithError()

    elif len(sys.argv) == 7 and sys.argv[1] == "-cmyk":
        try:
            cmyk = CMYKColor(0,0,0,0)
            cmyk.parseString(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
        except InvalidColorException:
            exitWithError()

        if sys.argv[6] == "-rgb":
            print(CMYK_to_RGB(cmyk))
        elif sys.argv[6] == "-rgbh":
            print(CMYK_to_RGBhex(cmyk))
        elif sys.argv[6] == "-cmyk":
            print(cmyk)
        elif sys.argv[6] == "-cmykr":
            print(CMYK_to_CMYKratio(cmyk))
        elif sys.argv[6] == "-hsv":
            print(CMYK_to_HSV(cmyk))
        elif sys.argv[6] == "-hsl":
            print(CMYK_to_HSL(cmyk))
        elif sys.argv[6] == "-cie":
            print(CMYK_to_CIE(cmyk))
        else:
            exitWithError()

    elif len(sys.argv) == 7 and sys.argv[1] == "-cmykr":
        try:
            cmykr = CMYKRatioColor(0,0,0,0)
            cmykr.parseString(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
        except InvalidColorException:
            exitWithError()

        if sys.argv[6] == "-rgb":
            print(CMYKratio_to_RGB(cmykr))
        elif sys.argv[6] == "-rgbh":
            print(CMYKratio_to_RGBhex(cmykr))
        elif sys.argv[6] == "-cmyk":
            print(CMYKratio_to_CMYK(cmykr))
        elif sys.argv[6] == "-cmykr":
            print(cmykr)
        elif sys.argv[6] == "-hsv":
            print(CMYKratio_to_HSV(cmykr))
        elif sys.argv[6] == "-hsl":
            print(CMYKratio_to_HSL(cmykr))
        elif sys.argv[6] == "-cie":
            print(CMYKratio_to_CIE(cmykr))
        else:
            exitWithError()

    elif len(sys.argv) == 6 and sys.argv[1] == "-hsv":
        try:
            hsv = HSVColor(0,0,0)
            hsv.parseString(sys.argv[2], sys.argv[3], sys.argv[4])
        except InvalidColorException:
            exitWithError()

        if sys.argv[5] == "-rgb":
            print(HSV_to_RGB(hsv))
        elif sys.argv[5] == "-rgbh":
            print(HSV_to_RGBhex(hsv))
        elif sys.argv[5] == "-cmyk":
            print(HSV_to_CMYK(hsv))
        elif sys.argv[5] == "-cmykr":
            print(HSV_to_CMYKratio(hsv))
        elif sys.argv[5] == "-hsv":
            print(hsv)
        elif sys.argv[5] == "-hsl":
            print(HSV_to_HSL(hsv))
        elif sys.argv[5] == "-cie":
            print(HSV_to_CIE(hsv))
        else:
            exitWithError()

    elif len(sys.argv) == 6 and sys.argv[1] == "-hsl":
        try:
            hsl = HSLColor(0,0,0)
            hsl.parseString(sys.argv[2], sys.argv[3], sys.argv[4])
        except InvalidColorException:
            exitWithError()

        if sys.argv[5] == "-rgb":
            print(HSL_to_RGB(hsl))
        elif sys.argv[5] == "-rgbh":
            print(HSL_to_RGBhex(hsl))
        elif sys.argv[5] == "-cmyk":
            print(HSL_to_CMYK(hsl))
        elif sys.argv[5] == "-cmykr":
            print(HSL_to_CMYKratio(hsl))
        elif sys.argv[5] == "-hsv":
            print(HSL_to_HSV(hsl))
        elif sys.argv[5] == "-hsl":
            print(hsl)
        elif sys.argv[5] == "-cie":
            print(HSL_to_CIE(hsl))
        else:
            exitWithError()

    elif len(sys.argv) == 6 and sys.argv[1] == "-cie":
        try:
            cie = CIEColor(0,0,0)
            cie.parseString(sys.argv[2], sys.argv[3], sys.argv[4])
        except InvalidColorException:
            exitWithError()

        if sys.argv[5] == "-rgb":
            print(CIE_to_RGB(cie))
        elif sys.argv[5] == "-rgbh":
            print(CIE_to_RGBhex(cie))
        elif sys.argv[5] == "-cmyk":
            print(CIE_to_CMYK(cie))
        elif sys.argv[5] == "-cmykr":
            print(CIE_to_CMYKratio(cie))
        elif sys.argv[5] == "-hsv":
            print(CIE_to_HSV(cie))
        elif sys.argv[5] == "-hsl":
            print(CIE_to_HSL(cie))
        elif sys.argv[5] == "-cie":
            print(cie)
        else:
            exitWithError()

    else:
        exitWithError()

if __name__ == "__main__":
    main()
