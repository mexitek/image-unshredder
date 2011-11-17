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

def getPixelColumnRGBAvgs(x):
	# Get the column pixel collection
	rgbLists = getPixelColumnRGBLists(x)
	return (sum(rgbLists[0])/imgHeight),(sum(rgbLists[1])/imgHeight),(sum(rgbLists[2])/imgHeight)
	

def printPixelColumnAverage(x):
	rgbAvgs = getPixelColumnRGBAvgs(x)
	rgbSum = (rgbAvgs[0]+rgbAvgs[1]+rgbAvgs[2])
	# print average rgb for column
	print str(x)+" -> ["+str(rgbAvgs[0])+","+str(rgbAvgs[1])+","+str(rgbAvgs[2])+"] = "+str(rgbSum)+"/3 = "+str(rgbSum/3)

def getColumnEdges(col):
	L_rgbAvgs = getPixelColumnRGBAvgs((col-1)*colWidth)
	L_rgbSum = (L_rgbAvgs[0]+L_rgbAvgs[1]+L_rgbAvgs[2])
	R_rgbAvgs = getPixelColumnRGBAvgs(col*colWidth-1)
	R_rgbSum = (R_rgbAvgs[0]+R_rgbAvgs[1]+R_rgbAvgs[2])
	return ( L_rgbSum/3,R_rgbSum/3 )

def printColumnEdges(col):
	edges = getColumnEdges(col)
	print str(col)+" Left: "+str(edges[0])
	print str(col)+" Right: "+str(edges[1])

def printColumnDiff(x1,x2):
	print str(x1)+" & "+str(x2)+" = "+str(calculate_difference(x1,x2))

def calculate_difference(x1,x2):
	from math import sqrt
	# Get our pixel column
	col1 = getPixelColumnLine(x1)
	col2 = getPixelColumnLine(x2)
	# start the diff calculation
	sum_squared_differences = 0.0
	pixel = 0
	while pixel < imgHeight:
		for channel in [0, 1, 2]:
	            pixel_one = col1[pixel][channel]
	            pixel_two = col2[pixel][channel]
	            diff_squared = (pixel_one-pixel_two)*(pixel_one-pixel_two)
	            sum_squared_differences += diff_squared
		pixel += 1
	return sqrt(sum_squared_differences/imgHeight)

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
"""
# This gives the pixel average for a single pixel column
# Will be used to match up column edges
printPixelColumnAverage(28)
printPixelColumnAverage(29)
printPixelColumnAverage(30)
printPixelColumnAverage(31)
printPixelColumnAverage(32)
printPixelColumnAverage(33)
printPixelColumnAverage(34)
"""

""" 
# This will show column edges (L,R)
# We can visually see what AI will encounter
printColumnEdges(1)
printColumnEdges(2)
printColumnEdges(3)
printColumnEdges(4)
printColumnEdges(5)
printColumnEdges(6)
printColumnEdges(7)
printColumnEdges(8)
printColumnEdges(9)
printColumnEdges(10)
printColumnEdges(11)
printColumnEdges(12)
printColumnEdges(13)
printColumnEdges(14)
printColumnEdges(15)
printColumnEdges(16)
printColumnEdges(17)
printColumnEdges(18)
printColumnEdges(19)
printColumnEdges(20)
"""

# Testing Euclidean Distance for pixel column distance
print "Testing Edge of Column 1R (31) with 2L (32)"
printColumnDiff(29,30)
printColumnDiff(30,31)
printColumnDiff(31,32)
printColumnDiff(32,33)
printColumnDiff(33,34)
print "Testing Edge of Column 2R (63) with 3L (64)"
printColumnDiff(61,62)
printColumnDiff(62,63)
printColumnDiff(63,64)
printColumnDiff(64,65)
printColumnDiff(65,66)
print "Testing Edge of Column 3R (95) with 4L (96)"
printColumnDiff(93,94)
printColumnDiff(94,95)
printColumnDiff(95,96)
printColumnDiff(96,97)
printColumnDiff(97,98)