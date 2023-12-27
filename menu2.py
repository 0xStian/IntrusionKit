import customtkinter as ctk

# Set the app style
ctk.set_appearance_mode("System")  # Can be "System", "Dark", or "Light"
ctk.set_default_color_theme("dark-blue")  # Placeholder, theme needs to be customized

class RedTeamToolkit(ctk.CTk):

    WIDTH = 900
    HEIGHT = 650

    def __init__(self):
        super().__init__()

        self.title("NetRavage Toolkit")
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")

        # Left navigation frame
        self.nav_frame = ctk.CTkFrame(self, width=200, corner_radius=10)
        self.nav_frame.pack(side="left", fill="y", padx=20, pady=20)

        # Main content frame
        self.content_frame = ctk.CTkFrame(self, corner_radius=10)
        self.content_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Add categories to navigation frame
        self.add_nav_button("Recon", self.show_recon_tools)
        self.add_nav_button("Weaponization", self.show_weaponization_tools)
        self.add_nav_button("Delivery", self.show_delivery_tools)
        self.add_nav_button("Exploitation", self.show_exploitation_tools)
        self.add_nav_button("Installation", self.show_installation_tools)
        self.add_nav_button("Actions", self.show_actions_tools)

        # Add an 'About' button
        self.about_button = ctk.CTkButton(self.nav_frame, text="About", command=self.show_about)
        self.about_button.pack(pady=5)

        # Add a 'Summary/Report' button
        self.report_button = ctk.CTkButton(self.nav_frame, text="Summary / Report", command=self.show_report)
        self.report_button.pack(pady=5)

    def add_nav_button(self, text, command):
        button = ctk.CTkButton(self.nav_frame, text=text, command=command, corner_radius=8)
        button.pack(pady=5, padx=10, fill="x")

    def show_about(self):
        self.clear_content_frame()
        label = ctk.CTkLabel(self.content_frame, text="About NetRavage Toolkit")
        label.pack(pady=10)

    def show_recon_tools(self):
        self.clear_content_frame()
        label = ctk.CTkLabel(self.content_frame, text="Recon Tools")
        label.pack(pady=10)

    def show_weaponization_tools(self):
        self.clear_content_frame()
        label = ctk.CTkLabel(self.content_frame, text="Weaponization Tools")
        label.pack(pady=10)

    def show_delivery_tools(self):
        self.clear_content_frame()
        label = ctk.CTkLabel(self.content_frame, text="Delivery Tools")
        label.pack(pady=10)

    def show_exploitation_tools(self):
        self.clear_content_frame()
        label = ctk.CTkLabel(self.content_frame, text="Exploitation Tools")
        label.pack(pady=10)

    def show_installation_tools(self):
        self.clear_content_frame()
        label = ctk.CTkLabel(self.content_frame, text="Installation Tools")
        label.pack(pady=10)

    def show_actions_tools(self):
        self.clear_content_frame()
        label = ctk.CTkLabel(self.content_frame, text="Actions Tools")
        label.pack(pady=10)

    def show_report(self):
        self.clear_content_frame()
        label = ctk.CTkLabel(self.content_frame, text="Summary / Report")
        label.pack(pady=10)

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = RedTeamToolkit()
    app.mainloop()
