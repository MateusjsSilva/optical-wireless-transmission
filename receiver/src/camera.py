import cv2
import numpy as np
import time

def detect_color(roi):
    """
    Detects if the region of interest (ROI) contains a predominance of green, blue, red, white, or black.
    
    Args:
    - roi (numpy.ndarray): The region of interest from the frame.
    
    Returns:
    - str: The color detected in the ROI ("green", "blue", "red", "white", "black") or "none" if no color matches.
    """
    # Convert ROI to HSV color space
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # Define HSV ranges for each color
    lower_green = np.array([35, 100, 100])
    upper_green = np.array([85, 255, 255])

    lower_blue = np.array([100, 150, 0])
    upper_blue = np.array([140, 255, 255])

    # Red has two ranges in HSV color space
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])

    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 20, 255])

    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 30])

    # Create masks for each color
    mask_green = cv2.inRange(hsv_roi, lower_green, upper_green)
    mask_blue = cv2.inRange(hsv_roi, lower_blue, upper_blue)
    
    # Red requires two masks, combined with bitwise OR
    mask_red1 = cv2.inRange(hsv_roi, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv_roi, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)
    
    mask_white = cv2.inRange(hsv_roi, lower_white, upper_white)
    mask_black = cv2.inRange(hsv_roi, lower_black, upper_black)

    # Calculate the mean of each mask
    mean_green = np.mean(mask_green)
    mean_blue = np.mean(mask_blue)
    mean_red = np.mean(mask_red)
    mean_white = np.mean(mask_white)
    mean_black = np.mean(mask_black)

    mean_black = np.sum(mask_black == 255)
    mean_white = np.sum(mask_white == 255)
    mean_red = np.sum(mask_red == 255)
    mean_green = np.sum(mask_green == 255)
    mean_blue = np.sum(mask_blue == 255)

    total_pixels = roi.size // 3
    l = total_pixels * 0.5 

    # Determine the predominant color based on the highest mean value
    if mean_green > l:
        return "green"
    elif mean_blue > l:
        return "blue"
    elif mean_red > l:
        return "red"
    elif mean_white > l:
        return "white"
    elif mean_black > l:
        return "black"
    else:
        return "none"

def bits_to_message(bits):
    """
    Converts a list of bits to an ASCII string.
    Assumes each character is represented by 8 bits.
    """
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) == 8:
            # Convert the list of bits to a character
            char = chr(int(''.join(map(str, byte)), 2))
            chars.append(char)
    return ''.join(chars)

def capture_frame(roi, cap, capture_interval, num_bits):
    """
    Captures frames from the camera at defined intervals, analyzes regions to transmit multiple bits, and displays them.
    """
    if not cap.isOpened():
        print("Error opening the camera.")
        return None

    green_detected = False
    start_x, start_y, width, height = roi
    end_x = start_x + width
    end_y = start_y + height
    bits_received = []

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error reading from the camera.")
                break

            # Extrair o ROI do quadro
            roi_extracted = frame[start_y:end_y, start_x:end_x]

            # Verificar se a cor verde está presente
            color_detected = detect_color(roi_extracted)

            # Se verde for detectado, iniciar a contagem
            if color_detected == "green" and not green_detected:
                green_detected = True
                print("Green detected - waiting for 1 second before capture.")
                capture_interval = 0.6
                time.sleep(1)

                prev_time = time.time()
                while True:
                    current_time = time.time()

                    # Re-detect color within the nested loop
                    ret, frame = cap.read()
                    roi_extracted = frame[start_y:end_y, start_x:end_x]
                    color_detected = detect_color(roi_extracted)

                    # Capturar a cada intervalo de 0,5 segundos
                    if (current_time - prev_time) >= capture_interval:
                        if color_detected == "blue":
                            print("Blue detected - stopping capture.")
                            message = bits_to_message(bits_received)
                            print("Decoded message:", message)
                            bits_received = []  # Clear bits for the next message
                            capture_interval = 0.1
                            green_detected = False
                            break
                        elif color_detected == "black":
                            bits_received.append(0)
                        elif color_detected == "white":
                            bits_received.append(1)
                        
                        print(f"Bits: {bits_received}")
                        prev_time = current_time

                    # Mostrar o quadro com a região do ROI
                    cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
                    cv2.imshow('Camera', frame)

                    # Encerrar o loop ao pressionar 'q'
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        return

            # Mostrar o quadro com a região do ROI
            cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
            cv2.imshow('Camera', frame)

            # Encerrar o loop ao pressionar 'q'
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()