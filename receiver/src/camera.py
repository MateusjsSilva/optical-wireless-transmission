import cv2
import numpy as np
import time
import os

def detect_color(roi):
    """
    Detects if the region of interest (ROI) contains a predominance of green, blue, red, black, or magenta.
    
    Args:
    - roi (numpy.ndarray): The region of interest from the frame.
    
    Returns:
    - str: The color detected in the ROI ("green", "blue", "red", "black", "magenta") or "none" if no color matches.
    """
    # Convert ROI to HSV color space
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # Define HSV ranges for each color
    lower_green = np.array([35, 100, 100])
    upper_green = np.array([85, 255, 255])

    lower_blue = np.array([100, 100, 100])
    upper_blue = np.array([140, 255, 255])

    # Red has two ranges in HSV color space
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])

    # Magenta (Rosa Choque) range in HSV
    lower_magenta = np.array([140, 100, 100])
    upper_magenta = np.array([170, 255, 255])

    # Create masks for each color
    mask_green = cv2.inRange(hsv_roi, lower_green, upper_green)
    mask_blue = cv2.inRange(hsv_roi, lower_blue, upper_blue)
    
    # Red requires two masks, combined with bitwise OR
    mask_red1 = cv2.inRange(hsv_roi, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv_roi, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)

    # Magenta mask
    mask_magenta = cv2.inRange(hsv_roi, lower_magenta, upper_magenta)

    # Calculate the mean of each mask
    mean_green = np.sum(mask_green == 255)
    mean_blue = np.sum(mask_blue == 255)
    mean_red = np.sum(mask_red == 255)
    mean_magenta = np.sum(mask_magenta == 255)

    total_pixels = roi.size // 3
    threshold = total_pixels * 0.5  # 50% threshold to determine predominant color

    # Determine the predominant color based on the highest mean value
    if mean_green > threshold:
        return "green"
    elif mean_blue > threshold:
        return "blue"
    elif mean_red > threshold:
        return "red"
    elif mean_magenta > threshold:
        return "magenta"
    else:
        mean_intensity = np.mean(roi)
        return "black" if mean_intensity < 127 else "none"

def capture_frame(roi, cap, capture_interval):
    """
    Captures frames from the camera at defined intervals, analyzes regions to transmit multiple bits, displays them,
    and saves each frame to the output folder.
    """
    if not cap.isOpened():
        print("Error opening the camera.")
        return None

    # Create output directory if it doesn't exist
    output_dir = "output_frames"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    green_detected = False
    start_x, start_y, width, height = roi
    end_x = start_x + width
    end_y = start_y + height
    bits_received = []
    frame_count = 0  # Counter for saved frames

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error reading from the camera.")
                break

            # Extract the ROI from the frame
            roi_extracted = frame[start_y:end_y, start_x:end_x]

            # Detect if a specific color is present in the ROI
            color_detected = detect_color(roi_extracted)

            # Save the frame to output directory
            # frame_filename = os.path.join(output_dir, f"frame_{frame_count}.png")
            # cv2.imwrite(frame_filename, frame)
            # frame_count += 1

            # If green is detected, start the countdown
            if color_detected == "green" and not green_detected:
                green_detected = True
                print("Green detected - waiting for 1 second before capture.")
                capture_interval = 1
                time.sleep(1)

                prev_time = time.time()
                while True:
                    current_time = time.time()

                    # Re-detect color within the nested loop
                    ret, frame = cap.read()
                    roi_extracted = frame[start_y:end_y, start_x:end_x]
                    color_detected = detect_color(roi_extracted)

                    # Capture at the defined interval
                    if (current_time - prev_time) >= capture_interval:
                        if color_detected == "magenta":
                            print("Magenta detected - stopping capture.")
                            bits_received = []  # Clear bits for the next message
                            capture_interval = 0.1
                            green_detected = False
                            break
                        elif color_detected == "black":
                            bits_received.append(0)
                        elif color_detected == "red":
                            bits_received.append(1)
                        
                        print(f"Bits: {bits_received}")
                        prev_time = current_time

                        # Save the current frame in the nested loop as well
                        # frame_filename = os.path.join(output_dir, f"frame_{frame_count}.png")
                        # cv2.imwrite(frame_filename, frame)
                        # frame_count += 1

                    # Display the frame with the ROI
                    cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
                    cv2.imshow('Camera', frame)

                    # Exit the loop on 'q' key press
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        return

            # Display the frame with the ROI
            cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
            cv2.imshow('Camera', frame)

            # Exit the loop on 'q' key press
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()