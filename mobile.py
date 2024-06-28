import cv2

for i in range(100):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Video device index: {i}")
    cap.release()
