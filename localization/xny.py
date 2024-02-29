import cv2
import numpy as np

def color_distance(color1, color2):
    return np.sqrt(np.sum((color1 - color2) ** 2))

def find_color_points(frame, target_color):
    points = []

    # Convert frame to BGR format (if not already in that format)
    bgr_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Iterate over each pixel in the frame
    for y in range(frame.shape[0]):
        for x in range(frame.shape[1]):
            # Get the color of the current pixel
            pixel_color = bgr_frame[y, x]

            # Calculate the distance between the current color and the target color
            dist = color_distance(pixel_color, target_color)

            # If the distance is below a threshold, consider it a match
            if dist < 50:  # You can adjust this threshold as needed
                points.append((x, y))

    return points

def main():
    # Initialize the webcam
    cap = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Define the target color in BGR format
        target_color = np.array([255, 0, 0])  # Blue

        # Find points with the target color in the frame
        color_points = find_color_points(frame, target_color)

        # Draw circles at the coordinates of the points with the target color
        for point in color_points:
            cv2.circle(frame, point, 5, (0, 255, 0), -1)

        # Display the frame
        cv2.imshow('frame', frame)

        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
