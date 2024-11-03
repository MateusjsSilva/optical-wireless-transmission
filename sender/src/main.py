import tkinter as tk
from tkinter import simpledialog

class BinaryBlinker:

    def __init__(self, window):
        self.window = window
        self.window.title("Blinking Binary Converter")
        self.window.configure(bg="#000000")  # Set initial background to black
        self.is_blinking = False  # Controls the blinking state
        self.binary_representation = ""  # Initializes the binary representation
        self.current_index = -1  # Index for blinking control

        # Create a frame to center the button
        self.center_frame = tk.Frame(self.window)  # Ensure the frame matches the window's background
        self.center_frame.pack(expand=True)

        # Button to initiate text input with increased padding and styled text
        self.input_button = tk.Button(
            self.center_frame, 
            text="Enter Text", 
            command=self.prompt_for_text,
            bg="gray",  # Match button background to the window
            fg="black",  # Set text color to black
            font=("Arial", 12, "bold"),  # Set font to bold with size 12
            padx=20,  # Increase horizontal padding
            pady=10   # Increase vertical padding
        )
        self.input_button.pack()

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
            # Start the blinking process after a 1 second delay
            self.window.after(5000, self.start_blinking_process, user_text)

    def start_blinking_process(self, user_text):
        """Handles the blinking process with the given user text."""
        self.binary_representation = self.convert_text_to_binary(user_text)
        self.is_blinking = True
        self.current_index = 0  # Start with the first bit
        self.blink_start_indicator()  # Indicate start with green color

    def blink_start_indicator(self):
        """Sets the window background to green for the start indication."""
        self.window.configure(bg="green")
        self.window.after(1000, self.blink_current_bit)  # Move to the first bit after 1 second

    def blink_current_bit(self):
        """Blinks the window based on the binary bit at the current index."""
        if self.current_index < len(self.binary_representation):
            current_bit = self.binary_representation[self.current_index]
            color = self.determine_color_for_bit(current_bit)
            self.window.configure(bg=color)
            self.current_index += 1  # Move to the next bit
            self.window.after(1000, self.blink_current_bit)  # Schedule the next blink in 1 second
        else:
            self.blink_end_indicator()  # Final blink to indicate the end

    def determine_color_for_bit(self, bit):
        """Returns the appropriate color based on the binary bit."""
        return "black" if bit == '1' else "white"

    def blink_end_indicator(self):
        """Finalizes the blinking process by setting the background to blue."""
        self.window.configure(bg="blue")
        self.is_blinking = False  # Stop blinking
        self.window.after(2000, self.complete_blinking)  # Wait before completing

    def complete_blinking(self):
        """Ends the blinking sequence by resetting the window background."""
        self.window.configure(bg="blue")  # Resets the window background

# Create and run the main application window
if __name__ == "__main__":
    main_window = tk.Tk()
    blinker_app = BinaryBlinker(main_window)

    # Start the application loop
    main_window.mainloop()