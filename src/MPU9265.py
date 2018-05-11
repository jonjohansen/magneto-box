import pycom
import time
from machine import I2C

# Slave addresses
SLAVE_ADDRESS = 0x68
AK8963_SLAVE_ADDRESS = 0x0C

''' MPU-9265 Register Addresses '''
# Sample rate driver
SMPLRT_DIV     = 0x19
CONFIG         = 0x1A
GYRO_CONFIG    = 0x1B
ACCEL_CONFIG   = 0x1C
ACCEL_CONFIG_2 = 0x1D
LP_ACCEL_ODR   = 0x1E
WOM_THR        = 0x1F
FIFO_EN        = 0x23
I2C_MST_CTRL   = 0x24
I2C_MST_STATUS = 0x36
INT_PIN_CFG    = 0x37
INT_ENABLE     = 0x38
INT_STATUS     = 0x3A
ACCEL_OUT      = 0x3B
TEMP_OUT       = 0x41
GYRO_OUT       = 0x43

I2C_MST_DELAY_CTRL = 0x67
SIGNAL_PATH_RESET  = 0x68
MOT_DETECT_CTRL    = 0x69
USER_CTRL          = 0x6A
PWR_MGMT_1         = 0x6B
PWR_MGMT_2         = 0x6C
FIFO_R_W           = 0x74
WHO_AM_I           = 0x75

## Gyro Full Scale Select 250dps
GFS_250  = 0x00
## Gyro Full Scale Select 500dps
GFS_500  = 0x01
## Gyro Full Scale Select 1000dps
GFS_1000 = 0x02
## Gyro Full Scale Select 2000dps
GFS_2000 = 0x03
## Accel Full Scale Select 2G
AFS_2G   = 0x00
## Accel Full Scale Select 4G
AFS_4G   = 0x01
## Accel Full Scale Select 8G
AFS_8G   = 0x02
## Accel Full Scale Select 16G
AFS_16G  = 0x03

# AK8963 Register Addresses
AK8963_ST1        = 0x02
AK8963_MAGNET_OUT = 0x03
AK8963_CNTL1      = 0x0A
AK8963_CNTL2      = 0x0B
AK8963_ASAX       = 0x10

# CNTL1 Mode select
## Power down mode
AK8963_MODE_DOWN   = 0x00
## One shot data output
AK8963_MODE_ONE    = 0x01

## Continous data output 8Hz
AK8963_MODE_C8HZ   = 0x02
## Continous data output 100Hz
AK8963_MODE_C100HZ = 0x06

# Magneto Scale Select
## 14bit output
AK8963_BIT_14 = 0x00
## 16bit output
AK8963_BIT_16 = 0x01

class MPU_9265:

    def __init__(self, address=SLAVE_ADDRESS):
        # The I2C slave address for MPU-9265
        self.i2c = I2C(0, I2C.MASTER)
        self.address = address

        # Set up sensor configurations
        self.configMPU_9265(GFS_250, AFS_2G)
        self.configAK8963(AK8963_MODE_C8HZ, AK8963_BIT_16)

    # Configure MPU-9265 sensor before outputting data
    def configMPU_9265(self, gfs, afs):

        if gfs == GFS_250:
            self.gres = 250.0/32768.0
        elif gfs == GFS_500:
            self.gres = 500.0/32768.0
        elif gfs == GFS_1000:
            self.gres = 1000.0/32768.0
        #else: gfs == GFS_2000
        #    self.gres = 2000.0/32768.0

        if afs == AFS_2G:
            self.ares = 2.0/32768.0
        elif afs == AFS_4G:
            self.ares = 4.0/32768.0
        elif afs == AFS_8G:
            self.ares = 8.0/32768.0
        else: # afs == AFS_16G:
            self.ares = 16.0/32768.0

        #sleep off
        self.i2c.writeto_mem(self.address, PWR_MGMT_1, 0x00)
        time.sleep(0.1)
        #auto select clock source
        self.i2c.writeto_mem(self.address, PWR_MGMT_1, 0x01)
        time.sleep(0.1)
        #DLPF_CFG
        self.i2c.writeto_mem(self.address, CONFIG, 0x03)
        #sample rate divider
        self.i2c.writeto_mem(self.address, SMPLRT_DIV, 0x04)
        #gyro full scale select
        self.i2c.writeto_mem(self.address, GYRO_CONFIG, gfs << 3)
        #accel full scale select
        self.i2c.writeto_mem(self.address, ACCEL_CONFIG, afs << 3)
        #A_DLPFCFG
        self.i2c.writeto_mem(self.address, ACCEL_CONFIG_2, 0x03)
        #BYPASS_EN
        self.i2c.writeto_mem(self.address, INT_PIN_CFG, 0x02)
        time.sleep(0.1)


    # Configure AK8963 sensor
    #  Magneto Mode Select(default:AK8963_MODE_C8HZ[Continous 8Hz])
    #  Magneto Scale Select(default:AK8963_BIT_16[16bit])
    def configAK8963(self, mode, mfs):
        if mfs == AK8963_BIT_14:
            self.mres = 4912.0/8190.0
        else: #  mfs == AK8963_BIT_16:
            self.mres = 4912.0/32760.
        
        # write to slave address
        self.i2c.writeto_mem(AK8963_SLAVE_ADDRESS, AK8963_CNTL1, 0x00)
        time.sleep(0.01)

        # set read FuseROM mode
        self.i2c.writeto_mem(AK8963_SLAVE_ADDRESS, AK8963_CNTL1, 0x0F)
        time.sleep(0.01)

        # read coef data
        data = self.i2c.readfrom_mem(AK8963_SLAVE_ADDRESS, AK8963_ASAX, 3)

        self.magXcoef = (data[0] - 128) / 256.0 + 1.0
        self.magYcoef = (data[1] - 128) / 256.0 + 1.0
        self.magZcoef = (data[2] - 128) / 256.0 + 1.0

        # set power down mode
        self.i2c.writeto_mem(AK8963_SLAVE_ADDRESS, AK8963_CNTL1, 0x00)
        time.sleep(0.01)

        # set scale and continous mode
        self.i2c.writeto_mem(AK8963_SLAVE_ADDRESS, AK8963_CNTL1, (mfs<<4|mode))
        time.sleep(0.01)

    # Read accelerometer, return data points
    def readAccel(self):
        data = self.i2c.readfrom_mem(self.address, ACCEL_OUT, 6)
        x = self.dataConv(data[1], data[0])
        y = self.dataConv(data[3], data[2])
        z = self.dataConv(data[5], data[4])

        # round data
        x = round(x*self.ares, 3)
        y = round(y*self.ares, 3)
        z = round(z*self.ares, 3)

        return {"x":x, "y":y, "z":z}

    # Check if data is ready and return true/false
    def checkDataReady(self):

        drdy = i2c.readfrom_mem(self.address, INT_STATUS)
        if drdy & 0x01:
            return True
        else:
            return False

    # Read gyroscope and return data points
    def readGyro(self):
        data = self.i2c.readfrom_mem(self.address, GYRO_OUT, 6)

        x = self.dataConv(data[1], data[0])
        y = self.dataConv(data[3], data[2])
        z = self.dataConv(data[5], data[4])

        x = round(x*self.gres, 3)
        y = round(y*self.gres, 3)
        z = round(z*self.gres, 3)

        return {"x":x, "y":y, "z":z}

    # Read magnet sensor and return data points
    def readMagnet(self):
        x=0
        y=0
        z=0

        # check data ready
        drdy = self.i2c.readfrom(AK8963_SLAVE_ADDRESS, AK8963_ST1)
        if drdy & 0x01 :
            data = self.i2c.readfrom_mem(AK8963_SLAVE_ADDRESS, AK8963_MAGNET_OUT, 7)

            # check overflow
            if (data[6] & 0x08)!=0x08:
                x = self.dataConv(data[0], data[1])
                y = self.dataConv(data[2], data[3])
                z = self.dataConv(data[4], data[5])

                x = round(x * self.mres * self.magXcoef, 3)
                y = round(y * self.mres * self.magYcoef, 3)
                z = round(z * self.mres * self.magZcoef, 3)

        return {"x":x, "y":y, "z":z}

    # Read temperature and return temperature
    def readTemperature(self):
        data = self.i2c.readfrom_mem(self.address, TEMP_OUT, 2)
        temp = self.dataConv(data[1], data[0])

        temp = round((temp / 333.87 + 21.0), 3)

        return temp

    ## Data convertion trough bit shifting, return new data
    def dataConv(self, data1, data2):
        value = data1 | (data2 << 8)
        if(value & (1 << 16 - 1)):
            value -= (1<<16)
    
        return value

    # Fetch all sensor data and return packaged
    def fetch_data(self):
        accel = self.readAccel()
        gyro = self.readGyro()
        temp = self.readTemperature()
        MPURETURN = (accel['x'],accel['y'],accel['z'],gyro['x'],gyro['y'],gyro['z'],temp)
        return MPURETURN

    # Print raw data from sensors
    def print_data(self, PACK):
        print("MPU DATA")
        print("=======================")
        print("Accelerometer")
        print("=============")
        print("x =", PACK[0])
        print("y =", PACK[1])
        print("z =", PACK[2])
        print("Gyro")
        print("=============")
        print("x =", PACK[3])
        print("y =", PACK[4])
        print("z =", PACK[5])
        print("Temperature")
        print("=============")
        print("Gyro temp = ", PACK[6])
        print("MPU DATA END")
        print("===========================")
