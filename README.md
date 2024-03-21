# Invisible Bruin 
Welcome to Invisible Bruin! This file contains the documentation of our game and its various components. 

## Environment
Run the following commands to install all packages required to run our game: 
```
conda install pip
conda install numpy pandas
conda install -c conda-forge opencv
pip install paho-mqtt
pip install pyaudio
pip install SpeechRecognition
```

## Main Game Logic
Run `python3 main.py` to play a text-based version of our game. Other components of our game (e.g. speech, gesture, etc.) will be integrated into the game soon. 

## Localization 
Our most recent localization approach involves calculating the ratio between the distance between the catcher and the target and a reference distance. This helps us decide if the catcher is close enough to the target when a catch gesture is performed. To run this script, do `cd localization` and `python3 ratio2.py`. 
Other files in the localizaiton folder contains incremental development history and other functions used in localization, such as determining the locations of and the distances between color blocks. 

## Speech Recognition
To run our most recent speech recognition script, do `cd Speech_Recognition` and `python3 speech_reco_test.py`. 

## Gesture Recognition and Remote Interaction 
`gesture_test.py` is our script that receives data from the IMU and classifies our catch gesture. `imu_mqtt.ino` is the script that is uploaded to our microcontroller and sends back IMU data. `mqtt_sub.py` is a generic subscriber that we use when we want to see the raw data sent back by the microcontroller. 