#
#NB use python3 to avoid issue with osc
#
import argparse
import threading
import RPi.GPIO as GPIO, time
from datetime import datetime
from enum import Enum

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

dialHasFinishedRotatingAfterMs = 100000 #100 in millisecond 
debounceDelay = 10000 # 10 in millisecond

class Sound(Enum):
    FREE_LINE = 0
    WRONG_LINE = 1
    AUDIO_0 = 2
    AUDIO_1 = 3
    AUDIO_2 = 4
    AUDIO_3 = 5
    AUDIO_4 = 6
    AUDIO_5 = 7
    AUDIO_6 = 8
    AUDIO_7 = 9
    AUDIO_8 = 10
    AUDIO_9 = 11
    NO_SOUND = 12

def playLoop(channel,content,waitPlay):
    
    global buttonUP

    loop = True
    channel.play(content)
    while channel.get_busy() and loop:
        pygame.time.wait(waitPlay)  #  wait in ms
        lock.acquire()
        try:
            loop = buttonUP 
        finally:
            lock.release()
    channel.stop()

def soundHandling(lock,stop_event):
    print("Initialize play thread")
    WAIT_PLAY = 1000
    #set up the mixer
    freq = 44100     # audio CD quality
    bitsize = -16    # unsigned 16 bit
    channels = 1     # 1 is mono, 2 is stereo
    buffer = 2048    # number of samples (experiment to get right sound)
    pygame.mixer.init(freq, bitsize, channels, buffer)
    pygame.mixer.init() #Initialize Mixer
    pygame.mixer.set_num_channels(13)

    #https://stackoverflow.com/questions/35805896/multiple-audio-files-running-on-raspberry
    freeLine = pygame.mixer.Sound("LineaLibera.wav")
    freeLine_ch = pygame.mixer.Channel(1)
    freeLine.set_volume(1.0)

    wrongNumber = pygame.mixer.Sound("LineaCaduta.wav")
    wrongNumber_ch = pygame.mixer.Channel(2)
    wrongNumber.set_volume(1.0)

    audio0 = pygame.mixer.Sound("audio0.wav")
    audio0_ch = pygame.mixer.Channel(3)
    audio0.set_volume(1.0)

    audio1 = pygame.mixer.Sound("audio1.wav")
    audio1_ch = pygame.mixer.Channel(4)
    audio1.set_volume(1.0)

    audio2 = pygame.mixer.Sound("audio2.wav")
    audio2_ch = pygame.mixer.Channel(5)
    audio2.set_volume(1.0)

    audio3 = pygame.mixer.Sound("audio3.wav")
    audio3_ch = pygame.mixer.Channel(6)
    audio3.set_volume(1.0)

    audio4 = pygame.mixer.Sound("audio4.wav")
    audio4_ch = pygame.mixer.Channel(7)
    audio4.set_volume(1.0)

    audio5 = pygame.mixer.Sound("audio5.wav")
    audio5_ch = pygame.mixer.Channel(8)
    audio5.set_volume(1.0)

    audio6 = pygame.mixer.Sound("audio6.wav")
    audio6_ch = pygame.mixer.Channel(9)
    audio6.set_volume(1.0)

    audio7 = pygame.mixer.Sound("audio7.wav")
    audio7_ch = pygame.mixer.Channel(10)
    audio7.set_volume(1.0)

    audio8 = pygame.mixer.Sound("audio8.wav")
    audio8_ch = pygame.mixer.Channel(11)
    audio8.set_volume(1.0)

    audio9 = pygame.mixer.Sound("audio9.wav")
    audio9_ch = pygame.mixer.Channel(12)
    audio9.set_volume(1.0)

    isPlay = False

    global soundToPlay
    global buttonUP

    print("Play thread Loop")
    while not stop_event.is_set():
        lock.acquire()
        try:
            #print("Update Params")
            _buttonUP = buttonUP
            _soundToPlay = soundToPlay 
        finally:
            #print("Release Params")
            lock.release()

        if _buttonUP:
            if _soundToPlay == Sound.FREE_LINE :
                if not isPlay:
                    #print("Play freeLine")
                    isPlay = True
                    playLoop(freeLine_ch,freeLine,WAIT_PLAY)
                    #print("Finish play freeLine")
                    isPlay = False
                else:
                    pass
            if _soundToPlay == Sound.NO_SOUND:
                freeLine_ch.stop()
                isPlay = False
            if _soundToPlay == Sound.AUDIO_0:
                if not isPlay:
                    isPlay = True
                    playLoop(audio0_ch,audio0,WAIT_PLAY)
                    lock.acquire()
                    try:
                        soundToPlay = Sound.NO_SOUND 
                    finally:
                        lock.release()
                    isPlay = False
                else:
                    pass
            else:
                pass

            if _soundToPlay == Sound.AUDIO_1:
                if not isPlay:
                    isPlay = True
                    playLoop(audio1_ch,audio1,WAIT_PLAY)
                    lock.acquire()
                    try:
                        soundToPlay = Sound.NO_SOUND 
                    finally:
                        lock.release()
                    isPlay = False
                else:
                    pass
            else:
                pass

            if _soundToPlay == Sound.AUDIO_2:
                if not isPlay:
                    isPlay = True
                    playLoop(audio2_ch,audio2,WAIT_PLAY)
                    lock.acquire()
                    try:
                        soundToPlay = Sound.NO_SOUND 
                    finally:
                        lock.release()
                    isPlay = False
                else:
                    pass
            else:
                pass
            
            if _soundToPlay == Sound.AUDIO_3:
                if not isPlay:
                    isPlay = True
                    playLoop(audio3_ch,audio3,WAIT_PLAY)
                    lock.acquire()
                    try:
                        soundToPlay = Sound.NO_SOUND 
                    finally:
                        lock.release()
                    isPlay = False
                else:
                    pass
            else:
                pass

            if _soundToPlay == Sound.AUDIO_4:
                if not isPlay:
                    isPlay = True
                    playLoop(audio4_ch,audio4,WAIT_PLAY)
                    lock.acquire()
                    try:
                        soundToPlay = Sound.NO_SOUND 
                    finally:
                        lock.release()
                    isPlay = False
                else:
                    pass
            else:
                pass

            if _soundToPlay == Sound.AUDIO_5:
                if not isPlay:
                    isPlay = True
                    playLoop(audio5_ch,audio5,WAIT_PLAY)
                    lock.acquire()
                    try:
                        soundToPlay = Sound.NO_SOUND 
                    finally:
                        lock.release()
                    isPlay = False
                else:
                    pass
            else:
                pass

            if _soundToPlay == Sound.AUDIO_6:
                if not isPlay:
                    isPlay = True
                    playLoop(audio6_ch,audio6,WAIT_PLAY)
                    lock.acquire()
                    try:
                        soundToPlay = Sound.NO_SOUND 
                    finally:
                        lock.release()
                    isPlay = False
                else:
                    pass
            else:
                pass

            if _soundToPlay == Sound.AUDIO_7:
                if not isPlay:
                    isPlay = True
                    playLoop(audio7_ch,audio7,WAIT_PLAY)
                    lock.acquire()
                    try:
                        soundToPlay = Sound.NO_SOUND 
                    finally:
                        lock.release()
                    isPlay = False
                else:
                    pass
            else:
                pass

            if _soundToPlay == Sound.AUDIO_8:
                if not isPlay:
                    isPlay = True
                    playLoop(audio8_ch,audio8,WAIT_PLAY)
                    lock.acquire()
                    try:
                        soundToPlay = Sound.NO_SOUND 
                    finally:
                        lock.release()
                    isPlay = False
                else:
                    pass
            else:
                pass

            if _soundToPlay == Sound.AUDIO_9:
                if not isPlay:
                    isPlay = True
                    playLoop(audio9_ch,audio9,WAIT_PLAY)
                    lock.acquire()
                    try:
                        soundToPlay = Sound.NO_SOUND 
                    finally:
                        lock.release()
                    isPlay = False
                else:
                    pass
            else:
                pass

            if _soundToPlay == Sound.WRONG_LINE:
                if not isPlay:
                    #print("Play wrongNumber")
                    isPlay = True
                    playLoop(wrongNumber_ch,wrongNumber,WAIT_PLAY)
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
    print("Play thread Loop exit")

def millis():
	return datetime.now().microsecond
    #return int(round(time.time() * 1000))

def event_lock_holder(lock,events,delay):
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
global buttonUP
global numberIsNotInsered
global soundToPlay

events = 0
targetProject = ""
buttonUP = False
soundToPlay = Sound.FREE_LINE

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
                soundToPlay = Sound.FREE_LINE
            finally:
                #print("Release isWrongNumber")
                lock_play.release()
            
            if len(targetProject) != 0:
                print("reset number %s" % (targetProject))
                targetProject=""
                
        elif soundToPlay != Sound.WRONG_LINE:

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
                    
                    number = (count%10)
                    #if(number < 0):
                    #    number = 9
                    targetProject += str(number)
                    print("Count is %d ,Target project is %s" % (count, targetProject))
                    path = ""
                    sendMessage = False
                    number = 0

                    lenTargetProject = len(targetProject)

                    if(lenTargetProject > 0):
                        lock_play.acquire()
                        try:
                            soundToPlay = Sound.NO_SOUND
                        finally:
                            #print("Release isWrongNumber")
                            lock_play.release()

                    #print("lenTargetProject %d" % (lenTargetProject))
                    if( lenTargetProject == TEL_NUM_LENGTH):
                        print(targetProject)
                        if( targetProject.find("11") > 5):
                            path = videoPaths(0)
                            sendMessage = True
                            number = 81#Q
                            _soundToPlay = Sound.AUDIO_0
                        if( targetProject.find("54") > 5):
                            path = videoPaths(1)
                            sendMessage = True
                            number = 87#W
                            _soundToPlay = Sound.AUDIO_1
                        if( targetProject.find("65") > 5):
                            path = videoPaths(2)
                            sendMessage = True
                            number = 69#E
                            _soundToPlay = Sound.AUDIO_2
                        if( targetProject.find("76") > 5):
                            path = videoPaths(3)
                            sendMessage = True
                            number = 82#R
                            _soundToPlay = Sound.AUDIO_3
                        if( targetProject.find("12") > 5):
                            path = videoPaths(4)
                            sendMessage = True
                            number = 84#T
                            _soundToPlay = Sound.AUDIO_4
                        if( targetProject.find("53") > 5):
                            path = videoPaths(5)
                            sendMessage = True
                            number = 89#Y
                            _soundToPlay = Sound.AUDIO_5
                        if( targetProject.find("25") > 5):
                            path = videoPaths(6)
                            sendMessage = True
                            number = 85#U
                            _soundToPlay = Sound.AUDIO_6 
                        if( targetProject.find("21") > 5):
                            path = videoPaths(7)
                            sendMessage = True
                            number = 73#I
                            _soundToPlay = Sound.AUDIO_7
                        if( targetProject.find("15") > 5):
                            path = videoPaths(8)
                            sendMessage = True
                            number = 65#A
                            _soundToPlay = Sound.AUDIO_8
                        if( targetProject.find("34") > 5):
                            path = videoPaths(9)
                            sendMessage = True
                            number = 83#S
                            _soundToPlay = Sound.AUDIO_9

                        print("TargetProject reset %s" % (targetProject))  
                        targetProject = ""
                        
                        if sendMessage:
                            print( "/play " + path[0] )
                            client.send_message("/play", path[0] )
                            client_pc.send_message("/play", number)
                            lock_play.acquire()
                            try:
                                soundToPlay = _soundToPlay
                            finally:
                                lock_play.release()
                            threading.Thread(target=event_lock_holder, args=(lock,events,path[1]), name='eventLockHolder').start()
                        else:
                            #print("Lock isWrongNumber")
                            lock_play.acquire()
                            try:
                                soundToPlay = Sound.WRONG_LINE
                            finally:
                                #print("Release isWrongNumber")
                                lock_play.release()

                    needToPrint = 0
                    count = 0

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
    print("Start Closing")
    sound_thread.join()
    print("Closed")
