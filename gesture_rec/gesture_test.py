# import paho.mqtt.client as mqtt
# import time
# import json

# data = []

# def on_connect(client, userdata, flags, rc):
#     print("Connection returned result: " + str(rc))
#     client.subscribe("ece180d/team6/johanna", qos=1)

# # The callback of the client when it disconnects.
# def on_disconnect(client, userdata, rc):
#     if rc != 0:
#         print('Unexpected Disconnect')
#     else:
#         print('Expected Disconnect')

# def on_message(client, userdata, message):
#     mes = message.payload
#     mes_decoded = mes.decode()

#     try:
#         data.append(json.loads(mes_decoded))
#         print(data)
#         pos_z = False 
#         neg_z = False 
#         if len(data) > 10:
#             data.pop(0)
#             forward = all(sample['acceleration']['x'] > 70 for sample in data[-5:])
#             up = all(sample['acceleration']['z'] < 980 for sample in data[-5:])
#             circle = all(sample['gyroscope']['x'] > 10 for sample in data[-5:]) or all(sample['gyroscope']['x'] < -10 for sample in data[-5:])
#             pos_z = any(sample['acceleration']['z'] > 900 for sample in data[-10:])
#             neg_z = any(sample['acceleration']['z'] < -900 for sample in data[-10:])
#             turn = pos_z and neg_z
#             idle = all(sample['acceleration']['x']< 50 
#                        and sample['acceleration']['y'] < 50 
#                        and sample['acceleration']['z'] > 990 
#                        and sample['acceleration']['z'] < 1030 for sample in data[-5:])

#             # if forward:
#             #     print("forward")
#             # if up:
#             #     print("up")
#             if circle and turn:
#                 print("invert")
#             elif circle:
#                 print("circle")
#             elif turn:
#                 print("turn")
#             # if idle:
#             #     print("idle")
#             # else:
#             #     print("haha")

#     except json.JSONDecodeError as e:
#         print(f"Error decoding JSON: {e}")


# client = mqtt.Client()
# client.on_connect = on_connect
# client.on_disconnect = on_disconnect
# client.on_message = on_message

# client.connect_async('mqtt.eclipseprojects.io')
# client.loop_start()

# while True: 
#     pass

# client.loop_stop()
# client.disconnect()

import paho.mqtt.client as mqtt
import time
import json
import numpy as np

data = []
process_data = True  # Control flag to enable/disable data processing

def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    client.subscribe("ece180d/team6/johanna", qos=1)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')

def on_message(client, userdata, message):
    global process_data  # Refer to the global variable
    if not process_data:  # Check if processing is disabled
        return  # Skip processing if disabled

    mes = message.payload
    mes_decoded = mes.decode()

    try:
        data.append(json.loads(mes_decoded))
        # Save data to file
        with open('imu_data.txt', 'a') as file:
            file.write(mes_decoded + '\n')
        pos_z = False 
        neg_z = False 
        if len(data) > 10:
            data.pop(0)
            # forward = all(sample['acceleration']['x'] > 70 for sample in data[-5:])
            # up = all(sample['acceleration']['z'] < 980 for sample in data[-5:])
            # circle = all(sample['gyroscope']['x'] > 10 for sample in data[-5:]) or all(sample['gyroscope']['x'] < -10 for sample in data[-5:])
            pos_z = any(sample['acceleration']['z'] > 850 for sample in data[-5:])
            neg_z = any(sample['acceleration']['z'] < -850 for sample in data[-5:])
            turn = pos_z and neg_z
            # idle = all(sample['acceleration']['x']< 50 
            #            and sample['acceleration']['y'] < 50 
            #            and sample['acceleration']['z'] > 990 
            #            and sample['acceleration']['z'] < 1030 for sample in data[-5:])

            if turn:
                print("-----------------Catch!!----------------------------")
                process_data = False  # Disable further data processing
                data.clear()
                with open('imu_data.txt', 'a') as file:
                    file.write("--------------A catch detected------------"+ '\n')
                process_data = True
                # Call OpenCV function here, if needed

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.connect_async('mqtt.eclipseprojects.io')
client.loop_start()

try:
    while True: 
        time.sleep(1)  # Avoids a busy-wait loop, allowing for keyboard interrupt
except KeyboardInterrupt:
    print("Disconnected by user")
finally:
    client.loop_stop()
    client.disconnect()
