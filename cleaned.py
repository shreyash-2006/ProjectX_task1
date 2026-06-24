import cv2
import numpy as np
import os

input_folder = r"D:\ProjectX\T1\X task 1 Windows\cleaned"
output_folder = r"D:\ProjectX\T1\X task 1 Windows\cleaned_final"
os.makedirs(output_folder, exist_ok=True)
for i in range(1, 101):
    filename = f"maze_{i:02d}.png"
    input_path = os.path.join(input_folder, filename)
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Could not read {filename}")
        continue
    _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    kernel = np.ones((5,5), np.uint8)
    clean = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    inv = cv2.bitwise_not(clean)
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(
        inv,
        connectivity=8
    )
    for label in range(1, num_labels):
        area = stats[label, cv2.CC_STAT_AREA]
        if area < 100:
            inv[labels == label] = 0
    result = cv2.bitwise_not(inv)
    output_path = os.path.join(output_folder, filename)
    cv2.imwrite(output_path, result)
    print(f"Processed {filename}")