from camera import capture_frame

def main():
    """
    Main function that runs the camera capture loop.
    """
    capture_interval = 1 # between captures
    capture_frame(capture_interval)

if __name__ == "__main__":
    main()