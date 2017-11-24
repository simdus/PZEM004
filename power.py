#!/usr/bin/env python2
#coding=utf-8

import serial
import struct
import mysql.connector
from datetime import date, datetime, timedelta
import time
import ConfigParser
import io

# Load the configuration file
with open("power.ini") as f:
    sample_config = f.read()
config = ConfigParser.RawConfigParser(allow_no_value=True)
config.readfp(io.BytesIO(sample_config))

_host = config.get('mysql', 'host')
_user = config.get('mysql', 'user')
_passwd = config.get('mysql', 'passwd')
_db = config.get('mysql', 'db')
_com_1 = config.get('comport', 'com_1')  
_com_2 = config.get('comport', 'com_2')  
_com_3 = config.get('comport', 'com_3')  
_baudrate = config.get('comport', 'baudrate')
_meassure = config.get('meassure', 'speed')



print
print("Host     : " + _host)
print("User     : " + _user)
print("Password : " + _passwd)
print("DB       : " + _db)
print("COMPORT-1: " + _com_1)
print("COMPORT-2: " + _com_2)
print("COMPORT-3: " + _com_3)
print("BAUDRATE : " + _baudrate)
print("SPEED    : " + _meassure)
print

class BTPOWER:

   setAddrBytes         =   [0xB4,0xC0,0xA8,0x01,0x01,0x00,0x1E]
   readVoltageBytes     =   [0xB0,0xC0,0xA8,0x01,0x01,0x00,0x1A]
   readCurrentBytes     =   [0XB1,0xC0,0xA8,0x01,0x01,0x00,0x1B]
   readPowerBytes       =   [0XB2,0xC0,0xA8,0x01,0x01,0x00,0x1C]
   readRegPowerBytes    =   [0XB3,0xC0,0xA8,0x01,0x01,0x00,0x1D]

   def init(self, com):
      self.ser = serial.Serial(
         port=com,
         baudrate=_baudrate,
         parity=serial.PARITY_NONE,
         stopbits=serial.STOPBITS_ONE,
         bytesize=serial.EIGHTBITS,
         timeout = 20.0
      )
      if self.ser.isOpen():
         self.ser.close()
      self.ser.open()

   def checkChecksum(self, _tuple):
      _list = list(_tuple)
      _checksum = _list[-1]
      _list.pop()
      _sum = sum(_list)
      if _checksum == _sum%256:
         return True
      else:
         raise Exception("Wrong checksum")
         
   def isReady(self):
      self.ser.write(serial.to_bytes(self.setAddrBytes))
      rcv = self.ser.read(7)
      if len(rcv) == 7:
         unpacked = struct.unpack("!7B", rcv)
         if(self.checkChecksum(unpacked)):
            return True
      else:
         raise serial.SerialTimeoutException("Timeout setting address")

   def readVoltage(self):
      self.ser.write(serial.to_bytes(self.readVoltageBytes))
      rcv = self.ser.read(7)
      if len(rcv) == 7:
         unpacked = struct.unpack("!7B", rcv)
         if(self.checkChecksum(unpacked)):
            tension = unpacked[2]+unpacked[3]/10.0
            return tension
      else:
         raise serial.SerialTimeoutException("Timeout reading tension")

   def readCurrent(self):
      self.ser.write(serial.to_bytes(self.readCurrentBytes))
      rcv = self.ser.read(7)
      if len(rcv) == 7:
         unpacked = struct.unpack("!7B", rcv)
         if(self.checkChecksum(unpacked)):
            current = unpacked[2]+unpacked[3]/100.0
            return current
      else:
         raise serial.SerialTimeoutException("Timeout reading current")

   def readPower(self):
      self.ser.write(serial.to_bytes(self.readPowerBytes))
      rcv = self.ser.read(7)
      if len(rcv) == 7:
         unpacked = struct.unpack("!7B", rcv)
         if(self.checkChecksum(unpacked)):
            power = unpacked[1]*256+unpacked[2]
            return power
      else:
         raise serial.SerialTimeoutException("Timeout reading power")

   def readRegPower(self):
      self.ser.write(serial.to_bytes(self.readRegPowerBytes))
      rcv = self.ser.read(7)
      if len(rcv) == 7:
         unpacked = struct.unpack("!7B", rcv)
         if(self.checkChecksum(unpacked)):
            regPower = unpacked[1]*256*256+unpacked[2]*256+unpacked[3]
            return regPower
      else:
         raise serial.SerialTimeoutException("Timeout reading registered power")

   def readAll(self):
      if(self.isReady()):
         return(self.readVoltage(),self.readCurrent(),self.readPower(),self.readRegPower())

   def close(self):
      self.ser.close()

      
def measure(_com, faze):
	sensor = BTPOWER()
	sensor.init(_com)
	print(_com)
	print(sensor.isReady())
	if (sensor.isReady()):
		_voltage = sensor.readVoltage()
		_current = sensor.readCurrent()
		_power   = sensor.readPower()
		_energy  = sensor.readRegPower()
		cnx = mysql.connector.connect(user=_user, password=_passwd,host=_host,database=_db)
		cursor = cnx.cursor()
		add_power = ("INSERT INTO power (datum, id_phase, voltage, current, power, energy) VALUES (%s, %s, %s, %s, %s, %s)")
		print("Write Database " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		print("Phase  : " + str(faze))
		print("Voltage: " + str(_voltage) + " V")
		print("Proud  : " + str(_current) + " A")
		print("Power  : " + str(_power) + " W")
		print("Energy : " + str(_energy) + " Wh")
		print
		data_power = (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), faze, _voltage, _current, _power, _energy )
		print data_power
		cursor.execute(add_power, data_power)
		cnx.commit()
		cursor.close()
		cnx.close()
		sensor.close()

while True:
	measure(_com_1,1)	
	measure(_com_2,2)
	measure(_com_3,3)
	print
	print("Waiting")
	print
	time.sleep(int(_meassure))

		
