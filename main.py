# imports 
import paho.mqtt.client as mqtt
import json
import numpy as np
import cv2
import speech_recognition as sr
import pygame
import sys
import os
# from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pycaw

#pygame initialization 
# pygame.init()

# WIDTH, HEIGHT = 800, 600
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Invisible Bruin")

# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# RED = (255, 0, 0)

# font = pygame.font.Font(None, 36)


# # object definitions
client = mqtt.Client()
recognizer = sr.Recognizer()

imu_data = []

def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    client.subscribe("ece180d/team6/johanna", qos=1)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')

def speech_rec():
    with sr.Microphone() as source:
        # Adjusts the recognizer sensitivity to ambient noise
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        # Listen for the first phrase and extract audio data
        audio = recognizer.listen(source)
        
        try:
            # Recognize speech using Google Web Speech API
            results = recognizer.recognize_google(audio, show_all=True)
            
            # Print the entire result just once
            print("result:")
            print(results)
            
            # Assuming we're taking the most likely result, which is the first one
            if results and 'alternative' in results:
                speech_text = results['alternative'][0]['transcript']
            
                print(f"You said: {speech_text}")
            
                # Check for the words 'fast', 'slow', and 'reverse' in the recognized speech
                if "start" in speech_text:
                    print("Start is recognized!")
                if "stop" in speech_text:
                    print("stop is recognized!")
                if "end" in speech_text:
                    print("end  is recognized!")
        except sr.UnknownValueError:
            # API was unable to understand the audio
            print("Google Web Speech API could not understand audio")
        except sr.RequestError as e:
            # API was unreachable or unresponsive
            print(f"Could not request results from Google Web Speech API; {e}")

#game 
bound_x = 9
bound_y = 5

catcher_x = 0
catcher_y = 0

target_x = np.random.randint(0,bound_x)
target_y = np.random.randint(0,bound_y)

def main():
    global catcher_x
    global catcher_y
    # "at each iteration, give each component a chance to do something"
    # 1. check audio for start/pause 
    # 2. receive and process IMU data 
    # 3. analyze distance and adjust feedback volume
    # 4. if a catch is performed, check distance and direction 
    # 5. decide whether the catch is successful 
    print("Welcome to Invisible Bruin!")

    while True: 
        #mimics the microphone that is always listening for verbal input
        print("Would you like to start or stop the game? Press enter if neither. [start/stop/enter]")
        start_or_stop = input()
        if start_or_stop.lower() == "start": 
            pass
        # elif start_or_stop.lower() == "continue":
        #     pass
        elif start_or_stop.lower() == "stop":
            print("Goodbye.")
            exit()
        
        #mimics the catcher's movement 
        print("Enter a coordinate to move to. You can only move by one in any direction")
        print("The limit of the grid is (4, 9)")
        print("You are currently at (" + str(catcher_x) + ", " +  str(catcher_y) + ")")
        catcher_move = input()
        catcher_x = int(catcher_move[0])
        catcher_y = int(catcher_move[2])

        #mimics distance measurement in localization 
        dist = np.sqrt((catcher_x - target_x)**2 + (catcher_y - target_y)**2)

        #mimics the sound volume feedback
        if dist <= 1: 
            print("You are very close")
            # what if the catcher continues playing and overlaps with the target??
        elif dist > 1 and dist <= 3: 
            print ("You are quite close")
        elif dist > 3 and dist <= 7: 
            print ("You are not that close")
        else: 
            print("You are quite far")
        
        #mimics direction recognition
        print("Would you like to perform a catch? [y/n]")
        does_catch = input()
        if does_catch == "y":
            print("Choose a direction to perform a catch [up/right/down/left]")
            catch_dir = input()
            if catch_dir == "up":
                if (catcher_y + 1 != target_y) or dist > 1:
                    print("Sorry, you failed to catch the target")
                    print("The target was at (" + str(target_x) + ", " +  str(target_y) + ")")
                elif dist <= 1:
                    print("Congratulations, you have caught the target!")
                exit()
            elif catch_dir == "down":
                if (catcher_y - 1 != target_y) or dist > 1:
                    print("Sorry, you failed to catch the target")
                    print("The target was at (" + str(target_x) + ", " +  str(target_y) + ")")
                elif dist <= 1:
                    print("Congratulations, you have caught the target!")
                exit()
            elif catch_dir == "left":
                if (catcher_x - 1 != target_x) or dist > 1:
                    print("Sorry, you failed to catch the target")
                    print("The target was at (" + str(target_x) + ", " +  str(target_y) + ")")
                elif dist <= 1:
                    print("Congratulations, you have caught the target!")
                exit()
            elif catch_dir == "right":
                if (catcher_x + 1 != target_x) or dist > 1:
                    print("Sorry, you failed to catch the target")
                    print("The target was at (" + str(target_x) + ", " +  str(target_y) + ")")
                elif dist <= 1:
                    print("Congratulations, you have caught the target!")
                exit()
        elif does_catch == 'n':
            continue   


if __name__ == "__main__":
    main()

