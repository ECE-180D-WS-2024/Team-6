# Import the necessary packages
import numpy as np
import cv2
from imutils import paths

def find_marker(image):
    # Convert the image to grayscale, blur it, and detect edges
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 35, 125)
    
    # Find the contours in the edged image and keep the largest one;
    # we'll assume that this is our piece of paper in the image
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]  # Handling contour finding based on OpenCV version compatibility
    c = max(cnts, key=cv2.contourArea)
    
    # Compute the bounding box of the paper region and return it
    return cv2.minAreaRect(c)

def distance_to_camera(knownWidth, focalLength, perWidth):
    # Compute and return the distance from the marker to the camera
    return (knownWidth * focalLength) / perWidth

# Initialize the known distance from the camera to the object, which
# in this case is 24 inches
KNOWN_DISTANCE = 24.0

# Initialize the known object width, which in this case, the piece of
# paper is 11 inches wide
KNOWN_WIDTH = 11.0

# Load the first image that contains an object that is known to be 2 feet
# from our camera, then find the paper marker in the image, and initialize
# the focal length
image = cv2.imread("/Users/heeohsmacbookpro/Desktop/Team-6/localization/2ft.png")
marker = find_marker(image)
focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH

# Loop over the images
# for imagePath in sorted(paths.list_images("images")):
#     # Load the image, find the marker in the image, then compute the
#     # distance to the marker from the camera
#     image = cv2.imread(imagePath)
#     marker = find_marker(image)
#     inches = distance_to_camera(KNOWN_WIDTH, focalLength, marker[1][0])
    
#     # Draw a bounding box around the image and display it
#     box = cv2.boxPoints(marker) if cv2.__version__.startswith('4') else cv2.cv.BoxPoints(marker)
#     box = np.int0(box)
#     cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
#     cv2.putText(image, "%.2fft" % (inches / 12),
#                 (image.shape[1] - 200, image.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
#                 2.0, (0, 255, 0), 3)
#     cv2.imshow("image", image)
#     cv2.waitKey(0)
