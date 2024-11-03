import cv2
import numpy as np
import time

def detect_red_area(frame):
    """
    Detects a red area in the frame and returns the coordinates of its bounding box.

    Args:
    - frame (numpy.ndarray): The captured frame.

    Returns:
    - tuple: Coordinates (x, y, w, h) of the bounding box around the red area, or None if not found.
    """
    # Convert frame to HSV color space for better color detection
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define HSV range for the color red
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    # Create a mask for the red color
    red_mask = cv2.inRange(hsv_frame, lower_red, upper_red)

    # Find contours in the red mask
    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Get the largest contour by area, assuming it is the intended red area
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        # Return bounding box coordinates for the red area
        return x, y, w, h
    
    # If no red area is detected, return None
    return None

def wait_for_red_area(cap, wait_time=5):
    """
    Waits for a red area to be detected and fixes it after a specified wait time.

    Args:
    - cap (cv2.VideoCapture): The video capture object.
    - wait_time (int): The time to wait before fixing the area (in seconds).

    Returns:
    - tuple: Fixed coordinates (x, y, w, h) of the red area after the wait time.
    """
    red_area_defined = False
    roi_coords = None
    start_time = None  # To track the start time for the countdown

    while not red_area_defined:
        ret, frame = cap.read()
        if not ret:
            print("Error reading from the camera.")
            break

        roi_coords = detect_red_area(frame)

        if roi_coords:
            if start_time is None:
                start_time = time.time()  # Record the start time
                print("Red area detected. Counting down 5 seconds to fix the area...")
            elif time.time() - start_time >= wait_time:
                red_area_defined = True  # Lock in the red area after the wait time
                print("Red area fixed at:", roi_coords)

        # Optionally, visualize the detection
        if roi_coords:
            x, y, w, h = roi_coords
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Camera", frame)
        
        # Quit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    return roi_coords