import cv2
import numpy as np
import time

from config import PARITY_TYPE, START_SEQUENCE, END_SEQUENCE
from synchronization import check_checksum, check_parity, decode_message, find_sequence

def capture_frame(capture_interval, num_bits=2):
    """
    Captures frames from the camera at defined intervals, analyzes regions to transmit multiple bits, and displays them.
    
    Args:
    - capture_interval (float): Frame capture interval in seconds.
    - num_bits (int): Number of bits to be transmitted per image (default = 4).
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error opening the camera.")
        return None

    prev_time = time.time()
    rect_width, rect_height = 500, 400
    bits_received = []

    try:
        while True:
            current_time = time.time()
            if (current_time - prev_time) >= capture_interval:
                ret, frame = cap.read()
                if not ret:
                    print("Erro ao abrir a câmera.")
                    break

                height, width, _ = frame.shape
                start_x = (width - rect_width) // 2
                start_y = (height - rect_height) // 2
                end_x = start_x + rect_width
                end_y = start_y + rect_height

                # Draw the central rectangle
                cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)

                # Extract the ROI and detect multiple bits
                roi = frame[start_y:end_y, start_x:end_x]
                bits_detected = detect_multiple_bits(roi, frame, start_x, start_y, num_bits=num_bits)
                bits_received.extend(bits_detected)

                # Check synchronization and complete message
                start_index = find_sequence(bits_received, START_SEQUENCE)
                end_index = find_sequence(bits_received, END_SEQUENCE, start_index + len(START_SEQUENCE))

                if start_index != -1 and end_index != -1:
                    message_bits = bits_received[start_index + len(START_SEQUENCE):end_index]

                    # Check parity and checksum for errors
                    if check_parity(message_bits, PARITY_TYPE) and check_checksum(message_bits):
                        message, status = decode_message(message_bits)
                        print("Mensagem:", message)
                        print("Status:", status)
                    else:
                        print("Erro de paridade ou checksum detectado!")

                    # Clear bits after processing
                    bits_received = bits_received[end_index + len(END_SEQUENCE):]

                # Show frame with detected bits
                cv2.imshow('Camera', frame)
                prev_time = current_time

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()

def detect_multiple_bits(roi, frame, start_x, start_y, num_bits=4):
    """
    Divides the ROI into 'num_bits' horizontal lines and detects the bit (0 or 1) in each line.
    """
    height, width = roi.shape[:2]
    bits_detected = []

    for i in range(num_bits):
        line_y = int((i + 0.5) * height / num_bits)
        line_roi = roi[max(0, line_y - 3):line_y + 3, :]
        mean_intensity = np.mean(line_roi)
        bit = 1 if mean_intensity > 127 else 0
        bits_detected.append(bit)
        cv2.line(frame, (start_x, start_y + line_y), (start_x + width, start_y + line_y), (0, 0, 255), 1)

    return bits_detected

def apply_mask(frame, start_x, start_y, width, height):
    """
    Applies a colored mask over a square area within the rectangle.
    """
    masked_frame = frame.copy()
    mask_width, mask_height = width // 4, height // 4  # Size of the mask square (1/4 of the rectangle)
    mask_x = start_x + (width - mask_width) // 2      # Center the mask square
    mask_y = start_y + (height - mask_height) // 2

    # Apply the mask with a semi-transparent color (example: blue)
    color = (255, 0, 0)  # Blue
    alpha = 0.5          # Mask transparency
    masked_frame[mask_y:mask_y + mask_height, mask_x:mask_x + mask_width] = cv2.addWeighted(
        frame[mask_y:mask_y + mask_height, mask_x:mask_x + mask_width], 1 - alpha,
        np.full((mask_height, mask_width, 3), color, dtype=np.uint8), alpha, 0)

    return masked_frame

def detect_bits_in_two_lines(roi, frame, start_x, start_y, rect_height, line_width=6):
    """
    Detects bits in two horizontal lines within the ROI.
    """
    height, width = roi.shape[:2]
    bits_detected = []

    # Line positions using proportion of rectangle height
    line_1_y = int(rect_height * 0.25)  # Line at 25% of rectangle height
    line_2_y = int(rect_height * 0.75)  # Line at 75% of rectangle height

    # Analyze the first line
    line_1_roi = roi[max(0, line_1_y - line_width // 2):line_1_y + line_width // 2, :]
    mean_intensity_1 = np.mean(line_1_roi)
    bit_1 = 1 if mean_intensity_1 > 127 else 0
    bits_detected.append(bit_1)

    # Draw the first red line on the original frame
    cv2.line(frame, (start_x, start_y + line_1_y), (start_x + width, start_y + line_1_y), (0, 0, 255), 1)

    # Analyze the second line
    line_2_roi = roi[max(0, line_2_y - line_width // 2):line_2_y + line_width // 2, :]
    mean_intensity_2 = np.mean(line_2_roi)
    bit_2 = 1 if mean_intensity_2 > 127 else 0
    bits_detected.append(bit_2)

    # Draw the second red line on the original frame
    cv2.line(frame, (start_x, start_y + line_2_y), (start_x + width, start_y + line_2_y), (0, 0, 255), 1)

    return bits_detected