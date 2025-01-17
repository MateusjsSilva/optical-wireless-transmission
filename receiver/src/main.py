import cv2
import numpy as np

from camera import capture_frame
from calibration import wait_for_color_area

def main():
    """
    Main function that runs the camera capture loop.
    """
    capture_interval = 0.1      # Interval between captures
    cap = cv2.VideoCapture(0)   # Open the default camera
    
    if not cap.isOpened():
        print("Error opening the camera.")
        return None

    try:
        # Define HSV range for cyan (blue light) calibration
        lower = np.array([80, 100, 100])
        upper = np.array([100, 255, 255])

        # Wait for a color area to calibrate
        roi_coords = wait_for_color_area(cap, lower, upper)
        if roi_coords:
            capture_frame(roi_coords, cap, capture_interval)

    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()