#!/usr/bin/python

#
# Script: metrochrome.py
# Author: Michael Stockman
#
# Purpose: A command line based tool for exploration and manipulation of color 
# values.
#

import sys

def printHelp():
    print("Printing help...")

def printUnrec():
    print("Ambiguous input... Run 'python metrochrome.py -help' to display help.")

def RGB_to_RGBhex(red, green, blue):
    total = red*65536 + green*256 + blue
    #return "#" + str(hex(total))
    return str(hex(total))

def RGB_to_CMYK(red, green, blue):
    redRatio = red / 255.0
    greenRatio = green / 255.0
    blueRatio = blue / 255.0

    key = 1.0 - max(redRatio, greenRatio, blueRatio)

    if key == 1.0:
        cyan = 0.0
        magenta = 0.0
        yellow = 0.0
    else:
        cyan = (1.0 - redRatio - key) / (1.0 - key)
        magenta = (1.0 - greenRatio - key) / (1.0 - key)
        yellow = (1.0 - blueRatio - key) / (1.0 - key)

    return "(%.3g, %.3g, %.3g, %.3g)" % (cyan, magenta, yellow, key)

def RGB_to_CMYKpercent(red, green, blue):
    return "RGB_to_CMYKpercent(): not implimented yet
 
def RGBhex_to_RGB():
    return "RGBhex_to_RGB(): not implimented yet"

def RGBhex_to_CMYK():
    return "RGBhex_to_CMYK(): not implimented yet"

def CMYK_to_RGB():
    return "CMYK_to_RGB(): not implimented yet"

def CMYK_to_RGBhex():
    return "CMYK_to_RGBhex(): not implimented yet"

def main():

    print("argv: " + str(sys.argv))

    if len(sys.argv) == 2 and (sys.argv[1] == "-h" or sys.argv[1] == "-help"):
        printHelp()

    if len(sys.argv) == 6 and sys.argv[1] == "-rgb":
        if sys.argv[2].isdigit() and sys.argv[3].isdigit() and sys.argv[4].isdigit():
            red = int(sys.argv[2])
            green = int(sys.argv[3])
            blue = int(sys.argv[4])

            # *** Temporary error checking should be handled as a class
            if red > 255:
                red = 255
            if red < 0:
                red = 0
            if green > 255:
                green = 255
            if green < 0:
                green = 0
            if blue > 255:
                blue = 255
            if blue < 0:
                blue = 0

            if sys.argv[5] == "-rgbh":
                print(RGB_to_RGBhex(red, green, blue))
            elif sys.argv[5] == "-cmyk":
                print(RGB_to_CMYK(red, green, blue))
            else:
                printUnrec()
        else:
            printUnrec()
    #else:
    #    printUnrec()

if __name__ == "__main__":
    main()
