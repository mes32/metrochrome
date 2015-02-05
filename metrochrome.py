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
    print("metrochrome.py")
    print("-- Unrecognized inputs. Type 'metrochrome.py -h' for help.")

def main():

    print(sys.argv)

    if len(sys.argv) >= 2 and (sys.argv[1] == "-h" or sys.argv[1] == "-help"):
        printHelp()
    else:
        printUnrec()

if __name__ == "__main__":
    main()
