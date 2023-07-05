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

if __name__ == '__main__':
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
    '''
    print("请耐心等待,机器人正在努力启动中...")
    count = 3
    while count > 0 :
        print(count)
        count = count - 1
        sleep(1)
	'''
    print("开始使能...")
    dashboard.EnableRobot()
    print("完成使能:)")

    dashboard.SpeedFactor(50)

    dashboard.GetAngle()
    print("moving to initial position")
    move.JointMovJ(0,40,85,50,90,0)
    sleep(5)


    end = 0
    
    while end == 0:
        lang = input("waiting for command:\n")
        match lang:
            #arm movement program
            case "up":
                move.RelMovLTool(0,20,0,0,0,0,0)
                sleep(1)
                end =0
            case "down":
                print("going down")
                move.RelMovLTool(0,-20,0,0,0,0,0)
                sleep(1)
                end =0
            case "left":
                print("going left")
                move.RelMovLTool(20,0,0,0,0,0,0)
                sleep(1)
                end =0        
            case "right":
                print("going right")
                move.RelMovLTool(-20,0,0,0,0,0,0)
                sleep(1)
                end =0

            #hand control program:
            case "grab":
                print("grabbing")
                mystring = '$111111' #the 1s or 0s represent the command to finger, 1 = bent and 0 = rest
                bytes_data = bytes(mystring, 'utf-8')
                arduino.write(bytes_data)
                print (mystring)
                end = 0
            case "release":
                print("releasing")
                mystring = '$000000'
                bytes_data = bytes(mystring, 'utf-8')
                arduino.write(bytes_data)
                print (mystring)
                end = 0
            case "change f":
                bit_string = input("please enter the finger control bit string (6 digits):\n")
                mystring = '$'+str(bit_string)
                bytes_data = bytes(mystring, 'utf-8')
                arduino.write(bytes_data)
                print (mystring)

            case "gestures": #can't do 7 or 9 since the dof cannot distinguish 7, 9, and 0
                bit_string = input("please select the desired gesture (1-6, 8, or thumb_up):\n")
                match bit_string:
                    case 'thumb_up':
                        mystring = '$100000'
                    case '1':
                        mystring = '$101111'
                    case '2':
                        mystring = '$100111'
                    case '3':
                        mystring = '$110001'
                    case '4':
                        mystring = '$100000'
                    case '5':
                        mystring = '$000000'
                    case '6':
                        mystring = '$011100'
                    case '8':
                        mystring = '$001111'
                    
                bytes_data = bytes(mystring, 'utf-8')
                arduino.write(bytes_data)
                print (mystring)

            case "end":
                print("ending program")
                move.JointMovJ(0,40,85,50,90,0)
                print("releasing fingers")
                mystring = '$000000'
                bytes_data = bytes(mystring, 'utf-8')
                arduino.write(bytes_data)
                sleep(2)
                dashboard.DisableRobot()
                sleep(1)
                dashboard.close()
                print('program ended')
                end = 1

            case "reset":
                print("reseting arm position")
                move.JointMovJ(0,40,85,50,90,0)
                print("releasing fingers")
                mystring = '$000000'
                bytes_data = bytes(mystring, 'utf-8')
                arduino.write(bytes_data)
                print (mystring)
                sleep(2)
                end = 0

            case "demo": #picking up an item by move up, left, and down for 5cm. then go back to original position and release it
                print('showing demo')
                move.JointMovJ(0,40,85,50,90,0)
                move.RelMovLTool(0,-50,0,0,0,0,0) #move down 5 cm to get the object
                move.RelMovLTool(0,50,0,0,0,0,0)  #move up   5 cm
                move.RelMovLTool(50,0,0,0,0,0,0)  #move left 5 cm
                move.RelMovLTool(0,-50,0,0,0,0,0) #move down 5 cm
                
                print("grabbing")
                mystring = '$111111' #the 1s or 0s represent the command to finger, 1 = bent and 0 = rest
                bytes_data = bytes(mystring, 'utf-8')
                arduino.write(bytes_data)
                sleep(5)
		
                move.RelMovLTool(0,50,0,0,0,0,0)  #move up   5 cm
                move.RelMovLTool(-50,0,0,0,0,0,0) #move left 5 cm
                move.RelMovLTool(0,-50,0,0,0,0,0) #move down 5 cm
                move.RelMovLTool(0,50,0,0,0,0,0)  #move up   5 cm to go back to original position
                
		
                print("releasing")
                mystring = '$000000'
                bytes_data = bytes(mystring, 'utf-8')
                arduino.write(bytes_data)
                sleep(3)
                print('demo done')
                end =0


            case _:
                print("invalid command, you can call demo, up, down, left, right, grab, release, change f, reset, or end")
                end = 0


