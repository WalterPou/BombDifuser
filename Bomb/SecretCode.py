import pyfirmata as pyf
import pyttsx3
import random
import time
import winsound
import threading
from pygame import mixer

# Initialize game settings
Code = [1, 2, 3]
random.shuffle(Code)
#print(f"Bomb code: {Code}")

# Initialize text-to-speech engine
engine = pyttsx3.init()
rate = engine.getProperty('rate')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate',150)

# Setup Arduino connection
COM = int(input('COM: '))
board = pyf.Arduino(f'COM{COM}')
print(f'Using {board} as Arduino Device.')

pin_9 = board.get_pin('d:9:i')  # Button 1
pin_8 = board.get_pin('d:8:i')  # Button 2
pin_7 = board.get_pin('d:7:i')  # Button 3

iterator = pyf.util.Iterator(board)
iterator.start()

def Beep():
    global noise
    noise = True
    while noise:
        winsound.Beep(500,150)
        time.sleep(1.5)

def Defused():
    winsound.Beep(1200, 150)
    winsound.Beep(1200, 150)
    global noise
    noise = False
    engine.setProperty('rate',150)
    message = 'Bomb has been defused! Mission Successful!'
    print(message)
    engine.say(message)
    engine.runAndWait()
    play = 'Pin 8 to play again..'
    print(play)
    engine.say(play)
    engine.runAndWait()
    while True:
        if pin_8.read() == 1:
            random.shuffle(Code)
            #print(Code)
            winsound.Beep(1200, 150)
            winsound.Beep(1200, 150)
            break
    global mem
    global Codes
    global temp
    global data
    global level
    global user_inputs
    mem = []
    Codes = []
    temp = 0
    data = [1,2,3]
    level = 1
    user_inputs = []
    main()

def Explode():
    winsound.Beep(1200, 150)
    winsound.Beep(1200, 150)
    winsound.Beep(1200, 150)
    global noise
    noise = False
    mixer.init()
    mixer.music.load('Explode.mp3')
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(0.5)
    engine.setProperty('rate',150)
    message = 'Bomb exploded! Mission Failed.'
    print(message)
    engine.say(message)
    engine.runAndWait()
    play = 'Pin 8 to play again..'
    print(play)
    engine.say(play)
    engine.runAndWait()
    global mem
    global Codes
    global temp
    global data
    global level
    global user_inputs
    mem = []
    Codes = []
    temp = 0
    data = [1,2,3]
    level = 1
    user_inputs = []
    while True:
        if pin_8.read() == 1:
            random.shuffle(Code)
            #print(Code)
            winsound.Beep(1200, 150)
            winsound.Beep(1200, 150)
            mem = []
            break
    main()

def main():
    global max_attempts
    engine.setProperty('rate',150)
    engine.say('Bomb has been planted.')
    engine.runAndWait()
    thread = threading.Thread(target=Beep)
    thread.start()
    attempts = 0
    max_attempts = 8
    #print(Code)
    engine.setProperty('rate',300)
    while True:
        time.sleep(1)
        user_input = []
        pin_9_state = False
        pin_8_state = False
        pin_7_state = False
        state = True
        while state == True:
            if pin_9_state == False:
                if pin_9.read() == 1:
                    user_input.append(3)
                    print(user_input)
                    winsound.Beep(1250, 150)
                    #engine.say('3')
                    #engine.runAndWait()
                    pin_9_state = True
            if pin_8_state == False:
                if pin_8.read() == 1:
                    user_input.append(2)
                    print(user_input)
                    winsound.Beep(1000, 150)
                    #engine.say('2')
                    #engine.runAndWait()
                    pin_8_state = True
            if pin_7_state == False:
                if pin_7.read() == 1:
                    user_input.append(1)
                    print(user_input)
                    winsound.Beep(750, 150)
                    #engine.say('1')
                    #engine.runAndWait()
                    pin_7_state = True
            if len(user_input) == len(Code):
                if user_input == Code:
                    winsound.Beep(1200, 150)
                    winsound.Beep(1200, 150)
                    winsound.Beep(1200, 150)
                    state = False
                    time.sleep(1.5)
                    engine.setProperty('rate',150)
                    engine.say('Section One passed. Finished the next sequence, remember the patterns.')
                    engine.runAndWait()
                    Sequence2()
                else:
                    attempts += 1
                    engine.setProperty('rate',150)
                    print(f"Incorrect code. You have {max_attempts - attempts} attempts left.")
                    winsound.Beep(1200, 150)
                    winsound.Beep(1200, 150)
                    #engine.say(f'Invalid Code! {max_attempts- attempts} left.')
                    #engine.runAndWait()
                    engine.setProperty('rate',300)
                    break

        if attempts >= max_attempts:
            Explode()

import os

data = [1,2,3]
user_inputs = []
level = 1
temp = 0
Codes = []
mem = []

def Sequence2():
    global user_inputs
    global data
    global Codes
    global temp
    global level
    global mem
    engine.setProperty('rate',150)
    time.sleep(0.5)
    while True:
        if len(Codes) != level:
            random.shuffle(data)
            Codes.append(data[0])
            mem.append(data[0])
        else:
            break
    i = 0
    while True:
        if Codes[i] == 1:
            os.system('cls')
            print(f'Code : {Codes[i]}')
            winsound.Beep(750,150)
        if Codes[i] == 2:
            os.system('cls')
            print(f'Code : {Codes[i]}')
            winsound.Beep(1000,150)
        if Codes[i] == 3:
            os.system('cls')
            print(f'Code : {Codes[i]}')
            winsound.Beep(1250,150)
        time.sleep(0.25)
        i += 1
        if i == len(Codes):
            break
    os.system('cls')
    print('Code : ')

    while len(user_inputs) != len(Codes):
        #print(Code)
        if pin_7.read() == 1:
            user_inputs.append(1)
            os.system('cls')
            print(f'Code : {user_inputs}')
            winsound.Beep(750, 150)
            time.sleep(0.25)
        if pin_8.read() == 1:
            user_inputs.append(2)
            os.system('cls')
            print(f'Code : {user_inputs}')
            winsound.Beep(1000, 150)
            time.sleep(0.25)
        if pin_9.read() == 1:
            user_inputs.append(3)
            os.system('cls')
            print(f'Code : {user_inputs}')
            winsound.Beep(1250, 150)
            time.sleep(0.25)
    if user_inputs == Codes:
        if level == 10:
            engine.setProperty('rate',150)
            Defused()
        else:
            level += 1
            temp = 0
            user_inputs = []
            Sequence2()
    else:
        Explode()

if __name__ == "__main__":
    engine.setProperty('rate',150)
    engine.say('Press pin 8 to activate bomb.')
    engine.runAndWait()
    while True:
        if pin_8.read() == 1:
            winsound.Beep(1200, 150)
            winsound.Beep(1200, 150)
            main()
