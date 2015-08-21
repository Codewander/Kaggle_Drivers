__author__= 'TraianMorar'
''' Driver - maintains the list of Trips and provides the
	operations to add, get, display the driver trips and profile'''

class Driver:
	m_Id = -1; #0..n-1
	m_Name = '';
   
	def __init__(self, id, name):
		self.m_Id = id;
		self.m_Name = name
		self.m_TripsList = [] #all the Trips of a driver
       
	def addTrip(self, trip):
		self.m_TripsList.append(trip);
	   
	def getId(self):
		return self.m_Id

	def getTotalTrips(self):
		return len(self.m_TripsList)
      
	def getTrip(self, id):
		size = len(self.m_TripsList)
		if (size > 0 and id < size):
			return  self.m_TripsList[id]
		else:
			print "Invalid trip Id: %s expected range: 0 to %s" % \
			      ( id, size-1)
			return None
      
	def displayDriver(self, tripId):
		print "Driver index: ", self.m_Id
		print " name: ", self.m_Name
		print " total trips: ", len(self.m_TripsList)
		t = self.getTrip(tripId)
		if (t != 0): 
			t.displayTrip()
