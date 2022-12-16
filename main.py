# Made By The Best, Donovan Whysong!!!

from os import system
import RPi.GPIO as GPIO
import time
import os
import json
import requests
from threading import Thread
import json
import random

getRequestCheck = True

username = ''
password = ''

greenLight = 40
yellowLight = 16
blueLight = 31
redLight = 12

greenBtn = 35
yellowBtn = 37

sensorPin = 11

trigger = False
active = True
sendingLock = False
responseLock = 0
count = 0

webhook_url = ""

serielNumFile = 'serielNum.json'
serielNum = 0

alarmOnlinePassword = ''


def setup():
    GPIO.setmode(GPIO.BOARD)
    
    sendAlarmState('Arm')
    
    #setup lights
    GPIO.setup(greenLight, GPIO.OUT)
    GPIO.setup(yellowLight, GPIO.OUT)
    GPIO.setup(blueLight, GPIO.OUT)
    GPIO.setup(redLight, GPIO.OUT)

    GPIO.output(greenLight, GPIO.LOW)
    GPIO.output(yellowLight, GPIO.LOW)
    GPIO.output(blueLight, GPIO.LOW)
    GPIO.output(redLight, GPIO.LOW)
    
    GPIO.setup(greenBtn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(yellowBtn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(sensorPin, GPIO.IN)

def timedArmed():
    global active
    global count
    global responseLock
    global sendingLock
    sendingLock = True
    
    prYellow('Timing...')
    
    # Turn Off Lights
    GPIO.output(greenLight, GPIO.LOW)
    GPIO.output(yellowLight, GPIO.LOW)
    GPIO.output(blueLight, GPIO.LOW)
    GPIO.output(redLight, GPIO.LOW)
    
    # Turn On Lights
    GPIO.output(greenLight, GPIO.HIGH)
    time.sleep(1.5)
    GPIO.output(yellowLight, GPIO.HIGH)
    time.sleep(1.5)
    GPIO.output(blueLight, GPIO.HIGH)
    time.sleep(1.5)
    GPIO.output(redLight, GPIO.HIGH)
    time.sleep(1.5)
    
    GPIO.output(greenLight, GPIO.LOW)
    time.sleep(1.5)
    GPIO.output(yellowLight, GPIO.LOW)
    time.sleep(1.5)
    GPIO.output(blueLight, GPIO.LOW)
    time.sleep(1.5)
    GPIO.output(redLight, GPIO.LOW)

    sendAlarmState('Arm')
    active = True
    responseLock +=1
    count = 0

def armToggle():
    global active
    global count
    global responseLock
    global sendingLock

    count +=1
    
    sendingLock = True
    
    if count == 1:
        prYellow('Disarming...')
        active = not active
        sendAlarmState('Disarm')
        GPIO.output(yellowLight, GPIO.HIGH)
        responseLock +=1
    elif count == 2:
        prYellow('Arming...')
        active = not active
        sendAlarmState('Arm')
        GPIO.output(yellowLight, GPIO.LOW)
        count = 0
        responseLock +=1

def btns():
    # Green Btn
    if GPIO.input(greenBtn)==GPIO.LOW:
        timedArmed()
    
    # Yellow Btn
    if GPIO.input(yellowBtn) == GPIO.LOW:
        armToggle()


def start():
    while True: 
        btns()
        sensor()

def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk))

def serielNumGnG(request):
    global serielNum
    if (request == 'generate'):
        serielNum = random.randrange(1123446890780000, 1123780283094827587678123908)
        data = {
            'AlarmSys' : [
                {
                    'serielNum' : serielNum
                }
            ]
        }

        if os.path.isfile(serielNumFile):
            prRed('Seriel Number Found, continuing will disconnect you from the QuackyOS network, until you re authorize this device. Are you sure y/n')
            userInput = input()

            if (userInput == 'y'):
                prYellow('Making Seriel Number...')
                with open(serielNumFile, 'w') as outfile:
                    json.dump(data, outfile)
                    prGreen('Seriel Number Created!')
            elif (userInput == 'n'):
                prRed('Canceled!')
            else:
                serielNumGnG('generate')
        else:
            prYellow('Making Seriel Number...')
            with open(serielNumFile, 'w') as outfile:
                    json.dump(data, outfile)
                    prGreen('Seriel Number Created!')
    elif (request == 'get'):
        # Make sure seriel num exist first if not alert user
        if os.path.isfile(serielNumFile):
            with open(serielNumFile) as json_file:
                file_data = json.load(json_file)
                # Get wtf counter
                for row in file_data['AlarmSys']:
                    prGreen('Seriel Number: ' + str(row['serielNum']))
                    serielNum = row['serielNum']
        else:
            prRed("Seriel Number doesnt exist please create one using 'generate seriel'")
            return False
        
def sendAlarmState(getAlarmState):
    global username
    global password
    global serielNum
    global sendingLock
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
        }
        pload = {'pythonUser':username,'pythonPass':password, 'pythonSeriel':serielNum,'request':'updateAlarmTable', 'alarmState':getAlarmState, 'log':'yes'}
        r = requests.post('https://www.quackyos.com/QuackAttack/backend/serverCom.php', data=pload, headers=headers)
        request = str(r.text)
        sendingLock = False
        print(request)
    except:
        prRed("Send Alarm State Fail!")


def getAlarmState():
    global username
    global password
    global serielNum
    global active
    global count
    global responseLock
    global sendingLock
    prGreen('Starting QuackyOS Updates')
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }

    while True:
        if (username != ''):
            try:
                pload = {'pythonUser':username,'pythonPass':password, 'pythonSeriel':serielNum,'request':'updateAlarm'}
                r = requests.post('https://www.quackyos.com/QuackAttack/backend/serverCom.php', data=pload, headers=headers, timeout=10)
                request = str(r.text)

                if (request == 'Arm' and active == False and sendingLock == False):
                    if (responseLock >= 1):
                        sendResponse(username,password,'send','100')
                    armToggle()
                    time.sleep(3)
                    sendResponse(username,password,'send','')
                    
                elif (request == 'Disarm' and active == True and sendingLock == False):
                    if (responseLock >= 1):
                        sendResponse(username,password,'send','100')
                    armToggle()
                    time.sleep(3)
                    sendResponse(username,password,'send','')
                    
                elif (request == 'Timed Arm' and sendingLock == False):
                    if (responseLock >= 1):
                        sendResponse(username,password,'send','100')
                    timedArmed()
                    time.sleep(3)
                    sendResponse(username,password,'send','')
                
                time.sleep(3)
            
            except Exception as e:
                prRed(' ------ Get Alarm State Fail! ' +str(e) + ' ------ ')
                time.sleep(10)
                pass
        

def comServer(username, password, request):
    global serielNum
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
        }
        pload = {'pythonUser':username,'pythonPass':password, 'pythonSeriel':serielNum, 'request':request, 'alarmOnlinePassword':alarmOnlinePassword}
        r = requests.post('https://www.quackyos.com/QuackAttack/backend/serverCom.php',data = pload, headers=headers)
        print(r.text)
    except:
        prRed("Comserver Fail")

def sendResponse(username, password, request, response):
    global serielNum
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
        }
        pload = {'pythonUser':username,'pythonPass':password, 'pythonSeriel':serielNum, 'request':request, 'response':response}
        r = requests.post('https://www.quackyos.com/QuackAttack/backend/response.php',data = pload, headers=headers)
        print(r.text)
    except:
        prRed("Send Response Fail")

def command():
    global username
    global password
    global serielNum

    global alarmOnlinePassword

    commandList = ['help','stop','login','logout','auth','generate seriel','get seriel', 'check connection']

    while True:
        userInput = input()

        if (userInput == 'help'):
            prGreen(commandList)
        elif (userInput == 'stop'):
            prYellow('STOPING...')
            exit()
        elif (userInput == 'login'):
            # Check user login
            prYellow('Username:')
            username = input()
            prYellow('Password:')
            password = input()
            comServer(username, password, 'login')
            sendResponse(username,password,'send','')
            sendAlarmState('Disarm')
            
        elif (userInput == 'logout'):
            username = ''
            password = ''
            prGreen('LOGGED OUT')
        elif (userInput == 'auth'):
            if (username == '' or password == ''):
                prRed('MUST BE LOGGED IN')
            else:
                prYellow('Type An Alarm Passowrd')
                alarmOnlinePassword = input()

                prYellow('AUTHORIZING...')
                
                # post to a auth script on server to check username and password
                if (serielNum == 0):
                    prRed("Seriel Number doesnt exist please create one using 'generate seriel'")
                else:
                    comServer(username, password, 'auth')
        elif (userInput == 'generate seriel'):
            serielNumGnG('generate')
        elif (userInput == 'get seriel'):
            serielNumGnG('get')
        elif (userInput == 'check connection'):
            if (username == '' or password == ''):
                prRed('MUST BE LOGGED IN')
            else:
                comServer(username, password, 'connection')
        else:
            prRed('The command `' + userInput + '` does not exist, type `help` for help')

            
def sensor():
    if GPIO.input(sensorPin)==GPIO.HIGH and active == True:
        GPIO.output(redLight,GPIO.HIGH)
        
        slack_data = {'text': "INTRUDER!"}
        response = requests.post(
            webhook_url, data =json.dumps(slack_data),
            headers={'Content-Type': 'application/json'}
        )
        
        time.sleep(3)
        
        GPIO.output(redLight, GPIO.LOW)

def destroy():
    GPIO.cleanup()                      # Release all GPIO

if __name__ == '__main__':    # Program entrance
    print ('Loading ... \n')
    setup()
    try:
        t1 = Thread(target=start, daemon=True)
        t2 = Thread(target=command, daemon=True)
        update = Thread(target=getAlarmState, daemon=True)
        
        t1.start()
        t2.start()
        update.start()

        print('Welcome To QuackAttack')
        # Load seriel number
        serielNumGnG('get')
        
        t2.join()
        
    except KeyboardInterrupt:   # Press ctrl-c to end the program.
        destroy()