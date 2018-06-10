from network import LoRa
import socket
import time
import binascii
import pycom
import machine

class Startiot:
  def __init__(self):
    self.dev_eui = binascii.unhexlify("**REMOVED**")
    self.app_eui = binascii.unhexlify("**REMOVED**")
    self.app_key = binascii.unhexlify("**REMOVED**")

    self.lora = LoRa(mode=LoRa.LORAWAN)

  def connect(self, blocking = False, timeout = 0, function = None):
    self.lora.join(activation=LoRa.OTAA, auth=(self.dev_eui, self.app_eui, self.app_key), timeout=0)

    if timeout == 0:
      while not self.lora.has_joined():
        if function == None:
          time.sleep(2.5)
        else:
          function()
    else:
      for x in range(timeout):
        if self.lora.has_joined():
          break
        if function == None:
          time.sleep(2.5)
        else:
          function()
          
    if not self.lora.has_joined():
      return False

    self.s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

    # set the LoRaWAN data rate
    self.s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

    # make the socket non-blocking
    self.s.setblocking(blocking)

    return True

  def send(self, data):
    self.s.send(data)

  def recv(self, length):
    return self.s.recv(length)
