__author__= 'TraianMorar'
''' DriversManager - maintains the list of drivers and provides the
	operations to add, get, display the driver '''

class DriversManager:
	m_DriversList = [];
    
	def __init__(self):
		self.m_DriversList = []

	def addDriver(self, driver):
		self.m_DriversList.append(driver); 

	def getDriver(self, id):
		size = len(self.m_DriversList)
		print "total Drivers: ", size
		if (size > 0 and id < size):
			return  self.m_DriversList[id]
		else:
			print "Invalid driver Id: ", id
			return None
	def getDriverCount(self):
		return len(self.m_DriversList)

	def getDriversList(self):
		return len(self.m_DriversList);

	def displayDriver(self, driverId, tripId):
		d = self.getDriver(driverId)
		d.displayDriver(tripId)	
