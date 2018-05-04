import pycom
from machine import I2C
import math
import time
from MAG3110 import MAG_3110
from MPU9265 import MPU_9265
from startiot import Startiot
from rot2 import *


#Initial
pycom.heartbeat(False) # disable the blue blinking
pycom.rgbled(0x0000FF)
#Toggle LORA mode.
CONNECT_DEVICE = 1

if CONNECT_DEVICE:
    pycom.rgbled(0xFF0000)
    iot = Startiot()
    print("Awaiting connection")
    iot.connect()
    print("Connected")
    pycom.rgbled(0x00FF00)

#Create instance of sensors
Mag = MAG_3110()
MPU = MPU_9265()

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
    
    MAGDATA = Mag.collect_data()
    # [0] = Mag X
    # [1] = Mag Y
    # [2] = MAg Z
    
    MPU.print_data(MPUDATA)

    #Adjust data for positiona axis
    data = matrixise(MPUDATA, MAGDATA)
    # Make the adjustments into nanotesla
    data = Mag.convert_to_nt(data)
    # And the data is
    print(data[0], data[1], data[2])

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
    print("\n\n")

    time.sleep(10)



