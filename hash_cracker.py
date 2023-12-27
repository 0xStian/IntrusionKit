import customtkinter as ctk

# Create the main window
app = ctk.CTk()

# Set the size of the window and make it non-resizable
app.geometry("800x600")
app.resizable(False, False)

# Set the title of the window
app.title("NetRavage Hash Cracker")

# Define modern colors
background_color = "#2a2d2e"
text_color = "#f5f5f5"
button_color = "#0078D7"
entry_bg_color = "#40444b"

# Set background color for the app
app.configure(bg=background_color)

# Create a logo placeholder
logo_placeholder = ctk.CTkLabel(app, text="NetRavage", width=200, height=50, corner_radius=10)
logo_placeholder.place(x=20, y=20)

# Create entry widgets for wordlist and hashlist with modern styling
wordlist_entry = ctk.CTkEntry(app, placeholder_text="Word List...", width=200, height=40, corner_radius=10)
wordlist_entry.place(x=20, y=100)

hashlist_entry = ctk.CTkEntry(app, placeholder_text="Hash List...", width=200, height=40, corner_radius=10)
hashlist_entry.place(x=20, y=160)

# Create a dropdown for hash type selection
hash_type = ctk.CTkOptionMenu(app, values=["MD5", "SHA1", "SHA256"], width=200, height=40, corner_radius=10)
hash_type.place(x=20, y=220)

# Create a start button
start_button = ctk.CTkButton(app, text="START", width=200, height=50, corner_radius=10, fg_color=button_color)
start_button.place(x=20, y=280)

# Create a frame for hashes output
hashes_frame = ctk.CTkFrame(app, width=350, height=200, corner_radius=10)
hashes_frame.place(x=250, y=20)

# Label for the hashes frame
hashes_label = ctk.CTkLabel(hashes_frame, text="Hashes", fg_color=entry_bg_color, text_color=text_color, corner_radius=10)
hashes_label.pack(pady=10, padx=10)

# Text widget for displaying hashes
hashes_text = ctk.CTkTextbox(hashes_frame, width=330, height=150, corner_radius=10)
hashes_text.pack()

# Create a frame for output
output_frame = ctk.CTkFrame(app, width=350, height=200, corner_radius=10)
output_frame.place(x=250, y=250)

# Label for the output frame
output_label = ctk.CTkLabel(output_frame, text="OUTPUT", fg_color=entry_bg_color, text_color=text_color, corner_radius=10)
output_label.pack(pady=10, padx=10)

# Text widget for displaying output
output_text = ctk.CTkTextbox(output_frame, width=330, height=150, corner_radius=10)
output_text.pack()

# Start the main loop
app.mainloop()
