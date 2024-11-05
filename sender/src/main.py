import tkinter as tk
from tkinter import simpledialog

class BinaryBlinker:

    def __init__(self, window):
        # Color variables
        self.bg_color_calibration = "cyan" 
        self.bg_color_start = "green"         
        self.bg_color_end = "orange"
        self.bg_color_zero = "black"
        self.bg_color_one = "red"
        self.btn_color = "cyan"
        self.btn_text_color = "black"
        self.label_text_color = "blue"

        # Setup window and initial configuration
        self.window = window
        self.window.title("Blinking Binary Converter")
        self.window.configure(bg=self.bg_color_calibration)
        self.is_blinking = False
        self.binary_representation = ""
        self.current_index = -1

        # Create a frame to center the button
        self.center_frame = tk.Frame(self.window, bg=self.bg_color_calibration)
        self.center_frame.pack(expand=True)

        # Button to initiate text input
        self.input_button = tk.Button(
            self.center_frame, 
            text="Enter Text", 
            command=self.prompt_for_text,
            bg=self.btn_color,
            fg=self.btn_text_color,
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10
        )
        self.input_button.pack()

        # Label to display the binary representation
        self.binary_label = tk.Label(
            self.center_frame,
            text="",
            bg=self.bg_color_calibration,
            fg=self.label_text_color,
            font=("Arial", 14),
            borderwidth=0,
            highlightthickness=0,
            padx=0,
            pady=0
        )
        self.binary_label.pack(pady=0)

        # Bind the F11 key to toggle full-screen mode and Esc to close the window
        self.window.bind("<F11>", self.toggle_fullscreen)
        self.window.bind("<Escape>", self.close_window)

        # Set the initial window size
        self.window.geometry("800x600")  

    def toggle_fullscreen(self, event=None):
        """Toggles full-screen mode."""
        current_fullscreen = self.window.attributes("-fullscreen")
        self.window.attributes("-fullscreen", not current_fullscreen)

    def close_window(self, event=None):
        """Closes the window when Esc is pressed."""
        self.window.destroy()

    def convert_text_to_binary(self, input_text):
        """Converts the input text to its binary equivalent."""
        return ''.join(format(ord(char), '08b') for char in input_text)

    def prompt_for_text(self):
        """Prompts the user to input text through a dialog box."""
        user_text = simpledialog.askstring("Input", "Please enter your text:")
        if user_text:
            self.binary_representation = self.convert_text_to_binary(user_text)
            self.binary_label.config(text=f"Binary: {self.binary_representation}")
            self.input_button.pack_forget()
            self.window.after(5000, self.start_blinking_process)

    def start_blinking_process(self):
        """Handles the blinking process with the given user text."""
        self.is_blinking = True
        self.current_index = 0
        self.blink_start_indicator()

    def blink_start_indicator(self):
        """Sets the window background to the start indication color."""
        self.set_background_color(self.bg_color_start)
        self.window.after(2000, self.blink_current_bit)

    def blink_current_bit(self):
        """Blinks the window based on the binary bit at the current index."""
        if self.current_index < len(self.binary_representation):
            current_bit = self.binary_representation[self.current_index]
            color = self.determine_color_for_bit(current_bit)
            self.set_background_color(color)
            self.current_index += 1
            self.binary_label.config(text=f"Binary: {self.binary_representation[:self.current_index]}")
            self.window.after(1000, self.blink_current_bit)
        else:
            self.blink_end_indicator()

    def determine_color_for_bit(self, bit):
        """Returns the appropriate color based on the binary bit."""
        return self.bg_color_one if bit == '1' else self.bg_color_zero

    def blink_end_indicator(self):
        """Finalizes the blinking process by setting the background to the end indication color."""
        self.set_background_color(self.bg_color_end)
        self.is_blinking = False
        self.window.after(2000, self.complete_blinking)

    def complete_blinking(self):
        """Ends the blinking sequence by resetting the window background and showing the input button."""
        self.input_button.pack()

    def set_background_color(self, color):
        """Sets the background color for the window, frame, and label."""
        self.window.configure(bg=color)
        self.center_frame.configure(bg=color)
        self.binary_label.configure(bg=color)

# Create and run the main application window
if __name__ == "__main__":
    main_window = tk.Tk()
    blinker_app = BinaryBlinker(main_window)

    # Start the application loop
    main_window.mainloop()