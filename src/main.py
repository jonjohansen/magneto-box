import pycom
from machine import I2C
import math
import time
from MAG3110 import MAG_3110
from MPU9265 import MPU_9265
from startiot import Startiot

#Initial
pycom.heartbeat(False) # disable the blue blinking
pycom.rgbled(0x0000FF)
#Toggle LORA mode.
CONNECT_DEVICE = 0

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
    temp = Mag.temperature()
    # Contains temperature from Mag
 
    sum = math.sqrt(MAGDATA[0]**2+MAGDATA[1]**2+MAGDATA[2]**2)
    print("The vector sum of the magnetic data is "+ str(sum))
    Mag.print(MAGDATA, temp)
    MPU.print_data(MPUDATA)
    if CONNECT_DEVICE:
        print("Attempting to send data")
        iot.send(MAGDATA)
        print("Data sent")
    print("\n\n")
    time.sleep(4)
def calibrate_data(MAGDATA, MPUDATA):
    pass

