import pycom
from machine import I2C
import math
import time
from MAG3110 import MAG_3110
from MPU9265 import MPU_9265
from lis2 import LIS3MDL
from startiot import Startiot
from rot2 import *

#################################
#       Configurations          #
#################################
# Toggling LORA mode.           #
CONNECT_DEVICE = 0              #
                                #
# MAG_3110 configurations       #
nMeasurements = 1500            #
nSeconds = 30                   #
prs_deviate = 20                #
                                #
#################################                  

# Initiation
print("Initializing")
pycom.heartbeat(False) # disable the blue blinking
pycom.rgbled(0x0000FF)
# Bus initializing
i2c = I2C(0, I2C.MASTER)
# Sensor initalizing
Mag = MAG_3110(nMeasurements, nSeconds, prs_deviate) # Used to read magnetic data
MPU = MPU_9265() # Used to read accellerometer data

print(i2c.scan())

if CONNECT_DEVICE:
    print("Device was set in lora mode.")
    iot = Startiot()
    pycom.rgbled(0xFF0000)
    print("Awaiting connection to lora network")
    iot.connect()
    print("Connection found. Continuing")
    pycom.rgbled(0x00FF00)


'''
This is the loop where the box will reside doing measurements. 
'''
while True:
    # Get accelerometer data
    MPUDATA = MPU.fetch_data()

    '''
    Since our device has the MPU and the MAG mounted side by side,
    their axises are not aligning perfectly, thus we have to flip some of the data
    MAGDATA flips from the axis into the correct tuple (X, Y, Z) 
    '''
    mdata = Mag.get_reading()
    MAGDATA = (-mdata[1],mdata[0],mdata[2])
    
    MPU.print_data(MPUDATA)
    print("The raw magnetic data is: ")
    Mag.print(MAGDATA)
    #Adjust data for positional axis
    data = matrixise(MPUDATA, MAGDATA)
    # Make the convertions into nanotesla
    data = Mag.convert_to_nt(data)
    print("\nThe finished processed magnetic data is: ")
    Mag.print(data)
    if CONNECT_DEVICE:
        # Pack the data for shipping
        package = pack_data(data, MAGDATA, MPUDATA)
        pycom.rgbled(0xFFC100)
        print("Attempting to send data")
        iot.send(package)
        print("Data sent")
        pycom.rgbled(0x00FF00)
    print("===============================")

# Packs all the different types of data into a string, for shipping to Mic
def pack_data(data, MAGDATA, MPUDATA):
    #Pack the calculated magdata
    calcx = str(data[0]) + ','
    calcy = str(data[1]) + ','
    calcz = str(data[2]) + ','
    # The raw magdata
    rawx = str(MAGDATA[0]*100/3) + ','
    rawy = str(MAGDATA[1]*100/3) + ','
    rawz = str(MAGDATA[2]*100/3) + ','
    # The MPU accelerometer data
    accx = str(MPUDATA[0]) + ','
    accy = str(MPUDATA[1]) + ','
    accz = str(MPUDATA[2]) + ','
    temperature = str(MPUDATA[6])+ ','
    # Into one long CSV-string
    package = calcx + calcy + calcz + rawx + rawy + rawz + accx + accy + accz + temperature
    return package
