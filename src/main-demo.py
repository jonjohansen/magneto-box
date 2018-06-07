import pycom
import time

#Initial
print("Initializing")
pycom.heartbeat(False)
# Display blue for intializing
pycom.rgbled(0x0000FF)
time.sleep(2)
# Go red for attempting to connect to lora
pycom.rgbled(0xFF0000)
time.sleep(5)
while true:
    #Go green for connected
    pycom.rgbled(0x00FF00)
    time.sleep(15)
    # go yellow for attempting to send
    pycom.rgbled(0xFFC100)
    