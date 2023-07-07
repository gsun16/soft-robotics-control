import threading
from dobot_api import DobotApiDashboard, DobotApi, DobotApiMove, MyType
from time import sleep
import numpy as np
import time
import serial
import serial.tools.list_ports
import sys

# 全局变量(当前坐标)
current_actual = None

def connect_robot():
    try:
        ip = "192.168.5.1"
        dashboard_p = 29999
        move_p = 30003
        feed_p = 30004
        print("正在建立连接...")
        dashboard = DobotApiDashboard(ip, dashboard_p)
        move = DobotApiMove(ip, move_p)
        feed = DobotApi(ip, feed_p)
        print(">.<连接成功>!<")
        return dashboard, move, feed
    except Exception as e:
        print(":(连接失败:(")
        raise e

def get_feed(feed: DobotApi):
    global current_actual
    hasRead = 0
    while True:
        data = bytes()
        while hasRead < 1440:
            temp = feed.socket_dobot.recv(1440 - hasRead)
            if len(temp) > 0:
                hasRead += len(temp)
                data += temp
        hasRead = 0

        a = np.frombuffer(data, dtype=MyType)
        if hex((a['test_value'][0])) == '0x123456789abcdef':

            # Refresh Properties
            current_actual = a["tool_vector_actual"][0]
            print("tool_vector_actual:", current_actual)

        sleep(0.001)

class Device():
	'''
		A Class to abstract a device connected by serial
		Attributes:
			name - The name of the device//
			baud - The device's data rate//
			vid - The device's vendor ID//
			port - The device's port (found automatically by VID if none provided)
	'''

	def __init__(self, name=None, vid='0000',
					   port=None, baud='9600', 
					   bytesize=8,parity='N',
					   stopbits=1,timeout=None,
					   xonxoff=False,dsrdtr=False):
		
		self.name, self.vid = name, vid
		self.port, self.baud = port, baud
		self.bytesize, self.parity = bytesize, parity
		self.stopbits, self.timeout = stopbits, timeout
		self.xonxoff, self.dsrdtr = xonxoff, dsrdtr

		self.ser = serial.Serial()
		self.ser.port = self.port
		self.ser.baud = self.baud
		self.ser.bytesize = self.bytesize
		self.ser.parity = self.parity
		self.ser.stopbits = self.stopbits
		self.ser.timeout = self.timeout
		self.ser.xonxoff = self.xonxoff
		self.ser.dsrdtr = self.dsrdtr

	def connect(self, timeout=10):
		t1 = time.time()
		while not self.isOpen():
			t2 = time.time()
			
			if self.port == None:
				self.port = self.find()
				self.ser.port = self.port
			
			try:	
				self.ser.open()
			except:
				pass
			
			if (t2 - t1) > timeout:
				return False, 'Timeout'

		if self.isOpen():
			return True, self.ser.port
		else:
			return False

	def disconnect(self):
		try:
			self.ser.close()
		except:
			pass

		if self.isOpen():
			return False
		else:
			return True

	def find(self):
		# Make a list of all available ports on the system
		available_ports = list(serial.tools.list_ports.comports())
	
		# Sweep all ports
		for port in available_ports:
			for string in port:		# Sweep all strings in a given port list
				if self.vid in string:		# If any of these strings contain the VID
					return port[0]		# Return the first string, which is the port name

		return None

	def isOpen(self):
		return self.ser.isOpen()

	def read(self, length):
		return self.ser.read(length)

	def readline(self):
		return self.ser.readline()

	def write(self, data):
		try:
			self.ser.write(data)
			return True
		except:
			return False








def robot_command(key, move:DobotApiMove, dashboard:DobotApiDashboard, feed: DobotApi, arduino:Device, speed = 50, acceleration = 50, angular_move_rate = 1.0):
        dashboard.SpeedFactor(speed)
        dashboard.AccJ(acceleration)

        if key == "up":
            print("going up")
            move.RelJointMovJ(0, 0, 0, -1*angular_move_rate, 0, 0)
            sleep(0.3)
        elif key == "down":
            print("going down")
            move.RelJointMovJ(0, 0, 0, 1*angular_move_rate, 0, 0)
            sleep(0.3)
        elif key == "left":
            print("going left")
            move.RelJointMovJ(0, 0, 0, 0, -1*angular_move_rate, 0)
            sleep(0.3)
        elif key == "right":
            print("going right")
            move.RelJointMovJ(0, 0, 0, 0, 1*angular_move_rate, 0)
            sleep(0.3)

        elif key == "grab":
            print("grabbing")
            mystring = '$111111'
            bytes_data = bytes(mystring, 'utf-8')
            arduino.write(bytes_data)
            print(mystring)
        elif key == "release":
            print("releasing")
            mystring = '$000000'
            bytes_data = bytes(mystring, 'utf-8')
            arduino.write(bytes_data)
            print(mystring) 

        elif key == 'thumb_up':
                print(key)
                mystring = '$100000'
                bytes_data = bytes(mystring, 'utf-8')
                arduino.write(bytes_data)
                print(mystring)
        elif key == '1':
                print(key)
                mystring = '$101111'
                bytes_data = bytes(mystring, 'utf-8')
                arduino.write(bytes_data)
                print(mystring)
        elif key == '2':
                print(key)
                mystring = '$100111'
                bytes_data = bytes(mystring, 'utf-8')
                arduino.write(bytes_data)
                print(mystring)
        elif key == '3':
                print(key)
                mystring = '$110001'
                bytes_data = bytes(mystring, 'utf-8')
                arduino.write(bytes_data)
                print(mystring)
        elif key == '4':
                print(key)
                mystring = '$100000'
                bytes_data = bytes(mystring, 'utf-8')
                arduino.write(bytes_data)
                print(mystring)
        elif key == '5':
                print(key)
                mystring = '$000000'
                bytes_data = bytes(mystring, 'utf-8')
                arduino.write(bytes_data)
                print(mystring)
        elif key == '6':
                print(key)
                mystring = '$011100'
                bytes_data = bytes(mystring, 'utf-8')
                arduino.write(bytes_data)
                print(mystring)
        elif key == '8':
                print(key)
                mystring = '$001111'
                bytes_data = bytes(mystring, 'utf-8')
                arduino.write(bytes_data)
                print(mystring)
        

        elif key == "end":
            print("ending program")
            move.JointMovJ(0, 40, 85, 50, 90, 0)
            print("releasing fingers")
            mystring = '$000000'
            bytes_data = bytes(mystring, 'utf-8')
            arduino.write(bytes_data)
            sleep(2)
            dashboard.DisableRobot()
            sleep(1)
            dashboard.close()
            print('program ended')

        elif key == "reset":
            print("resetting arm position")
            move.JointMovJ(0, 40, 85, 50, 90, 0)
            print("releasing fingers")
            mystring = '$000000'
            bytes_data = bytes(mystring, 'utf-8')
            arduino.write(bytes_data)
            print(mystring)
            sleep(2)

        else:
            print('You entered: ')
            print(key)
            print("Invalid command. The following keys are available: up, down, left, right, grab, release, reset, or end. Additionally, you can use 1-6, 8, or thumb_up to control the gesture of the hand")

def robot_connect():
    #initialize the connection with arduino/hand
    print('please connect your arduino')
    sleep(5)
    arduino = Device(name='arduino nano',vid='1A86', port = 'COM3', baud='9600')  # Specify the vendor ID of your device

    success, port = arduino.connect()
    reconnect = 0
    if success:
            print('Connected to Arduino on port:', port)
    else:
	    while success == False and reconnect < 5:
                reconnect = reconnect + 1
                mystring = 'Failed to connect to Arduino, attempt: ' +str(reconnect) + '/5, please check your connection'
                print(mystring)
                success, port = arduino.connect()
    dashboard, move, feed = connect_robot()	

    print("开始上电...")
    dashboard.PowerOn()

    print("开始使能...")
    dashboard.EnableRobot()
    print("完成使能:)")

    dashboard.SpeedFactor(50)

    dashboard.GetAngle()
    print("moving to initial position")
    move.JointMovJ(0,40,85,50,90,0)
    sleep(5)
    return arduino, dashboard, move, feed
