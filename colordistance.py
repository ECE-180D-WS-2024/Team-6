import cv2
import numpy as np

def color_distance(color1, color2):
    return np.sqrt(np.sum((color1 - color2) ** 2))

def main():
    # Define the colors in BGR format
    color1 = np.array([255, 0, 0])  # Blue
    color2 = np.array([0, 0, 255])  # Red

    # Calculate the distance between the colors
    distance = color_distance(color1, color2)

    print("Distance between the colors:", distance)

if __name__ == "__main__":
    main()
