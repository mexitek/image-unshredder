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

# Holding tank for correct order of shreds
# We always start with shred 1 in the tank
shred_ordered = [1]
# We need to know how many columns
total_shreds = imgWidth/colWidth
# Here are the left over shreds
shreds_mixed = range(2,total_shreds+1)

# New image data
unshredded = Image.new("RGBA", image.size)

# Access an arbitrary pixel. Data is stored as a 2d array where rows are
# sequential. Each element in the array is a RGBA tuple (red, green, blue,
# alpha).

def getPixelValue(x, y):
   pixel = data[y * imgWidth + x]
   return pixel

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
	print str(x1)+" & "+str(x2)+" = "+str(calculateDifference(x1,x2))

def calculateDifference(x1,x2):
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

def cropShred(shred):
	# calculate start and end points for crop of shredded image
	startXY = ((shred-1)*colWidth, 0)
	endXY = (shred*colWidth, imgHeight)
	# make the crop
	return image.crop((startXY[0], startXY[1], endXY[0], endXY[1]))
	
def placeShred(shredded_column, unshredded_column):
	# Calculate destination start point for unshredded column
	destinationXY = ((unshredded_column-1)*colWidth, 0)
	# Put the crop in it's place
	unshredded.paste(cropShred(shredded_column), destinationXY)

def saveUnshredded():
	unshredded.save(unshredded_filename, "JPEG")

def sortShreds():
	# Let's keep going till we're done
	# raising the minDiff level will ensure completion
	maxDiffLevel = 100
	while len(shreds_mixed) > 0:
		# Recursion time!
		# Add the shreds the match the right edge, of last shred in the pot, to the back
		matchShredOnRight( shred_ordered[len(shred_ordered)-1],maxDiffLevel )
		# Add the shreds the match the left edge, of last shred in the pot, to the back
		matchShredOnLeft( shred_ordered[0],maxDiffLevel )
		# We there yet?
		if(len(shreds_mixed) > 0):
			maxDiffLevel += 10
			print "Hmm, still some shreds left. Increasing maxDiff to: "+str(maxDiffLevel)
	print shred_ordered
	
def matchShredOnLeft(shredToMatch,maxDiff):
	# Get right most x coordinate
	lCol = (shredToMatch-1)*colWidth
	for shred in shreds_mixed:
		# Get left most x coordinate from unmatche shred
		rCol = shred*colWidth-1
		diff = calculateDifference(lCol,rCol)
		# check for a match
		if diff < maxDiff:
			# We have a match. Add this shred to back of ordered shreds and 
			# find the right most partner again
			shred_ordered.insert(0,shred)
			shreds_mixed.remove(shred)
			print "Matched "+str(shred)+" <- "+str(shredToMatch)+": "+str(diff)+" diff"
			# Recursion
			matchShredOnLeft(shred,maxDiff)
			return
	# All done the ones to the right
	return

		
def matchShredOnRight(shredToMatch,maxDiff):
	# Get right most x coordinate
	rCol = shredToMatch*colWidth-1
	# iterate unused shreds
	for shred in shreds_mixed:
		# Get left most x coordinate from unmatche shred
		lCol = (shred-1)*colWidth
		diff = calculateDifference(lCol,rCol)
		# check for a match
		if diff < maxDiff:
			# We have a match. Add this shred to back of ordered shreds and 
			# find the right most partner again
			shred_ordered.append(shred)
			shreds_mixed.remove(shred)
			print "Matched "+str(shredToMatch)+" -> "+str(shred)+": "+str(diff)+" diff"
			# Recursion
			matchShredOnRight(shred,maxDiff)
			return
	# All done the ones to the right
	return

def remakeUnshreddedImage():
	# Iterate through the ordered shreds and place them in new image
	for shred_index in range(1,len(shred_ordered)+1):
		placeShred( shred_ordered[shred_index-1], shred_index )
	# Now save final image
	saveUnshredded()

sortShreds()
remakeUnshreddedImage()
#print calculateDifference(192,415)