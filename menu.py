from PIL import Image, ImageTk
import customtkinter as ctk
from tkinter import filedialog
import tkinter as tk
import tkinter.messagebox as messagebox
import threading
import asyncio
import os
import re


# custom imports
import exploitation.hashCracker as HashCracker
import reconnaissance.subDirectoryFinder as SubDirFinder
import reconnaissance.subDomainFinder as SubDomainFinder
import reconnaissance.portScanner as PortScanner
import weaponization.custom_wordlist as CustomWordlist
import payload_delivery.fileServer as FileServer
import weaponization.reverseShell as ReverseShell
import installation.backdoor as Backdoor
import actions_on_system.retrieveFiles as retrieveFiles
import actions_on_system.retrieveFilesExecutable as retrieveFilesExecutable


app = ctk.CTk()
app.title('IntrusionKit')
app.geometry('900x500')
app.iconbitmap("Images\\Icon.ico")
app.resizable(True, True)
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
          
def action_summary_report(): #TODO: add date and time to summary when adding data (info found at (time))
    ################################# Summary Functions ####################################
    
    def save_to_summary():
        try:
            with open("Summary.txt", "w") as f:  
                f.write(summary_textbox.get("1.0", tk.END)) # Writing the current state
            messagebox.showinfo("Success!","Succesfully saved to Summary.txt!")
        except:
            messagebox.showerror("ERROR SAVING", "There was an error saving to Summary.txt")

    def clear_summary():
        if messagebox.askyesno("Confirmation", "Are you sure you want to clear the summary?"): # yes/no confirmation to clear
            summary_textbox.delete("1.0", "end")
            open("Summary.txt", "w").close()
            # messagebox.showinfo("Success!","Succesfully cleared Summary!")
            
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
        f.seek(0)  # Moving cursor to the start
        content = f.read()
        summary_textbox.insert(tk.END, content)
    

def action_sub_directory_finder():
    clear_body()
    
    ########################### sub directory functions #############################
    
    def startSubDirFinder():
        # set status to active
        status_label.configure(text="Status: Active", fg_color="green")
        # run sub directory finder
        domains = SubDirFinder.start(domain_entry.get(), wordlist_entry.get())
        # insert domains into textbox
        for currentDomain in domains:
            found_domains_textbox.insert(tk.END, currentDomain + "\n")
        # set status to idle
        status_label.configure(text="Status: Inactive ", fg_color="grey")
        
        
    #TODO: this function needs to be in each "module", needs to find a better way.    
    def add_to_summary():
        result = found_domains_textbox.get("1.0", tk.END)
        with open("Summary.txt", "a+") as f:
            f.seek(0)
            content = f.read()
            if result not in content:
                try:
                    f.write(str(result))
                except:
                    f.write("Error writing sub domains to summary.")
            else:
                messagebox.showerror("ERROR","sub domains are already in the Summary!")    
    #################################################################################
    
    # Configure the rows and columns
    app.grid_rowconfigure(0, weight=0)
    app.grid_rowconfigure(1, weight=1)
    app.grid_rowconfigure(2, weight=0)  
    app.grid_columnconfigure(0, weight=1)
    app.grid_columnconfigure(1, weight=300)
    app.grid_columnconfigure(2, weight=0)
    
    # Create left frame
    left_frame = ctk.CTkFrame(master=app, corner_radius=15)
    left_frame.grid(row=1, column=0, padx=(10, 5), pady=10, sticky='nsew')
    
    # Create middle frame
    middle_frame = ctk.CTkFrame(master=app, corner_radius=15)
    middle_frame.grid(row=1, column=1, padx=(5, 5), pady=10, sticky='nsew')
    
    
    # right frame // can delete to create bigger text/result box
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
    
    # domain label
    domain_label = ctk.CTkLabel(master=left_frame, text="Domain: ")
    domain_label.pack(padx=10, pady=(10, 0))
    #domain entry field
    domain_entry = ctk.CTkEntry(master=left_frame)
    domain_entry.pack(padx=10, pady=5)
    example_label = ctk.CTkLabel(master=left_frame, text="E.g. https://www.example.com/", font=("Helvetica", 12))
    example_label.pack(padx=10, pady=(0, 5))
    
    # wordlist label
    wordlist_label = ctk.CTkLabel(master=left_frame, text="Wordlist Path:")
    wordlist_label.pack(padx=10, pady=(10, 0))
    # wordlist entryfield
    wordlist_entry = ctk.CTkEntry(master=left_frame)
    wordlist_entry.pack(padx=10, pady=10)
    # wordlist browse button
    wordlist_button = ctk.CTkButton(master=left_frame, text="Browse", command=lambda: open_file_browser(wordlist_entry))
    wordlist_button.pack(padx=10, pady=(1,10))
    
    # start button
    start_button = ctk.CTkButton(master=left_frame, text="Start", fg_color="darkgreen", hover_color="green",
    command=lambda: threading.Thread(target=startSubDirFinder, daemon=True).start()) 
    start_button.pack(padx=10, pady=(30,5))
    
    found_domains_textbox = ctk.CTkTextbox(master=middle_frame)
    found_domains_textbox.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.94, relheight=0.94)
    

def action_sub_domain_finder():
    clear_body()
    
    ########################### Sub Domain Finder Functions #############################
    
    def update_gui_with_subdomain(subdomain_url):
        app.after(0, lambda: found_domains_textbox.insert(tk.END, subdomain_url + "\n"))

    
    def startSubDomainFinder(domain, wordlist_path):
        # set status to active
        status_label.configure(text="Status: Active", fg_color="green")
        # run sub domain finder
        SubDomainFinder.start(domain_entry.get(), wordlist_entry.get(), update_gui_with_subdomain)
        # set status to idle
        status_label.configure(text="Status: Inactive ", fg_color="grey")
        
    def add_to_summary():
        result = found_domains_textbox.get("1.0", tk.END)
        with open("Summary.txt", "a+") as f:
            f.seek(0)
            content = f.read()
            if result not in content:
                try:
                    f.write(str(result))
                except:
                    f.write("Error writing subdomains to summary.")
            else:
                messagebox.showerror("ERROR","Subdomains are already in the Summary!")    
    #################################################################################
    
    # Configure the rows and columns
    app.grid_rowconfigure(0, weight=0)
    app.grid_rowconfigure(1, weight=1)
    app.grid_rowconfigure(2, weight=0)  
    app.grid_columnconfigure(0, weight=1)
    app.grid_columnconfigure(1, weight=300)
    app.grid_columnconfigure(2, weight=0)
    
    # Create left frame
    left_frame = ctk.CTkFrame(master=app, corner_radius=15)
    left_frame.grid(row=1, column=0, padx=(10, 5), pady=10, sticky='nsew')
    
    # Create middle frame
    middle_frame = ctk.CTkFrame(master=app, corner_radius=15)
    middle_frame.grid(row=1, column=1, padx=(5, 5), pady=10, sticky='nsew')
    
    # Right frame // can delete to create bigger text/result box
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
    
    # Domain label
    domain_label = ctk.CTkLabel(master=left_frame, text="Domain: ")
    domain_label.pack(padx=10, pady=(10, 0))
    # Domain entry field
    domain_entry = ctk.CTkEntry(master=left_frame)
    domain_entry.pack(padx=10, pady=5)
    # Example label for domain input
    example_label = ctk.CTkLabel(master=left_frame, text="E.g., example.com (omit 'https://')", font=("Helvetica", 12))
    example_label.pack(padx=10, pady=(0, 5))
    
    # Wordlist label
    wordlist_label = ctk.CTkLabel(master=left_frame, text="Wordlist Path:")
    wordlist_label.pack(padx=10, pady=(10, 0))
    # Wordlist entry field
    wordlist_entry = ctk.CTkEntry(master=left_frame)
    wordlist_entry.pack(padx=10, pady=10)
    # Wordlist browse button
    wordlist_button = ctk.CTkButton(master=left_frame, text="Browse", command=lambda: open_file_browser(wordlist_entry))
    wordlist_button.pack(padx=10, pady=(1,10))
    
    # Start button
    start_button = ctk.CTkButton(
        master=left_frame, 
        text="Start", 
        fg_color="darkgreen", 
        hover_color="green",
        command=lambda: threading.Thread(
            target=lambda: startSubDomainFinder(domain_entry.get(), wordlist_entry.get()), 
            daemon=True
        ).start()
    )
    start_button.pack(padx=10, pady=(30,5))
    
    # Textbox for found domains
    global found_domains_textbox
    found_domains_textbox = ctk.CTkTextbox(master=middle_frame)
    found_domains_textbox.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.94, relheight=0.94)

    # Set status label at the bottom or somewhere appropriate to indicate idle status initially
    status_label.configure(text="Status: Inactive ", fg_color="grey")

    
def action_port_scanner():
    clear_body()

    #########################################################
    def add_to_summary():
        result = open_ports_textbox.get("1.0", tk.END)
        with open("Summary.txt", "a+") as f:
            f.seek(0)
            content = f.read()
            if result not in content:
                try:
                    f.write(str(result))
                except:
                    f.write("Error writing subdomains to summary.")
            else:
                messagebox.showerror("ERROR","Subdomains are already in the Summary!") 

    def portScannerCallbacks(callback_message):
        app.after(0, lambda: open_ports_textbox.insert(tk.END, callback_message + "\n"))

    def start_port_scanner():
        ip_address = IPaddress_entry.get()
        ports = ports_entry.get().replace(" ", "") if not all_ports_checkbox_var.get() else "all ports"
        vulnScan = scan_for_vulnerability_var.get() == 1
        open_ports_textbox.insert(tk.END, f"Started scanning Ports[{ports}] on {ip_address}\n")
        
        # Set status to active
        update_scanner_status(True)
        
        def on_scan_complete():
            # This function will be passed as a callback to be called when scanning is complete
            app.after(0, lambda: update_scanner_status(False))

        # Start the scanning in a new thread
        threading.Thread(target=lambda: PortScanner.startPortScanner(ip_address, ports, vulnScan, portScannerCallbacks, on_scan_complete), daemon=True).start()

    #########################################################


    # Configure the rows and columns
    app.grid_rowconfigure(0, weight=0)
    app.grid_rowconfigure(1, weight=1)
    app.grid_rowconfigure(2, weight=0)  
    app.grid_columnconfigure(0, weight=0)
    app.grid_columnconfigure(1, weight=300, minsize=500)
    app.grid_columnconfigure(2)
    
    # Create left frame
    left_frame = ctk.CTkFrame(master=app, corner_radius=15)
    left_frame.grid(row=1, column=0, padx=(10, 5), pady=10, sticky='nsew')
    
    # Create middle frame
    middle_frame = ctk.CTkFrame(master=app, corner_radius=15)
    middle_frame.grid(row=1, column=1, padx=(5, 5), pady=10, sticky='nsew')
    # result texbox
    open_ports_textbox = ctk.CTkTextbox(master=middle_frame)
    open_ports_textbox.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.94, relheight=0.94)
    
    # right frame // can delete to create bigger text/result box
    right_frame = ctk.CTkFrame(master=app, corner_radius=15)
    right_frame.grid(row=1, column=2, padx=(5, 10), pady=10, sticky='nsew')
    add_to_summary_button = ctk.CTkButton(
        master=right_frame, 
        text="Save\nResult", 
        fg_color="green", 
        hover_color="grey", 
        command=add_to_summary
    )
    add_to_summary_button.pack(padx=10, pady=20)
    
    
    # ipaddress label
    IPaddress = ctk.CTkLabel(master=left_frame, text="IP Address:")
    IPaddress.pack(padx=10, pady=(10, 0))
    # ipaddress entryfield
    IPaddress_entry = ctk.CTkEntry(master=left_frame, width=130)
    IPaddress_entry.pack(padx=0, pady=5)
    
    # ports label
    ports_label = ctk.CTkLabel(master=left_frame, text="Ports:")
    ports_label.pack(padx=10, pady=(10, 0))
    # ports entryfield
    ports_entry = ctk.CTkEntry(master=left_frame, width=130)
    ports_entry.pack(padx=10, pady=10)
    

    # Scan all ports checkbox
    all_ports_checkbox_var = ctk.IntVar()
    all_ports_checkbox = ctk.CTkCheckBox(master=left_frame, text="All ports", variable=all_ports_checkbox_var)
    all_ports_checkbox.pack(pady=(10), padx=(20), anchor="w")

    # Scan for vulnerabilities checkbox
    scan_for_vulnerability_var = ctk.IntVar()
    scan_for_vulnerability_checkbox = ctk.CTkCheckBox(master=left_frame, text="Check for Vulns", variable=scan_for_vulnerability_var)
    scan_for_vulnerability_checkbox.pack(padx=(20), anchor="w")
    

    # start scan button
    scan_button = ctk.CTkButton(master=left_frame, text="Start Scanning", command=lambda: start_port_scanner())
    scan_button.pack(padx=15, pady=(30,5))

  
def action_reverse_shell():
    clear_body()
        
    ########################### hash cracker functions #############################

    def open_directory_browser():
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            output_entry.set(folder_selected)
    
    def log_output():
        log_textbox.after(0, lambda: log_textbox.insert(tk.END, f'Reverse Shell Output Location:\n{output_entry.get()}/{"Reverse_Shell"}.exe\n\nIP Address set to: {ipaddress_entry.get()}\nPort: {port_entry.get()}'))

    
    ##############################################################################
    
    app.grid_rowconfigure(0, weight=0)
    app.grid_rowconfigure(1, weight=1)
    app.grid_columnconfigure(0, weight=100)
    app.grid_columnconfigure(1, weight=200) 


    # Create left frame
    left_frame = ctk.CTkFrame(master=app, corner_radius=15)
    left_frame.grid(row=1, column=0, padx=(10, 5), pady=10, sticky='nsew')
    
    # Create middle frame
    middle_frame = ctk.CTkFrame(master=app, corner_radius=15)
    middle_frame.grid(row=1, column=1, padx=(5, 5), pady=10, sticky='nsew')  # Stretch to fill grid cell


    ### Left frame content ###
    
    # IP Address label
    ipaddress_label = ctk.CTkLabel(master=left_frame, text="Listening IP-Address:")
    ipaddress_label.pack(padx=10, pady=(10, 0))
    #IP Address entry field
    ipaddress_entry = ctk.CTkEntry(master=left_frame)
    ipaddress_entry.pack(padx=10, pady=0)

    
    # port label
    port_label = ctk.CTkLabel(master=left_frame, text="Listening Port:")
    port_label.pack(padx=10, pady=(10, 0))
    # port entry field
    port_entry = ctk.CTkEntry(master=left_frame)
    port_entry.pack(padx=10, pady=0)


    # output label
    output_label = ctk.CTkLabel(master=left_frame, text="File Output Path:")
    output_label.pack(padx=10, pady=(10, 0))
    # output entryfield
    output_entry = ctk.StringVar()
    output_entry_widget = ctk.CTkEntry(left_frame, textvariable=output_entry)
    output_entry_widget.pack(padx=10, pady=(0,10))
    # output browse button
    output_button = ctk.CTkButton(master=left_frame, text="Browse", command=lambda: open_directory_browser())
    output_button.pack(padx=10, pady=(1,10))

    # OS type
    hash_type_label = ctk.CTkLabel(master=left_frame, text="File Type:")
    hash_type_label.pack(padx=10, pady=(10, 0))
    
    OS_types = ["EXE", "Python Script", "bash script", "powershell script"] #TODO: add more than exe
    OS_type_var = ctk.StringVar()
    
    hash_type_dropdown = ctk.CTkOptionMenu(master=left_frame, variable=OS_type_var, values=OS_types)
    hash_type_dropdown.pack(padx=10, pady=0)
    hash_type_dropdown.set("Select...")
    
    # Create button
    start_button = ctk.CTkButton(master=left_frame, text="Create", fg_color="darkgreen", hover_color="green", 
    command=lambda: (log_output(),update_scanner_status(True), threading.Thread(target=ReverseShell.make_executable(output_entry.get(), ipaddress_entry.get(), port_entry.get(), script_name="Reverse_Shell.py", exe_name="Reverse_Shell"), daemon=True).start())) 
    start_button.pack(padx=10, pady=(30,5))
    
    ######## Right frame content #########

    #textbox for cracked hashes
    log_textbox = ctk.CTkTextbox(master=middle_frame)
    log_textbox.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.94, relheight=0.94)
    
    #TODO: error handling to check if fields are empty
    #TODO: add better method to set status active and inactive
    #TODO: add button to go to interact with reverse shell / backdoor
    
    
    
def action_custom_wordlist():
    clear_body()
    # TODO - add function to calculate how many words will be generated
        
    #TODO: this function needs to be in each "module", needs to find a better way.    
    def save_to_file():
        result = found_domains_textbox.get("1.0", tk.END)
        with open("custom_wordlist.txt", "a+") as f:
            f.seek(0)
            content = f.read()
            if result not in content:
                try:
                    f.write(str(result))
                except:
                    f.write("Error writing custom wordlist to file.")
            else:
                messagebox.showerror("ERROR","Custom wordlist is already in the file!")    
    #################################################################################
    
    # Configure the rows and columns
    app.grid_rowconfigure(0, weight=0)
    app.grid_rowconfigure(1, weight=1)
    app.grid_rowconfigure(2, weight=0)  
    app.grid_columnconfigure(0, weight=1)
    app.grid_columnconfigure(1, weight=3)
    app.grid_columnconfigure(2, weight=0)
    
    # Create left frame
    left_frame = ctk.CTkFrame(master=app, corner_radius=15)
    left_frame.grid(row=1, column=0, padx=(10, 5), pady=10, sticky='nsew')
    
    # Create middle frame
    middle_frame = ctk.CTkFrame(master=app, corner_radius=15)
    middle_frame.grid(row=1, column=1, padx=(5, 5), pady=10, sticky='nsew')
    
    
    # right frame // can delete to create bigger text/result box
    right_frame = ctk.CTkFrame(master=app, corner_radius=15)
    right_frame.grid(row=1, column=2, padx=(5, 10), pady=10, sticky='nsew')
    
    # output name label
    output_name = ctk.CTkLabel(master=right_frame, text="Output filename:")
    output_name.pack(padx=10, pady=(10, 0))
    # output name entryfield
    output_entry = ctk.CTkEntry(master=right_frame, width=150)
    output_entry.pack(padx=10, pady=10)

    
    add_to_summary_button = ctk.CTkButton(
        master=right_frame, 
        text="Save to File", 
        fg_color="grey", 
        hover_color="lightgrey", 
        command=save_to_file
    )
    add_to_summary_button.pack(padx=10, pady=20)
    
    
    
    example_label = ctk.CTkLabel(master=left_frame, text="Seperate With Commas", font=("Helvetica", 15), text_color="lightblue")
    example_label.pack(padx=10, pady=(10, 5))
    
    # Words label
    words = ctk.CTkLabel(master=left_frame, text="Words: ")
    words.pack(padx=10, pady=(10, 0))
    # words entryfield
    words_entry = ctk.CTkEntry(master=left_frame, width=250)
    words_entry.pack(padx=0, pady=5)
    
    # numbers label
    wordlist_label = ctk.CTkLabel(master=left_frame, text="Numbers:")
    wordlist_label.pack(padx=10, pady=(10, 0))
    # numbers entryfield
    numbers_entry = ctk.CTkEntry(master=left_frame, width=250)
    numbers_entry.pack(padx=10, pady=10)
    
    
    # special characters label
    special_chars = ctk.CTkLabel(master=left_frame, text="Special Characters:")
    special_chars.pack(padx=10, pady=(10, 0))
    # special characters entryfield
    special_chars_entry = ctk.CTkEntry(master=left_frame, width=250)
    special_chars_entry.pack(padx=10, pady=10)
    
    
    generated_words_textbox = ctk.CTkTextbox(master=middle_frame)
    generated_words_textbox.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.94, relheight=0.94)

    # Generate button
    generate_button = ctk.CTkButton(master=left_frame, text="Generate Wordlist", command=lambda: start_generate_wordlist(words_entry.get(), numbers_entry.get(), special_chars_entry.get(), output_entry.get()))
    generate_button.pack(padx=10, pady=(30,5))

    def start_generate_wordlist(gen_words, gen_numbers, gen_special_chars, filename):
        gen_words = gen_words.split(',')
        gen_numbers = gen_numbers.split(',')
        gen_special_chars = gen_special_chars.split(',')
        filename = filename.strip() if filename else "custom_wordlist.txt"
        generated_words = CustomWordlist.generate_wordlist(gen_words, gen_numbers, gen_special_chars, filename)
        
        # print words to textbox
        for word in generated_words:
            generated_words_textbox.insert(tk.END, word + "\n")
        
        messagebox.showinfo("Success", f"Wordlist saved as {filename}")


def action_file_server():
    clear_body()

#################################################################################################################

    def make_ascii_tree(path, prefix=''):
        tree_str = f"{prefix}+-- {os.path.basename(path)}/\n"
        prefix += "|   "
        try:
            # List directory contents
            contents = [os.path.join(path, d) for d in os.listdir(path)]
            # Separate directories and files
            directories = [d for d in contents if os.path.isdir(d)]
            files = [f for f in contents if os.path.isfile(f)]
            # Add directories and files to tree
            for directory in directories:
                tree_str += make_ascii_tree(directory, prefix)
            for file in files:
                tree_str += f"{prefix}+-- {os.path.basename(file)}\n"
        except PermissionError:
            tree_str += f"{prefix}+-- [Permission Denied]\n"
        return tree_str

    def open_directory_browser():
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            directory_entry.set(folder_selected)
            ascii_tree = make_ascii_tree(folder_selected)
            fileserver_textbox.delete('1.0', ctk.END)  # Assuming ctk supports this method or use equivalent
            fileserver_textbox.insert('1.0', ascii_tree)

#################################################################################################################

    # Configure the rows and columns
    app.grid_rowconfigure(0, weight=0)
    app.grid_rowconfigure(1, weight=1)
    app.grid_rowconfigure(2, weight=0)  
    app.grid_columnconfigure(0, weight=0)
    app.grid_columnconfigure(1, weight=300)

    # Create left frame for inputs
    left_frame = ctk.CTkFrame(master=app, corner_radius=15)
    left_frame.grid(row=1, column=0, padx=(10, 5), pady=10, sticky='nsew')

    # LEFT FRAME CONTENTS
    directory_label = ctk.CTkLabel(left_frame, text="Directory Path:")
    directory_label.pack(padx=10, pady=(10,0))

    # Directory
    directory_entry = ctk.StringVar()
    directory_entry_widget = ctk.CTkEntry(left_frame, textvariable=directory_entry)
    directory_entry_widget.pack(padx=10, pady=(0,10))
    directory_button = ctk.CTkButton(left_frame, text="Browse", command=open_directory_browser)
    directory_button.pack(padx=10, pady=(0,10))

    # Port
    port_label = ctk.CTkLabel(left_frame, text="Server Port:")
    port_label.pack(padx=10, pady=(10,0))
    port_entry = ctk.CTkEntry(left_frame)
    port_entry.pack(padx=10, pady=(0,10))

    # Start button
    start_server_button = ctk.CTkButton(left_frame, text="Start Server", fg_color="darkgreen" , command=lambda: (update_scanner_status(True) , fileserver_textbox.insert(tk.END, f"\n\nAvailable at | http://localhost:{port_entry.get()}") ,FileServer.start_file_server(directory_entry.get(), int(port_entry.get()))))
    start_server_button.pack(padx=10, pady=(20,5))

    # stop button
    stop_server_button = ctk.CTkButton(left_frame, text="Stop Server", fg_color="darkred", command=lambda: (update_scanner_status(False) ,FileServer.stop_file_server()))
    stop_server_button.pack(padx=10, pady=(5,10))


    # Create right frame for displaying directory content or other messages
    right_frame = ctk.CTkFrame(master=app, corner_radius=15)
    right_frame.grid(row=1, column=1, padx=(5, 10), pady=10, sticky='nsew')

    # tree texbox
    fileserver_textbox = ctk.CTkTextbox(master=right_frame)
    fileserver_textbox.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.94, relheight=0.94)



def action_hash_cracker(): 
    clear_body()
        
    ########################### hash cracker functions #############################
    
    # function to start the hash cracker
    def insert_cracked_hash_callback(hash, cracked_password):
        # Safe update to GUI from thread
        cracked_textbox.after(0, lambda: cracked_textbox.insert(tk.END, f"{hash}: {cracked_password}\n"))

    def insert_cracked_hash():
        if hash_file_entry.get() == "" or wordlist_entry.get() == "":
            messagebox.showerror("ERROR", "Missing hash file or wordlist path!")
            return
        
        cracked_textbox.delete("1.0", "end")


        def run_async_cracker():
            asyncio.run(HashCracker.startHashCracker(
                wordlist_entry.get().lower(),
                hash_file_entry.get().lower(),
                hash_type_var.get().lower(),
                insert_cracked_hash_callback,
                on_crack_complete
            ))

        update_scanner_status(True)
        threading.Thread(target=run_async_cracker, daemon=True).start()
                
        def on_crack_complete():
            app.after(0, lambda: update_scanner_status(False))
            
    # function to add cracked hashes to summary
    def add_to_summary():
        result = cracked_textbox.get("1.0", tk.END)
        with open("Summary.txt", "a+") as summary:
            summary.seek(0)
            content = summary.read()
            if result == "" or result == " ":
                messagebox.showerror("ERROR","No hashes to add to Summary!")
                return
            elif result not in content:
                try:
                    summary.write(str(result))
                    return
                except:
                    summary.write("Error writing cracked hashes to summary.")
            else:
                messagebox.showerror("ERROR","Hashes are already in the Summary!")
    
    ##############################################################################
    
    app.grid_rowconfigure(0, weight=0)
    app.grid_rowconfigure(1, weight=1)
    app.grid_rowconfigure(2, weight=0)  
    
    app.grid_columnconfigure(0, weight=100)
    app.grid_columnconfigure(1, weight=900) 
    app.grid_columnconfigure(2, weight=0) 

    # Create left frame
    left_frame = ctk.CTkFrame(master=app, corner_radius=15)
    left_frame.grid(row=1, column=0, padx=(10, 5), pady=10, sticky='nsew')
    
    # Create middle frame
    middle_frame = ctk.CTkFrame(master=app, corner_radius=15)
    middle_frame.grid(row=1, column=1, padx=(5, 5), pady=10, sticky='nsew')  # Stretch to fill grid cell
    
    # right frame // can delete to create bigger text/result box
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

    ### left frame content ###
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
    
    ### middle frame content ###
    #textbox for cracked hashes
    cracked_textbox = ctk.CTkTextbox(master=middle_frame)
    cracked_textbox.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.94, relheight=0.94)
    
    ### right frame content ###
    
    # start button
    start_button = ctk.CTkButton(master=left_frame, text="Start Cracking", fg_color="darkgreen", hover_color="green", 
    command=lambda: threading.Thread(target=insert_cracked_hash, daemon=True).start()) 
    start_button.pack(padx=10, pady=(30,5))
    

def action_backdoor():
    clear_body()
        
    ########################### shell functions #############################
    
    def send_command(command, ipaddress, port):
        log_textbox.delete("1.0", "end")
        if port == "" or command == "":
            messagebox.showerror("ERROR", "Missing port or command!")
            return
        response = Backdoor.send_command(command, ipaddress, port)
        log_textbox.insert(ctk.END, response)
        
    
    ##############################################################################
    
    app.grid_rowconfigure(0, weight=0)
    app.grid_rowconfigure(1, weight=10)
    app.grid_columnconfigure(0, weight=100)
    app.grid_columnconfigure(1, weight=200) 


    # Create left frame
    left_frame = ctk.CTkFrame(master=app, corner_radius=15)
    left_frame.grid(row=1, column=0, padx=(10, 5), pady=10, sticky='nsew')
    
    # Create middle frame
    middle_frame = ctk.CTkFrame(master=app, corner_radius=15)
    middle_frame.grid(row=1, column=1, padx=(5, 5), pady=10, sticky='nsew')  # Stretch to fill grid cell


    ### Left frame content ###
    
    # port label
    port_label = ctk.CTkLabel(master=left_frame, text="Port:")
    port_label.pack(padx=10, pady=(20, 0))
    # port entry field
    port_entry = ctk.CTkEntry(master=left_frame)
    port_entry.pack(padx=10, pady=(0, 30))


    # output label
    output_label = ctk.CTkLabel(master=left_frame, text="Command:")
    output_label.pack(padx=10, pady=(10, 0))
    # output entryfield
    output_entry = ctk.StringVar()
    output_entry_widget = ctk.CTkEntry(left_frame, textvariable=output_entry)
    output_entry_widget.pack(padx=10, pady=(0,10))
    
    # send command button
    start_button = ctk.CTkButton(master=left_frame, text="Send", fg_color="darkgreen", hover_color="green", 
    command=lambda: send_command(output_entry.get(), "localhost", port_entry.get()))
    start_button.pack(padx=10, pady=(0,50))
    
    #TODO: add connection label to let know if shell is working
    
    ######## Right frame content #########

    # output label
    output_label = ctk.CTkLabel(master=middle_frame, text="Response:")
    output_label.pack(padx=10, pady=(5, 5))

    #textbox for cracked hashes
    log_textbox = ctk.CTkTextbox(master=middle_frame)
    log_textbox.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.94, relheight=0.80)

      
def action_retrieve_documents():
    clear_body()
        
    ########################### shell functions #############################

    def save_location():
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            save_location_entry.set(folder_selected)

    def send_file_request():
        files = retrieveFiles.retrieve_documents(directory_entry.get(), extention_entry.get(), connect_ipaddress_entry.get(), port_entry.get())
        log_textbox.delete("1.0", tk.END)
        for x in files:
            log_textbox.insert(ctk.END, f"{x}\n")

    def download_file():
        retrieveFiles.request_file(directory_entry.get(), download_file_entry.get(), connect_ipaddress_entry.get(), port_entry.get())
    
    def create_executable():
        retrieveFilesExecutable.make_executable(save_location_entry.get(), ipaddress_entry.get(), port_entry.get(), "File_Retriever.py", "File_Retriever")
    ##############################################################################
    
    app.grid_rowconfigure(0, weight=0)
    app.grid_rowconfigure(1, weight=10)
    app.grid_columnconfigure(0, weight=50)
    app.grid_columnconfigure(1, weight=50)
    app.grid_columnconfigure(2, weight=200) 


    # Create left frame
    left_frame = ctk.CTkFrame(master=app, corner_radius=15)
    left_frame.grid(row=1, column=0, padx=(10, 5), pady=10, sticky='nsew')

    # Create middle frame
    middle_frame = ctk.CTkFrame(master=app, corner_radius=15)
    middle_frame.grid(row=1, column=1, padx=(5, 5), pady=10, sticky='nsew')  # Stretch to fill grid cell
    
    # Create right frame
    right_frame = ctk.CTkFrame(master=app, corner_radius=15)
    right_frame.grid(row=1, column=2, padx=(5, 5), pady=10, sticky='nsew')  # Stretch to fill grid cell

    ###left frame content ###

    # left header label
    port_label = ctk.CTkLabel(master=left_frame, text="Create client\nexecutable", font=("courier", 16))
    port_label.pack(padx=10, pady=(5, 10))


    # ipaddress label
    ipaddress_label = ctk.CTkLabel(master=left_frame, text="IP Address:")
    ipaddress_label.pack(padx=10, pady=(10, 0))
    # ipaddress entry field
    ipaddress_entry = ctk.CTkEntry(master=left_frame)
    ipaddress_entry.pack(padx=10, pady=(0, 10))

    # ipaddress label
    port_label = ctk.CTkLabel(master=left_frame, text="Port To Listen On:")
    port_label.pack(padx=10, pady=(10, 0))
    # ipaddress entry field
    port_entry = ctk.CTkEntry(master=left_frame)
    port_entry.pack(padx=10, pady=(0, 10))

    # output label
    save_location_label = ctk.CTkLabel(master=left_frame, text="File Output Path:")
    save_location_label.pack(padx=10, pady=(10, 0))
    # output entryfield
    save_location_entry = ctk.StringVar()
    save_location_entry_widget = ctk.CTkEntry(left_frame, textvariable=save_location_entry)
    save_location_entry_widget.pack(padx=10, pady=(0,10))
    # output browse button
    save_location_button = ctk.CTkButton(master=left_frame, text="Browse", command=lambda: save_location())
    save_location_button.pack(padx=10, pady=(1,10))


    # create executable button
    create_executable_button = ctk.CTkButton(master=left_frame, text="Create Executable", fg_color="darkgreen", hover_color="green", 
    command=lambda: create_executable())
    create_executable_button.pack(padx=10, pady=(0,20))

    ### middle frame content ###
    
    # middle header label
    port_label = ctk.CTkLabel(master=middle_frame, text="Intecract with executable", font=("courier", 16))
    port_label.pack(padx=10, pady=(5, 0))


    # ipaddress label
    connect_ipaddress_label = ctk.CTkLabel(master=middle_frame, text="IP Address:")
    connect_ipaddress_label.pack(padx=10, pady=(10, 0))
    # ipaddressentryfield
    connect_ipaddress_entry = ctk.StringVar()
    connect_ipaddress_entry_widget = ctk.CTkEntry(middle_frame, textvariable=connect_ipaddress_entry)
    connect_ipaddress_entry_widget.pack(padx=10, pady=(0,5))


    # port label
    port_label = ctk.CTkLabel(master=middle_frame, text="Connect to Port:")
    port_label.pack(padx=10, pady=(10, 0))
    # port entry field
    port_entry = ctk.CTkEntry(master=middle_frame)
    port_entry.pack(padx=10, pady=(0, 10))


    # directory label
    directory_label = ctk.CTkLabel(master=middle_frame, text="Directory to search:")
    directory_label.pack(padx=10, pady=(5, 0))
    # directory entryfield
    directory_entry = ctk.StringVar()
    directory_entry_widget = ctk.CTkEntry(middle_frame, textvariable=directory_entry)
    directory_entry_widget.pack(padx=10, pady=(0,5))

    # extention label
    extention_label = ctk.CTkLabel(master=middle_frame, text="File Extention ( TXT, PDF, ... ):")
    extention_label.pack(padx=10, pady=(5, 0))
    # extention entryfield
    extention_entry = ctk.StringVar()
    extention_entry_widget = ctk.CTkEntry(middle_frame, textvariable=extention_entry)
    extention_entry_widget.pack(padx=10, pady=(0,5))



    # send command button
    start_button = ctk.CTkButton(master=middle_frame, text="Search For Files", fg_color="darkgreen", hover_color="green", 
    command=lambda: send_file_request())
    start_button.pack(padx=10, pady=(10,0))
    
    #TODO: add connection label to let know if shell is working
    

    ######## Right frame content #########

    # bottom frame
    bottom_frame = ctk.CTkFrame(master=right_frame)
    bottom_frame.pack(side='bottom', pady=(0,10))

    # output label
    download_file_label = ctk.CTkLabel(master=bottom_frame, text="Download file:")
    download_file_label.pack(padx=0, pady=(0, 0))
    # output entryfield
    download_file_entry = ctk.StringVar()
    download_file_entry_widget = ctk.CTkEntry(bottom_frame, textvariable=download_file_entry)
    download_file_entry_widget.pack(padx=0, pady=(0,0))
    #save to file
    download_button = ctk.CTkButton(master=bottom_frame, text="Download", command=lambda: download_file()) #TODO: add function
    download_button.pack()

    # output label
    output_label = ctk.CTkLabel(master=right_frame, text="Response:")
    output_label.pack(padx=10, pady=(0, 0))
    #textbox for cracked hashes
    log_textbox = ctk.CTkTextbox(master=right_frame)
    log_textbox.place(relx=0.5, rely=0.4, anchor='center', relwidth=0.94, relheight=0.65)



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
highlighted_logo_image = Image.open("Images\\logo_highlighted.png")
highlighted_logo_image = highlighted_logo_image.resize((300, 50), Image.Resampling.LANCZOS)
highlighted_logo_image = ImageTk.PhotoImage(highlighted_logo_image)

# Adding logo to banner
logo_label = ctk.CTkLabel(master=top_banner, image=logo_image, text="")
logo_label.pack(side='left', padx=20, pady=(10,10))
logo_label.bind("<Button-1>", lambda event: build_menu())

# logo hover animation
def on_enter(event):
    logo_label.configure(image=highlighted_logo_image)
def on_leave(event):
    logo_label.configure(image=logo_image)
logo_label.bind("<Enter>", on_enter)
logo_label.bind("<Leave>", on_leave)


# status label
status_label = ctk.CTkLabel(master=top_banner, text="Status: Inactive", fg_color="grey", text_color="black", corner_radius=10 ,font=("courier", 11))
status_label.pack(side=ctk.LEFT, padx=(100,0), pady=5)


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
        app.grid_columnconfigure(i%3, weight=1, minsize=0)
        app.grid_rowconfigure((i//3)+1, weight=1, minsize=0)
        
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
        ("Actions on system", [("Retrieve Files", action_retrieve_documents)], frames[5])
    ]

    # Add labels and buttons to each frame with corresponding actions
    for category, buttons, frame in buttons_info:
        label = ctk.CTkLabel(master=frame, text=category, text_color="grey", font=("Small fonts", 18))
        label.pack(pady=12)
        for btn_text, action in buttons:
            button = ctk.CTkButton(master=frame, text=btn_text, corner_radius=10, text_color="black", hover_color="grey", font=("courier", 15), command=action)
            button.pack(pady=8)

    
############################### END #######################################
        
def update_scanner_status(is_active):
    status = "Status: active" if is_active else "Status: inactive"
    fg_color = "green" if is_active else "grey"
    status_label.configure(text=status, fg_color=fg_color)


###############################CLEAR#####################################

def clear_body():
    for widget in app.winfo_children():
        if widget != top_banner:
            widget.destroy()

###########################################################################
build_menu()
app.mainloop()
