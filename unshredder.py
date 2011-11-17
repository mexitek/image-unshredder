#!/usr/bin/env python
# encoding: utf-8
"""
unshredder.py

Created by Arlo Carreon on 2011-11-14.
License: arlo.mit-license.org
"""

import sys
import os
import math
import Image

# ASSUMPTIONS -----
colWidth = 32

# Image data
image = Image.open('tokyo-shredded.png')
data = image.getdata() # This gets pixel data
imgWidth,imgHeight = image.size


# Access an arbitrary pixel. Data is stored as a 2d array where rows are
# sequential. Each element in the array is a RGBA tuple (red, green, blue,
# alpha).

def getPixelValue(x, y):
   pixel = data[y * imgWidth + x]
   return pixel

"""def print_pixel_lineHorizontal(y, startx, finishx):
	while startx <= finishx:
		print str(startx) + ": " + str(get_pixel_value(y, startx))
		startx = startx + 1;
"""

def getPixelColumn(x):
	# Create array that will hold column data
	colData = []
	# Iterate through all pixels
	y=0
	while y < imgHeight:
		colData.append(getPixelValue(y,x))
		y += 1
	# Return the collection
	return colData

def getPixelColumnRGBLists(x):
	# get all pixels in the column
	columns = getPixelColumn(x)
	# Iterate and seperate into individual lists
	r,g,b = [],[],[]
	for col in columns:
		r.append(col[0])
		g.append(col[1])
		b.append(col[2])
	# Return list of rgb lists
	return (r,g,b)
	
def printPixelColumnAverage(x):
	# Get the column pixel collection
	rgbLists = getPixelColumnRGBLists(x)
	avgR,avgG,avgB = (sum(rgbLists[0])/imgHeight),(sum(rgbLists[1])/imgHeight),(sum(rgbLists[2])/imgHeight)
	rgbSum = (avgR+avgG+avgB)
	# print average rgb for column
	print str(x)+" -> ["+str(avgR)+","+str(avgG)+","+str(avgB)+"] = "+str(rgbSum)+"/3 = "+str(rgbSum/3)


printPixelColumnAverage(26)
printPixelColumnAverage(27)
printPixelColumnAverage(28)
printPixelColumnAverage(29)
printPixelColumnAverage(30)
printPixelColumnAverage(31)
printPixelColumnAverage(32)
printPixelColumnAverage(33)
printPixelColumnAverage(34)
printPixelColumnAverage(35)
printPixelColumnAverage(36)
