__author__= 'TraianMorar'
''' Utils - provides utility functions to 
	compute and plot trip, feature, etc.
'''

import numpy as np
import matplotlib.pyplot as plt

def filterData(pointList, window = 5, order = 2):
	from scipy.signal import savgol_filter
	''' filters the data point in the list '''
	
	return savgol_filter(pointList.T, window_length = window, \
	                     polyorder = order).T 

def getDistances(pointList):
	''' Returns the euclidean distances between adjacent points (x,y),
		using numpy hypot() function
	'''
	deltas = np.diff(pointList, axis=0)
	distances = np.hypot(deltas[:,0], deltas[:,1])   
	#OR use: distances = np.sqrt( (deltas ** 2).sum(axis=1) )
	return distances
   
def getDistances2(pointList):
	from scipy.spatial.distance import (pdist, cdist)
	''' Returns the euclidean distances between adjacent points (x,y);
		pdist() function returns the distance between all the   
		points in the trip for a total of m(m-1)/2 entries, 
		Where: m = total points in the list.
		We are interested only in the adjacent points. For this we step 
		through the list while updating the index and the step
	'''
	distances = []
	dist = pdist(pointList, 'euclidean')   
	size = len(pointList); 
	index = 0
	''' get the first distance at index 0'''
	distances.append(dist[index])
	step = size - 1
	''' parse the list and get only the adjacent point distances '''
	for i in xrange(size-2):  # ignore the first and the last point
		index += step
		distances.append(dist[index])
		step -= 1
      
	return distances

def getStops(pointList):
    ''' returns the number of stops (i.e overlaped) points in matrix '''
    count = 0
    X = pointList[:,0]
    Y = pointList[:,1]
    for i in xrange(1, len(X)):
        if X[i-1] == X[i] and Y[i-1] == Y[i]:
            count += 1
    return count

def getDataJumps(distaceList, magnitude = 45):
	''' counts how many times the data is missing in the list, where the 
		magnitude  between consecutive distances is very high;
	'''
	count = 0
	maxDist = distaceList[0]
	
	for i in xrange(1, len(distaceList)):
		currentDist = distaceList[i]
		if currentDist > maxDist:
			if currentDist > magnitude * maxDist:
				count += 1
			maxDist = currentDist
			
	return count

def getMinMaxPos(valList):
	'''returns the min, max and sum of positive values from the list '''
	posVals = valList[np.where(valList > 0.0)]
	minVal = posVals.min()
	maxVal = posVals.max()
	totalSum = posVals.sum()
	
	return minVal, maxVal, totalSum

def getMinMaxNeg(valList):
	'''returns the min, max and sum of negative values from the list '''
	negList = valList[np.where(valList < 0.0)]
	minVal = negList.max()
	maxVal = negList.min()
	totalSum = negList.sum()

	return minVal, maxVal, totalSum
	
def getAngles(pointList, degree = True):
	''' returns the list of angle between adjacent points in the list,
		using the arctan2 (y,x); also returns the origin angle for 
		each point.
	'''
	toDegrees = (180 / np.pi)
	angleList = []
	originAngleList = []
	X = pointList[:,0]
	Y = pointList[:,1]
	for i in xrange(len(pointList)):
		originAngleList = np.arctan2( Y, X )
		
	angleList = np.diff(originAngleList)
	
	if (degree == True):
		angleList *= toDegrees
		originAngleList *= toDegrees
							
	return angleList, originAngleList
	
def getPCAVariance(X):#x, y):
	from sklearn.decomposition import PCA
	''' retruns the variance in principal direction '''	
	
	pca = PCA(n_components = 2)	
	pca.fit_transform(X)
	
	return pca.explained_variance_ratio_

def getSpeedRatio(speedList, medianspeed):
	acc = 0.0
	dec = 0.0
	cruise = 0.0
	offset = 1.0
	alpha = 0.01
	threshold = alpha * medianspeed
	prevSpeed = speedList[0]
	for i in xrange(1, len(speedList)):
		if (speedList[i] > (offset+threshold) * prevSpeed):
			acc += 1
		elif speedList[i] < (offset-threshold) * prevSpeed:
			dec += 1
		else:
			cruise += 1
	return acc, dec, cruise
	

def plotTrip(trip, driverId, fileName):
	plt.gca().xaxis.grid(True)
	plt.gca().yaxis.grid(True)
	X = trip[:,0]
	Y = trip[:,1]
	plt.plot(X, Y, marker='o', linestyle='--',color='b',label = 'trip');
	plt.title("Driver %s, Trip: %s"%(driverId, fileName))
	plt.ylabel('Y')
	plt.xlabel('X')
	plt.legend()
	plt.show()

def plotSpeed(speeds, accels, jerks, driverId, fileName):	
	plt.gca().xaxis.grid(True)
	plt.gca().yaxis.grid(True)
	   
	plt.plot(xrange(len(speeds)), speeds, marker='o', linestyle='--', \
					color='b', label = 'speeds');
	plt.plot(xrange(len(accels)), accels, marker='+', linestyle='--', \
					color='r', label = 'accels');
	plt.plot(xrange(len(jerks)), jerks, marker='x', linestyle='--', \
					color='g', label = 'jerks');
	#plt.plot(range(len(speeds)), [0] * len(speeds), 'm-')	# zero line
	plt.title("Driver %s, Trip: %s"%(driverId, fileName))
	plt.ylabel('val')
	plt.xlabel('time')
	plt.legend()
	plt.show()

def plotAngle(angles, arcTanAngles, driverId, fileName):
	plt.gca().xaxis.grid(True)
	plt.gca().yaxis.grid(True)
	
	plt.plot(xrange(len(angles)), angles, marker='o', linestyle='--', \
									color='b', label = 'angl');
	plt.plot(xrange(len(arcTanAngles)), arcTanAngles, marker='+', \
					linestyle='--', color='r', label = 'originAngl');
	#plt.plot(range(len(angles)), [0] * len(angles), 'm-')
	plt.title("Driver %s, Trip: %s"%(driverId, fileName))
	plt.ylabel('val')
	plt.xlabel('time')
	plt.legend()
	plt.show()

def plotAngularSpeed(angularSpeeds, driverId, fileName):
	plt.gca().xaxis.grid(True)
	plt.gca().yaxis.grid(True)
	
	plt.plot(xrange(len(angularSpeeds)), angularSpeeds, marker='o', \
						linestyle='--', color='b', label = 'angSpeed');
	plt.title("Driver %s, Trip: %s"%(driverId, fileName))
	plt.ylabel('val')
	plt.xlabel('time')
	plt.legend()
	plt.show()


def plotTripFeatures(trip, speeds, accels, angles, driverId, fileName):
	plt.gca().xaxis.grid(True)
	plt.gca().yaxis.grid(True)

	plt.plot(trip[:,0], trip[:,1], marker='x', linestyle='--', \
					color='b', label = 'trip');
	plt.title("Driver %s, Trip: %s"%(driverId, fileName))
	plt.ylabel('Y')
	plt.xlabel('X')
	plt.legend()
	plt.show()
	   
	plt.plot(xrange(len(speeds)), speeds, marker='o', linestyle='--', \
					color='b', label = 'speeds');
	plt.plot(xrange(len(accels)), accels, marker='+', linestyle='--', \
					color='r', label = 'accels');
	plt.title("Driver %s, Trip: %s"%(driverId, fileName))
	plt.ylabel('val')
	plt.xlabel('time')
	plt.legend()
	plt.show()

	plt.plot(xrange(len(angles)), angles, marker='^', linestyle='--', \
					color='b', label = 'angles');
	plt.plot(range(len(angles)), [0] * len(angles), 'm-')
	plt.title("Driver %s, Trip: %s"%(driverId, fileName))
	plt.ylabel('val')
	plt.xlabel('time')
	plt.legend()
	plt.show()
