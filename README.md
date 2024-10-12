# Optical Wireless Transmission Simulation

## Description

This project simulates an optical wireless communication system where one monitor transmits binary data using colors (black as 0 and white as 1), and a camera captures the transmitted information. The captured data is analyzed to calculate the Bit Error Rate (BER), which reflects the accuracy of the transmission.

The project involves:

- Capturing frames from a camera.
- Detecting the predominant color (black or white).
- Simulating the transmission of bits using visual signals.
- Calculating the Bit Error Rate (BER) for performance evaluation.

## Folder Structure

- `src/camera.py`: Captures frames from the camera and detects colors.
- `src/utils.py`: Contains utility functions, including the BER calculation.
- `src/main.py`: Main script to execute the transmission simulation and print results.

## Getting Started

1. Clone the repository:
    ```bash
    git clone git@github.com:MateusjsSilva/optical-wireless-transmission.git
    cd optical-wireless-transmission
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment**:
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4. **Install the required Python packages**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Running the Simulation

To start the simulation, run the following command:

```bash
python src/main.py
```

## Contribution

Feel free to open issues or submit pull requests. All contributions are welcome!

## License

This project is licensed under the Apache License - see the [LICENSE](LICENSE) file for details.