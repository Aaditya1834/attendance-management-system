import tkinter
import customtkinter as ctk
import os
from tkcalendar import DateEntry
import pandas as pd
from datetime import datetime


class admin_page(ctk.CTkFrame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)

        # Horizontal Frames
        self.frame_top = ctk.CTkFrame(self)
        self.frame_middle = ctk.CTkFrame(self)
        self.frame_bottom = ctk.CTkFrame(self)
        
        # Grid Frames
        self.frame_top.grid(row=0, column=0, sticky="nsew")
        self.frame_middle.grid(row=1, column=0, sticky="nsew")
        self.frame_bottom.grid(row=2, column=0, sticky="nsew")
        
        # Configure grid weights
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=3)
        self.rowconfigure(2, weight=1)
        
        # Column config
        self.frame_top.columnconfigure(0, weight=1)
        self.frame_middle.columnconfigure(0, weight=1)
        self.frame_middle.columnconfigure(1, weight=1)
        self.frame_middle.columnconfigure(2, weight=1)
        self.frame_bottom.columnconfigure(0, weight=1)
        self.frame_bottom.columnconfigure(1, weight=1)
        
        # Row Config
        self.frame_top.rowconfigure(0, weight=1)
        self.frame_middle.rowconfigure(0, weight=1)
        self.frame_middle.rowconfigure(1, weight=1)
        self.frame_middle.rowconfigure(2, weight=1)
        self.frame_middle.rowconfigure(3, weight=1)
        self.frame_middle.rowconfigure(4, weight=1)
        self.frame_bottom.rowconfigure(0, weight=1)

        # Text
        self.string_header = tkinter.StringVar(value="Welcome Admin!")
        self.label_header = ctk.CTkLabel(master=self.frame_top, textvariable=self.string_header, 
                                         width=120, height=25)
        self.label_header.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Button Launch Excel
        self.button_launch_excel = ctk.CTkButton(master=self.frame_middle, 
                                                 text="Launch the Original Excel", 
                                                 width=20, height=5, 
                                                 command=self.launch_excel)
        self.button_launch_excel.grid(row=0, columnspan=3, padx=10, pady=10)

        # Select Date Label
        self.string_select_date = tkinter.StringVar(value="Or please Select a Date:")
        self.label_select_date = ctk.CTkLabel(master=self.frame_middle, 
                                              textvariable=self.string_select_date, width=20)
        self.label_select_date.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Label Date Entry
        self.string_date_begin = tkinter.StringVar(value="Begin Date")
        self.label_date_begin = ctk.CTkLabel(master=self.frame_middle, 
                                             textvariable=self.string_date_begin, width=20, height=5)
        self.label_date_begin.grid(row=2, column=0, padx=3, pady=3)

        # Label Date Entry 2
        self.string_date_end = tkinter.StringVar(value="End Date")
        self.label_date_end = ctk.CTkLabel(master=self.frame_middle, 
                                           textvariable=self.string_date_end, width=20, height=5)
        self.label_date_end.grid(row=2, column=1, padx=3, pady=3)

        # Date Entry 1
        self.date_entry = DateEntry(master=self.frame_middle, width=12)
        self.date_entry.grid(row=3, column=0, padx=10, pady=10)

        # Date Entry 2
        self.date_entry2 = DateEntry(master=self.frame_middle, width=12)
        self.date_entry2.grid(row=3, column=1, padx=10, pady=10)

        # Save entry data
        self.button_excel = ctk.CTkButton(master=self.frame_middle, text="Save Data", 
                                          width=20, height=5, command=self.save)
        self.button_excel.grid(row=4, columnspan=3, padx=20, pady=20)

        # Quit Button
        self.button_quit = ctk.CTkButton(master=self.frame_bottom, text="Back to Home",
                                         command=lambda: controller.up_frame(welcome_page))
        self.button_quit.grid(row=0, column=0, padx=10, pady=10)

    def launch_excel(self):
        """Launch the original CSV file"""
        try:
            if os.path.exists('data.csv'):
                if os.name == 'nt':  # Windows
                    os.startfile('data.csv')
                elif os.name == 'posix':  # macOS and Linux
                    if os.uname().sysname == 'Darwin':  # macOS
                        os.system('open data.csv')
                    else:  # Linux
                        os.system('xdg-open data.csv')
            else:
                print("Error: data.csv not found!")
        except Exception as e:
            print(f"Error opening file: {e}")

    def save(self):
        """Save filtered data based on date range"""
        try:
            begin = self.date_entry.get_date()
            end = self.date_entry2.get_date()

            # Check if data.csv exists
            if not os.path.exists('data.csv'):
                print("Error: data.csv not found!")
                return

            # Read the csv file
            df = pd.read_csv('data.csv', header=None)
            
            # Assign column names
            df.columns = ['Name', 'Status', 'Agree', 'Date']

            # Convert the date column to datetime
            df['Date'] = pd.to_datetime(df['Date'])
            begin_dt = pd.to_datetime(begin)
            end_dt = pd.to_datetime(end)

            # Filter data
            df_filtered = df[(df['Date'] >= begin_dt) & (df['Date'] <= end_dt)]

            # Save the data
            df_filtered.to_csv('new.csv', header=True, index=False)

            # Create Top Level Window
            self.popup = tkinter.Toplevel()
            self.popup.title("Success!")
            self.popup.geometry("350x150")
            self.popup.columnconfigure(0, weight=1)
            self.popup.rowconfigure(0, weight=1)

            # Label Ask
            self.string_ask = tkinter.StringVar(value="Would you like to open the file?")
            self.label_ask = ctk.CTkLabel(master=self.popup, textvariable=self.string_ask, 
                                          width=20, height=5)
            self.label_ask.grid(row=0, rowspan=2, column=0, padx=5, pady=5)

            # Button Yes and No
            self.button_yes = ctk.CTkButton(self.popup, text="Yes", width=20, height=5, 
                                            command=self.answer_yes)
            self.button_yes.grid(row=2, column=0, padx=20, pady=10)
            
            self.button_no = ctk.CTkButton(self.popup, text="No", width=20, height=5,
                                           command=self.popup.destroy)
            self.button_no.grid(row=3, column=0, padx=20, pady=10)

        except Exception as e:
            print(f"Error saving data: {e}")

    def answer_yes(self):
        """Open the new CSV file"""
        try:
            if os.path.exists('new.csv'):
                if os.name == 'nt':  # Windows
                    os.startfile('new.csv')
                elif os.name == 'posix':  # macOS and Linux
                    if os.uname().sysname == 'Darwin':  # macOS
                        os.system('open new.csv')
                    else:  # Linux
                        os.system('xdg-open new.csv')
            self.popup.destroy()
        except Exception as e:
            print(f"Error opening file: {e}")
            self.popup.destroy()


class user_page(ctk.CTkFrame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)

        # Horizontal Frames
        self.frame_top = ctk.CTkFrame(self)
        self.frame_middle = ctk.CTkFrame(self)
        self.frame_bottom = ctk.CTkFrame(self)
        
        # Grid Frames
        self.frame_top.grid(row=0, column=0, sticky="nsew")
        self.frame_middle.grid(row=1, column=0, sticky="nsew")
        self.frame_bottom.grid(row=2, column=0, sticky="nsew")
        
        # Configure grid weights
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=3)
        self.rowconfigure(2, weight=1)
        
        # Column config
        self.frame_top.columnconfigure(0, weight=1)
        self.frame_middle.columnconfigure(0, weight=1)
        self.frame_middle.columnconfigure(1, weight=1)
        self.frame_middle.columnconfigure(2, weight=1)
        self.frame_bottom.columnconfigure(0, weight=1)
        self.frame_bottom.columnconfigure(1, weight=1)
        
        # Row Config
        self.frame_top.rowconfigure(0, weight=1)
        self.frame_middle.rowconfigure(0, weight=1)
        self.frame_middle.rowconfigure(1, weight=1)
        self.frame_middle.rowconfigure(2, weight=1)
        self.frame_middle.rowconfigure(3, weight=1)
        self.frame_middle.rowconfigure(4, weight=1)
        self.frame_middle.rowconfigure(5, weight=1)
        self.frame_bottom.rowconfigure(0, weight=1)

        # Text
        self.string_wlcm = tkinter.StringVar(value="Welcome Student!")
        self.label_wlcm = ctk.CTkLabel(master=self.frame_top, textvariable=self.string_wlcm, 
                                       width=120, height=25)
        self.label_wlcm.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Entry Field
        self.entry = ctk.CTkEntry(master=self.frame_middle,
                                  placeholder_text="Name",
                                  width=120,
                                  height=25,
                                  border_width=2,
                                  corner_radius=10)
        self.entry.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Option Box
        self.status_var = ctk.StringVar(value="Present")
        self.combobox = ctk.CTkComboBox(master=self.frame_middle,
                                        values=["Present", "Late", "Absent"],
                                        variable=self.status_var)
        self.combobox.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Label Date Entry
        self.string_select_date = tkinter.StringVar(value="Please Select a Date")
        self.label_select_date = ctk.CTkLabel(master=self.frame_middle, 
                                              textvariable=self.string_select_date, width=20)
        self.label_select_date.grid(row=3, column=0, padx=10, pady=10)

        # Entry Date
        self.date_entry = DateEntry(master=self.frame_middle, width=12)
        self.date_entry.grid(row=3, column=1, padx=10, pady=10)

        # Check Box
        self.checkbox_var = tkinter.StringVar(value="Disagree")
        self.checkbox = ctk.CTkCheckBox(master=self.frame_middle,
                                        text="I certify that the above information is correct.",
                                        variable=self.checkbox_var, 
                                        onvalue="Agree", 
                                        offvalue="Disagree")
        self.checkbox.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        # Submit Button
        self.button_submit = ctk.CTkButton(master=self.frame_bottom, text="Submit", 
                                           command=self.save_data)
        self.button_submit.grid(row=0, column=0, padx=10, pady=10)

        # Quit Button
        self.button_quit = ctk.CTkButton(master=self.frame_bottom, text="Back to Home",
                                         command=lambda: controller.up_frame(welcome_page))
        self.button_quit.grid(row=0, column=1, padx=10, pady=10)

    def save_data(self):
        """Save attendance data to CSV"""
        try:
            name = self.entry.get()
            status = self.status_var.get()
            agree = self.checkbox_var.get()
            date = self.date_entry.get_date()

            if not name:
                print("Error: Please enter a name!")
                return

            if agree != "Agree":
                print("Error: Please certify the information!")
                return

            var = (name, status, agree, date)
            dataframe = pd.DataFrame([var], columns=['Name', 'Status', 'Agree', 'Date'])
            
            # Create file with header if it doesn't exist
            if not os.path.exists('data.csv'):
                dataframe.to_csv('data.csv', header=False, index=False, mode='w')
            else:
                dataframe.to_csv('data.csv', header=False, index=False, mode='a')
            
            print("SUBMITTED SUCCESSFULLY!")
            print(dataframe)
            
            # Clear the entry field
            self.entry.delete(0, 'end')
            self.checkbox_var.set("Disagree")
            
        except Exception as e:
            print(f"Error saving data: {e}")


class welcome_page(ctk.CTkFrame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.controller = controller

        self.frame = ctk.CTkFrame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)
        self.frame.rowconfigure(3, weight=1)
        self.frame.rowconfigure(4, weight=1)

        # Text Welcome
        self.string_wlcm = tkinter.StringVar(value="Welcome to the Attendance Management System")
        self.label_wlcm = ctk.CTkLabel(master=self.frame, textvariable=self.string_wlcm)
        self.label_wlcm.grid(row=0, column=0, padx=10, pady=20)

        # Button User
        self.button_user = ctk.CTkButton(master=self.frame, text="User",
                                         command=lambda: controller.up_frame(user_page))
        self.button_user.grid(row=2, column=0, padx=10, pady=10)

        # Button Admin
        self.button_admin = ctk.CTkButton(master=self.frame, text="Admin",
                                          command=lambda: controller.up_frame(admin_page))
        self.button_admin.grid(row=3, column=0, padx=10, pady=10)

        # Quit Button
        self.button_quit = ctk.CTkButton(master=self.frame, text="Quit", 
                                         command=lambda: controller.quit())
        self.button_quit.grid(row=4, column=0, padx=10, pady=10)