import cv2
import os

input_folder = r"D:\ProjectX\T1\X task 1 Windows\cleaned_final"
output_folder = r"D:\ProjectX\T1\X task 1 Windows\inverted"
os.makedirs(output_folder, exist_ok=True)
for filename in os.listdir(input_folder):
    if not filename.lower().endswith(".png"):
        continue
    img = cv2.imread(
        os.path.join(input_folder, filename),
        cv2.IMREAD_GRAYSCALE
    )
    inverted = cv2.bitwise_not(img)
    cv2.imwrite(
        os.path.join(output_folder, filename),
        inverted
    )
    print(f"Processed {filename}")