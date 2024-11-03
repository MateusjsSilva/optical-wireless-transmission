import cv2
from camera import capture_frame
from calibration import wait_for_red_area

def main():
    """
    Main function that runs the camera capture loop.
    """
    capture_interval = 0.1                      # between captures
    num_bits = 1                                # number of bits to detect

    cap = cv2.VideoCapture(0)                   # camera capture object
    if not cap.isOpened():
        print("Error opening the camera.")
        return None

    roi = wait_for_red_area(cap)
    if roi:
        capture_frame(roi, cap, capture_interval, num_bits) # capture frames

if __name__ == "__main__":
    main()