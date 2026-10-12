import cv2
import numpy as np
import os

#################################
frameWidth = 640
frameHeight = 480

# FIX 1: Resolve cascade path relative to this script's location,
#         so the script runs correctly from any working directory.
CASCADE_PATH = os.path.join(os.path.dirname(__file__), 'models', 'haarcascade_russian_plate_number.xml')

nplateCascade = cv2.CascadeClassifier(CASCADE_PATH)
minArea = 500
color = (255, 0, 255)

# FIX 2: Validate that the cascade loaded correctly.
#         CascadeClassifier silently returns an empty object if the file is missing.
if nplateCascade.empty():
    print(f"ERROR: Could not load cascade classifier from: {CASCADE_PATH}")
    print("Make sure haarcascade_russian_plate_number.xml exists in the models/ folder.")
    exit(1)

#####################################
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 100)

while True:
    ret, img = cap.read()

    # FIX 3: Validate the frame was captured successfully.
    #         Without this check, img is None on camera failure and cvtColor crashes.
    if not ret or img is None:
        print("WARNING: Failed to read frame from camera. Retrying...")
        continue

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    numberPlates = nplateCascade.detectMultiScale(img_gray, 1.3, 5)
    for (x, y, w, h) in numberPlates:
        area = w * h
        if area > minArea:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(img, "Number Plate", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 2)
            imgRoi = img[y:y + h, x:x + w]
            cv2.imshow("Number Plate", imgRoi)
    cv2.imshow('Result', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# FIX 4: Release the camera and close all windows on exit.
#         The original script had cap.release() unreachably placed inside the break block.
cap.release()
cv2.destroyAllWindows()
