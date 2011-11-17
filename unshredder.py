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
shredded_filename = 'tokyo-shredded.png'
unshredded_filename = 'unshredded.jpg'

# Image data
image = Image.open(shredded_filename)
data = image.getdata() # This gets pixel data
imgWidth,imgHeight = image.size

# New image data
unshredded = Image.new("RGBA", image.size)

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

def getPixelColumnLine(x):
	# Create array that will hold column data
	colData = []
	# Iterate through all pixels
	y=0
	while y < imgHeight:
		colData.append(getPixelValue(x,y))
		y += 1
	# Return the collection
	return colData

def getPixelColumnRGBLists(x):
	# get all pixels in the column
	columns = getPixelColumnLine(x)
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

def cropColumn(col):
	# calculate start and end points for crop of shredded image
	startXY = ((col-1)*colWidth, 0)
	endXY = (col*colWidth, imgHeight)
	# make the crop
	return image.crop((startXY[0], startXY[1], endXY[0], endXY[1]))
	
def placeColumn(shredded_column, unshredded_column):
	# Calculate destination start point for unshredded column
	destinationXY = ((unshredded_column-1)*colWidth, 0)
	# Put the crop in it's place
	unshredded.paste(cropColumn(shredded_column), destinationXY)

def saveUnshredded():
	unshredded.save(unshredded_filename, "JPEG")

"""
# This arranges the correct columns in the correct order	
placeColumn(9,1)
placeColumn(11,2)
placeColumn(15,3)
placeColumn(17,4)
placeColumn(19,5)
placeColumn(14,6)
placeColumn(8,7)
placeColumn(4,8)
placeColumn(3,9)
placeColumn(12,10)
placeColumn(5,11)
placeColumn(20,12)
placeColumn(18,13)
placeColumn(13,14)
placeColumn(7,15)
placeColumn(16,16)
placeColumn(2,17)
placeColumn(6,18)
placeColumn(1,19)
placeColumn(10,20)
saveUnshredded();
"""
