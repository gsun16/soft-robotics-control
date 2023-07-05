import cv2
import os
import time
import handTrackingModule as htm
import serial
import serial.tools.list_ports

class Device():
	'''
		A Class to abstract a device connected by serial
		Attributes:
			name - The name of the device
			baud - The device's data rate
			vid - The device's vendor ID
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
                      
 

wcam,hcam=640,480
cap=cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)
pTime=0
detector = htm.handDetector(detectionCon=1)

arduino = Device(name='arduino nano',vid='1A86', port = 'COM3', baud='9600')  # Specify the vendor ID of your device

success, port = arduino.connect()
if success:
            print('Connected to Arduino on port:', port)
else:
            print('Failed to connect to Arduino')


while True:
    success,img=cap.read()
    img = detector.findHands(img, draw=True )
    lmList=detector.findPosition(img,draw=False)
    #print(lmList)
    tipId=[4,8,12,16,20]
    if(len(lmList)!=0):
        f1 = 0
        f2 = 0
        f3 = 0
        f4 = 0
        f0 = 0
        fingers=[]
        # Thumb
        if lmList[tipId[0]][1] < lmList[tipId[0] - 1][1] and abs(lmList[tipId[0]][1] - lmList[tipId[0] - 1][1])>5:
            f0=1
            fingers.append(1)
        else:
            f0=0
            fingers.append(0)

        # 4 Fingers

        if lmList[tipId[1]][2] > lmList[tipId[1] - 2][2] and abs(lmList[tipId[1]][2] - lmList[tipId[1] - 2][2])>8:
                f1=1
                fingers.append(1)
        else:
                f1=0
                fingers.append(0)

        if lmList[tipId[2]][2] > lmList[tipId[2] - 2][2] and abs(lmList[tipId[2]][2] - lmList[tipId[2] - 2][2])>8:
                f2=1
                fingers.append(1)
        else:
                f2=0
                fingers.append(0)

        if lmList[tipId[3]][2] > lmList[tipId[3] - 2][2] and abs(lmList[tipId[3]][2] - lmList[tipId[3] - 2][2])>8:
                f3=1
                fingers.append(1)
        else:
                f3=0
                fingers.append(0)
        if lmList[tipId[4]][2] > lmList[tipId[4] - 2][2] and abs(lmList[tipId[4]][2] - lmList[tipId[4] - 2][2])>8:
                f4=1
                fingers.append(1)
        else:
                f4=0
                fingers.append(0)

              
        
        mystring = '$'+str(f0)+str(f1)+str(f2)+str(f3)+str(f4)
        bytes_data = bytes(mystring, 'utf-8')
        arduino.write(bytes_data)
        print (mystring)


        
    
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img, f'FPS: {int(fps)}',(400,70),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,0),3)
    cv2.imshow("image",img)
    if(cv2.waitKey(1) & 0xFF== ord('q')):
        break


