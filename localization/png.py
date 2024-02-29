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

while True:
    # Read the current frame from the video
    ret, frame = video.read()
    if not ret:
        break

    # Convert to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create masks for pink and green
    mask_pink = cv2.inRange(hsv, lower_pink, upper_pink)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # Find contours for each color
    contours_pink, _ = cv2.findContours(mask_pink, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find centers of the largest contour for each color
    center_pink = find_center_of_largest_contour(contours_pink)
    center_green = find_center_of_largest_contour(contours_green)

    # Draw the center for each object
    if center_pink:
        cv2.circle(frame, center_pink, 5, (255, 0, 255), -1)  # Pink color
    if center_green:
        cv2.circle(frame, center_green, 5, (0, 255, 0), -1)  # Green color

    # Calculate and display the distance between the two centers
    if center_pink and center_green:
        distance = calculate_distance(center_pink, center_green)
        cv2.line(frame, center_pink, center_green, (0, 255, 0), 2)
        cv2.putText(frame, f"{distance:.2f}", (int((center_pink[0] + center_green[0]) / 2), int((center_pink[1] + center_green[1]) / 2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Frame', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release everything when done
video.release()
cv2.destroyAllWindows()
