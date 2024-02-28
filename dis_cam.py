import cv2
import numpy as np

# Function to find the center of the largest contour in the mask
def find_center_of_largest_contour(contours):
    if contours:
        # Sort the contours by area and grab the largest one
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)
        if M["m00"] > 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            return (cX, cY)
    return None

# Function to calculate the distance between two points
def calculate_distance(point1, point2):
    distance = np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
    return distance

# Start capturing video
video = cv2.VideoCapture(0)

# Define the color range for pink in HSV
lower_pink = np.array([140, 100, 100])
upper_pink = np.array([180, 255, 255])

# Define the color range for green in HSV
lower_green = np.array([40, 100, 100])
upper_green = np.array([80, 255, 255])

# Initialize known parameters for distance calculation
KNOWN_WIDTH = 11.0  # Known object width of the pink object (in inches)
KNOWN_DISTANCE_PINK = 24.0  # Known distance from the camera to the pink object (in inches)

while True:
    # Read the current frame from the video
    ret, frame = video.read()
    if not ret:
        break

    # Convert to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create mask for pink
    mask_pink = cv2.inRange(hsv, lower_pink, upper_pink)

    # Find contours for pink
    contours_pink, _ = cv2.findContours(mask_pink, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find center of the largest contour for pink
    center_pink = find_center_of_largest_contour(contours_pink)

    # Calculate distance between camera and pink object
    if center_pink:
        focalLength_pink = (KNOWN_WIDTH * KNOWN_DISTANCE_PINK) / KNOWN_WIDTH
        distance_pink = (KNOWN_WIDTH * focalLength_pink) / center_pink[0]
        print(f"Distance between camera and pink object: {distance_pink:.2f} inches")

    # Display the resulting frame
    cv2.imshow('Frame', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release everything when done
video.release()
cv2.destroyAllWindows()
