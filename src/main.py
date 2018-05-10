import pycom
from machine import I2C
import math
import time
from MAG3110 import MAG_3110
from MPU9265 import MPU_9265
from lis2 import LIS3MDL
from startiot import Startiot
from rot2 import *


#Initial
print("Initializing")
pycom.heartbeat(False) # disable the blue blinking
pycom.rgbled(0x0000FF)
#Toggle LORA mode.
CONNECT_DEVICE = 1

if CONNECT_DEVICE:
    print("LORA mode activated")
    pycom.rgbled(0xFF0000)
    iot = Startiot()
    print("Awaiting connection")
    iot.connect()
    print("Connected")
    pycom.rgbled(0x00FF00)

#Create instance of sensors
i2c = I2C(0, I2C.MASTER)
Mag = MAG_3110()
MPU = MPU_9265()
#magnet = LIS3MDL()
#magnet.enableLIS()

print(i2c.scan())

while True:
    # Get data from the sensors
    MPUDATA = MPU.fetch_data()
    # MPUDATA:
    # [0] = Accellerometer X
    # [1] = Accellerometer Y
    # [2] = Accellerometer Z
    # [3] = Gyro X
    # [4] = Gyro Y
    # [5] = Gyro Z
    # [6] = Temperature
    x = 0
    y = 0
    z = 0
    # How many measurments to do
    nMeasurements = 5
    # In how many seconds
    nSeconds = 10
    print("Fetching "+ str(nMeasurements) + " packets of data in " + str(nSeconds))
    for i in range(nMeasurements):
        data = Mag.collect_data()
        x += data[0]
        y += data[1]
        z += data[2]
        time.sleep(nSeconds/nMeasurements)

    x /= nMeasurements
    y /= nMeasurements
    z /= nMeasurements

    MAGDATA = (x,y,z)
    print("Done\n")
    # [0] = Mag X
    # [1] = Mag Y
    # [2] = MAg Z
    
    #MPU.print_data(MPUDATA)
    
    #Adjust data for positiona axis
    print("Adjusting data by accellerometer ")
    data = matrixise(MPUDATA, MAGDATA)
    # Make the adjustments into nanotesla
    data = Mag.convert_to_nt(data)
    # And the data is
    print("Magnet1\nX:" + str(data[0]) + "\tY:" + str(data[1])+ "\tZ:" + str(data[2]))

    #Holy hell this sensor does not work at all as expected.
    #mag2rawshit = magnet.getMagnetometerRaw()
    #print("Magnet2\nX:" + str(mag2rawshit[0]) + "\tY:" + str(mag2rawshit[1])+ "\tZ:" + str(mag2rawshit[2]))
    ### Packing the data
    x = str(data[0]) + ','
    y = str(data[1]) + ','
    z = str(data[2]) + ','
    temperature = str(MPUDATA[6])+ ','

    package = x + y + z + temperature

    if CONNECT_DEVICE:
        print("Attempting to send data")
        iot.send(package)
        print("Data sent")
    print("===============================")
