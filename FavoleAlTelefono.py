import argparse
import threading
import RPi.GPIO as GPIO, time
from datetime import datetime

import pygame
from pygame import mixer

GPIO.setmode(GPIO.BCM)

from pythonosc import osc_message_builder
from pythonosc import udp_client

globalVideoPath = "/home/pi/media"
lock = threading.Lock()
lock_play = threading.Lock()

needToPrint = 0
count = 0
PIN_INPUT = 2
BUTTON_PIN = 27
TEL_NUM_LENGTH = 8
GPIO.setup(PIN_INPUT, GPIO.IN)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

lastState = GPIO.LOW
trueState = GPIO.LOW
lastStateChangeTime = 0
cleared = 0

dialHasFinishedRotatingAfterMs = 100000 #100 in millisecond 
debounceDelay = 10000 # 10 in millisecond

def playLoop(channel,content,waitPlay):
    channel.play(content)
    while channel.get_busy():
        pygame.time.wait(waitPlay)  #  wait in ms
        #print("...busy")
    channel.stop()

def soundHandling(lock,stop_event):
    print("Initialize play thread")
    waitPlay = 1000
    #set up the mixer
    freq = 44100     # audio CD quality
    bitsize = -16    # unsigned 16 bit
    channels = 1     # 1 is mono, 2 is stereo
    buffer = 2048    # number of samples (experiment to get right sound)
    pygame.mixer.init(freq, bitsize, channels, buffer)
    pygame.mixer.init() #Initialize Mixer

    #https://stackoverflow.com/questions/35805896/multiple-audio-files-running-on-raspberry
    freeLine = pygame.mixer.Sound("LineaLibera.wav")
    freeLine_ch = pygame.mixer.Channel(1)
    freeLine.set_volume(1.0)

    wrongNumber = pygame.mixer.Sound("LineaCaduta.wav")
    wrongNumber_ch = pygame.mixer.Channel(2)
    wrongNumber.set_volume(1.0)

    isPlay = False

    print("Play thread Loop")
    while not stop_event.is_set():
        lock.acquire()
        try:
            #print("Update Params")
            _buttonUP = buttonUP
            _numberIsNotInsered = numberIsNotInsered
            _wrongNumber = isWrongNumber
        finally:
            #print("Release Params")
            lock.release()

        if _buttonUP:
            if _numberIsNotInsered:
                if not isPlay:
                    #print("Play freeLine")
                    isPlay = True
                    playLoop(freeLine_ch,freeLine,waitPlay)
                    #print("Finish play freeLine")
                    isPlay = False
                else:
                    pass
            else:
                freeLine_ch.stop()
                #print("Finish play freeLine")
                isPlay = False
            if _wrongNumber:
                if not isPlay:
                    #print("Play wrongNumber")
                    isPlay = True
                    playLoop(wrongNumber_ch,wrongNumber,waitPlay)
                    #print("Finish play wrongNumber")
                    isPlay = False
                else:
                    pass
            else:
                pass
        #else:
            #if not _numberIsNotInsered:
            #    print("reset number %s" % (targetProject))
            #    targetProject=""
            #    wrongNumber = False #NB LOCK
            #else:
            #    pass

def millis():
	return datetime.now().microsecond

def event_lock_holder(lock,delay):
    print('Lock.Starting')
    print('events is: {0}'.format(events))
    print('delay is: {0}'.format(delay))    
    
    th_id = 0
    lock.acquire()
    try:
        print("Increase")
        events += 1
        th_id = events
    finally:
        lock.release()
        
    time.sleep(delay)
        
    if events == th_id :
        print("/play "+globalVideoPath+"/Loop.mp4")
        client.send_message("/play", globalVideoPath+"/LOOP-B-Zanuso.mp4" )
    else:
        print('terminated {0}'.format(th_id))
    return

def videoPaths(x):
    return {
       0: [globalVideoPath+"/01-ZANUSO.mp4", 59 ],
       1: [globalVideoPath+"/02-ZANUSO.mp4", 53 ],
       2: [globalVideoPath+"/03-ZANUSO.mp4", 60 ],
       3: [globalVideoPath+"/04-ZANUSO.mp4", 67 ],
       4: [globalVideoPath+"/05-ZANUSO.mp4", 67 ],
       5: [globalVideoPath+"/06-ZANUSO.mp4", 80 ],
       6: [globalVideoPath+"/07-ZANUSO.mp4", 87 ],
       7: [globalVideoPath+"/08-ZANUSO.mp4", 59 ],
       8: [globalVideoPath+"/09-ZANUSO.mp4", 86 ],
       9: [globalVideoPath+"/10-ZANUSO.mp4", 52 ],
    }.get(x, [globalVideoPath+"/00.mp4", 10 ])    # 9 is default if x not found

print('Favole Al Telefono - IdeasBitFactory')
print('Press Ctrl-C to quit.')

parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="192.168.1.3",
    help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=9000,
    help="The port the OSC server is listening on")
args = parser.parse_args()

client = udp_client.SimpleUDPClient(args.ip, args.port)

parser_pc = argparse.ArgumentParser()
parser_pc.add_argument("--ip", default="192.168.1.79",
    help="The ip of the OSC server")
parser_pc.add_argument("--port", type=int, default=15000,
    help="The port the OSC server is listening on")
args_pc = parser_pc.parse_args()

client_pc = udp_client.SimpleUDPClient(args_pc.ip, args_pc.port)

global events
global targetProject
global isWrongNumber
global buttonUP
global numberIsNotInsered

events = 0
targetProject = ""
isWrongNumber = False
buttonUP = False
numberIsNotInsered = True

stop_event = threading.Event()

sound_thread = threading.Thread(target=soundHandling, args=(lock_play,stop_event), name='soundHandling')
sound_thread.start()

try:

    while True:
        if GPIO.input(BUTTON_PIN) == False:
            #print("Lock isWrongNumber")
            lock_play.acquire()
            try:
                buttonUP = False
                isWrongNumber = False
            finally:
                #print("Release isWrongNumber")
                lock_play.release()
            
            if len(targetProject) != 0:
                print("reset number %s" % (targetProject))
                targetProject=""
                lock_play.acquire()
                try:
                    numberIsNotInsered = True
                finally:
                    #print("Release numberIsNotInsered")
                    lock_play.release()
        else:

            #print("Lock buttonUP")
            lock_play.acquire()
            try:
                buttonUP = True
            finally:
                #print("Release buttonUP")
                lock_play.release()

            reading = GPIO.input(PIN_INPUT)

            if ((millis() - lastStateChangeTime) > dialHasFinishedRotatingAfterMs):
                # the dial isn't being dialed, or has just finished being dialed.
                if (needToPrint):
                    # if it's only just finished being dialed, we need to send the number down the serial
                    # line and reset the count. We mod the count by 10 because '0' will send 10 pulses.
                    
                    number = (count%10)-1
                    if(number < 0):
                        number = 9
                    targetProject += str(number)
                    print("Count is %d ,Target project is %s" % (count, targetProject))
                    path = ""
                    sendMessage = False
                    number = 0

                    lenTargetProject = len(targetProject)
                    print("lenTargetProject %d" % (lenTargetProject))
                    if lenTargetProject > 0:
                        #print("Lock numberIsNotInsered")
                        lock_play.acquire()
                        try:
                            numberIsNotInsered = False
                        finally:
                            #print("Release numberIsNotInsered")
                            lock_play.release()
                    if( len(targetProject) == TEL_NUM_LENGTH):
                        print(targetProject)
                        if( targetProject.find("11") > 5):
                            path = videoPaths(0)
                            sendMessage = True
                            number = 81#Q
                        if( targetProject.find("54") > 5):
                            path = videoPaths(1)
                            sendMessage = True
                            number = 87#W
                        if( targetProject.find("65") > 5):
                            path = videoPaths(2)
                            sendMessage = True
                            number = 69#E
                        if( targetProject.find("76") > 5):
                            path = videoPaths(3)
                            sendMessage = True
                            number = 82#R
                        if( targetProject.find("12") > 5):
                            path = videoPaths(4)
                            sendMessage = True
                            number = 84#T
                        if( targetProject.find("53") > 5):
                            path = videoPaths(5)
                            sendMessage = True
                            number = 89#Y
                        if( targetProject.find("25") > 5):
                            path = videoPaths(6)
                            sendMessage = True
                            number = 85#U    
                        if( targetProject.find("21") > 5):
                            path = videoPaths(7)
                            sendMessage = True
                            number = 73#I
                        if( targetProject.find("15") > 5):
                            path = videoPaths(8)
                            sendMessage = True
                            number = 65#A
                        if( targetProject.find("34") > 5):
                            path = videoPaths(9)
                            sendMessage = True
                            number = 83#S

                        print("TargetProject reset %s" % (targetProject))  
                        targetProject = ""

                        if sendMessage:
                            print( "/play " + path[0] )
                            client.send_message("/play", path[0] )
                            client_pc.send_message("/play", number)
                            threading.Thread(target=event_lock_holder, args=(lock,path[1]), name='eventLockHolder').start()
                        else:
                            print("Lock isWrongNumber")
                            lock_play.acquire()
                            try:
                                isWrongNumber = True
                            finally:
                                print("Release isWrongNumber")
                                lock_play.release()

                    needToPrint = 0
                    count = 0
                    cleared = 0

            if (reading != lastState):
                lastStateChangeTime = millis()

            if ((millis() - lastStateChangeTime) > debounceDelay):
                #debounce - this happens once it's stablized
                if (reading != trueState):
                    # this means that the switch has either just gone from closed->open or vice versa.
                    trueState = reading
                    if (trueState == GPIO.HIGH):
                        # increment the count of pulses if it's gone high.
                        count = count + 1; 
                        needToPrint = 1; # we'll need to print this number (once the dial has finished rotating)
            lastState = reading

except (KeyboardInterrupt, SystemExit):
    stop_event.set()
    sound_thread.join()
