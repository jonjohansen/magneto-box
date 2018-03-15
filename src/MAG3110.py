from machine import I2C
import time


class MAG_3110:
	def __init__(self):
		
		self.i2c = I2C(0, I2C.MASTER)
		self.address = 0x0E # MAG3110 address, 0x0E(14)
		self.i2c.writeto_mem(self.address, 0x10, 0x1)
		#If there is an temperature offset.
		self.temp_OFFSET = 8
		#print(self.i2c.scan()) Prints address
	def collect_data(self):
		
		# Select Control register, 0x10(16)
		#		0x01(01)	Normal mode operation, Active mode
		self.i2c.writeto_mem(self.address,0x10,0x1)
		time.sleep(0.5)

		# MAG3110 address, 0x0E(14)
   		# Read data back from 0x01(1), 6 bytes
    	# X-Axis MSB, X-Axis LSB, Y-Axis MSB, Y-Axis LSB, Z-Axis MSB, Z-Axis LSB
		data = self.i2c.readfrom_mem(self.address, 0x01, 6) #Read data into "data"
		package = self.convert_magnetic_data(data)

		return package
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

		package = (xMag, yMag, zMag)
		return (package)

	def print(self, package, temperature):
		print("Temperature: " +str(temperature)+"C")
		print("Magnetic data: X: "+str(package[0])+" Y: "+str(package[1])+" Z: "+str(package[2]))