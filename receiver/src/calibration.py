import cv2
import numpy as np
import time

def detect_color_area(frame, lower_hsv, upper_hsv):
    """
    Detects an area with a specific color in the frame based on the HSV range provided.

    Args:
    - frame (numpy.ndarray): The captured frame.
    - lower_hsv (numpy.ndarray): Lower HSV bound for the target color.
    - upper_hsv (numpy.ndarray): Upper HSV bound for the target color.

    Returns:
    - tuple: Coordinates (x, y, w, h) of the bounding box around the detected area, or None if not found.
    """
    # Convert frame to HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask for the target color based on provided HSV range
    color_mask = cv2.inRange(hsv_frame, lower_hsv, upper_hsv)

    # Find contours in the color mask
    contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Get the largest contour by area, assuming it is the intended target area
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        # Return bounding box coordinates for the detected area
        return x, y, w, h
    
    # If no area is detected, return None
    return None

def wait_for_color_area(cap, lower_hsv, upper_hsv, wait_time=5):
    """
    Waits for a specific color area to be detected and fixes it after a specified wait time.

    Args:
    - cap (cv2.VideoCapture): The video capture object.
    - lower_hsv (numpy.ndarray): Lower HSV bound for the target color.
    - upper_hsv (numpy.ndarray): Upper HSV bound for the target color.
    - wait_time (int): The time to wait before fixing the area (in seconds).

    Returns:
    - tuple: Fixed coordinates (x, y, w, h) of the color area after the wait time.
    """
    area_defined = False
    roi_coords = None
    start_time = None  # To track the start time for the countdown

    while not area_defined:
        ret, frame = cap.read()
        if not ret:
            print("Error reading from the camera.")
            break

        # Detect area with the specified color
        roi_coords = detect_color_area(frame, lower_hsv, upper_hsv)

        if roi_coords:
            if start_time is None:
                start_time = time.time()  # Record the start time
                print(f"Target color area detected. Counting down {wait_time} seconds to fix the area...")
            elif time.time() - start_time >= wait_time:
                area_defined = True  # Lock in the area after the wait time
                print("Color area fixed at:", roi_coords)

        # Optionally, visualize the detection
        if roi_coords:
            x, y, w, h = roi_coords
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Camera", frame)
        
        # Quit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    return roi_coords