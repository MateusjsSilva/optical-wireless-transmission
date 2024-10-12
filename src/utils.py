def calculate_ber(transmitted, received):
    """
    Calculates the Bit Error Rate (BER) between transmitted and received bits.
    """
    errors = sum(t != r for t, r in zip(transmitted, received))
    ber = errors / len(transmitted) if len(transmitted) > 0 else 0
    return ber

def adjust_capture_interval_by_ber(capture_interval, ber):
    """
    Automatically adjusts the capture rate (interval) based on the BER.
    If the BER is high, the interval is reduced to try to capture more quickly.
    If the BER is low, the interval is increased to save resources.
    """
    if ber > 0.1:  # If the BER is greater than 10%, we capture faster
        capture_interval = max(0.1, capture_interval - 0.1)
    elif ber < 0.01:  # If the BER is less than 1%, we capture slower
        capture_interval += 0.1
    
    return capture_interval