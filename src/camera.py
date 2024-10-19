import cv2
import numpy as np
import time

def capture_frame(capture_interval):
    """
    Captures frames from the camera at defined intervals and displays the image in real time.
    A central rectangle is drawn, and two lines within it are analyzed for bit detection.
    The two lines are drawn in red on the frame.
    """
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error opening the camera.")
        return None

    prev_time = time.time()

    try:
        while True:
            # Capture the current time to control the capture interval
            current_time = time.time()

            # Check if the capture interval has been reached
            if (current_time - prev_time) >= capture_interval:
                ret, frame = cap.read()
                if not ret:
                    print("Error capturing the image.")
                    break

                # Get the image dimensions
                height, width, _ = frame.shape

                # Define the size of the centered rectangle (e.g., 300x200 pixels)
                rect_width = 500
                rect_height = 400

                # Calculate the coordinates of the central rectangle
                start_x = (width - rect_width) // 2
                start_y = (height - rect_height) // 2
                end_x = start_x + rect_width
                end_y = start_y + rect_height

                # Draw the rectangle on the frame
                cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)

                # Extract the region of interest (ROI) within the rectangle
                roi = frame[start_y:end_y, start_x:end_x]

                # Convert the ROI to grayscale
                gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

                # Choose two specific lines to analyze
                line_1_y = rect_height // 3  # First line at 1/3 of the rectangle height
                line_2_y = (rect_height // 3) * 2  # Second line at 2/3 of the rectangle height

                # Detect bits on the two lines and draw them in red on the frame
                bits_detected = detect_bits_in_two_lines(gray_roi, frame, start_x, start_y, line_1_y, line_2_y)

                # Display the detected bits
                print(f"Bits detected on the lines: {bits_detected}")

                # Show the image with the rectangle and lines on the screen
                cv2.imshow('Camera', frame)

                # Update the last capture time
                prev_time = current_time

            # Allow the program to be stopped by pressing 'q'
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                print("Exiting...")
                break

            # Manual adjustments to the capture rate
            elif key == ord('u'):  # increase interval (slower capture)
                capture_interval += 0.1
                print(f"Increasing capture interval: {capture_interval} seconds")

            elif key == ord('d'):  # decrease interval (faster capture)
                capture_interval = max(0.1, capture_interval - 0.1)
                print(f"Decreasing capture interval: {capture_interval} seconds")

    finally:
        cap.release()
        cv2.destroyAllWindows()

def detect_bits_in_two_lines(roi, frame, start_x, start_y, line_1_y, line_2_y):
    """
    Detects the predominant bits (black or white) in two specific lines of the ROI and draws these
    lines in red on the original frame.
    
    Parameters:
    - roi: The region of interest in grayscale.
    - frame: The original frame to draw the lines.
    - start_x, start_y: Coordinates of the top-left corner of the ROI on the original frame.
    - line_1_y, line_2_y: Vertical positions of the two lines within the ROI.
    """
    height, width = roi.shape
    bits_detected = []

    # Analyzing the first line
    line_1 = roi[line_1_y, :]  # Extract the complete line 1
    mean_intensity_1 = np.mean(line_1)
    bit_1 = 1 if mean_intensity_1 > 127 else 0  # Set bit as 1 or 0
    bits_detected.append(bit_1)

    # Draw the first red line on the original frame
    cv2.line(frame, (start_x, start_y + line_1_y), (start_x + width, start_y + line_1_y), (0, 0, 255), 1)

    # Analyzing the second line
    line_2 = roi[line_2_y, :]  # Extract the complete line 2
    mean_intensity_2 = np.mean(line_2)
    bit_2 = 1 if mean_intensity_2 > 127 else 0  # Set bit as 1 or 0
    bits_detected.append(bit_2)

    # Draw the second red line on the original frame
    cv2.line(frame, (start_x, start_y + line_2_y), (start_x + width, start_y + line_2_y), (0, 0, 255), 1)

    return bits_detected

def detect_and_display_color(frame):
    """
    Detects if the predominant color in the frame is black (0) or white (1) and returns the result.
    This method is kept for compatibility with the main function but now uses the two lines for analysis.
    """
    return detect_bits_in_two_lines(frame)