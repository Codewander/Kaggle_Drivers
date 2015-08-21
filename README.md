# Kaggle_Drivers
Python code for AXA Driver Telematics Analysis Competition
Phase1:

	1.MainModel.py instantiates the DriverManager object, reads the drivers data (trips), computes the features and passes the information to DriverManager:

		1.1 DriverManager has a list of all Driver objects and provides operations to set, get, etc. a Driver object as needed:

			1.1.1 Each Driver(id, name) object has a list of its own Trip objects (200) and provides operations to set, get, etc. a Trip object as needed:

				1.1.1.1 Each Trip(id, name) object encapsulates(stores) the coresponding features computed for each trip. The features can be retrieved and
					analized as needed

	
Phase2: Use the Nervana Systems' Neon ML to test/refine the features generated in 1 above
