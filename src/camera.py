import cv2
import numpy as np
import time

def capture_frame(capture_interval):
    """
    Captures frames from the camera at defined intervals and displays the image in real-time.
    """
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Erro ao abrir a câmera.")
        return None

    prev_time = time.time()

    while True:
        # Capture the current time to control the capture interval
        current_time = time.time()

        # Check if the capture interval has been reached
        if (current_time - prev_time) >= capture_interval:
            ret, frame = cap.read()
            if not ret:
                print("Erro ao capturar a imagem.")
                break

            # Convert to grayscale
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Display the captured image
            cv2.imshow('Camera', frame)

            # Detect the predominant color and display it in the terminal
            detect_and_display_color(gray_frame)

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

    cap.release()
    cv2.destroyAllWindows()

def detect_and_display_color(frame):
    """
    Detects whether the predominant color in the frame is black (0) or white (1) and prints the result.
    """
    mean_intensity = np.mean(frame)
    threshold = 127
    color = "White (1)" if mean_intensity > threshold else "Black (0)"
    print(f"Detected color: {color}")
    return 0 if mean_intensity < threshold else 1