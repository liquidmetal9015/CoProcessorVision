#!/usr/bin/python3

#This is the code that runs the vision on the tegra board

import cv2
from Pipeline import Pipeline
import numpy as np
import logging
import time
from networktables import NetworkTable



#This is where I will move the processing and network tables to once I get my shit together
def extra_processing(pipe):
	print("I like to eat hats on tuesdays")

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
	#extra_processing(pipeline)
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

#def lookForGoal(contList)

def main():

	shootCamera = True
	sd.putBoolean("boilerCamera", True);
	sd = setupNetworkTable("visionTable", "10.26.82.101")

	topCamera = cv2.VideoCapture(0)
	bottomCamera = cv2.VideoCapture(1);
	#This calls the shell commands that turn off auto exposure, and manually set the exposure
	e = Pipeline()

	#sd.putNumber();

	while(True):
		shootCamera = sd.getBoolean("boilerCamera", True);
		#Eventually this code will need to access a network table value to determine which vision program to run
		if(shootCamera):
			conts = getContours(topCamera, e)
			boilerBands = []
			scores = []
			distanceA = 0
			if(conts != None):
				for i in conts:
					scores.append(scoreGoal(i))


			#Get the first contour in the list
			a = conts[0]
			#b = cv2.moments(e.filter_contours_output[0])
			#cx = int(b['m10']/b['m00'])
			#cy = int(b['m01']/b['m00'])
			#area = cv2.contourArea(a)
			#perimiter = cv2.arcLength(a, True)

			#epsilon = 0.1*cv2.arcLength(a, True)
			#approx = cv2.approxPolyDP(a,epsilon,True)

			#hull = cv2.convexHull(a)
			x,y,w,h = cv2.boundingRect(boilerBands)
			# print(hull)
			# print(approx)
			# print(cx)
			# print(cy)
			print("--------------------------")
			print(x)
			sd.putNumber("boundRectX" , x )
			print(y)
			sd.putNumber("boundRectY" , y )
			print(w)
			sd.putNumber("boundRectW", w)
			sd.putNumber("FreshFrame", 1)
			sd.put
			print("--------------------------")


                else:
                	sd.putNumber("FreshFrame", 0)
		else:
            conts = getContours(bottomCamera, e)
			if(conts != None):
				#Get the first contour in the list
				a = conts[0]
				#b = cv2.moments(e.filter_contours_output[0])
				#cx = int(b['m10']/b['m00'])
				#cy = int(b['m01']/b['m00'])
				#area = cv2.contourArea(a)
				#perimiter = cv2.arcLength(a, True)

				#epsilon = 0.1*cv2.arcLength(a, True)
				#approx = cv2.approxPolyDP(a,epsilon,True)

				#hull = cv2.convexHull(a)
				x,y,w,h = cv2.boundingRect(a)
				# print(hull)
				# print(approx)
				# print(cx)
				# print(cy)
				print("--------------------------")
				print(x)
				sd.putNumber("boilerX" , x )
				print(y)
				sd.putNumber("boilerY" , y )
				print(w)
				sd.putNumber("boilerW", w)
				print(h)
				sd.putNumber("boilerH", h)
				print("--------------------------")
				sd.putNumber("FreshFrame", 1)

			else:
				sd.putNumber("FreshFrame", 0)

	print("Code Has finished")
	NetworkTable.shutdown()

if __name__ == '__main__':
    main()


def contourUnpack(conts){
	print("Unpack contours")


}



'''
	print("Are we connected? ")
	print(NetworkTable.isConnected())
	print("Are we a server ? ")
	print(NetworkTable.isServer())
	print("Is there a robot key?")
	print(sd.containsKey("Robot"))
'''
