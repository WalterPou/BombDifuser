import pyfirmata as pyf
import pyttsx3
import random
import time
import winsound

# Initialize game settings
Code = [1, 2, 3]
random.shuffle(Code)
#print(f"Bomb code: {Code}")

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Setup Arduino connection
COM = int(input('COM: '))
board = pyf.Arduino(f'COM{COM}')
print(f'Using {board} as Arduino Device.')

pin_9 = board.get_pin('d:9:i')  # Button 1
pin_8 = board.get_pin('d:8:i')  # Button 2
pin_7 = board.get_pin('d:7:i')  # Button 3

iterator = pyf.util.Iterator(board)
iterator.start()

def Defused():
    message = 'Bomb has been defused! Mission Successful!'
    print(message)
    engine.say(message)
    engine.runAndWait()
    Play = int(input('Do you want to play again? 0/1: '))
    if Play == 1:
        random.shuffle(Code)
        #print(Code)
        main()

def Explode():
    winsound.Beep(1200, 150)
    winsound.Beep(1200, 150)
    winsound.Beep(1200, 150)
    message = 'Bomb exploded! Mission Failed.'
    print(message)
    engine.say(message)
    engine.runAndWait()
    Play = int(input('Do you want to play again? 0/1: '))
    if Play == 1:
        random.shuffle(Code)
        #print(Code)
        main()

def main():
    attempts = 0
    max_attempts = 5
    while True:
        time.sleep(1.5)
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
                    winsound.Beep(750, 150)
                    pin_9_state = True
            if pin_8_state == False:
                if pin_8.read() == 1:
                    user_input.append(2)
                    print(user_input)
                    winsound.Beep(750, 150)
                    pin_8_state = True
            if pin_7_state == False:
                if pin_7.read() == 1:
                    user_input.append(1)
                    print(user_input)
                    winsound.Beep(750, 150)
                    pin_7_state = True
            if len(user_input) == 3:
                if user_input == Code:
                    winsound.Beep(1200, 150)
                    winsound.Beep(1200, 150)
                    winsound.Beep(1200, 150)
                    Defused()
                    break
                else:
                    attempts += 1
                    print(f"Incorrect code. You have {max_attempts - attempts} attempts left.")
                    winsound.Beep(1200, 150)
                    winsound.Beep(1200, 150)
                    state = False

        if attempts == max_attempts:
            Explode()

if __name__ == "__main__":
    main()
