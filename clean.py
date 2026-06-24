import cv2
import numpy as np
import os

input_folder = r"D:\ProjectX\T1\X task 1 Windows\mazes"
output_folder = r"D:\ProjectX\T1\X task 1 Windows\cleaned"
os.makedirs(output_folder, exist_ok=True)
for filename in os.listdir(input_folder):
    if not filename.lower().endswith(".png"):
        continue
    input_path = os.path.join(input_folder, filename)
    img = cv2.imread(input_path)
    if img is None:
        continue
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower1 = np.array([0, 100, 100])
    upper1 = np.array([10, 255, 255])
    lower2 = np.array([170, 100, 100])
    upper2 = np.array([180, 255, 255])
    mask1 = cv2.inRange(hsv, lower1, upper1)
    mask2 = cv2.inRange(hsv, lower2, upper2)
    mask = cv2.bitwise_or(mask1, mask2)
    cv2.imwrite(os.path.join(output_folder, filename), mask)
    print(f"Processed {filename}")