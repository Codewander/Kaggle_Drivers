__author__= 'TraianMorar'
''' Trip - maintains the list of trip features and provides the
	operations to add, get, display the trip features '''
class Trip:
	m_Id = -1;
	m_Name = '';
      
	def __init__(self, id, name, duration, length):
		self.m_Id = id
		self.m_Name = name
		self.m_FeatureList = []
     
	def setFeatureList(self, features):
		self.m_FeatureList = features

	def getFeatureList(self):
		return self.m_FeatureList

	def displayTrip(self):
		print "   Trip index: ", self.m_Id
		print "     name: ", self.m_Name
		print "     features: ", self.m_FeatureList
