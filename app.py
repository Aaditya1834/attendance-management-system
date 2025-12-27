import customtkinter as ctk
import pages


class App(ctk.CTk):
    """Main application window for Attendance Management System"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Configure appearance
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        # Window settings
        self.geometry("565x350")
        self.title("Attendance Management System")

        # Configure grid
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Create the container that will hold all the pages
        container = ctk.CTkFrame(self)
        container.grid(row=0, column=0, sticky="nsew")
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)

        # Dictionary to store all frames
        self.frames = {}

        # List of pages to create
        page_list = [pages.welcome_page, pages.admin_page, pages.user_page]

        # Create and store all pages
        for Page in page_list:
            frame = Page(parent=container, controller=self)
            frame.grid(row=0, column=0, sticky="nsew")
            frame.columnconfigure(0, weight=1)
            frame.rowconfigure(0, weight=1)
            self.frames[Page] = frame

        # Show the welcome page first
        self.up_frame(pages.welcome_page)

    def up_frame(self, page_class):
        """Raise a specific page to the front"""
        page = self.frames[page_class]
        page.tkraise()


# Main entry point
if __name__ == "__main__":
    app = App()
    app.mainloop()