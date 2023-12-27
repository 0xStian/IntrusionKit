import customtkinter as ctk
import random


def on_button_click():
    # Clear the body of the GUI
    for widget in app.winfo_children():
        if widget != button:
            widget.destroy()

    # Add new text
    label = ctk.CTkLabel(app, text=str(random.randint(1,999999999999999)))
    label.pack(pady=20)

# Create the main window
app = ctk.CTk()

# Set window title and size
app.title("CustomTkinter Example")
app.geometry("300x200")

# Create a button
button = ctk.CTkButton(app, text="Press Me", command=on_button_click)
button.pack(pady=20)

# Run the application
app.mainloop()
