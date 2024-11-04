import tkinter as tk
from tkinter import simpledialog

class BinaryBlinker:

    def __init__(self, window):
        self.window = window
        self.window.title("Blinking Binary Converter")
        self.window.configure(bg="red")
        self.is_blinking = False
        self.binary_representation = ""
        self.current_index = -1

        # Create a frame to center the button
        self.center_frame = tk.Frame(self.window)
        self.center_frame.pack(expand=True)

        # Button to initiate text input
        self.input_button = tk.Button(
            self.center_frame, 
            text="Enter Text", 
            command=self.prompt_for_text,
            bg="gray",
            fg="black",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10
        )
        self.input_button.pack()

        # Label to display the binary representation
        self.binary_label = tk.Label(
            self.center_frame,
            text="Binary: ",
            bg="red",
            fg="white",
            font=("Arial", 14)
        )
        self.binary_label.pack(pady=20)  # Add some vertical space

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
            self.binary_label.config(text=f"Binary: {self.binary_representation}")  # Update label with binary representation
            # Start the blinking process after a 1 second delay
            self.window.after(5000, self.start_blinking_process)

    def start_blinking_process(self):
        """Handles the blinking process with the given user text."""
        self.is_blinking = True
        self.current_index = 0
        self.blink_start_indicator()

    def blink_start_indicator(self):
        """Sets the window background to green for the start indication."""
        self.window.configure(bg="green")
        self.window.after(2000, self.blink_current_bit)

    def blink_current_bit(self):
        """Blinks the window based on the binary bit at the current index."""
        if self.current_index < len(self.binary_representation):
            current_bit = self.binary_representation[self.current_index]
            color = self.determine_color_for_bit(current_bit)
            self.window.configure(bg=color)
            self.current_index += 1
            self.binary_label.config(text=f"Binary: {self.binary_representation[:self.current_index]}")  # Update label
            self.window.after(1000, self.blink_current_bit)  # Schedule the next blink in 1 second
        else:
            self.blink_end_indicator()

    def determine_color_for_bit(self, bit):
        """Returns the appropriate color based on the binary bit."""
        return "white" if bit == '1' else "black"

    def blink_end_indicator(self):
        """Finalizes the blinking process by setting the background to orange."""
        self.window.configure(bg="orange")
        self.is_blinking = False
        self.window.after(2000, self.complete_blinking)

    def complete_blinking(self):
        """Ends the blinking sequence by resetting the window background."""
        self.window.configure(bg="orange")

# Create and run the main application window
if __name__ == "__main__":
    main_window = tk.Tk()
    blinker_app = BinaryBlinker(main_window)

    # Start the application loop
    main_window.mainloop()