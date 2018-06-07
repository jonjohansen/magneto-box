from machine import I2C
import time

'''
Simple library for using the MAG3110 sensor through i2c.
'''
class MAG_3110:
	def __init__(self, nMeasurements, nSeconds, prs_deviate):
		self.i2c = I2C(0, I2C.MASTER)
		self.address = 0x0E # MAG3110 address, 0x0E(14)
		# 0x01(01)	Normal mode operation, Active mode
		self.i2c.writeto_mem(self.address, 0x10, 0x1)
		#Set temperature offset (I found it to be 10)
		self.temp_OFFSET = 10
		# For the rate of measuring
		self.nMeasurements = nMeasurements
		self.nSeconds = nSeconds
		# For discarding bad data
		self.prs_deviate = prs_deviate
	'''
	Function should read data and return as a tuple containing (X, Y, Z)
	This only returns one reading. To get multiple of them over a timespan
	use get_reading 
	'''
	def read_sensor(self):	
		data = self.i2c.readfrom_mem(self.address, 0x01, 6) #Read data into "data"
		# Converts the data and returns it!
		return self.convert_magnetic_data(data)

	# Returns sensor temperature.
	def temperature(self):
		#Read temeperature from sensor
		temp = self.i2c.readfrom_mem(self.address, 0x0F, 1)
		#Convert it into decimal. (True for signed bit)
		temp = int.from_bytes(temp, 'big', True)
		temp += self.temp_OFFSET
		return temp

	#Returns a tuple of converted data with format (x, y, z)
	def convert_magnetic_data(self, data):

		# Convert the data
		xMag = data[0] * 256 + data[1]
		if xMag > 32767 :
			xMag -= 65536

		yMag = data[2] * 256 + data[3]
		if yMag > 32767 :
			yMag -= 65536

		zMag = data[4] * 256 + data[5]
		if zMag > 32767 :
			zMag -= 65536

		return (xMag, yMag, zMag)
	'''
	Fetches an amount of readings from a given time and amount.
	Averages the readings to increase accuracy.
	'''
	def get_reading(self):
	    x = 0
	    y = 0
	    z = 0
	    print("Fetching "+ str(self.nMeasurements) + " packets of data in " + str(self.nSeconds)+ " seconds")
	    for i in range(self.nMeasurements):
	        data = self.read_sensor()
	        x += data[0]
	        y += data[1]
	        z += data[2]
	        time.sleep(self.nSeconds/self.nMeasurements)

	    x /= self.nMeasurements
	    y /= self.nMeasurements
	    z /= self.nMeasurements

	    return (x, y, z)

	''' Since the data we get from the magnetic sensor is given in a 8 bit
	    we need to convert it to actual nano-tesla.
	'''
	def convert_to_nt(self, package):
		package[0] *= 100/3
		package[1] *= 100/3
		package[2] *= 100/3
		return package

	def print(self, package):
		print("X: "+str(package[0])+" Y: "+str(package[1])+" Z: "+str(package[2]))