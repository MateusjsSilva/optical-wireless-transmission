import cv2
import numpy as np
import time

def capture_frame(capture_interval):
    """
    Captures frames from the camera at defined intervals and displays the image in real-time.
    A rectangle is drawn, and the color detection is limited to the area within the rectangle.
    """
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Erro ao abrir a câmera.")
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
                    print("Erro ao capturar a imagem.")
                    break

                # Define the coordinates for the rectangle (top-left and bottom-right)
                rect_start = (100, 100)  # Top-left corner
                rect_end = (400, 400)    # Bottom-right corner

                # Draw the rectangle on the frame
                cv2.rectangle(frame, rect_start, rect_end, (0, 255, 0), 2)

                # Extract the region of interest (ROI) inside the rectangle
                roi = frame[rect_start[1]:rect_end[1], rect_start[0]:rect_end[0]]

                # Convert the ROI to grayscale
                gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

                # Display the captured image with the rectangle
                cv2.imshow('Camera', frame)

                # Detect the predominant color in the ROI and display it in the terminal
                detect_and_display_color(gray_roi)

                # Update the time of the last captured frame
                prev_time = current_time

            # Allow stopping the program by pressing 'q'
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                print("Finalizando...")
                break

            # Manual adjustment of the capture rate
            elif key == ord('u'):  # increase the interval (slower capture)
                capture_interval += 0.1
                print(f"Aumentando o intervalo de captura: {capture_interval} segundos")

            elif key == ord('d'):  # decrease the interval (faster capture)
                capture_interval = max(0.1, capture_interval - 0.1)
                print(f"Diminuindo o intervalo de captura: {capture_interval} segundos")

    finally:
        cap.release()
        cv2.destroyAllWindows()

def detect_and_display_color(frame):
    """
    Detects whether the predominant color in the frame is black (0) or white (1) and prints the result.
    This function only analyzes the region within the defined rectangle.
    """
    mean_intensity = np.mean(frame)
    threshold = 127  # Threshold to determine black or white
    color = "White (1)" if mean_intensity > threshold else "Black (0)"
    print(f"Detected color in ROI: {color}")
    return 0 if mean_intensity < threshold else 1