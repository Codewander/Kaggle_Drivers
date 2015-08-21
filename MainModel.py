__author__= 'TraianMorar'
import sys

from DriverManager import *
from Driver import *
from Trip import *
from Utils import *

driverMgr = DriversManager()
featureType = [	'tripDist'
				,'tripTime'
				,'maxDist'
				,'stdDist'
				,'meanDist'
				,'medianDist'
				,'xVariance'
				,'yVariance'
				,'stopCount'
				,'dataJumpCount'
				
				,'maxSpeed'
				,'mimSpeed'
				,'stdSpeed'
				,'meanSpeed'
				,'medianSpeed'
				,'maxAccel'
				,'minAccel'
				,'totalAccel'
				,'maxDecel'
				,'minDecel'
				,'totalDecel'
				
				,'maxAccelJerk'
				,'minAccelJerk'
				,'totalAccelJerck'
				,'maxDecelJerk'
				,'minDecelJerk'
				,'totalDecelJerck'
				
				,'maxAngle'
				,'minAngle'
				,'meanAngle'
				,'medianAngle'
				,'totalAngle'
				,'maxAngularSpeed'
				,'minAngularSpeed'
				,'meanAngularSpeed'
				,'medianAngularSpeed' ]

features = []

''' test DriverManager - display the driver id and the trip id features
'''
def testDriverManager():

	print "\nTesting: "
	driverId = 0; #use: 0..n-1
	tripId = 199;   #use: 0..199; 
	driverMgr.displayDriver(driverId, tripId)

	d = driverMgr.getDriver(driverId)
	d.displayDriver(tripId)
	myTrip = d.getTrip(tripId)
	

''' For each driver read the trip data and compute the features; 
	"driverLimit" input parameter is used only for testing purposes to 
	get out of the drivers loop. Set the "driverLimit" to 0, 1, 2, to 
	process 1, 2 or	3 drivers, otherwise it will process all the dirs
	present in the Kaggel "drivers" path(.
'''
def generateFeatures(driversDataPath, driverLimit = 10000):
	import os
	import glob
		
	driverIndex = 0;
	tripIndex = 0;
    
	''' read drivers directory '''
	for dId in sorted(os.listdir(driversDataPath)):
		print " driver: index %s name %s " % (driverIndex, dId)
		driver = Driver(driverIndex, dId)
		tripIndex = 0	
     
		''' for each driver read the trip files, one file at a time and
			compute the features and stores them in the Trip object
		'''
		folder = '%s/%s/*.csv'%(driversDataPath, dId) 
		for f in sorted( glob.glob(folder) ):
			#print " f: ", f
			fileName = os.path.basename(f)
			[name, ext] = os.path.splitext(fileName)
			tripMatrix = []
			features = []
		    
			''' data sample rate is 1 sec '''
			tripMatrix = np.loadtxt(f, delimiter=',', skiprows=1)
			
			''' distances ''' 
			distances = getDistances(tripMatrix)
			
			medianDist = np.median(distances)
			meanDist = np.mean(distances)
			stdDist = np.std(distances)
			maxDist = distances.max()
			tripTime = len(tripMatrix)
			tripDist = distances.sum()#np.sum(distances)

			''' distance features '''
			features.append(tripDist)
			features.append(tripTime)
			features.append(maxDist)
			features.append(stdDist)
			features.append(meanDist)
			features.append(medianDist)
			
			variances = getPCAVariance(tripMatrix)
			xVariance = variances[0]
			yVariance = variances[1]
			
			''' xy variance features '''
			features.append(xVariance)
			features.append(yVariance)
			
			''' stops '''
			stopCount = getStops(tripMatrix)
			dataJumpCount  = getDataJumps(distances)
			
			''' stops and jumps features '''
			features.append(stopCount)
			features.append(dataJumpCount)			

			'''speeds '''
			speeds = distances
			medianSpeed = np.median(speeds)
			meanSpeed = np.mean(speeds)
			maxSpeed = speeds.max()
			mimSpeed = speeds.min()
			stdSpeed = np.std(speeds)
			
			'''speeds features '''
			features.append(maxSpeed)
			features.append(mimSpeed)
			features.append(stdSpeed)
			features.append(meanSpeed)
			features.append(medianSpeed)

			''' accelerations - derivative of speed'''
			accels = np.diff(speeds)
			[minAccel, maxAccel, totalAccel] = getMinMaxPos(accels)
			[minDecel, maxDecel, totalDecel] = getMinMaxNeg(accels)
			
			''' accelerations features '''
			features.append(maxAccel)
			features.append(minAccel)
			features.append(totalAccel)
			features.append(maxDecel)
			features.append(minDecel)
			features.append(totalDecel)

			''' jerks - derivative of acceleration'''
			jerks = np.diff(accels)
			[minAccelJerk, maxAccelJerk, totalAccelJerck] = getMinMaxPos(jerks)
			[minDecelJerk, maxDecelJerk, totalDecelJerck] = getMinMaxNeg(jerks)
			
			''' jerk features '''
			features.append(maxAccelJerk)
			features.append(minAccelJerk)
			features.append(totalAccelJerck)
			features.append(maxDecelJerk)
			features.append(minDecelJerk)
			features.append(totalDecelJerck)
			
			''' angles '''
			angles, originAngles = getAngles(tripMatrix)
						
			maxAngle = angles.max()
			minAngle = angles.min()
			totalAngle = angles.sum()
			meanAngle = np.mean(angles)
			medianAngle = np.median(angles)
			
			''' angles features '''
			features.append(maxAngle)
			features.append(minAngle)
			features.append(meanAngle)
			features.append(medianAngle)
			features.append(totalAngle)

			''' angularVelocity '''
			angularSpeeds = angles * speeds
			
			maxAngularSpeed = angularSpeeds.max()
			minAngularSpeed = angularSpeeds.min()
			medianAngularSpeed = np.median(angularSpeeds)
			meanAngularSpeed = np.mean(angularSpeeds)

			features.append(maxAngularSpeed)
			features.append(minAngularSpeed)
			features.append(meanAngularSpeed)
			features.append(medianAngularSpeed)
					
			''' instantiate Trip object '''
			trip = Trip(tripIndex, name, tripTime, tripDist)
			
			''' add the feature list to the current trip'''
			trip.setFeatureList(features)
			
			''' add the trip to the driver '''
			driver.addTrip(trip)
			del trip #the local trip should be dealocated every loop
			
			tripIndex += 1
			      
		''' add driver to the manager. At this point the driver has
			all the trips with the corresponding features
		'''
		driverMgr.addDriver(driver);
		
		del driver #the local driver should be dealocated every loop   
		
		driverIndex += 1   
		
		''' to get out of the drivers loop - for testing only '''
		if driverIndex > driverLimit:
			break

def main():
	print "Numpy ver: ", np.__version__ 
	
	''' "driversPath" is the path to your "drivers" directory where you
		unzipped all the drivers and trips from Kaggle;
		On my terminal I type: "python MainModel.py ../../drivers"
	'''
	driversPath = '../../drivers' #my deault path
	if len(sys.argv) >= 2:
		driversPath = sys.argv[1]
	
	maxDrivers = 4000
	print "Processing up to %s drivers" % (maxDrivers+1)
	print "Generating features..."
	
	''' compute all the features '''
	generateFeatures(driversPath, maxDrivers)
	
	count = driverMgr.getDriverCount()
	print "\nDone: Processed %s drivers!\n" % count

	''' simple test to display the dirver and the trip '''
	testDriverManager()

##########################################################
if __name__ == '__main__':
	main()
