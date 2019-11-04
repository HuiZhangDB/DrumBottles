add_library('serial')
add_library('sound')
add_library('oscP5')

import math
import time

class Toggle(object):
	def __init__(self):
		self.xPos = width/2
		self.yPos = height/2
		self.size = 260
		self.color = 255
		self.on = 0
		self.text = 'Start'
		# self.textsize = 32

	def display(self):
		fill(self.color)
		noStroke()
		ellipse(self.xPos, self.yPos, self.size, self.size)

		fill(0)
		textSize(int(self.size/4))
		textAlign(CENTER, CENTER)
		text(self.text, self.xPos, self.yPos)

	def overMe(self):
		distance = math.sqrt((mouseX - self.xPos)**2 + (mouseY - self.yPos)**2)
		# ellipse CENTER mode use the third and fourth parameters are its width and height.
		if distance<self.size/2:
			return True
		else:
			return False

	def changeColor(self, color):
		self.color = color

	def changePos(self, xPos, yPos):
		self.xPos = xPos
		self.yPos = yPos

	def changeSize(self, size):
		self.size = size

	def click(self):
		if not self.on:
			self.on = 1
			self.text = 'Stop'
			self.changeColor(100)
			self.changePos(width-30, 50)
			self.changeSize(50)
		else:
			self.on = 0
			self.text = 'Start'
			self.changeColor(255)
			self.changePos(width/2, height/2)
			self.changeSize(260)

class Bottle(object):
    def __init__(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos
        self.width = 100
        self.height = 150
        self.state = 0
        self.color = 40

    def display(self):
        noStroke()
        fill(self.color)
        rect(self.xPos, self.yPos, self.width, self.height, 10)
        rect(self.xPos, self.yPos-self.height/2-20+5, 50, 30, 7)

    def raiseMe(self, color):
        self.yPos = height - self.height/2
        self.state = 1
        self.color = color

    def putDown(self):
        self.yPos = height
        self.state = 0
        self.color = 40

def mouseClicked():
    if start_toggle.overMe():
        start_toggle.click()
        newMessage = OscMessage("/bottles/start_toggle")
    # print('X', mouseX, 'Y', mouseY)
        # send start to Max
        # newMessage.add(start_toggle.on)
        # print(start_toggle.on)
        # print(newMessage.toString())
        # gOscController.send(newMessage, gRemoteDestination)
    # else:
    #     if not left_bottle.state:
    #         # left_bottle.raiseMe(0xFFF05757)
    #         left_bottle.raiseMe(0xFF57DAFC)
    #     else:
    #         left_bottle.putDown()


def keyPressed():
    global kick1
    global kick2
    if start_toggle.on:
        if key=='a' or key=='A':
            kick1.play()
        elif key=='s' or key=='S':
            kick2.play()

def mouseMoved():
    cursor()

def kick_kick_from_port(myPort):
    global kick1
    global kick2
    left_virb = 0
    right_virb = 0
    if myPort.available()>0:
        state_str =  myPort.readStringUntil(10) #10==\n
        if state_str != None and len(state_str) >= 4:
            # usually state_str == (u'L0R0\r\n', 6)
            if 'left_bang' in state_str:
                kick1.play()
                print('kick1')
            if 'right_bang' in state_str:
                kick2.play()
                print('kick2')

def setup():
    global start_toggle
    # global gOscController
    # global gRemoteDestination
    global chord
    global bands
    global fft
    global amp
    global left_bottle
    global right_bottle
    global kick1
    global kick2
    global kick1_timestamp
    global kick2_timestamp
    global chord_start_time
    global chord_duration
    global IF_USE_ARDUINO
    global myPort 
    global start_img

    fullScreen()
    # size(640,640) # for test

    start_toggle = Toggle()
    imageMode(CENTER)
    start_img = loadImage("bottles_start.jpeg")
    start_img.resize(0,height)

    # set OSP to communicate with Max------------------------------------
    # gOscReceivePort = 12001  # Port to receive messages on
    # gOscTransmitHost = "127.0.0.1"  # Host to send messages to
    # gOscTransmitPort = 12000       # Port to send messages to
    # gOscController = OscP5(this, gOscReceivePort)
    # gRemoteDestination = NetAddress(gOscTransmitHost, gOscTransmitPort)

    chord = SoundFile(this, 'lofichords.wav') # lofichords.wav or lofi_with_drums.mp3
    kick1 = SoundFile(this, 'drum1.mp3')
    kick2 = SoundFile(this, 'drum2.mp3')

    bands = 64
    fft = FFT(this, bands)
    fft.input(chord)
    amp = Amplitude(this)
    amp.input(chord)

    ellipseMode(CENTER)

    left_bottle = Bottle(width/2-300, height)
    right_bottle = Bottle(width/2+300, height)

    kick1_timestamp = [0,1873,2993,4864,5990, 7864, 8990,  10864]
    kick2_timestamp= [740, 2244, 3739, 5238, 6737, 8239, 9739, 11240]
    chord_start_time = 0
    chord_duration = chord.duration()*1000
    # print('chord_duration', chord_duration)
    IF_USE_ARDUINO = True

    if IF_USE_ARDUINO:
        # portName = Serial.list()[len(Serial.list()) - 1]
        portName = u'/dev/tty.usbmodem14101'
        myPort = Serial(this, portName, 9600)


def draw():
    global start_toggle
    global left_bottle, right_bottle
    global myPort
    global IF_USE_ARDUINO
    global start_img

    background(10)
    kick1_d = 240
    kick2_d = 160
    start_toggle.display()
    if start_toggle.on:
        noCursor()
        draw_spec_amp()
        left_bottle.display()
        right_bottle.display()
        if_kick1, if_kick2 = if_raise_bottle(kick1_d, kick2_d)
        if if_kick1:
            left_bottle.raiseMe(0xFF57DAFC)
        else:
            left_bottle.putDown()
        if if_kick2:
            right_bottle.raiseMe(0xFFF05757)
        else:
            right_bottle.putDown()
        
        if IF_USE_ARDUINO:
            kick_kick_from_port(myPort)
    else:
        if chord.isPlaying():
            chord.stop()
        cursor()
        image(start_img, width/2, height/2)


def if_raise_bottle(kick1_d, kick2_d):
    global chord_start_time
    global chord_duration
    global kick1_timestamp
    global kick2_timestamp

    if_kick1 = False
    if_kick2 = False
    time_now = time.time()
    time_2_know = 100
    chord_pos = round((time_now - chord_start_time)*1000)%chord_duration
    for ks in kick1_timestamp:
        if chord_pos>ks-time_2_know and chord_pos<ks+kick1_d:
            if_kick1 = True
            break
    for hs in kick2_timestamp:
        if chord_pos>hs-time_2_know and chord_pos<hs+kick2_d:
            if_kick2 = True
            break
    return if_kick1, if_kick2


def draw_spec_amp():
    global chord
    global chord_start_time

    if not chord.isPlaying():
        chord.loop()
        chord_start_time = time.time()

    spectrum = fft.analyze()
    spectrum_2_show = spectrum[:32]
    rectMode(CENTER)
    colorMode(HSB)
    num_bars = len(spectrum_2_show)
    for i in range(num_bars):
        barWidth = width / num_bars
        xPos = barWidth * i
        c = 255 / num_bars * i
        fill(c, 100, 100);
        rect(xPos, height/2, barWidth-5, spectrum[i]*(height/2-50))
    
    # Get Volume
    vol  = amp.analyze()

    #volume indicator for center, left, right speaker 
    noStroke()
    fill(40)
    # ellipse(width/2,    height/2,  200*vol,   200*vol)
    # ellipse(width/2-400,height/2, 200*vol,   200*vol)
    ellipse(width/2+400,height/2, 200*vol,  200*vol)





    
    
