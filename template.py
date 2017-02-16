#!/usr/bin/python3

#This is the code that runs the vision on the tegra board

import cv2
from Pipeline import Pipeline
import numpy as np
import logging
import time
import math
from networktables import NetworkTable

#Sets up the network table with the name table at the address address and returns an instance of it
def setupNetworkTable(table, address):
	# To see messages from networktables, you must setup logging
	logging.basicConfig(level=logging.DEBUG)
	NetworkTable.setIPAddress(address)
	NetworkTable.setClientMode()
	NetworkTable.initialize()
	return NetworkTable.getTable(table)

#Returns the list of contours
def getContours(camera, pipeline):
	frame = camera.read()
	pipeline.set_source0(np.asarray(frame[1]))
	pipeline.process()
	ret = None
	frame = None
	if(len(pipeline.filter_contours_output) > 0):
		return pipeline.filter_contours_output
	else:
		return None

#return true if the contour matches the paramters for being a high goal target
def scoreGoal(cont):
	return 5

#returns true if the contour matches the parameters for being a hook target
def scoreHook(cont):
	return 5

def main():

	shootCamera = True
	sd.putBoolean("boilerCamera", True);
	sd = setupNetworkTable("visionTable", "10.26.82.101")

	topCamera = cv2.VideoCapture(0)
	bottomCamera = cv2.VideoCapture(1);
	#This calls the shell commands that turn off auto exposure, and manually set the exposure
	e = Pipeline()
	thresh = 0.2

	while(True):
		shootCamera = sd.getBoolean("boilerCamera", True);
		#Eventually this code will need to access a network table value to determine which vision program to run
		if(shootCamera):
			conts = getContours(topCamera, e)
			if conts != None
				boilerBands = [None, None]
				scores = []


				for i in conts:
					scores.append(scoreGoal(i))

				for i in range(0,len(scores)-1):
					if scores[i] < thresh:
						del conts[i]
						del scores[i]

				firstBandI = scores.index(max(scores))
				boilerBands[0] = conts[firstBandI]
				del scores[firstBandI]
				del conts[firstBandI]

				secondBandI = scores.index(max(scores))
				boilerBands.append[conts[secondBandI]]

				#a = conts[0]
				#b = cv2.moments(e.filter_contours_output[0])
				#cx = int(b['m10']/b['m00'])
				#cy = int(b['m01']/b['m00'])
				#area = cv2.contourArea(a)
				#perimiter = cv2.arcLength(a, True)
				#epsilon = 0.1*cv2.arcLength(a, True)
				#approx = cv2.approxPolyDP(a,epsilon,True)
				#hull = cv2.convexHull(a)

				x1,y1,w1,h1,x2,y2,w2,h2 = -1,-1,-1,-1,-1,-1,-1,-1

				if boilerBands[0] != None:
					x1,y1,w1,h1 = cv2.boundingRect(boilerBands[0])
				if boilerBands[1] != None:
					x2,y2,w2,h2 = cv2.boundingRect(boilerBands[1])

				if y1 != -1 and y2 != -1:
					deltaY = abs(y2-y1)
				else:
					deltaY = -1

				xAvg = (x1+x2)/2
				yAvg = (y1+y2)/2




				# print(hull)
				# print(approx)
				# print(cx)
				# print(cy)
				'''
				print("--------------------------")
				print(x)
				sd.putNumber("boundRectX" , x )
				print(y)
				sd.putNumber("boundRectY" , y )
				print(w)
				sd.putNumber("boundRectW", w)
				sd.putNumber("FreshFrame", 1)
				sd.putNumber("boundRectH", h1)
				print("--------------------------")
				'''
				sd.putBoolean("freshFrame",True)
			else:
				sd.putBoolean("freshFrame",False)

		else:
            conts = getContours(bottomCamera, e)
			if(conts != None):
				sd.putBoolean("freshFrame",True)
			else:
				sd.putBoolean("freshFrame",False)




	print("Code Has finished")
	NetworkTable.shutdown()

if __name__ == '__main__':
    main()


'''
	print("Are we connected? ")
	print(NetworkTable.isConnected())
	print("Are we a server ? ")
	print(NetworkTable.isServer())
	print("Is there a robot key?")
	print(sd.containsKey("Robot"))
'''
