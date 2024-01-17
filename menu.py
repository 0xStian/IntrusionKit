from PIL import Image, ImageTk
import customtkinter as ctk
from tkinter import filedialog
import tkinter as tk
import tkinter.messagebox as messagebox
import threading

import exploitation.hCracker as HashCracker


app = ctk.CTk()
app.title('IntrusionKit')
app.geometry('800x500')
app.iconbitmap("Images\\Icon.ico")

############################### THEME #####################################

ctk.set_appearance_mode("dark")

###########################################################################
################################# file dialog ####################################

def open_file_browser(entry_field):
    filepath = filedialog.askopenfilename()
    if filepath:
        entry_field.delete(0, "end")  # Clear the current text
        entry_field.insert(0, filepath)  # Insert the new filepath



############################### END #######################################

############################### BUTTON ACTIONS ############################
          
def action_summary_report():
    ################################# Summary Functions ####################################
    
    def save_to_summary(): #pass in the text from the textbox in summary
        try:
            with open("Summary.txt", "w") as f:  # Open the file for writing, which overwrites the file
                f.write(summary_textbox.get("1.0", tk.END)) # Write the current state of the textbox to the file
            messagebox.showinfo("Success!","Succesfully saved to Summary.txt!")
        except:
            messagebox.showerror("ERROR SAVING", "There was an error saving to Summary.txt")

    def clear_summary():
        if messagebox.askyesno("Confirmation", "Are you sure you want to clear the summary?"): # yes/no confirmation to clear
            summary_textbox.delete("1.0", "end")
            open("Summary.txt", "w").close()
            messagebox.showinfo("Success!","Succesfully cleared Summary!")
            
    ############################### END #######################################
    clear_body()
    
    app.grid_rowconfigure(0, weight=0)
    app.grid_rowconfigure(1, weight=99)
    
    app.grid_columnconfigure(0, weight=0)  # First column 
    app.grid_columnconfigure(1, weight=999)  # Second column 
    
    #buttons
    lcontent_frame = ctk.CTkFrame(master=app, corner_radius=15)
    lcontent_frame.grid(row=1, column=0, rowspan=1, columnspan=1, padx=5, pady=(10, 10), sticky='nsew')
    
    #save to file
    save_button = ctk.CTkButton(master=lcontent_frame, text="Save Summary", hover_color="green", fg_color="darkgreen", text_color="white", command=lambda: save_to_summary()) #pass text
    save_button.pack(padx=10, pady=10)
    
    rcontent_frame = ctk.CTkFrame(master=app, corner_radius=15)
    rcontent_frame.grid(row=1, column=1, rowspan=1, columnspan=1, padx=5, pady=(10, 10), sticky='nsew')

    # Clear sumamry text
    clear_button = ctk.CTkButton(master=lcontent_frame, text="Clear Summary", hover_color="red", text_color="white", fg_color="darkred",  command=lambda: clear_summary())
    clear_button.pack( padx=10, pady=10)

    # textbox
    summary_textbox = ctk.CTkTextbox(master=rcontent_frame)
    summary_textbox.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.98, relheight=0.94)
    summary_textbox.delete("1.0", tk.END)  # Clear the textbox
    with open("Summary.txt", "a+") as f:
        f.seek(0)  # Move cursor to the start of the file
        content = f.read()
        summary_textbox.insert(tk.END, content)
    
    

    
def action_sub_directory_finder():
    print("Sub Directory Finder")
    clear_body()

def action_sub_domain_finder():
    print("Sub domain finder")
    clear_body()
    
def action_port_scanner():
    print("port scanner")
    clear_body()
    
def action_reverse_shell():
    print("reverse shell")
    clear_body()
    
def action_custom_wordlist():
    print("custom wordlist")
    clear_body()

def action_file_server():
    print("file server")
    clear_body()
    
def action_hash_cracker(): # hash cracker button
    clear_body()
    
    ###########################hash cracker functions#############################
    def insert_cracked_hash():
        cracked_textbox.delete("1.0", "end")
        hash_type, cracked_hashes_str = HashCracker.startHashCracker(wordlist_entry.get().lower(), hash_file_entry.get().lower(), hash_type_var.get().lower())
        cracked_textbox.insert(tk.END, f"[+] Cracked Hashes   [ {hash_type.upper()} ]\n")
        cracked_textbox.insert(tk.END, f"-"*75 + "\n")
        cracked_textbox.insert(tk.END, cracked_hashes_str + "\n")
        cracked_textbox.insert(tk.END, f"-"*75 + "\n")
    
    ##############################################################################
    
    # configure all rows and columns except for those used by the frames
    app.grid_rowconfigure(0, weight=0)
    app.grid_rowconfigure(1, weight=1)
    app.grid_rowconfigure(2, weight=0)  
    
    app.grid_columnconfigure(0, weight=1)  # First column 
    app.grid_columnconfigure(1, weight=900)  # Second column 
    app.grid_columnconfigure(2, weight=0)  # third column

    # Create left frame
    left_frame = ctk.CTkFrame(master=app, corner_radius=15)
    left_frame.grid(row=1, column=0, padx=(10, 5), pady=10, sticky='nsew')

    # hash file label
    hash_file_label = ctk.CTkLabel(master=left_frame, text="Hash List Path:")
    hash_file_label.pack(padx=10, pady=(10, 0))
    #hashfile entry field
    hash_file_entry = ctk.CTkEntry(master=left_frame)
    hash_file_entry.pack(padx=10, pady=10)
    #hashfile browse button
    hash_file_button = ctk.CTkButton(master=left_frame, text="Browse", command=lambda: open_file_browser(hash_file_entry)) 
    hash_file_button.pack(padx=10, pady=(1,10))

    # wordlist label
    wordlist_label = ctk.CTkLabel(master=left_frame, text="Wordlist Path:")
    wordlist_label.pack(padx=10, pady=(10, 0))
    #wordlist entryfield
    wordlist_entry = ctk.CTkEntry(master=left_frame)
    wordlist_entry.pack(padx=10, pady=10)
    #wordlist browse button
    wordlist_button = ctk.CTkButton(master=left_frame, text="Browse", command=lambda: open_file_browser(wordlist_entry))
    wordlist_button.pack(padx=10, pady=(1,10))


    # hash type
    hash_type_label = ctk.CTkLabel(master=left_frame, text="Hash Type:")
    hash_type_label.pack(padx=10, pady=(10, 0))
    
    hash_types = ["MD5", "SHA1", "SHA256", "SHA512"]
    hash_type_var = ctk.StringVar()

    # hash type dropdown menu
    hash_type_dropdown = ctk.CTkOptionMenu(master=left_frame, variable=hash_type_var, values=hash_types)
    hash_type_dropdown.pack(padx=10, pady=0)
    hash_type_dropdown.set("Select...")
    

 

    # Create middle frame
    middle_frame = ctk.CTkFrame(master=app, corner_radius=15)
    middle_frame.grid(row=1, column=1, padx=(5, 5), pady=10, sticky='nsew')  # Stretch to fill grid cell
    #textbox for cracked hashes
    cracked_textbox = ctk.CTkTextbox(master=middle_frame)
    cracked_textbox.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.94, relheight=0.94)
 
    def add_to_summary():
        result = cracked_textbox.get("1.0", tk.END)
        with open("Summary.txt", "a+") as f:
            f.seek(0)
            content = f.read()
            if result not in content:
                try:
                    f.write(str(result))
                except:
                    f.write("Error writing cracked hashes to summary.")
            else:
                messagebox.showerror("ERROR","Hashes are already in the Summary!")

    # right frame // can delete to create bigger text box
    right_frame = ctk.CTkFrame(master=app, corner_radius=15)
    right_frame.grid(row=1, column=2, padx=(5, 10), pady=10, sticky='nsew')
    add_to_summary_button = ctk.CTkButton(
        master=right_frame, 
        text="Add Result to Summary", 
        fg_color="darkgreen", 
        hover_color="green", 
        command=add_to_summary
    )
    add_to_summary_button.pack(padx=10, pady=20)
    
    
    # start button
    start_button = ctk.CTkButton(master=left_frame, text="Start Cracking", fg_color="darkgreen", hover_color="green", 
    command=lambda: threading.Thread(target=insert_cracked_hash(), daemon=True).start()
) 
    start_button.pack(padx=10, pady=(30,5))
    

def action_backdoor():
    print("backdoor")
    clear_body()
    
def action_retrieve_documents():
    print("retrieve documents")
    clear_body()

############################### END #######################################
############################### BANNER ####################################

# Banner frame
top_banner = ctk.CTkFrame(master=app, corner_radius=10)
top_banner.grid(row=0, column=0, columnspan=3, sticky="new")
app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure(0, weight=0)

# Loading and resizing logo in banner
original_image = Image.open("Images\\Logo.png")
resized_image = original_image.resize((300, 50), Image.Resampling.LANCZOS)
logo_image = ImageTk.PhotoImage(resized_image)

# loading highlighted image
highlighted_logo_image = Image.open("Images\\logo_highlighted6.png")  # Path to the highlighted image
highlighted_logo_image = highlighted_logo_image.resize((300, 50), Image.Resampling.LANCZOS)
highlighted_logo_image = ImageTk.PhotoImage(highlighted_logo_image)

# Adding logo to banner
logo_label = ctk.CTkLabel(master=top_banner, image=logo_image, text="")
logo_label.image = logo_image  # Prevent garbage collection
logo_label.pack(side='left', padx=20, pady=(10,10))
logo_label.bind("<Button-1>", lambda event: build_menu())


# logo hover
def on_enter(event):
    logo_label.configure(image=highlighted_logo_image)
    logo_label.image = highlighted_logo_image  # Keep a reference

def on_leave(event):
    logo_label.configure(image=logo_image)
    logo_label.image = logo_image  # Keep a reference

logo_label.bind("<Enter>", on_enter)
logo_label.bind("<Leave>", on_leave)

# Top right Frame in banner
top_right_frame = ctk.CTkFrame(master=top_banner)
top_right_frame.pack(side='right', padx=20)

# Version Label
version_label = ctk.CTkLabel(master=top_right_frame, text="V1.0", text_color="grey", font=("small fonts", 10), padx=8)
version_label.grid(row=0, column=1, sticky="w")

# Summary/Report button
summary_btn = ctk.CTkButton(master=top_right_frame, text="Summary/Report",
                            corner_radius=10, text_color="black",
                            hover_color="grey", font=("courier", 15), 
                            command=action_summary_report)
summary_btn.grid(row=0, column=0) 

############################### END #######################################
############################### FRAMES ####################################
def build_menu():
    clear_body()
    # Creating frames for each section
    frames = [ctk.CTkFrame(master=app, corner_radius=15) for _ in range(6)]

    # Position the frames as per the layout using grid
    for i, frame in enumerate(frames):
        frame.grid(row=(i//3)+1, column=i%3, padx=8, pady=8, sticky="nsew")
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
###############################CLEAR#####################################

def clear_body():
    for widget in app.winfo_children():
        if widget != top_banner:
            widget.destroy()

###########################################################################
build_menu()
app.mainloop()
