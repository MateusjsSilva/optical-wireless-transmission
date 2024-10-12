from camera import capture_frame, detect_and_display_color
from utils import adjust_capture_interval_by_ber, calculate_ber
import random

def main():
    """
    Main function that runs the camera capture loop, automatically adjusting
    the capture interval based on the Bit Error Rate (BER).
    """
    capture_interval = 0.5 # between captures

    transmitted_bits = []
    received_bits = []

    for _ in range(50):   # Simulating the transmission of 50 bits
        transmitted_bit = random.randint(0, 1)
        transmitted_bits.append(transmitted_bit)

        # Capture the bit from the camera
        frame = capture_frame(capture_interval)
        received_bit = detect_and_display_color(frame)
        received_bits.append(received_bit)

        # Calculate the Bit Error Rate (BER)
        ber = calculate_ber(transmitted_bits, received_bits)
        print(f"Bit Error Rate (BER): {ber}")

        # Automatically adjust the capture interval based on the BER
        capture_interval = adjust_capture_interval_by_ber(capture_interval, ber)

    print("Transmissão finalizada.")

if __name__ == "__main__":
    main()