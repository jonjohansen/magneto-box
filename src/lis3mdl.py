from machine import I2C
import time

class LIS3MDL:
	def __init__(self):
		self.i2c = I2C(0, I2C.MASTER)
		# Setting different addresses
		self.address = 0x1E
		self.REG_ADDR_OUT_X_L = 0x28
		self.REG_ADDR_OUT_Y_L = 0x2A
		self.REG_ADDR_OUT_Z_L = 0x2C
		self.REG_CTL_1 = 0x20
		self.REG_CTL_2 = 0x21
		self.REG_CTL_3 = 0x22
		self.REG_CTL_4 = 0x23
		self.REG_CTL_5 = 0x24
		self.REG_STATUS = 0x27
		self.REG_INT_CFG = 0x30
		self.REG_INT_SRC = 0x31
		self.REG_INT_THS_L = 0x32
		self.REG_INT_THS_H = 0x33

		# Set performance level to Ultra-high
		self.setPerformance()

		#Data modes
		self.DATA_RATE = 0x01 # Fast
		#self.setDatarate

	def read_axis(self, address):
		raw = self.i2c.readfrom_mem(self.address, address, 2)
		#if (raw & 0x8000):
		#	raw = -1 * ((~raw + 1) & 0xFFFF)
		#scaled = raw * _scale / SENSITIVITY_OF_MIN_SCALE;
		return raw

	def collect_data(self):
		self.i2c.writeto_mem(self.address, self.REG_ADDR_OUT_X_L, 0x80)
		time.sleep(0.1)
		x = self.read_axis(self.REG_ADDR_OUT_X_L)
		y = self.read_axis(self.REG_ADDR_OUT_Z_L)
		z = self.read_axis(self.REG_ADDR_OUT_Z_L)
		#x = int.from_bytes(x, 'big', True)
		#y = int.from_bytes(y, 'big', True)
		#z = int.from_bytes(z, 'big', True)
		print("X Y Z" +"\t"+ str(x) +"\t" + str(y)+"\t" + str(z))

		'''
		Performances:
		0	Low power				1.2ms
		1	Medium performance		1.65ms
		2	High performance		3.23ms
		3	Ultra-high Performances	6.4ms

		Reads the registers as they are, and just re-set the performance ratio for X Y AND Z axis
		(Yes, they are for some reason placed on different control registers)
		'''
	def setPerformance(self):
		self.i2c.writeto_mem(self.address, self.REG_CTL_1, 0x00)
		self.i2c.writeto_mem(self.address, self.REG_CTL_3, 0x03)