from PIL import Image, ImageTk
import customtkinter as ctk

#name IntrusionKit

# Start main window
app = ctk.CTk()
app.title('IntrusionKit')
app.geometry('800x500')
app.iconbitmap("Images\\Icon.ico")

############################### THEME #####################################

# Set custom theme to dark mode
def set_custom_theme():
    ctk.set_appearance_mode("dark")

set_custom_theme()

############################### END #######################################
############################### BUTTON ACTIONS ############################
            
def action_summary_report():
    print("Summary / Report")

def action_sub_directory_finder():
    print("Sub Directory Finder")

def action_sub_domain_finder():
    print("Sub domain finder")
    
def action_port_scanner():
    print("port scanner")
    
def action_reverse_shell():
    print("reverse shell")
    
def action_custom_wordlist():
    print("custom wordlist")

def action_file_server():
    print("file server")
    
def action_hash_cracker():
    print("Hash cracker")
    
def action_backdoor():
    print("backdoor")
    
def action_retrieve_documents():
    print("retrieve documents")

############################### END #######################################
############################### BANNER ####################################

# Banner frame
top_banner = ctk.CTkFrame(master=app, corner_radius=10)
top_banner.grid(row=0, column=0, columnspan=3, sticky="new")
app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure(0, weight=0)

# Loading and resizing logo in banner
original_image = Image.open("Images\\Logo2.png")
resized_image = original_image.resize((300, 50), Image.Resampling.LANCZOS)
logo_image = ImageTk.PhotoImage(resized_image)

# Adding logo to banner
logo_label = ctk.CTkLabel(master=top_banner, image=logo_image, text="")
logo_label.image = logo_image  # Prevent garbage collection
logo_label.pack(side='left', padx=20, pady=(10,10))

# Top right Frame in banner
top_right_frame = ctk.CTkFrame(master=top_banner)
top_right_frame.pack(side='right', padx=20)

# Version Label
version_label = ctk.CTkLabel(master=top_right_frame, text="V0.0", text_color="grey", font=("small fonts", 10), padx=8)
version_label.grid(row=0, column=1, sticky="w")

# Summary/Report button
summary_btn = ctk.CTkButton(master=top_right_frame, text="Summary/Report",
                            corner_radius=10, text_color="black",
                            hover_color="grey", font=("courier", 15), 
                            command=action_summary_report)
summary_btn.grid(row=0, column=0) 

############################### END #######################################
############################### FRAMES ####################################

# Creating frames for each section
frames = [ctk.CTkFrame(master=app, corner_radius=15) for _ in range(6)]

# Position the frames as per the layout using grid
for i, frame in enumerate(frames):
    frame.grid(row=(i//3)+1, column=i%3, padx=15, pady=15, sticky="nsew")
    app.grid_columnconfigure(i%3, weight=1)
    app.grid_rowconfigure((i//3)+1, weight=1)
    
############################### END ########################################
############################### BUTTONS ####################################

# Defining frame name, button name and their actions
buttons_info = [
    ("Reconnaissance",    [("Sub-Directory Finder", action_sub_directory_finder),
                           ("Sub-Domain Finder", action_sub_domain_finder),
                           ("Port Scanner", action_port_scanner)], frames[0]),
    ("Weaponization",     [("Reverse shell", action_reverse_shell),
                           ("Custom Wordlist", action_custom_wordlist)], frames[1]),
    ("Payload Delivery",  [("File server", action_file_server)], frames[2]),
    ("Exploitation",      [("Hash cracker", action_hash_cracker)], frames[3]),
    ("Installation",      [("Backdoor", action_backdoor)], frames[4]),
    ("Actions on system", [("Retrieve Documents", action_retrieve_documents)], frames[5])
]

# Add labels and buttons to each frame with corresponding actions
for category, buttons, frame in buttons_info:
    label = ctk.CTkLabel(master=frame, text=category, text_color="grey", font=("Small fonts", 18))
    label.pack(pady=12)
    for btn_text, action in buttons:
        button = ctk.CTkButton(master=frame, text=btn_text, corner_radius=10, text_color="black", hover_color="grey", font=("courier", 15), command=action)
        button.pack(pady=8)

    
############################### END #######################################

app.mainloop()
