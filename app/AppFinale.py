import customtkinter as ctk
import os
from PIL import Image
import sqlite3
from datetime import date, datetime, timedelta
import tkinter as tk
import random
import tkinter.ttk as ttk
import datetime as dt

c_user="#6dceff"
c_user_bg="#d8f2ff"


giorni= [str(i) for i in range(1, 32)]
mesi= [str(i) for i in range(1, 13)]
anni= [str(i) for i in range(2025, 2100)]
ore= [str(i) for i in range(8, 19)]
minuti=["00","15","30","45"]

today = date.today()


class App():
    def __init__(self):
        super().__init__()

        # connect to SQLite database
        self.conn = sqlite3.connect("MySleep.db")
        self.cursor = self.conn.cursor()

        # set appearance and theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # main window
        self.root = ctk.CTk()
        self.root.title("MySleep")
        self.root.geometry("700x500")

        # caricamento login gui
        self.Login_gui() 
        self.root.mainloop()







    # LOGIN GUI 
    def Login_gui(self):

        self.conn.commit()
        self.content_frame = ctk.CTkFrame(self.root, width=700, height=500, fg_color=c_user_bg)
        self.content_frame.place(x=0,y=0)

        # label and entries
        self.login_label = ctk.CTkLabel(self.content_frame, text="Username and Password", font=("Arial",14),
                                        width=300, height=30)
        self.login_label.place(relx=0.5, y=130, anchor="n")
        self.user_entry = ctk.CTkEntry(self.content_frame, placeholder_text="E-mail", width=200, height=30, font=("Arial",14))
        self.user_entry.place(relx=0.5, y=170, anchor="n")
        self.pass_entry = ctk.CTkEntry(self.content_frame, placeholder_text="Password", width=200, height=30, font=("Arial",14),
                                       show="*")
        self.pass_entry.place(relx=0.5, y=210, anchor="n")

        # buttons 
        self.login_button = ctk.CTkButton(self.content_frame, text="Login", text_color="black", width=150, height=30, font=("Arial",14), fg_color=c_user, hover=True,
                                          command=self.login_callback)
        self.login_button.place(relx=0.5, y=255, anchor="n")
        self.newaccount_button = ctk.CTkButton(self.content_frame, text="Create new account", text_color="black", width=150, height=30, font=("Arial",14), fg_color=c_user, hover=True,
                                          command=self.newaccount_callback)
        self.newaccount_button.place(relx=0.5, y=295, anchor="n")

        self.outcome_label = ctk.CTkLabel(self.content_frame, text="", font=("Arial",14))
        self.outcome_label.place(relx=0.5, y=380, anchor="n")
    
    def login_callback(self):
        email = self.user_entry.get()
        pw = self.pass_entry.get()

        # check on email and password
        if email !="":
            self.cursor.execute("SELECT Password FROM user WHERE Email = ?", (email,))
            check = self.cursor.fetchone()

            if not check:
                self.outcome_label.configure(text="Incorrect Username", text_color="red")
            elif pw == check[0]:
                self.cursor.execute("SELECT UserID,Role FROM user WHERE Email = ?", (email,))
                result = self.cursor.fetchone()
                self.user = result[0]
                self.user_role = result[1]

                if self.user_role == "D":
                    self.c_buttons="#8282ff"
                    self.c_buttons_hoover="#5656ff"
                    self.c_buttons_text="white"
                    self.c_sidebar="#adadff"
                    self.c_main="#d8d8ff"
                    self.c_frame="#adadff"
                    self.c_text="#204080"
                    self.Doctor_gui()  # load doctor gui
                elif self.user_role == "P":
                    # self.c_buttons="#6cd800"
                    # self.c_buttons_hoover="#59b200"
                    # self.c_buttons_text="black"
                    # self.c_sidebar="#b6ff6d"
                    # self.c_main="#d1ffa3"
                    # self.c_frame="#b6ff6d"
                    # self.c_text="#23731A"
                    
                    # Colori chiesti a chat chiedendo un verde chiaro pastello
                    # self.c_buttons="#8FCF9E"   
                    # self.c_buttons_hoover="#7DBD8D"   
                    # self.c_buttons_text="black"
                    # self.c_sidebar="#CBEED0"   
                    # self.c_main="#E3F7E7"   
                    # self.c_frame="#CBEED0"   
                    # self.c_text="#2E6B44"

                    # Colori chiesti a chat partendo dal colore del patient dal class 
                    self.c_buttons="#AEEA67"  
                    self.c_buttons_hoover="#99D255"  
                    self.c_buttons_text="black"
                    self.c_sidebar="#D9FFB5"  
                    self.c_main="#F3FFE4" 
                    self.c_frame="#D1FFA3" 
                    self.c_text="#3D6C11"

                    self.cursor.execute("SELECT DoctorID FROM patient WHERE UserID = ?", (self.user,))
                    self.doctorID = self.cursor.fetchone()
                    self.doctorID = self.doctorID[0] if self.doctorID else "Unknown"
                    self.patientID = self.user

                    self.Patient_gui()


            else:
                self.outcome_label.configure(text="Incorrect Password", text_color="red")
        else:
            self.outcome_label.configure(text="Incorrect Username", text_color="red")

    def newaccount_callback(self):
        self.clear_content_frame()

        newuser_label = ctk.CTkLabel(self.content_frame, text="Are you a doctor or a patient?", font=("Arial", 18), text_color="black", width=600, height=50)
        newuser_label.place(relx=0.5, y=150, anchor="n")

        button_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        button_frame.place(relx=0.5, y=270, anchor="center")
        self.newdoctor_button = ctk.CTkButton(button_frame, text="Doctor", command=self.newdoctor_callback, width=200, fg_color=c_user, hover=True)
        self.newdoctor_button.pack(side="left", padx=10)
        self.newpatient_button = ctk.CTkButton(button_frame, text="Patient", command=self.newpatient_callback, width=200, fg_color=c_user, hover=True)
        self.newpatient_button.pack(side="right", padx=10)
    
    def newdoctor_callback(self):
        self.clear_content_frame()
        newaccount_label =ctk.CTkLabel(self.content_frame, text="Insert Personal data", font=("Arial",18), text_color="black")
        newaccount_label.place(relx=0.5, y=10, anchor="n")

        # entries
        frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        frame.place(relx=0.5, y=50, anchor="n")
        name_label = ctk.CTkLabel(frame, text="Name", font=("Arial",14))
        name_label.grid(row=0, column=0, padx=10, pady=0, sticky="e")
        self.name_entry = ctk.CTkEntry(frame, placeholder_text="Name", width=200, height=20, font=("Arial",14))
        self.name_entry.grid(row=0, column=1, padx=10, pady=0, sticky="w")
        
        surname_label = ctk.CTkLabel(frame, text="Surname", font=("Arial",14))
        surname_label.grid(row=1, column=0, padx=10, pady=0, sticky="e")
        self.surname_entry = ctk.CTkEntry(frame, placeholder_text="Surame", width=200, height=20, font=("Arial",14))
        self.surname_entry.grid(row=1, column=1, padx=10, pady=0, sticky="w")

        birthdate_label = ctk.CTkLabel(frame, text="Date of Birth", font=("Arial",14))
        birthdate_label.grid(row=2, column=0, padx=10, pady=0, sticky="e")
        self.birthdate_entry = ctk.CTkEntry(frame, placeholder_text="dd/mm/yyyy", width=200, height=20, font=("Arial",14))
        self.birthdate_entry.grid(row=2, column=1, padx=10, pady=0, sticky="w")

        birthplace_label = ctk.CTkLabel(frame, text="Place of Birth", font=("Arial",14))
        birthplace_label.grid(row=3, column=0, padx=10, pady=0, sticky="e")
        self.birthplace_entry = ctk.CTkEntry(frame, placeholder_text="Place of Birth", width=200, height=20, font=("Arial",14))
        self.birthplace_entry.grid(row=3, column=1, padx=10, pady=0, sticky="w")

        address_label = ctk.CTkLabel(frame, text="Office Address", font=("Arial",14))
        address_label.grid(row=4, column=0, padx=10, pady=0, sticky="e")
        self.address_entry = ctk.CTkEntry(frame, placeholder_text="via Milano 4, Torino", width=200, height=20, font=("Arial",14))
        self.address_entry.grid(row=4, column=1, padx=10, pady=0, sticky="w")

        opening_label = ctk.CTkLabel(frame, text="Opening hour", font=("Arial",14))
        opening_label.grid(row=5, column=0, padx=10, pady=0, sticky="e")
        self.opening_entry = ctk.CTkEntry(frame, placeholder_text="HH:MM", width=200, height=20, font=("Arial",14))
        self.opening_entry.grid(row=5, column=1, padx=10, pady=0, sticky="w")

        closing_label = ctk.CTkLabel(frame, text="Closing hour", font=("Arial",14))
        closing_label.grid(row=6, column=0, padx=10, pady=0, sticky="e")
        self.closing_entry = ctk.CTkEntry(frame, placeholder_text="HH:MM", width=200, height=20, font=("Arial",14))
        self.closing_entry.grid(row=6, column=1, padx=10, pady=0, sticky="w")

        email_label = ctk.CTkLabel(frame, text="E-mail", font=("Arial",14))
        email_label.grid(row=7, column=0, padx=10, pady=0, sticky="e")
        self.email_entry = ctk.CTkEntry(frame, placeholder_text="E-mail", width=200, height=20, font=("Arial",14))
        self.email_entry.grid(row=7, column=1, padx=10, pady=0, sticky="w")

        phone_label = ctk.CTkLabel(frame, text="Phone Number", font=("Arial",14))
        phone_label.grid(row=8, column=0, padx=10, pady=0, sticky="e")
        self.phone_entry = ctk.CTkEntry(frame, placeholder_text="+39 123456789", width=200, height=20, font=("Arial",14))
        self.phone_entry.grid(row=8, column=1, padx=10, pady=0, sticky="w")

        ssn_label = ctk.CTkLabel(frame, text="Social Security Number", font=("Arial",14))
        ssn_label.grid(row=9, column=0, padx=10, pady=0, sticky="e")
        self.ssn_entry = ctk.CTkEntry(frame, placeholder_text="RSSMRA85T10A562S", width=200, height=20, font=("Arial",14))
        self.ssn_entry.grid(row=9, column=1, padx=10, pady=0, sticky="w")

        pass_label = ctk.CTkLabel(frame, text="Password", font=("Arial",14))
        pass_label.grid(row=10, column=0, padx=10, pady=0, sticky="e")
        self.pass_entry = ctk.CTkEntry(frame, placeholder_text="Password", width=200, height=20, font=("Arial",14), show="*")
        self.pass_entry.grid(row=10, column=1, padx=10, pady=0, sticky="w")

        # buttons
        button_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        button_frame.place(relx=0.5, y=430, anchor="n")
        self.newuser_button = ctk.CTkButton(button_frame, text="Register", command=self.newdoctor_registration_callback, width=300, fg_color=c_user, hover=True)
        self.newuser_button.grid(row=0, column=1, padx=10, pady=0, sticky="w")

        self.back_button = ctk.CTkButton(button_frame, text="Back", command=self.back_callback, width=300, fg_color=c_user, hover=True)
        self.back_button.grid(row=0, column=0, padx=10, pady=0, sticky="e")

        self.error_label = ctk.CTkLabel(self.content_frame, text="", font=("Arial", 14), text_color="black")
        self.error_label.place(relx=0.5, y=460, anchor="n")
    
    def newdoctor_registration_callback(self):
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        birthdate = self.birthdate_entry.get()
        birthplace = self.birthplace_entry.get()
        address = self.address_entry.get()
        opening = self.opening_entry.get()
        closing = self.closing_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        ssn = self.ssn_entry.get()
        password = self.pass_entry.get()

        if name!="" and surname!="" and birthdate!="" and birthplace!="" and address!="" and opening!="" and closing!="" and email!="" and phone!="" and ssn!="" and password!="":
            # check birthdate
            try:
                bdate = datetime.strptime(birthdate, "%d/%m/%Y").date()
            except ValueError:
                self.error_label.configure(text="Invalid Date of Birth", text_color="red")
                bdate = ""
            
            # check orari
            error = 0
            try: 
                opens = datetime.strptime(opening, "%H:%M").time()
            except ValueError:
                self.error_label.configure(text="Invalid Opening hour", text_color="red")
                opens = ""
                error = 1

            try: 
                closes = datetime.strptime(closing, "%H:%M").time()
                if error:
                    error = 0
            except ValueError:
                self.error_label.configure(text="Invalid Closing hour", text_color="red")
                closes = ""
                if error:
                    error = 1
                else:
                    error = 0
            if error:
                self.error_label.configure(text="Invalid Opening and Closing hours", text_color="red")

            if bdate!="" and opens!="" and closes!="":
                # inserimento nel DB
                self.cursor.execute(f"""INSERT INTO user (Role, Password, Name, Surname, Email, PhoneNumber, SocialSecurityNumber, Address, BirthPlace, BirthDate)
                                    VALUES ('D', '{password}', '{name}', '{surname}', '{email}', '{phone}', '{ssn}', '{address}', '{birthplace}', '{bdate}');""")
            
                new_user_id = self.cursor.lastrowid
            
                self.cursor.execute(f"""INSERT INTO doctors (openinghour,closinghour,doctorID)
                                    VALUES ('{opens}', '{closes}','{new_user_id}');""")
            
                self.conn.commit()
                self.Login_gui()
                self.outcome_label.configure(text="Registration completed!", text_color="green")

        else:
         self.error_label.configure(text="Please insert all the data", text_color= "red")

    
    def back_callback(self):
        self.Login_gui()
    
    def newpatient_callback(self):
        self.clear_content_frame()
        newaccount_label =ctk.CTkLabel(self.content_frame, text="Insert Personal data", font=("Arial",18), text_color="black")
        newaccount_label.place(relx=0.5, y=10, anchor="n")

        # entries
        frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        frame.place(relx=0.5, y=50, anchor="n")
        name_label = ctk.CTkLabel(frame, text="Name", font=("Arial",14))
        name_label.grid(row=0, column=0, padx=10, pady=0, sticky="e")
        self.name_entry = ctk.CTkEntry(frame, placeholder_text="Name", width=200, height=20, font=("Arial",14))
        self.name_entry.grid(row=0, column=1, padx=10, pady=0, sticky="w")
        
        surname_label = ctk.CTkLabel(frame, text="Surname", font=("Arial",14))
        surname_label.grid(row=1, column=0, padx=10, pady=0, sticky="e")
        self.surname_entry = ctk.CTkEntry(frame, placeholder_text="Surame", width=200, height=20, font=("Arial",14))
        self.surname_entry.grid(row=1, column=1, padx=10, pady=0, sticky="w")

        birthdate_label = ctk.CTkLabel(frame, text="Date of Birth", font=("Arial",14))
        birthdate_label.grid(row=2, column=0, padx=10, pady=0, sticky="e")
        self.birthdate_entry = ctk.CTkEntry(frame, placeholder_text="dd/mm/yyyy", width=200, height=20, font=("Arial",14))
        self.birthdate_entry.grid(row=2, column=1, padx=10, pady=0, sticky="w")

        birthplace_label = ctk.CTkLabel(frame, text="Place of Birth", font=("Arial",14))
        birthplace_label.grid(row=3, column=0, padx=10, pady=0, sticky="e")
        self.birthplace_entry = ctk.CTkEntry(frame, placeholder_text="Place of Birth", width=200, height=20, font=("Arial",14))
        self.birthplace_entry.grid(row=3, column=1, padx=10, pady=0, sticky="w")

        address_label = ctk.CTkLabel(frame, text="Residence Address", font=("Arial",14))
        address_label.grid(row=4, column=0, padx=10, pady=0, sticky="e")
        self.address_entry = ctk.CTkEntry(frame, placeholder_text="via Milano 4, Torino", width=200, height=20, font=("Arial",14))
        self.address_entry.grid(row=4, column=1, padx=10, pady=0, sticky="w")

        height_label = ctk.CTkLabel(frame, text="Height", font=("Arial",14))
        height_label.grid(row=5, column=0, padx=10, pady=0, sticky="e")
        self.height_entry = ctk.CTkEntry(frame, placeholder_text="Height in cm", width=200, height=20, font=("Arial",14))
        self.height_entry.grid(row=5, column=1, padx=10, pady=0, sticky="w")

        weight_label = ctk.CTkLabel(frame, text="Weight", font=("Arial",14))
        weight_label.grid(row=6, column=0, padx=10, pady=0, sticky="e")
        self.weight_entry = ctk.CTkEntry(frame, placeholder_text="Weight in kg", width=200, height=20, font=("Arial",14))
        self.weight_entry.grid(row=6, column=1, padx=10, pady=0, sticky="w")

        email_label = ctk.CTkLabel(frame, text="E-mail", font=("Arial",14))
        email_label.grid(row=7, column=0, padx=10, pady=0, sticky="e")
        self.email_entry = ctk.CTkEntry(frame, placeholder_text="E-mail", width=200, height=20, font=("Arial",14))
        self.email_entry.grid(row=7, column=1, padx=10, pady=0, sticky="w")

        phone_label = ctk.CTkLabel(frame, text="Phone Number", font=("Arial",14))
        phone_label.grid(row=8, column=0, padx=10, pady=0, sticky="e")
        self.phone_entry = ctk.CTkEntry(frame, placeholder_text="+39 123456789", width=200, height=20, font=("Arial",14))
        self.phone_entry.grid(row=8, column=1, padx=10, pady=0, sticky="w")

        ssn_label = ctk.CTkLabel(frame, text="Social Security Number", font=("Arial",14))
        ssn_label.grid(row=9, column=0, padx=10, pady=0, sticky="e")
        self.ssn_entry = ctk.CTkEntry(frame, placeholder_text="RSSMRA85T10A562S", width=200, height=20, font=("Arial",14))
        self.ssn_entry.grid(row=9, column=1, padx=10, pady=0, sticky="w")

        pass_label = ctk.CTkLabel(frame, text="Password", font=("Arial",14))
        pass_label.grid(row=10, column=0, padx=10, pady=0, sticky="e")
        self.pass_entry = ctk.CTkEntry(frame, placeholder_text="Password", width=200, height=20, font=("Arial",14), show="*")
        self.pass_entry.grid(row=10, column=1, padx=10, pady=0, sticky="w")

        # selezione dottore
        doctor_label = ctk.CTkLabel(frame, text="Select your Doctor", font=("Arial",14))
        doctor_label.grid(row=11, column=0, padx=10, pady=0, sticky="e")
        self.selected_doctor = ctk.StringVar()
        self.cursor.execute("SELECT UserID, Surname FROM user WHERE Role = ?", "D")
        doctor_rows = self.cursor.fetchall()
        # crea dizionario
        self.doctor_dict = {f"Dr. {surname}": user_id for user_id, surname in doctor_rows}
        # lista per combobox
        doctors = list(self.doctor_dict.keys())
        self.doctor_combobox = ctk.CTkComboBox(frame, values=doctors, variable=self.selected_doctor, font=("Arial",14), width=200, height=20, 
                                               dropdown_fg_color="white", button_color=c_user, hover=True)
        self.doctor_combobox.grid(row=11, column=1, padx=10, pady=0, sticky="w")

        # buttons
        button_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        button_frame.place(relx=0.5, y=430, anchor="n")
        self.newuser_button = ctk.CTkButton(button_frame, text="Register", command=self.newpatient_registration_callback, width=300, fg_color=c_user, hover=True)
        self.newuser_button.grid(row=0, column=1, padx=10, pady=0, sticky="w")

        self.back_button = ctk.CTkButton(button_frame, text="Back", command=self.back_callback, width=300, fg_color=c_user, hover=True)
        self.back_button.grid(row=0, column=0, padx=10, pady=0, sticky="e")

        self.error_label = ctk.CTkLabel(self.content_frame, text="", font=("Arial", 14), text_color="black")
        self.error_label.place(relx=0.5, y=460, anchor="n")

    def newpatient_registration_callback(self):
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        birthdate = self.birthdate_entry.get()
        birthplace = self.birthplace_entry.get()
        address = self.address_entry.get()
        height = self.height_entry.get()
        weight = self.weight_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        ssn = self.ssn_entry.get()
        password = self.pass_entry.get()

        selected_label = self.selected_doctor.get() # Es: "Dr. Bianchi"
        selected_user_id = self.doctor_dict.get(selected_label)

        if name!="" and surname!="" and birthdate!="" and birthplace!="" and address!="" and height!="" and weight!="" and email!="" and phone!="" and ssn!="" and password!="":
            # check birthdate
            try:
                bdate = datetime.strptime(birthdate, "%d/%m/%Y").date()
            except ValueError:
                self.error_label.configure(text="Invalid Date of Birth", text_color="red")
                bdate = ""
            
            if bdate!="":
                # inserimento nel DB
                self.cursor.execute(f"""INSERT INTO user (Role, Password, Name, Surname, Email, PhoneNumber, SocialSecurityNumber, Address, BirthPlace, BirthDate)
                                    VALUES ('P', '{password}', '{name}', '{surname}', '{email}', '{phone}', '{ssn}', '{address}', '{birthplace}', '{bdate}');""")
            
                new_user_id = self.cursor.lastrowid
            
                self.cursor.execute(f"""INSERT INTO patient (height,weight,doctorid,userID)
                                    VALUES ('{height}', '{weight}','{selected_user_id}','{new_user_id}');""")
            
                self.conn.commit()
                self.Login_gui()
                self.outcome_label.configure(text="Registration completed!", text_color="green")

        else:
         self.error_label.configure(text="Please insert all the data", text_color= "red")


    def clear_content_frame(self):
        # Clear all widgets from the main content area
        for widget in self.content_frame.winfo_children():
            widget.destroy()













    # DOCTOR GUI
    def Doctor_gui(self):
        self.conn.commit()
        self.content_frame = ctk.CTkFrame(self.root, fg_color=self.c_main)
        self.content_frame.grid(row=0,column=1, sticky="nsew")

        # set grid layout 1x2
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # load images
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = ctk.CTkImage(Image.open(os.path.join(image_path, "sleep_light.png")), size=(26, 26))
        self.home_image = ctk.CTkImage(Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.user_image = ctk.CTkImage(Image.open(os.path.join(image_path, "user_light.png")), size=(20, 20))
        self.calendar_image = ctk.CTkImage(Image.open(os.path.join(image_path, "calendar_light.png")), size=(20, 20))
        self.patients_image = ctk.CTkImage(Image.open(os.path.join(image_path, "patients_light.png")), size=(20, 20))
        self.logout_image = ctk.CTkImage(Image.open(os.path.join(image_path, "logout_light.png")), size=(20, 20))

        self.oggi = date.today().isoformat()
        
        # create navigation frame
        self.navigation_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color=self.c_sidebar)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="  MySleep", image=self.logo_image,
                                                             compound="left", font=ctk.CTkFont(size=15, weight="bold"), text_color="white")
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color="white", hover_color=self.c_buttons,
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.doc_appointments_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Appointments",
                                                      fg_color="transparent", text_color="white", hover_color=self.c_buttons,
                                                      image=self.calendar_image, anchor="w", command=self.doc_appointments_button_event)
        self.doc_appointments_button.grid(row=2, column=0, sticky="ew")

        self.patients_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Patients",
                                                      fg_color="transparent", text_color="white", hover_color=self.c_buttons,
                                                      image=self.patients_image, anchor="w", command=self.patients_button_event)
        self.patients_button.grid(row=3, column=0, sticky="ew")

        self.profile_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="My Profile",
                                                      fg_color="transparent", text_color="white", hover_color=self.c_buttons,
                                                      image=self.user_image, anchor="w", command=self.profile_button_event)
        self.profile_button.grid(row=5, column=0, sticky="ew")

        self.logout_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Logout",
                                                      fg_color="transparent", text_color="white", hover_color=self.c_buttons,
                                                      image=self.logout_image, anchor="w", command=self.logout_button_event)
        self.logout_button.grid(row=6, column=0, sticky="ew")


        # create home frame
        self.home_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color=self.c_main)
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.cursor.execute("SELECT Surname FROM user WHERE UserID = ?", (self.user,))
        doctor_surname = self.cursor.fetchone()
        doctor_surname = doctor_surname[0] if doctor_surname else "Unknown" 
        
        self.cursor.execute("SELECT Name FROM user WHERE UserID = ?", (self.user,))
        doctor_name = self.cursor.fetchone()
        doctor_name = doctor_name[0] if doctor_name else "Unknown"   

        welcome_label = ctk.CTkLabel(self.home_frame, text=f"Welcome back Dr. {doctor_name} {doctor_surname}!", font=("Arial",20), text_color=self.c_text) 
        welcome_label.place(relx=0.5,rely=0.5, anchor="center")

        # create MyData frame
        self.data_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color=self.c_main)
    
        # create appointments frame
        self.doc_appointments_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color=self.c_main)

        # create patients frame
        self.patients_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color=self.c_main)

        # create myprofile frame
        self.profile_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color=self.c_main)

        # create logout frame
        self.logout_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color=self.c_main)

        # select default frame
        self.select_frame_by_name("home")
        

    def home_button_event(self):
        self.select_frame_by_name("home")
        if self.user_role == 'P':
             self.show_home()
       

    def doc_appointments_button_event(self):
        self.select_frame_by_name("doc_appointments")
        self.show_appointments_per_date()

    def patients_button_event(self):
        self.select_frame_by_name("patients")
        self.show_patients()
    
    def profile_button_event(self):
        self.select_frame_by_name("profile")
        self.personal_data()
    
    def logout_button_event(self):
        self.select_frame_by_name("logout")
        self.logout()

    # Patients' window
    def show_patients(self):
        for widget in self.patients_frame.winfo_children():
            widget.destroy()

        selection_frame = ctk.CTkFrame(self.patients_frame, width=520, height=295, fg_color=self.c_frame)
        selection_frame.place(x=20, y=20)

        select_label = ctk.CTkLabel(selection_frame, text="Select patient and data:", font=("Arial", 14), text_color=self.c_text)
        select_label.place(x=20, y=10)

        # Recupera nome completo, telefono e email dei pazienti 
        self.cursor.execute("""SELECT u.Surname || ' ' || u.Name AS FullName, u.PhoneNumber, u.Email, u.UserID
        FROM user u JOIN patient p ON u.UserID = p.UserID WHERE p.DoctorID = ? ORDER BY u.Surname, u.Name 
        """, (self.user,))
        records = self.cursor.fetchall()

        # Crea dizionario: "Cognome Nome" -> (telefono, email)
        self.patient_info_dict = {full_name: (phone, email, self.patientID) for full_name, phone, email, self.patientID in records}
        patients_list = list(self.patient_info_dict.keys())


        # Recupera altri dati del paziente
        self.cursor.execute("""SELECT u.Surname || ' ' || u.Name AS FullName, u.SocialSecurityNumber, 
                            u.Address, u.BirthPlace, u.BirthDate, u.UserID
        FROM user u JOIN patient p ON u.UserID = p.UserID WHERE p.DoctorID = ? ORDER BY u.Surname, u.Name 
        """, (self.user,))
        data = self.cursor.fetchall()

        # Crea dizionario: "Cognome Nome" -> (info)
        self.patient_data_dict = {full_name: (ssn, address, birthplace, birthdate) for full_name, ssn, address, birthplace, birthdate, _ in data}

        # ComboBox per selezione paziente
        self.selected_patient = ctk.StringVar()
        self.patients_combobox = ctk.CTkComboBox(
            selection_frame,
            values=patients_list,
            variable=self.selected_patient,
            width=250,
            dropdown_fg_color="white",
            button_color=self.c_buttons,
            button_hover_color=self.c_buttons_hoover,
            command=self.display_patient_contact  # Funzione chiamata quando si seleziona
        )
        self.patients_combobox.place(x=250, y=50)

        patient_label = ctk.CTkLabel(selection_frame, text="Select patient:", font=("Arial", 12))
        patient_label.place(x=20, y=50)

        # Etichette da aggiornare
        self.info_label = ctk.CTkLabel(selection_frame, text="", font=("Arial", 14), text_color=self.c_text, fg_color="transparent")
        self.info_label.place(x=20, y=130)
        self.birthdate_label = ctk.CTkLabel(selection_frame, text="", font=("Arial", 12), fg_color="transparent")
        self.birthdate_label.place(x=20, y=160)
        self.birthplace_label = ctk.CTkLabel(selection_frame, text="", font=("Arial", 12), fg_color="transparent")
        self.birthplace_label.place(x=20, y=180)
        self.ssn_label = ctk.CTkLabel(selection_frame, text="", font=("Arial", 12), fg_color="transparent")
        self.ssn_label.place(x=20, y=200)
        self.address_label = ctk.CTkLabel(selection_frame, text="", font=("Arial", 12), fg_color="transparent")
        self.address_label.place(x=20, y=220)
        self.phone_label = ctk.CTkLabel(selection_frame, text="", font=("Arial", 12), fg_color="transparent")
        self.phone_label.place(x=20, y=240)
        self.email_label = ctk.CTkLabel(selection_frame, text="", font=("Arial", 12), fg_color="transparent")
        self.email_label.place(x=20, y=260)

        self.selection_outcome_label= ctk.CTkLabel(selection_frame, text="",text_color="red",width=600, height=30, font=("Arial", 12))
        self.selection_outcome_label.place(x=0, y=320)

        self.viewappointments_button = ctk.CTkButton(self.patients_frame, text="Appointments", command=self.show_appointments, width=520, fg_color=self.c_buttons, hover_color=self.c_buttons_hoover, text_color=self.c_buttons_text)
        self.viewappointments_button.place(relx=0.5, y=330, anchor="n")
        self.viewappointments_button.configure(state="disabled")

        # Button: View Data
        self.viewdata_button = ctk.CTkButton(self.patients_frame, text="View Data", command=self.show_data, width=520, fg_color=self.c_buttons, hover_color=self.c_buttons_hoover, text_color=self.c_buttons_text)
        self.viewdata_button.place(relx=0.5, y=450, anchor="n")
        self.viewdata_button.configure(state="disabled")

        # Button: Questionnaires
        self.viewquest_button = ctk.CTkButton(self.patients_frame, text="Questionnaires", command=self.show_quest, width=520, fg_color=self.c_buttons, hover_color=self.c_buttons_hoover, text_color=self.c_buttons_text)
        self.viewquest_button.place(relx=0.5, y=370, anchor="n")
        self.viewquest_button.configure(state="disabled")

        # Button: Prescriptions
        self.viewprescriptions_button = ctk.CTkButton(self.patients_frame, text="Prescriptions", command=self.show_prescriptions, width=520, fg_color=self.c_buttons, hover_color=self.c_buttons_hoover, text_color=self.c_buttons_text)
        self.viewprescriptions_button.place(relx=0.5, y=410, anchor="n")
        self.viewprescriptions_button.configure(state="disabled")

    # Patient's contact
    def display_patient_contact(self, *args):
        selected = self.selected_patient.get()
        info = self.patient_info_dict.get(selected, ("N/A", "N/A"))
        phone, email, self.patientID = info

        data = self.patient_data_dict.get(selected, ("N/A", "N/A", "N/A", "N/A"))
        ssn, address, birthplace, birthdate = data

        self.info_label.configure(text="Patient's data:")
        self.birthdate_label.configure(text=f"Birth Date: {birthdate}")
        self.birthplace_label.configure(text=f"Birth Place: {birthplace}")
        self.ssn_label.configure(text=f"Social Security Number: {ssn}")
        self.address_label.configure(text=f"Address: {address}")
        self.phone_label.configure(text=f"Phone number: {phone}")
        self.email_label.configure(text=f"E.mail: {email}")

        self.viewdata_button.configure(state="normal")
        self.viewprescriptions_button.configure(state="normal")
        self.viewquest_button.configure(state="normal")
        self.viewappointments_button.configure(state="normal")

    # Data window
    def show_data(self):
        for widget in self.patients_frame.winfo_children():
            widget.destroy() 
         
        self.show_doc_parameters_selection()    
        #da finire post DB

    
    

    # Prescriptions:
    def show_prescriptions(self):
        self.clear_content_frame()
        self.content_frame.tkraise()

        # Estrazione prescriptions
        self.cursor.execute("""SELECT PatientID,DoctorID, Drug,Dosage,Frequency,Warnings,Datetime,StartDate,EndingDate
                            FROM Prescriptions WHERE PatientID = ? ORDER BY EndingDate ASC""", (self.patientID,))
        # Recupera i risultati
        self.prescriptions_found = self.cursor.fetchall()

        today = date.today()

        # Dividi le prescrizioni
        self.prescriptions_active = []
        self.prescriptions_expired = []

        for row in self.prescriptions_found:
            ending_date_str = row[8]  # EndingDate è la colonna 9 (indice 8)
            ending_date = date.fromisoformat(ending_date_str)  # Assumiamo che sia in formato YYYY-MM-DD
            if ending_date >= today:
                self.prescriptions_active.append(row)
            else:
                self.prescriptions_expired.append(row)  

        # Container principale
        container = tk.Frame(self.content_frame, bg=self.c_main)
        container.pack(fill="both", expand=True)

        # Canvas scrollabile
        canvas = tk.Canvas(container, highlightthickness=0, bg=self.c_main)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Frame interno dentro al canvas
        self.scroll_frame = ctk.CTkFrame(canvas, fg_color=self.c_main)
        scroll_window = canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        # Adatta scroll_frame
        def on_canvas_resize(event):
            canvas.itemconfig(scroll_window, width=event.width)

        canvas.bind("<Configure>", on_canvas_resize)

        # Scroll dinamico
        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        self.scroll_frame.bind("<Configure>", on_configure)

        # Scroll con rotella
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Titolo
        title_label = ctk.CTkLabel(self.scroll_frame, text="Active prescriptions", font=("Arial", 18, "bold"),
                                   text_color=self.c_text, fg_color="transparent")
        title_label.pack(padx=20, pady=20, anchor="w")

        # Risultati
        if not self.prescriptions_active:
            no_results_label = ctk.CTkLabel(self.scroll_frame, text="No prescriptions found.", font=("Arial", 14),
                                            fg_color="transparent")
            no_results_label.pack(padx=20, pady=10, anchor="w")
        else:
            for idx, row in enumerate(self.prescriptions_active):
                drug = row[2]
                dosage = row[3]
                frequency = row[4]
                warnings = row[5]
                ending_date = row[8]

                label = ctk.CTkLabel(self.scroll_frame, text=f" {drug} - {dosage}, {frequency} - Expiry date: {ending_date} - Warnings: {warnings}",
                                    font=("Arial", 11), fg_color="transparent",wraplength=500, justify="left")
                label.pack(padx=30, pady=5, anchor="w")

        # Button frame
        b_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        b_frame.pack(pady=20, anchor="center")
        # Button new prescription
        newprescription_button = ctk.CTkButton(b_frame, text="Create new prescription", command=self.new_prescription, fg_color=self.c_buttons, 
                                               hover_color=self.c_buttons_hoover, text_color=self.c_buttons_text, width=500)
        newprescription_button.pack(pady=10)

        # Buttons frame
        button_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        button_frame.pack(pady=10, anchor="center")
        # Bottone "Back"
        back_button = ctk.CTkButton(button_frame, text="Back", command=self.prescription_reset, fg_color=self.c_buttons,
                                    hover_color=self.c_buttons_hoover, text_color=self.c_buttons_text, width=240)
        back_button.pack(side="left", padx=10)
        # Bottone "Prescription history"
        old_prescription_button = ctk.CTkButton(button_frame, text="Prescription history", command=self.expired_prescription,
                                                fg_color=self.c_buttons, hover_color=self.c_buttons_hoover, text_color=self.c_buttons_text,
                                                width=240)
        old_prescription_button.pack(side="left", padx=10)


    def expired_prescription(self): 
        for widget in self.scroll_frame.winfo_children():
           widget.destroy()
    
        title_label = ctk.CTkLabel(self.scroll_frame, text="Expired prescriptions", font=("Arial", 18, "bold"),
                                   text_color=self.c_text, fg_color="transparent")
        title_label.pack(padx=20, pady=20, anchor="w")

        # Risultati
        if not self.prescriptions_expired:
            no_results_label = ctk.CTkLabel(self.scroll_frame, text="No expired prescriptions found.", font=("Arial", 14),
                                            fg_color="transparent")
            no_results_label.pack(padx=20, pady=10, anchor="w")
        else:
            for idx, row in enumerate(self.prescriptions_expired):
                drug = row[2]
                dosage = row[3]
                frequency = row[4]
                warnings = row[5]
                ending_date = row[8]

                label = ctk.CTkLabel(self.scroll_frame, text=f" {drug} - {dosage}, {frequency} - Expired date: {ending_date} - Warnings: {warnings}",
                                    font=("Arial", 11), fg_color="transparent", wraplength=300, justify="left")
                label.pack(padx=30, pady=5, anchor="w")

        # Button back
        back_button = ctk.CTkButton(self.scroll_frame, text="Back", command=self.show_prescriptions, fg_color=self.c_buttons,
                                    hover_color=self.c_buttons_hoover, text_color=self.c_buttons_text, width=240)
        back_button.pack(padx=230, pady=15)


    def new_prescription(self):
        self.clear_content_frame()

        # Titolo
        title_label = ctk.CTkLabel(self.content_frame, text="New prescription", font=("Arial", 18, "bold"),text_color=self.c_text, fg_color="transparent")
        title_label.pack(padx=20, pady=20, anchor="w")

        labels = ["Drug:", "Dosage:", "Frequency:", "Warnings:", "Start Date:", "Ending Date:"]
        entries = {}
        placeholders = ["Drug's Name", "Dosage in mg or ml", "Frequency", "Warnings", "YYYY-MM-DD", "YYYY-MM-DD"]

        for i, (label_text, placeholder_text) in enumerate(zip(labels, placeholders)):
            label = ctk.CTkLabel(self.content_frame, text=label_text, font=("Arial", 14))
            label.place(x=40, y=60 + i*45)
            entry = ctk.CTkEntry(self.content_frame, placeholder_text=placeholder_text, width=300)
            entry.place(x=200, y=60 + i*45 - 3)
            entries[label_text] = entry

        def save_prescription():
            drug = entries["Drug:"].get()
            dosage = entries["Dosage:"].get()
            frequency = entries["Frequency:"].get()
            warnings = entries["Warnings:"].get()
            start_date = entries["Start Date:"].get()
            ending_date = entries["Ending Date:"].get()

            outcome_label = ctk.CTkLabel(self.content_frame, text="", text_color="red", width=600, height=30, font=("Arial",14))
            outcome_label.place(relx=0.5, y=350, anchor="n")

            # Data odierna senza ora e minuti
            datetime_today = date.today().isoformat()

            if drug!="" and dosage!="" and frequency!="" and warnings!="" and start_date!="" and ending_date!="":
                self.cursor.execute("""INSERT INTO prescriptions (PatientID, DoctorID, Drug, Dosage, Frequency, Warnings, Datetime, StartDate, EndingDate)
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", (self.patientID, self.user, drug, dosage, frequency, warnings, datetime_today, start_date, ending_date))
                self.conn.commit()
                self.show_prescriptions() # Torna alla lista prescrizioni o aggiorna 
            else: 
                outcome_label.configure(text="Please complete all fields!")

        # Button frame
        button_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        button_frame.place(relx=0.5, y=450, anchor="n")
        # Bottone "cancel"
        cancel_button = ctk.CTkButton(button_frame, text="Cancel", command=self.show_prescriptions, fg_color=self.c_buttons, hover_color=self.c_buttons_hoover, width=250)
        cancel_button.grid(row=0, column=0, padx=10, pady=0, sticky="e")
        # Bottone "save"
        save_button = ctk.CTkButton(button_frame, text="Save", command=save_prescription, fg_color=self.c_buttons, hover_color=self.c_buttons_hoover, width=250)
        save_button.grid(row=0, column=1, padx=10, pady=0, sticky="w")


    def prescription_reset(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.content_frame.lower()
        self.select_frame_by_name("patients")
        self.show_patients()  
       

    # Questionari
    def show_quest(self):
        
        if self.user_role == "D":
            for widget in self.patients_frame.winfo_children():
                widget.destroy()
            
            self.clear_content_frame()
            self.dynamic_widgets = []

            # Frame per dropdown e checkbox
            self.selection_frame = ctk.CTkFrame(self.patients_frame, width=520, height=140, fg_color=self.c_frame)
            self.selection_frame.place(x=20, y=20)


        elif self.user_role == "P":
            for widget in self.questionnaire_frame.winfo_children():
                widget.destroy()

            # Frame per dropdown e checkbox
            self.selection_frame = ctk.CTkFrame(self.questionnaire_frame, width=520, height=140, fg_color=self.c_frame)
            self.selection_frame.place(x=20, y=20)

            self.patients_frame=self.questionnaire_frame
            self.dynamic_widgets = []
        
            self.patientID = self.user


        label1 = ctk.CTkLabel(self.selection_frame, text="View questionnaires for a selected time range", font=("Arial", 14), text_color=self.c_text)
        label1.place(x=20, y=10)

        self.range_label = ctk.CTkLabel(self.selection_frame, text="Select the time range desired", font=("Arial", 12))
        self.range_label.place(x=20, y=50)

        self.selection_label1 = ctk.CTkLabel(self.selection_frame, text="", font=("Arial", 12))
        self.selection_label1.place(x=20, y=90)

        self.selection_label2 = ctk.CTkLabel(self.selection_frame, text="", font=("Arial", 12))
        self.selection_label2.place(x=170, y=90)

        self.quest_outcome_label = ctk.CTkLabel(self.patients_frame, text="", text_color="red", width=600, height=30,
                                                font=("Arial", 12))
        self.quest_outcome_label.place(relx=0.5, y=180, anchor="n")

        # range combobox
        self.selected_range = ctk.StringVar()
        self.range_combobox = ctk.CTkComboBox(self.selection_frame, values=["Weeks", "Months", "Custom"], variable=self.selected_range,
                                              width=250, command=self.range_selection, dropdown_fg_color="white", button_color=self.c_buttons, 
                                              button_hover_color=self.c_buttons_hoover)
        self.range_combobox.place(x=250, y=50)

        # Results buttons
        self.questmean_button = ctk.CTkButton(self.patients_frame, text="Mean: ", command=self.rangenotselected,
            width=520, fg_color=self.c_buttons, hover_color=self.c_buttons_hoover, text_color=self.c_buttons_text)
        self.questmean_button.place(relx=0.5, y=450, anchor="n")

        self.questmax_button = ctk.CTkButton(self.patients_frame, text="Max: ", command=self.rangenotselected,
            width=520, fg_color=self.c_buttons, hover_color=self.c_buttons_hoover, text_color=self.c_buttons_text)
        self.questmax_button.place(relx=0.5, y=350, anchor="n")

        self.questmin_button = ctk.CTkButton(self.patients_frame, text="Min: ", command=self.rangenotselected,
            width=520, fg_color=self.c_buttons, hover_color=self.c_buttons_hoover, text_color=self.c_buttons_text)
        self.questmin_button.place(relx=0.5, y=400, anchor="n")

    def rangenotselected(self):
     self.quest_outcome_label.configure(text="Select a time range")
     self.quest_outcome_label.after(1000, lambda: self.quest_outcome_label.configure(text=""))        

    def range_selection(self, value):
       
       self.clear_dynamic_widgets()
       self.quest_outcome_label.configure(text="") 
       
       
       if self.selected_range.get() == "Weeks":
          self.selection_label1.configure(text="Last")
          self.selection_label2.configure(text="weeks")

          self.weeks_selected = ctk.StringVar()
          self.weeks_selection_combobox= ctk.CTkComboBox(
            self.selection_frame,
            values=["1","2","3","4"],
            variable=self.weeks_selected,
            width=100,
            command=self.week_range_quest,
            dropdown_fg_color="white",
            button_color=self.c_buttons,
            button_hover_color=self.c_buttons_hoover 
          )
          self.weeks_selection_combobox.place(x=60,y=90)
          self.dynamic_widgets.append(self.weeks_selection_combobox)

       elif self.selected_range.get() == "Months":
          self.selection_label1.configure(text="Last")
          self.selection_label2.configure(text="months")

          self.months_selected = ctk.StringVar()
          self.months_selection_combobox= ctk.CTkComboBox(
            self.selection_frame,
            values=["1","2","3","4","5","6"],
            variable=self.months_selected,
            width=100,
            command=self.months_range_quest,
            dropdown_fg_color="white",
            button_color=self.c_buttons,
            button_hover_color=self.c_buttons_hoover 
          )

          self.months_selection_combobox.place(x=60,y=90)
          self.dynamic_widgets.append(self.months_selection_combobox)

       else:
          self.selection_label1.configure(text="from")
          self.selection_label2.configure(text="to")
           
           #Date1
      
          self.custom1_selection_entry= ctk.CTkEntry(
            self.selection_frame,
            placeholder_text="YYYY/MM/GG",
            width=100
          )
          self.custom1_selection_entry.place(x=50,y=90)


           #Date2
         
          self.custom2_selection_entry= ctk.CTkEntry(
            self.selection_frame,
            placeholder_text="YYYY/MM/GG",
            width=100
          )
          self.custom2_selection_entry.place(x=200,y=90)

          self.custom_button = ctk.CTkButton(self.selection_frame, text="Search", command=self.custom_range_quest, width=100, fg_color=self.c_buttons, 
                                             hover_color=self.c_buttons_hoover, text_color=self.c_buttons_text)
          self.custom_button.place(x=350, y=90)
          self.dynamic_widgets.append(self.custom1_selection_entry)
          self.dynamic_widgets.append(self.custom2_selection_entry)
          self.dynamic_widgets.append(self.custom_button)

    def week_range_quest(self, value):
   

    # Calcola la data di inizio
     starting_date = date.today() - timedelta(days=int(self.weeks_selected.get()) * 7)
     ending_date = date.today()
     

    # Query per estrarre i dati dalla tabella Questionnaire
     self.cursor.execute("""
        SELECT UserID, QuestionnaireDate, SleepScore, SubjectiveQuality, Sleeplatency, SleepDuration, SleepDisturbances,Medications,TroubleAwake, DayNapDuration, Screens30Mins
        FROM Questionnaire
        WHERE UserID = ?
          AND QuestionnaireDate BETWEEN ? AND ?
        ORDER BY SleepScore ASC
     """, (self.patientID, starting_date.isoformat(), ending_date.isoformat()))

    # Recupera i risultati
     self.questresults = self.cursor.fetchall()


     if self.questresults:
        sleep_scores = [row[2] for row in self.questresults]  # SleepScore è alla posizione 2

        media = sum(sleep_scores) / len(sleep_scores)
        minimo = min(sleep_scores)
        massimo = max(sleep_scores)

        
        self.questmean_button.configure(text=f"Mean: {media}",command=self.show_all_scores)
        self.questmax_button.configure(text=f"Max: {massimo}",command=self.show_max_score_details)
        self.questmin_button.configure(text=f"Min: {minimo}",command=self.show_min_score_details)
        
     else:
        self.quest_outcome_label.configure(text="No questionnaires found for this time range") 
        self.questmean_button.configure(text=f"Mean: -")
        self.questmax_button.configure(text=f"Max: -")
        self.questmin_button.configure(text=f"Min: -")  

    def months_range_quest(self, value):
     
     starting_date = date.today() - timedelta(days=int(self.months_selected.get()) * 30)
     ending_date = date.today()
     

    # Query per estrarre i dati dalla tabella Questionnaire
     # Query per estrarre i dati dalla tabella Questionnaire
     self.cursor.execute("""
        SELECT UserID, QuestionnaireDate, SleepScore, SubjectiveQuality, Sleeplatency, SleepDuration, SleepDisturbances,Medications,TroubleAwake, DayNapDuration, Screens30Mins
        FROM Questionnaire
        WHERE UserID = ?
          AND QuestionnaireDate BETWEEN ? AND ?
        ORDER BY SleepScore ASC
     """, (self.patientID, starting_date.isoformat(), ending_date.isoformat()))

    # Recupera i risultati
     self.questresults = self.cursor.fetchall()


     if self.questresults:
        sleep_scores = [row[2] for row in self.questresults]  # SleepScore è alla posizione 2

        media = sum(sleep_scores) / len(sleep_scores)
        minimo = min(sleep_scores)
        massimo = max(sleep_scores)

        
        self.questmean_button.configure(text=f"Mean: {media}",command=self.show_all_scores)
        self.questmax_button.configure(text=f"Max: {massimo}",command=self.show_max_score_details)
        self.questmin_button.configure(text=f"Min: {minimo}",command=self.show_min_score_details)
        
     else:
        self.quest_outcome_label.configure(text="No questionnaires found for this time range")
        self.questmean_button.configure(text=f"Mean: -")
        self.questmax_button.configure(text=f"Max: -")
        self.questmin_button.configure(text=f"Min: -")  


    def custom_range_quest(self):
     
     starting_date=datetime.strptime(self.custom1_selection_entry.get(),"%Y/%m/%d").date()
     ending_date=datetime.strptime(self.custom2_selection_entry.get(),"%Y/%m/%d").date()

    # Query per estrarre i dati dalla tabella Questionnaire
     self.cursor.execute("""
        SELECT UserID, QuestionnaireDate, SleepScore, SubjectiveQuality, Sleeplatency, SleepDuration, SleepDisturbances,Medications,TroubleAwake, DayNapDuration, Screens30Mins
        FROM Questionnaire
        WHERE UserID = ?
          AND QuestionnaireDate BETWEEN ? AND ?
        ORDER BY SleepScore ASC
     """, (self.patientID, starting_date.isoformat(), ending_date.isoformat()))

    # Recupera i risultati
     self.questresults = self.cursor.fetchall()


     if self.questresults:
        sleep_scores = [row[2] for row in self.questresults]  # SleepScore è alla posizione 2


        media = sum(sleep_scores) / len(sleep_scores)
        minimo = min(sleep_scores)
        massimo = max(sleep_scores)

        
        self.questmean_button.configure(text=f"Mean: {media}",command=self.show_all_scores)
        self.questmax_button.configure(text=f"Max: {massimo}",command=self.show_max_score_details)
        self.questmin_button.configure(text=f"Min: {minimo}",command=self.show_min_score_details)
        
     else:
        self.quest_outcome_label.configure(text="No questionnaires found for this time range")
        self.questmean_button.configure(text=f"Mean: -")
        self.questmax_button.configure(text=f"Max: -")
        self.questmin_button.configure(text=f"Min: -")  

    def clear_dynamic_widgets(self):
     for widget in self.dynamic_widgets:
        widget.destroy()
     self.dynamic_widgets.clear() 

    def show_min_score_details(self):
        if self.user_role == "D":
            self.clear_content_frame()
            for widget in self.patients_frame.winfo_children():
                widget.destroy()
        elif self.user_role == "P":
            for widget in self.questionnaire_frame.winfo_children():
                widget.destroy()

        week_min = self.questresults[0]
        questdate = week_min[1]
        sleepscore = week_min[2]

        subjectivequality = week_min[3]
        if (subjectivequality == 0): subjectivequality='Very good'
        if (subjectivequality == 1): subjectivequality='Fairly good'
        if (subjectivequality == 2): subjectivequality='Fairly bad'
        if (subjectivequality == 3): subjectivequality='Very bad'

        sleeplatency = week_min[4]
        if (sleeplatency == 0): sleeplatency='Less than 15 minutes'
        if (sleeplatency == 1): sleeplatency='15-30 minutes'
        if (sleeplatency == 2): sleeplatency='30-60 minutes'
        if (sleeplatency == 3): sleeplatency='More than 60 minutes'

        sleepduration = week_min[5]
        if (sleepduration == 0): sleepduration='More than 7 hours'
        if (sleepduration == 1): sleepduration='6-7 hours'
        if (sleepduration == 2): sleepduration='5-6 Hours'
        if (sleepduration == 3): sleepduration='Less than 5 hours'
        
        sleepdisturbances = week_min[6]
        if (sleepdisturbances == 0): sleepdisturbances='0'
        if (sleepdisturbances == 1): sleepdisturbances='1'
        if (sleepdisturbances == 2): sleepdisturbances='2'
        if (sleepdisturbances == 3): sleepdisturbances='3 or more'

        medications = week_min[7]
        if (medications == 0): medications='No'
        if (medications == 3): medications='Yes'

        troubleawake = week_min[8]
        if (troubleawake == 0): troubleawake='No'
        if (troubleawake == 3): troubleawake='Yes'

        daynapduration = week_min[9]
        if (daynapduration == 0): daynapduration='No'
        if (daynapduration == 1): daynapduration='Less than 15 minutes'
        if (daynapduration == 2): daynapduration='15-30 minutes'
        if (daynapduration == 3): daynapduration='More than 30 minutes'
       
        screens30mins = week_min[10]
        if (screens30mins == 0): screens30mins='No'
        if (screens30mins == 3): screens30mins='Yes'

        size = 14
        if self.user_role == "D":
            profile_label = ctk.CTkLabel(self.patients_frame, text=f"{self.selected_patient.get()} - {questdate} - Sleep Score: {sleepscore}", font=("Arial", 20), text_color=self.c_text)
            profile_label.place(x=20, y=20)
        elif self.user_role == "P":
            profile_label = ctk.CTkLabel(self.patients_frame, text=f"Questionario {questdate} - Sleep Score: {sleepscore}", font=("Arial", 20), text_color=self.c_text)
            profile_label.place(x=20, y=20)

        subjective_quality_label = ctk.CTkLabel(self.patients_frame, text=f"Subjective sleep quality: {subjectivequality}", font=("Arial", size), text_color=self.c_text)
        subjective_quality_label.place(x=20, y=70)

        sleeplatency_label = ctk.CTkLabel(self.patients_frame, text=f"Sleep latency: {sleeplatency}", font=("Arial", size), text_color=self.c_text)
        sleeplatency_label.place(x=20, y=100)

        sleepduration_label = ctk.CTkLabel(self.patients_frame, text=f"Sleep duration: {sleepduration}", font=("Arial", size), text_color=self.c_text)
        sleepduration_label.place(x=20, y=130)

        sleepdisturbances_label = ctk.CTkLabel(self.patients_frame, text=f"Sleep disturbances: {sleepdisturbances}", font=("Arial", size), text_color=self.c_text)
        sleepdisturbances_label.place(x=20, y=160)

        medications_label = ctk.CTkLabel(self.patients_frame, text=f"Medications: {medications}", font=("Arial", size), text_color=self.c_text)
        medications_label.place(x=20, y=190)

        troubleawake_label = ctk.CTkLabel(self.patients_frame, text=f"Trouble staying awake: {troubleawake}", font=("Arial", size), text_color=self.c_text)
        troubleawake_label.place(x=20, y=220)

        daynap_label = ctk.CTkLabel(self.patients_frame, text=f"Day nap duration: {daynapduration} ", font=("Arial", size), text_color=self.c_text)
        daynap_label.place(x=20, y=250)

        screen_label = ctk.CTkLabel(self.patients_frame, text=f"Screens before sleep: {screens30mins}", font=("Arial", size), text_color=self.c_text)
        screen_label.place(x=20, y=280)

        back_button = ctk.CTkButton(self.patients_frame, text="Back", command=self.show_quest, width=500, fg_color=self.c_buttons, 
                                    hover_color=self.c_buttons_hoover, text_color=self.c_buttons_text)
        back_button.place(x=30, y=450)

    def show_max_score_details(self):
        if self.user_role == "D":
            self.clear_content_frame()
            for widget in self.patients_frame.winfo_children():
                widget.destroy()
        elif self.user_role == "P":
            for widget in self.questionnaire_frame.winfo_children():
                widget.destroy()

        week_max = self.questresults[-1]
        questdate = week_max[1]
        sleepscore = week_max[2]

        subjectivequality = week_max[3]
        if (subjectivequality == 0): subjectivequality='Very good'
        if (subjectivequality == 1): subjectivequality='Fairly good'
        if (subjectivequality == 2): subjectivequality='Fairly bad'
        if (subjectivequality == 3): subjectivequality='Very bad'

        sleeplatency = week_max[4]
        if (sleeplatency == 0): sleeplatency='Less than 15 minutes'
        if (sleeplatency == 1): sleeplatency='15-30 minutes'
        if (sleeplatency == 2): sleeplatency='30-60 minutes'
        if (sleeplatency == 3): sleeplatency='More than 60 minutes'

        sleepduration = week_max[5]
        if (sleepduration == 0): sleepduration='More than 7 hours'
        if (sleepduration == 1): sleepduration='6-7 hours'
        if (sleepduration == 2): sleepduration='5-6 Hours'
        if (sleepduration == 3): sleepduration='Less than 5 hours'
        
        sleepdisturbances = week_max[6]
        if (sleepdisturbances == 0): sleepdisturbances='0'
        if (sleepdisturbances == 1): sleepdisturbances='1'
        if (sleepdisturbances == 2): sleepdisturbances='2'
        if (sleepdisturbances == 3): sleepdisturbances='3 or more'

        medications = week_max[7]
        if (medications == 0): medications='No'
        if (medications == 3): medications='Yes'

        troubleawake = week_max[8]
        if (troubleawake == 0): troubleawake='No'
        if (troubleawake == 3): troubleawake='Yes'

        daynapduration = week_max[9]
        if (daynapduration == 0): daynapduration='No'
        if (daynapduration == 1): daynapduration='Less than 15 minutes'
        if (daynapduration == 2): daynapduration='15-30 minutes'
        if (daynapduration == 3): daynapduration='More than 30 minutes'
       
        screens30mins = week_max[10]
        if (screens30mins == 0): screens30mins='No'
        if (screens30mins == 3): screens30mins='Yes'

        size = 14
        if self.user_role == "D":
            profile_label = ctk.CTkLabel(self.patients_frame, text=f"{self.selected_patient.get()} - {questdate} - Sleep Score: {sleepscore}", font=("Arial", 20), text_color=self.c_text)
            profile_label.place(x=20, y=20)
        elif self.user_role == "P":
            profile_label = ctk.CTkLabel(self.patients_frame, text=f"Questionario {questdate} - Sleep Score: {sleepscore}", font=("Arial", 20), text_color=self.c_text)
            profile_label.place(x=20, y=20)

        subjective_quality_label = ctk.CTkLabel(self.patients_frame, text=f"Subjective sleep quality: {subjectivequality}", font=("Arial", size), text_color=self.c_text)
        subjective_quality_label.place(x=20, y=70)

        sleeplatency_label = ctk.CTkLabel(self.patients_frame, text=f"Sleep latency: {sleeplatency}", font=("Arial", size), text_color=self.c_text)
        sleeplatency_label.place(x=20, y=100)

        sleepduration_label = ctk.CTkLabel(self.patients_frame, text=f"Sleep duration: {sleepduration}", font=("Arial", size), text_color=self.c_text)
        sleepduration_label.place(x=20, y=130)

        sleepdisturbances_label = ctk.CTkLabel(self.patients_frame, text=f"Sleep disturbances: {sleepdisturbances}", font=("Arial", size), text_color=self.c_text)
        sleepdisturbances_label.place(x=20, y=160)

        medications_label = ctk.CTkLabel(self.patients_frame, text=f"Medications: {medications}", font=("Arial", size), text_color=self.c_text)
        medications_label.place(x=20, y=190)

        troubleawake_label = ctk.CTkLabel(self.patients_frame, text=f"Trouble staying awake: {troubleawake}", font=("Arial", size), text_color=self.c_text)
        troubleawake_label.place(x=20, y=220)

        daynap_label = ctk.CTkLabel(self.patients_frame, text=f"Day nap duration: {daynapduration} ", font=("Arial", size), text_color=self.c_text)
        daynap_label.place(x=20, y=250)

        screen_label = ctk.CTkLabel(self.patients_frame, text=f"Screens before sleep: {screens30mins}", font=("Arial", size), text_color=self.c_text)
        screen_label.place(x=20, y=280)

        back_button = ctk.CTkButton(self.patients_frame, text="Back", command=self.show_quest, width=500, fg_color=self.c_buttons, 
                                    hover_color=self.c_buttons_hoover, text_color=self.c_buttons_text)
        back_button.place(x=30, y=450)

    def show_all_scores(self):
        if self.user_role == "D":
            self.clear_content_frame()
            for widget in self.patients_frame.winfo_children():
                widget.destroy()
        elif self.user_role == "P":
            for widget in self.questionnaire_frame.winfo_children():
                widget.destroy()
        self.patients_frame.grid(row=0, column=1, sticky="nsew")

        # Container principale 
        container = ctk.CTkFrame(self.patients_frame, bg_color=self.c_main)
        container.grid(row=0, column=0, sticky="nsew")
        self.patients_frame.grid_rowconfigure(0, weight=1)
        self.patients_frame.grid_columnconfigure(0, weight=1)

        # Canvas scrollabile
        self.canvas = tk.Canvas(container, highlightthickness=0, bg=self.c_main)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Frame interno al canvas 
        self.scroll_frame = ctk.CTkFrame(self.canvas, fg_color=self.c_main, width=520, height=500)
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        # Scroll dinamico 
        def on_configure(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.scroll_frame.bind("<Configure>", on_configure)

        # Scroll con rotella
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta /120)), "units")

        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Contenuto dello scroll_frame
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(
            self.scroll_frame,
            text="Sleep Scores per Date",
            font=("Arial", 18, "bold"),
            text_color=self.c_text,
            fg_color="transparent"
        )
        title_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        if not self.questresults:
            no_results_label = ctk.CTkLabel(
                self.scroll_frame,
                text="No questionnaires found.",
                font=("Arial", 14),
                text_color="black",
                fg_color="transparent"
            )
            no_results_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
            return

        for idx, row in enumerate(self.questresults):
            questionnaire_date = row[1]
            sleep_score = row[2]

            label = ctk.CTkLabel(
                self.scroll_frame,
                text=f"{idx + 1}. {questionnaire_date} - Score: {sleep_score}",
                font=("Arial", 13),
                text_color="black",
                fg_color="transparent"
            )
            label.grid(row=idx + 1, column=0, padx=30, pady=5, sticky="w")

        # Pulsante Back
        back_button = ctk.CTkButton(
            self.scroll_frame,
            text="Back",
            command=self.questreset,
            fg_color=self.c_buttons,
            hover_color=self.c_buttons_hoover,
            text_color=self.c_buttons_text,
            width=300
        )
        back_button.grid(row=len(self.questresults) + 1, column=0, padx=100, pady=20, sticky="w")

    def questreset(self):
       self.show_quest() 

    





    def show_appointments_per_date(self):
        
        for widget in self.doc_appointments_frame.winfo_children():
            widget.destroy()

        
        self.selected_patient= ctk.StringVar()
        self.patientID='xeno'
        self.appointment_flag=1



        # Frame for dropdowns and checkbox
        self.selection_frame = ctk.CTkFrame(self.doc_appointments_frame, width=520, height=170, fg_color=self.c_frame)
        self.selection_frame.place(x=20, y=20)


        day_label = ctk.CTkLabel(self.selection_frame, text="Select a day:", font=("Arial",12))
        day_label.place(x=20, y=40)
        self.day_selection_entry= ctk.CTkEntry(
            self.selection_frame,
            placeholder_text="YYYY/MM/GG",
            width=100
          )
        self.day_selection_entry.place(x=250,y=40)

        self.custom_button = ctk.CTkButton(self.selection_frame, text="Search", command=self.day_selection, width=100, fg_color=self.c_buttons, 
                                            hover_color=self.c_buttons_hoover, text_color=self.c_buttons_text)
        self.custom_button.place(x=380, y=40)

    
        

        # Ottieni nome selezionato
        self.selected_appointment = ctk.StringVar()
        self.appointment_combobox = ctk.CTkComboBox(self.selection_frame, values="", variable=self.selected_appointment, 
                                                    command=self.enableupdate_button, width=250,
                                                    dropdown_fg_color="white", button_color=self.c_buttons, button_hover_color=self.c_buttons_hoover)
        self.appointment_combobox.place(x=250, y=90)
        appointment_label = ctk.CTkLabel(self.selection_frame, text="Select appointment:", font=("Arial",12))
        appointment_label.place(x=20, y=90)
        self.appointment_combobox.configure(state="disabled")

        # Frame for additional notes 
        notes_frame = ctk.CTkFrame(self.doc_appointments_frame, width=520, height=130, fg_color=self.c_frame)
        notes_frame.place(x=20, y=210)

        selectdate_label = ctk.CTkLabel(notes_frame, text="Select new date and location:", font=("Arial", 14), text_color=self.c_text)
        selectdate_label.place(x=20, y=10)

        # Select date and hour
        date_label = ctk.CTkLabel(notes_frame, text="New date:", font=("Arial",12))
        date_label.place(x=20, y=50)
        self.newdate_selection_entry = ctk.CTkEntry(notes_frame, placeholder_text="dd/mm/yyyy", width=100)
        self.newdate_selection_entry.place(x=120, y=50)

        hour_label = ctk.CTkLabel(notes_frame, text="New hour:", font=("Arial",12))
        hour_label.place(x=300, y=50)
        self.newhour_selection_entry = ctk.CTkEntry(notes_frame, placeholder_text="HH:MM", width=100)
        self.newhour_selection_entry.place(x=400, y=50)

        # Select location
        location_label = ctk.CTkLabel(notes_frame, text="New Location:", font=("Arial",12))
        location_label.place(x=20, y=90)
        self.location_selection_entry = ctk.CTkEntry(notes_frame, placeholder_text="Address", width=200)
        self.location_selection_entry.place(x=120, y=90)

       

        # Button frame
        button_frame = ctk.CTkFrame(self.doc_appointments_frame, fg_color="transparent")
        button_frame.place(relx=0.5, y=450, anchor="n")
        # Bottone "delete"
        self.delete_button = ctk.CTkButton(button_frame, text="Delete appointment", command=self.deleteappointment_callback, fg_color=self.c_buttons, 
                                           hover_color=self.c_buttons_hoover, text_color=self.c_buttons_text, width=250)
        self.delete_button.grid(row=0, column=0, padx=10, pady=0, sticky="e")
        self.delete_button.configure(state="disabled")
        # Bottone "update"
        self.update_button = ctk.CTkButton(button_frame, text="Update appointment", command=self.updateappointment_callback, fg_color=self.c_buttons, 
                                           hover_color=self.c_buttons_hoover, text_color=self.c_buttons_text, width=250)
        self.update_button.grid(row=0, column=1, padx=10, pady=0, sticky="w")
        self.update_button.configure(state="disabled")

        # Output label for confimation message
        self.outcome_label = ctk.CTkLabel(self.doc_appointments_frame, text="", font=("Arial",14), width=600, height=30)
        self.outcome_label.place(relx=0.5, y=360, anchor="n")







    def day_selection(self):
        self.selected_day=datetime.strptime(self.day_selection_entry.get(),"%Y/%m/%d").date()
        self.update_doc_appointments_combobox()

    # Appointments:
    def show_appointments(self):
        self.select_frame_by_name("doc_appointments")
        for widget in self.doc_appointments_frame.winfo_children():
            widget.destroy()


        if self.user_role == "D":
            patient_name = self.selected_patient.get()
            patient_id = self.patientID
            doctor_id = self.user
            if not patient_id:
                self.outcome_label.configure(text="Patient not selected.", text_color="red")
        elif self.user_role == "P":
            patient_id = self.user
            doctor_id = self.doctorID 

        self.appointment_flag=0
       
       
        
        # Frame for dropdowns and checkbox
        self.selection_frame = ctk.CTkFrame(self.doc_appointments_frame, width=520, height=100, fg_color=self.c_frame)
        self.selection_frame.place(x=20, y=20)

        # select_label = ctk.CTkLabel(self.selection_frame, text="Select patient and create a new appointment or edit an existing one:", font=("Arial", 14), text_color=self.c_text)
        # select_label.place(x=20, y=10)

        # # Recupera nome completo e userid dei pazienti 
        # self.cursor.execute("""SELECT u.UserID, Surname || ' ' || Name AS FullName
        # FROM user u JOIN patient p ON u.UserID = p.UserID WHERE Role = 'P' AND p.DoctorID = ? 
        # ORDER BY Surname, Name 
        # """, (self.user,))
        # results = self.cursor.fetchall()

        # # Crea dizionario per mappare FullName -> UserID
        # self.patient_map = {f"{surname} {name}": user_id for user_id, full_name in results for surname, name in [full_name.split()]}
        # # Combobox 
        # patient_names = list(self.patient_map.keys())
        # self.selected_patient = ctk.StringVar()
        # self.patients_combobox = ctk.CTkComboBox(self.selection_frame, values=patient_names, variable=self.selected_patient,
        #                                         command=self.update_doc_appointments_combobox, width=250, dropdown_fg_color="white",
        #                                         button_color=self.c_buttons, button_hover_color=self.c_buttons_hoover)
        # self.patients_combobox.place(x=250, y=50)
        # patient_label = ctk.CTkLabel(self.selection_frame, text="Select patient:", font=("Arial", 12))
        # patient_label.place(x=20, y=50)


        
        

        # Ottieni nome selezionato
        self.selected_appointment = ctk.StringVar()
        self.appointment_combobox = ctk.CTkComboBox(self.selection_frame, values="", variable=self.selected_appointment, 
                                                    command=self.enableupdate_button, width=250,
                                                    dropdown_fg_color="white", button_color=self.c_buttons, button_hover_color=self.c_buttons_hoover)
        self.update_doc_appointments_combobox()
        self.appointment_combobox.place(x=250, y=40)
        appointment_label = ctk.CTkLabel(self.selection_frame, text="Select appointment:", font=("Arial",12))
        appointment_label.place(x=20, y=40)

        # Frame for additional notes 
        notes_frame = ctk.CTkFrame(self.doc_appointments_frame, width=520, height=130, fg_color=self.c_frame)
        notes_frame.place(x=20, y=210)

        selectdate_label = ctk.CTkLabel(notes_frame, text="Select new date and location:", font=("Arial", 14), text_color=self.c_text)
        selectdate_label.place(x=20, y=10)

        # Select date and hour
        date_label = ctk.CTkLabel(notes_frame, text="New date:", font=("Arial",12))
        date_label.place(x=20, y=50)
        self.newdate_selection_entry = ctk.CTkEntry(notes_frame, placeholder_text="dd/mm/yyyy", width=100)
        self.newdate_selection_entry.place(x=120, y=50)

        hour_label = ctk.CTkLabel(notes_frame, text="New hour:", font=("Arial",12))
        hour_label.place(x=300, y=50)
        self.newhour_selection_entry = ctk.CTkEntry(notes_frame, placeholder_text="HH:MM", width=100)
        self.newhour_selection_entry.place(x=400, y=50)

        # Select location
        location_label = ctk.CTkLabel(notes_frame, text="New Location:", font=("Arial",12))
        location_label.place(x=20, y=90)
        self.location_selection_entry = ctk.CTkEntry(notes_frame, placeholder_text="Address", width=200)
        self.location_selection_entry.place(x=120, y=90)

        # Appointment buttons
        self.newappointment_button = ctk.CTkButton(self.doc_appointments_frame, text="Create new appointment", command=self.newappointment_callback, width=520, fg_color=self.c_buttons, 
                                                   hover_color=self.c_buttons_hoover, text_color=self.c_buttons_text)
        self.newappointment_button.place(relx=0.5, y=400, anchor="n")
       

        # Button frame
        button_frame = ctk.CTkFrame(self.doc_appointments_frame, fg_color="transparent")
        button_frame.place(relx=0.5, y=450, anchor="n")
        # Bottone "delete"
        self.delete_button = ctk.CTkButton(button_frame, text="Delete appointment", command=self.deleteappointment_callback, fg_color=self.c_buttons, 
                                           hover_color=self.c_buttons_hoover, text_color=self.c_buttons_text, width=250)
        self.delete_button.grid(row=0, column=0, padx=10, pady=0, sticky="e")
        self.delete_button.configure(state="disabled")
        # Bottone "update"
        self.update_button = ctk.CTkButton(button_frame, text="Update appointment", command=self.updateappointment_callback, fg_color=self.c_buttons, 
                                           hover_color=self.c_buttons_hoover, text_color=self.c_buttons_text, width=250)
        self.update_button.grid(row=0, column=1, padx=10, pady=0, sticky="w")
        self.update_button.configure(state="disabled")

        # Output label for confimation message
        self.outcome_label = ctk.CTkLabel(self.doc_appointments_frame, text="", font=("Arial",14), width=600, height=30)
        self.outcome_label.place(relx=0.5, y=360, anchor="n")

    

    def update_doc_appointments_combobox(self):
        

        if self.user_role == "D":
            patient_name = self.selected_patient.get()
            patient_id = self.patientID
            doctor_id = self.user        
        elif self.user_role == "P":
            patient_id = self.user
            doctor_id = self.doctorID

        
        if self.appointment_flag==1:

            self.appointment_combobox.configure(values=[])
            self.cursor.execute("""SELECT Datetime,Location FROM appointments WHERE DoctorID = ? AND DATE(DateTime) = ? ORDER BY Datetime""", (doctor_id,self.selected_day))
            appointments = self.cursor.fetchall()
            if not appointments:
                self.outcome_label.configure(text='No appointments for that day', text_color='red')
                self.outcome_label.after(1500, lambda: self.outcome_label.configure(text="")) 



        else:    

            self.appointment_combobox.configure(values=[])
            self.cursor.execute("""SELECT Datetime,Location FROM appointments WHERE PatientID = ? AND DoctorID = ? ORDER BY Datetime""", (patient_id, doctor_id))
            appointments = self.cursor.fetchall()

        # Salva ID -> stringa per dopo 
        # Crea mappa stringa visuae -> tuple (Datetime, Location)
        self.appointment_map = {
            datetime: datetime  # o f"{datetime}" se vuoi stringa
            for datetime, location in appointments
            }
        appointment_display_list = list(self.appointment_map.keys())

        # Se ci sono valori si aggiorna, altrimenti la combobox rimane disabilitata
        if appointment_display_list:
            self.appointment_combobox.configure(state="normal")
            self.appointment_combobox.configure(values=appointment_display_list)


    def update_appointments_combobox(self):
        

        if self.user_role == "D":
            patient_name = self.selected_patient.get()
            patient_id = self.patient_map.get(patient_name)
            doctor_id = self.user
            if not patient_id:
                self.outcome_label.configure(text="Patient not selected.", text_color="red")
        elif self.user_role == "P":
            patient_id = self.user
            doctor_id = self.doctorID

        selected_patient_id =patient_id
        if not selected_patient_id:
            return
        else: 
            self.newappointment_button.configure(state="normal")
            self.outcome_label.configure(text="")
        
        self.cursor.execute("""SELECT Datetime,Location FROM appointments WHERE PatientID = ? AND DoctorID = ? ORDER BY Datetime""", (selected_patient_id, doctor_id))
        appointments = self.cursor.fetchall()

        # Salva ID -> stringa per dopo 
        # Crea mappa stringa visuae -> tuple (Datetime, Location)
        self.appointment_map = {
            datetime: datetime  # o f"{datetime}" se vuoi stringa
            for datetime, location in appointments
            }
        appointment_display_list = list(self.appointment_map.keys())

        # Se ci sono valori si aggiorna, altrimenti la combobox rimane disabilitata
        if appointment_display_list:
            self.appointment_combobox.configure(state="normal")
            self.appointment_combobox.configure(values=appointment_display_list)        

    def enableupdate_button(self, selected_appointment):
        selected_appointment = self.selected_appointment.get()  # formato: "2025-06-03 10:00:00"
        
        if not selected_appointment:
            return

        self.delete_button.configure(state="normal")
        self.update_button.configure(state="normal")
        self.outcome_label.configure(text="")
        if self.appointment_flag!=1:
            self.newappointment_button.configure(state="disabled")

    def newappointment_callback(self):
        if self.user_role == "D":
            patient_name = self.selected_patient.get()
            patient_id = self.patientID
            doctor_id = self.user
            if not patient_id:
                self.outcome_label.configure(text="Patient not selected.", text_color="red")
        elif self.user_role == "P":
            patient_id = self.user
            doctor_id = self.doctorID
            
        # get location
        location = self.location_selection_entry.get()
        if not location:
            self.outcome_label.configure(text="Insert location", text_color="red")

        # Check data e ora 
        error = 0
        try:
            date_str = datetime.strptime(self.newdate_selection_entry.get(), "%d/%m/%Y").date()
        except ValueError:
            self.outcome_label.configure(text="Invalid date", text_color="red")
            date_str = ""
            error = 1

        try:
            time_str = datetime.strptime(self.newhour_selection_entry.get(), "%H:%M").time()
            if error:
                error = 0
        except ValueError:
            self.outcome_label.configure(text="Invalid hour", text_color="red")
            time_str = ""
            if error:
                error = 1
            else:
                error = 0
        if error: 
            self.outcome_label.configure(text="Invalid date and hour", text_color="red")
            
        if date_str!="" and time_str!="" and location!="":
            datetime_str = f"{date_str} {time_str}"
            
            # Verifica che non esista già 
            self.cursor.execute("""SELECT * FROM appointments WHERE DoctorID = ? AND Datetime = ?""", (doctor_id, datetime_str))
            if self.cursor.fetchone():
                self.outcome_label.configure(text="Appointment already exists.", text_color="red")
                return
            
            # Inserisci appuntamento
            self.cursor.execute("""INSERT INTO appointments (PatientID, DoctorID, Datetime, Location) VALUES (?, ?, ?, ?)""", (patient_id, doctor_id, datetime_str, location))

            self.conn.commit()
            if self.user_role == "D":
                self.outcome_label.configure(text=f"New appointment created for {patient_name} on {self.newdate_selection_entry.get()} at {self.newhour_selection_entry.get()}", text_color="green")
                self.selected_patient.set("")
            elif self.user_role == "P":
                self.cursor.execute("""SELECT Surname || ' ' || Name AS FullName
                                    FROM user WHERE UserID = ?""", (doctor_id,))
                result = self.cursor.fetchone()
                doctor_name = result[0] if result else "Unknown"
                self.outcome_label.configure(text=f"New appointment created with Dr. {doctor_name} on {self.newdate_selection_entry.get()} at {self.newhour_selection_entry.get()}", text_color="green")

            # Clear
            self.selected_appointment.set("")
            self.newhour_selection_entry.delete(0, "end")
            self.newdate_selection_entry.delete(0, "end")
            self.location_selection_entry.delete(0, "end")
            self.refresh_appointments_combobox()

    def deleteappointment_callback(self):
        selected_appointment = self.selected_appointment.get()  # formato: "2025-06-03 10:00:00"
        if self.user_role == "D":
            patient_name = self.selected_patient.get()
            patient_id = self.patientID
            doctor_id = self.user
            if not patient_id or selected_appointment == "-- :":
                self.outcome_label.configure(text="Patient of appointment not selected.", text_color="red")
                return
        elif self.user_role == "P":
            patient_id = self.user
            doctor_id = self.doctorID
            if selected_appointment == "-- :":
                self.outcome_label.configure(text="Appointment not selected.", text_color="red")
                return
        
        # Cancella appuntamento 
        if self.appointment_flag==1:
            self.cursor.execute("""DELETE FROM appointments WHERE DoctorID = ? AND Datetime = ?""", ( doctor_id, selected_appointment))
        else:    
            self.cursor.execute("""DELETE FROM appointments WHERE PatientID = ? AND DoctorID = ? AND Datetime = ?""", (patient_id, doctor_id, selected_appointment))
        self.conn.commit()

        self.refresh_appointments_combobox()
        

        self.outcome_label.configure(text=f"Appointment on {selected_appointment} deleted.", text_color="green")

        # Clear campi
        if self.user_role == "D":
            self.selected_patient.set("")
        self.selected_appointment.set("")
        self.newhour_selection_entry.delete(0, "end")
        self.newdate_selection_entry.delete(0, "end")
        self.location_selection_entry.delete(0, "end")

    def updateappointment_callback(self):
        old_appointment = self.selected_appointment.get()

        if self.user_role == "D":
            patient_name = self.selected_patient.get()
            patient_id = self.patientID
            doctor_id = self.user
            if not patient_id or old_appointment == "-- :":
                self.outcome_label.configure(text="Patient of appointment not selected.", text_color="red")
                return
        elif self.user_role == "P":
            patient_id = self.user
            doctor_id = self.doctorID
            if old_appointment == "-- :":
                self.outcome_label.configure(text="Appointment not selected.", text_color="red")
                return
    
        # Check data e ora (come sopra)
        error = 0
        try:
            date_str = datetime.strptime(self.newdate_selection_entry.get(), "%d/%m/%Y").date()
        except ValueError:
            self.outcome_label.configure(text="Invalid date", text_color="red")
            date_str = ""
            error = 1

        try:
            time_str = datetime.strptime(self.newhour_selection_entry.get(), "%H:%M").time()
            if error:
                error = 0
        except ValueError:
            self.outcome_label.configure(text="Invalid hour", text_color="red")
            time_str = ""
            if error:
                error = 1
            else:
                error = 0
        if error: 
            self.outcome_label.configure(text="Invalid date and hour", text_color="red")

        if date_str!="" and time_str!="":
            new_datetime = f"{date_str} {time_str}"

            # Esegui update
            if self.appointment_flag==1:
                self.cursor.execute("""UPDATE appointments SET Datetime = ? WHERE DoctorID = ? AND Datetime = ?""", (new_datetime, doctor_id, old_appointment))

            else:    
                self.cursor.execute("""UPDATE appointments SET Datetime = ? WHERE PatientID = ? AND DoctorID = ? AND Datetime = ?""", (new_datetime, patient_id, doctor_id, old_appointment))
            self.conn.commit()
            self.refresh_appointments_combobox()

            self.outcome_label.configure(text=f"Appointment updated to {new_datetime}", text_color="green")

            # Clear campi
            if self.user_role == "D":
                self.selected_patient.set("")
            self.selected_appointment.set("")
            self.newhour_selection_entry.delete(0, "end")
            self.newdate_selection_entry.delete(0, "end")
            self.location_selection_entry.delete(0, "end")

    def refresh_appointments_combobox(self):
        if self.user_role == 'P':
            self.update_appointments_combobox()
        self.appointment_combobox.configure(values=[])
        if self.user_role == "D":
            if self.appointment_flag!=1:
                self.newappointment_button.configure(state="disabled")
            self.update_doc_appointments_combobox()
        elif self.user_role == "P":
            self.newappointment_button.configure(state="normal")
            appointment_display_list = list(self.appointment_map.keys())
            if appointment_display_list:
                self.appointment_combobox.configure(state="normal")
                self.appointment_combobox.configure(values=appointment_display_list)

        self.outcome_label.configure(text="")
        self.delete_button.configure(state="disabled")
        self.update_button.configure(state="disabled")

    
        
      
        






        

    # PATIENT GUI

    def Patient_gui(self):
        self.conn.commit()
        self.patient_frame = ctk.CTkFrame(self.root, width=700, height=500, fg_color=self.c_main)
        self.patient_frame.place(x=0,y=0)
        # set grid layout 1x2
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        # IMMAGINI SONO DA SISTEMARE/ALCUNE DA TOGLIERE/AGGIUNGERE: 
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = ctk.CTkImage(Image.open(os.path.join(image_path, "sleep_dark.png")), size=(26, 26))
        self.home_image = ctk.CTkImage(Image.open(os.path.join(image_path, "home_dark.png")), size=(20, 20))
        self.chat_image = ctk.CTkImage(Image.open(os.path.join(image_path, "chat_dark.png")), size=(20, 20))
        self.user_image = ctk.CTkImage(Image.open(os.path.join(image_path, "user_dark.png")), size=(20, 20))
        self.quest_image = ctk.CTkImage(Image.open(os.path.join(image_path, "quest_dark.png")), size=(20, 20))
        self.calendar_image = ctk.CTkImage(Image.open(os.path.join(image_path, "calendar_dark.png")), size=(20, 20))
        self.doctor_image = ctk.CTkImage(Image.open(os.path.join(image_path, "doctor_dark.png")), size=(20, 20))
        self.data_image = ctk.CTkImage(Image.open(os.path.join(image_path, "data_dark.png")), size=(20, 20))
        self.tips_image = ctk.CTkImage(Image.open(os.path.join(image_path, "lightbulb.png")), size=(20, 20))
        self.logout_image = ctk.CTkImage(Image.open(os.path.join(image_path, "logout_dark.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color=self.c_sidebar)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(7, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="  MySleep", image=self.logo_image,
                                                             compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color="black", hover_color=self.c_buttons,
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.data_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="My Data",
                                                    fg_color="transparent", text_color="black", hover_color=self.c_buttons,
                                                    image=self.data_image, anchor="w", command=self.data_button_event)
        self.data_button.grid(row=2, column=0, sticky="ew")

        self.notes_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Doctor's Notes",
                                                      fg_color="transparent", text_color="black", hover_color=self.c_buttons,
                                                      image=self.chat_image, anchor="w", command=self.notes_button_event)
        self.notes_button.grid(row=3, column=0, sticky="ew")

        self.questionnaire_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Questionnaires",
                                                      fg_color="transparent", text_color="black", hover_color=self.c_buttons,
                                                      image=self.quest_image, anchor="w", command=self.questionnaire_button_event)
        self.questionnaire_button.grid(row=4, column=0, sticky="ew")
    
        self.doctor_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="My Doctor",
                                                      fg_color="transparent", text_color="black", hover_color=self.c_buttons,
                                                      image=self.doctor_image, anchor="w", command=self.doctor_button_event)
        self.doctor_button.grid(row=5, column=0, sticky="ew")

        self.appointment_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Appointments",
                                                      fg_color="transparent", text_color="black", hover_color=self.c_buttons,
                                                      image=self.calendar_image, anchor="w", command=self.appointment_button_event)
        self.appointment_button.grid(row=6, column=0, sticky="ew")

        self.profile_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="My Profile",
                                                      fg_color="transparent", text_color="black", hover_color=self.c_buttons,
                                                      image=self.user_image, anchor="w", command=self.profile_button_event)
        self.profile_button.grid(row=8, column=0, sticky="ew")

        self.logout_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Logout",
                                                      fg_color="transparent", text_color="black", hover_color=self.c_buttons,
                                                      image=self.logout_image, anchor="w", command=self.logout_button_event)
        self.logout_button.grid(row=9, column=0, sticky="ew")

        # create home frame
        self.home_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color=self.c_main)
        self.home_frame.grid_columnconfigure(0, weight=1)


    

        # create MyData frame
        self.data_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color=self.c_main)

        # create Doctor's Notes frame
        self.notes_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color=self.c_main)

        # create third frame = QUESTIONARIO
        self.questionnaire_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color=self.c_main)

        # Controllo se il questionario è già stato fatto
        self.oggi = date.today().isoformat()
        self.cursor.execute("SELECT SleepScore FROM Questionnaire WHERE UserID = ? AND DATE(QuestionnaireDate) = ?", (self.user, self.oggi))
        if self.cursor.fetchone():
            self.show_quest()
        else:    
            questionnaire_frame = ctk.CTkScrollableFrame(self.questionnaire_frame, width=470, height=450, fg_color=self.c_frame)
            questionnaire_frame.place(x=20, y=20)

            questionnaire_frame.grid_columnconfigure(0, minsize=280)
            questionnaire_frame.grid_columnconfigure(1, minsize=200)
            
            ## Domanda 1
            question1_label = ctk.CTkLabel(questionnaire_frame, text="1. Subjective sleep quality", font=("Arial", 12), anchor="w", justify="left")
            question1_label.grid(row=0, column=0, sticky="w", padx=20, pady=10)

            self.radio_var1 = ctk.StringVar(value="")
            radio_frame1 = ctk.CTkFrame(questionnaire_frame, fg_color="transparent")
            ctk.CTkRadioButton(radio_frame1, text="Very good", variable=self.radio_var1, value="0",
                               fg_color=self.c_buttons_hoover, hover_color=self.c_text).pack(anchor="w", pady=2)
            ctk.CTkRadioButton(radio_frame1, text="Fairly good", variable=self.radio_var1, value="1",
                               fg_color=self.c_buttons_hoover, hover_color=self.c_text).pack(anchor="w", pady=2)
            ctk.CTkRadioButton(radio_frame1, text="Fairly bad", variable=self.radio_var1, value="2",
                               fg_color=self.c_buttons_hoover, hover_color=self.c_text).pack(anchor="w", pady=2)
            ctk.CTkRadioButton(radio_frame1, text="Very bad", variable=self.radio_var1, value="3",
                               fg_color=self.c_buttons_hoover, hover_color=self.c_text).pack(anchor="w", pady=2)
            radio_frame1.grid(row=0, column=1, sticky="nw", padx=10, pady=10)

            ## Domanda 2
            question2_label = ctk.CTkLabel(questionnaire_frame, text="2. How long did it take you to fall asleep?", font=("Arial", 12), anchor="w", justify="left")
            question2_label.grid(row=1, column=0, sticky="w", padx=20, pady=10)

            self.radio_var2 = ctk.StringVar(value="")
            radio_frame2 = ctk.CTkFrame(questionnaire_frame, fg_color="transparent")
            ctk.CTkRadioButton(radio_frame2, text="≤ 15 minutes", variable=self.radio_var2, value="0",
                               fg_color=self.c_buttons_hoover, hover_color=self.c_text).pack(anchor="w", pady=2)
            ctk.CTkRadioButton(radio_frame2, text="16–30 minutes", variable=self.radio_var2, value="1",
                               fg_color=self.c_buttons_hoover, hover_color=self.c_text).pack(anchor="w", pady=2)
            ctk.CTkRadioButton(radio_frame2, text="31–60 minutes", variable=self.radio_var2, value="2",
                               fg_color=self.c_buttons_hoover, hover_color=self.c_text).pack(anchor="w", pady=2)
            ctk.CTkRadioButton(radio_frame2, text="> 60 minutes", variable=self.radio_var2, value="3",
                               fg_color=self.c_buttons_hoover, hover_color=self.c_text).pack(anchor="w", pady=2)
            radio_frame2.grid(row=1, column=1, sticky="nw", padx=10, pady=10)

            ## Domanda 3
            question3_label = ctk.CTkLabel(questionnaire_frame, text="3. Sleep duration", font=("Arial", 12), anchor="w", justify="left")
            question3_label.grid(row=2, column=0, sticky="w", padx=20, pady=10)

            self.radio_var3 = ctk.StringVar(value="")
            radio_frame3 = ctk.CTkFrame(questionnaire_frame, fg_color="transparent")
            ctk.CTkRadioButton(radio_frame3, text=">7h", variable=self.radio_var3, value="0",
                               fg_color=self.c_buttons_hoover, hover_color=self.c_text).pack(anchor="w", pady=2)
            ctk.CTkRadioButton(radio_frame3, text="6–7h", variable=self.radio_var3, value="1",
                               fg_color=self.c_buttons_hoover, hover_color=self.c_text).pack(anchor="w", pady=2)
            ctk.CTkRadioButton(radio_frame3, text="5–6h", variable=self.radio_var3, value="2",
                               fg_color=self.c_buttons_hoover, hover_color=self.c_text).pack(anchor="w", pady=2)
            ctk.CTkRadioButton(radio_frame3, text="<5h", variable=self.radio_var3, value="3",
                               fg_color=self.c_buttons_hoover, hover_color=self.c_text).pack(anchor="w", pady=2)
            radio_frame3.grid(row=2, column=1, sticky="nw", padx=10, pady=10)

            ## Domanda 4
            question4_label = ctk.CTkLabel(questionnaire_frame, text="4. Sleep disturbances", font=("Arial", 12), anchor="w", justify="left")
            question4_label.grid(row=3, column=0, sticky="w", padx=20, pady=10)

            self.radio_var4 = ctk.StringVar(value="")
            radio_frame4 = ctk.CTkFrame(questionnaire_frame, fg_color="transparent")
            ctk.CTkRadioButton(radio_frame4, text="0", variable=self.radio_var4, value="0",
                               fg_color=self.c_buttons_hoover, hover_color=self.c_text).pack(anchor="w", pady=2)
            ctk.CTkRadioButton(radio_frame4, text="1", variable=self.radio_var4, value="1",
                               fg_color=self.c_buttons_hoover, hover_color=self.c_text).pack(anchor="w", pady=2)
            ctk.CTkRadioButton(radio_frame4, text="2", variable=self.radio_var4, value="2",
                               fg_color=self.c_buttons_hoover, hover_color=self.c_text).pack(anchor="w", pady=2)
            ctk.CTkRadioButton(radio_frame4, text="≥3", variable=self.radio_var4, value="3",
                               fg_color=self.c_buttons_hoover, hover_color=self.c_text).pack(anchor="w", pady=2)
            radio_frame4.grid(row=3, column=1, sticky="nw", padx=10, pady=10)

            ## Domanda 5
            question5_label = ctk.CTkLabel(questionnaire_frame, text="5. Use of sleep medication", font=("Arial", 12), anchor="w", justify="left")
            question5_label.grid(row=4, column=0, sticky="w", padx=20, pady=10)

            self.radio_var5 = ctk.StringVar(value="")
            radio_frame5 = ctk.CTkFrame(questionnaire_frame, fg_color="transparent")
            ctk.CTkRadioButton(radio_frame5, text="No", variable=self.radio_var5, value="0",
                               fg_color=self.c_buttons_hoover, hover_color=self.c_text).pack(anchor="w", pady=2)
            ctk.CTkRadioButton(radio_frame5, text="Yes", variable=self.radio_var5, value="3",
                               fg_color=self.c_buttons_hoover, hover_color=self.c_text).pack(anchor="w", pady=2)
            radio_frame5.grid(row=4, column=1, sticky="nw", padx=10, pady=10)

            ## Domanda 6
            question6_label = ctk.CTkLabel(questionnaire_frame, text="6. Trouble at staying awake during the day", font=("Arial", 12), anchor="w", justify="left")
            question6_label.grid(row=5, column=0, sticky="w", padx=20, pady=10)

            self.radio_var6 = ctk.StringVar(value="")
            radio_frame6 = ctk.CTkFrame(questionnaire_frame, fg_color="transparent")
            ctk.CTkRadioButton(radio_frame6, text="No", variable=self.radio_var6, value="0",
                               fg_color=self.c_buttons_hoover, hover_color=self.c_text).pack(anchor="w", pady=2)
            ctk.CTkRadioButton(radio_frame6, text="Yes", variable=self.radio_var6, value="3",
                               fg_color=self.c_buttons_hoover, hover_color=self.c_text).pack(anchor="w", pady=2)
            radio_frame6.grid(row=5, column=1, sticky="nw", padx=10, pady=10)

            ## Domanda 7
            question7_label = ctk.CTkLabel(questionnaire_frame, text="7. Day nap duration", font=("Arial", 12), anchor="w", justify="left")
            question7_label.grid(row=6, column=0, sticky="w", padx=20, pady=10)

            self.radio_var7 = ctk.StringVar(value="")
            radio_frame7 = ctk.CTkFrame(questionnaire_frame, fg_color="transparent")
            ctk.CTkRadioButton(radio_frame7, text="No", variable=self.radio_var7, value="0",
                               fg_color=self.c_buttons_hoover, hover_color=self.c_text).pack(anchor="w", pady=2)
            ctk.CTkRadioButton(radio_frame7, text="<15 min", variable=self.radio_var7, value="1",
                               fg_color=self.c_buttons_hoover, hover_color=self.c_text).pack(anchor="w", pady=2)
            ctk.CTkRadioButton(radio_frame7, text="15–30 min", variable=self.radio_var7, value="2",
                               fg_color=self.c_buttons_hoover, hover_color=self.c_text).pack(anchor="w", pady=2)
            ctk.CTkRadioButton(radio_frame7, text=">30 min", variable=self.radio_var7, value="3",
                               fg_color=self.c_buttons_hoover, hover_color=self.c_text).pack(anchor="w", pady=2)
            radio_frame7.grid(row=6, column=1, sticky="nw", padx=10, pady=10)

            ## Domanda 8
            question8_label = ctk.CTkLabel(questionnaire_frame, text="8. Screens within 30 min before sleep", font=("Arial", 12), anchor="w", justify="left")
            question8_label.grid(row=7, column=0, sticky="w", padx=20, pady=10)

            self.radio_var8 = ctk.StringVar(value="")
            radio_frame8 = ctk.CTkFrame(questionnaire_frame, fg_color="transparent")
            ctk.CTkRadioButton(radio_frame8, text="No", variable=self.radio_var8, value="0",
                               fg_color=self.c_buttons_hoover, hover_color=self.c_text).pack(anchor="w", pady=2)
            ctk.CTkRadioButton(radio_frame8, text="Yes", variable=self.radio_var8, value="3",
                               fg_color=self.c_buttons_hoover, hover_color=self.c_text).pack(anchor="w", pady=2)
            radio_frame8.grid(row=7, column=1, sticky="nw", padx=10, pady=10)

            ## Risultato e Submit
            self.risultato_label = ctk.CTkLabel(questionnaire_frame, text="", font=("Arial", 14))
            self.risultato_label.grid(row=9, column=0, columnspan=2, pady=10)

            submit_button = ctk.CTkButton(questionnaire_frame, text="Submit", command=self.submit_questionnaire,
                                          fg_color=self.c_buttons, hover_color=self.c_buttons_hoover, text_color=self.c_buttons_text)
            submit_button.grid(row=10, column=0, columnspan=2, pady=20)
        # create My Doctor frame
        self.doctor_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color=self.c_main)

        # create appointments frame
        self.appointment_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color=self.c_main)

        # create MyProfile frame
        self.profile_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color=self.c_main)

        # create logout frame
        self.logout_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color=self.c_main)

        # select default frame
        self.select_frame_by_name("home")
        self.show_home()

    def show_home(self):
                self.cursor.execute("SELECT Surname FROM user WHERE UserID = ?", (self.user,))
                patient_surname = self.cursor.fetchone()
                patient_surname = patient_surname[0] if patient_surname else "Unknown"

                self.cursor.execute("SELECT Name FROM user WHERE UserID = ?", (self.user,))
                patient_name = self.cursor.fetchone()
                patient_name = patient_name[0] if patient_name else "Unknown"

                label1 = ctk.CTkLabel(self.home_frame, text=f"Welcome back {patient_name} {patient_surname}!", font=("Arial", 27), text_color=self.c_text)
                label1.place(x=20, y=20)
                label2 = ctk.CTkLabel(self.home_frame, text="How are you today?", font=("Arial", 14), text_color=self.c_text)
                label2.place(x=20, y=60)
                label3 = ctk.CTkLabel(self.home_frame, text="", font=("Arial", 14))
                label3.place(x=20, y=100)
                self.quest_button = ctk.CTkButton(self.home_frame, text="Go to Daily Questionnaire", command=self.questionnaire_button_event, width=220, fg_color=self.c_buttons, 
                                                hover_color=self.c_buttons_hoover, text_color=self.c_buttons_text) 
                self.quest_button.place(x=300, y=100)
                label4 = ctk.CTkLabel(self.home_frame, text="", font=("Arial", 14))
                label4.place(x=20, y=140)
                self.go_to_note_button = ctk.CTkButton(self.home_frame, text="Go to Doctor's Notes", command=self.notes_button_event, width=220, fg_color=self.c_buttons,
                                                    hover_color=self.c_buttons_hoover, text_color=self.c_buttons_text)
                self.go_to_note_button.place(x=300, y=140)
                label5 = ctk.CTkLabel(self.home_frame, text="", font=("Arial", 14))
                label5.place(x=20, y=180)
                self.appoint_button = ctk.CTkButton(self.home_frame, text="Go to Appointment management", command=self.appointment_button_event, width=220, fg_color=self.c_buttons, 
                                                    hover_color=self.c_buttons_hoover, text_color=self.c_buttons_text) 
                self.appoint_button.place(x=300, y=180)


                #TIPS
                # Conta il numero totale di suggerimenti
                self.cursor.execute("SELECT COUNT(*) FROM Tips")
                total_tips = self.cursor.fetchone()[0]

                random_id = random.randint(1, total_tips)

                self.cursor.execute("SELECT Tips FROM Tips WHERE TipsID = ?", (random_id,))
                tip = self.cursor.fetchone()
                
                # Configura la riga sopra perché spinga la label in basso
                self.home_frame.rowconfigure(0, weight=1)
                self.home_frame.rowconfigure(1, weight=0)  # riga della label

                # Se vuoi, configura anche le colonne per essere ridimensionabili
                self.home_frame.columnconfigure((0,1,2), weight=1)

                # Posiziona la label in basso, al centro sulle 3 colonne
                tip_label = ctk.CTkLabel(self.home_frame, text=f"Sleep Tip: {tip[0]}", font=("Arial", 12), text_color=self.c_text, wraplength=300)
                tip_label.grid(row=1, column=0, columnspan=3, sticky='s', pady=20)
                tip_label.configure(anchor='center')



                # Riamanda l'utente al questionario quotidiano se non ancora compilato
                
                self.cursor.execute("SELECT SleepScore FROM Questionnaire WHERE UserID = ? AND DATE(QuestionnaireDate) = ?", (self.user, self.oggi))
                result = self.cursor.fetchone()
                if result is None:
                    label3.configure(text="Fill in the Daily Questionnaire!")
                else:
                    self.quest_button.configure(state="disabled")
                    label3.configure(text="Today's questionnaire already submitted!")

                # Rimanda alle notes del dottore se ce n'è una nuova presente (per semplificare se c'è una nota inserita in data odierna tipo)
                self.cursor.execute("SELECT Note FROM notes WHERE PatientID = ? AND DoctorID = ? AND DATE(DateTime) = ?", (self.user, self.doctorID, self.oggi))
                result = self.cursor.fetchone()
                if result is None:
                    self.go_to_note_button.configure(state="disabled")
                    label4.configure(text="No new doctor's notes available.")
                else:
                    self.go_to_note_button.configure(state="normal")
                    label4.configure(text="A new note from your doctor is available!")

                # Promemoria del prossimo appuntamento col doc
                self.cursor.execute("SELECT DateTime FROM appointments WHERE PatientID = ? AND DoctorID = ?", (self.user, self.doctorID))
                appoint = self.cursor.fetchall()
                date_list = [row[0] for row in appoint]
                date_obj = [datetime.fromisoformat(dt) for dt in date_list]
                now = datetime.now()
                future_dates =[dt for dt in date_obj if dt>now]
                if future_dates:
                    next_appointment = min(future_dates)
                    label5.configure(text=f"Next appointment: {next_appointment.date()} at {next_appointment.time()}")
                else:
                    label5.configure(text="No appointment in the calendar")
                    self.appoint_button.configure(text="Request an appointment")    

    def data_button_event(self):
        self.select_frame_by_name("data")

    def notes_button_event(self):
        self.select_frame_by_name("notes")
        self.doctors_notes()
    
    def questionnaire_button_event(self):
        self.select_frame_by_name("questionnaire")
    
    def doctor_button_event(self):
        self.select_frame_by_name("doctor")
        self.my_doctor()
    
    def appointment_button_event(self):
        self.select_frame_by_name("appointment")
        self.appointment()

    def my_doctor(self):
        for widget in self.doctor_frame.winfo_children():
            widget.destroy()
        
        selection_frame = ctk.CTkFrame(self.doctor_frame, width=515, height=210, fg_color=self.c_frame)
        selection_frame.place(x=20, y=20)

        mydoctor_label = ctk.CTkLabel(selection_frame, text="My Doctor's information:", font=("Arial", 14), text_color=self.c_text)
        mydoctor_label.place(x=20, y=10)

        self.cursor.execute("SELECT Name FROM user WHERE UserID = ?", (self.doctorID,))
        doctor_name = self.cursor.fetchone()
        doctor_name = doctor_name[0] if doctor_name else "Unknown"

        self.cursor.execute("SELECT Surname FROM user WHERE UserID = ?", (self.doctorID,))
        doctor_surname = self.cursor.fetchone()
        doctor_surname = doctor_surname[0] if doctor_surname else "Unknown"

        self.cursor.execute("SELECT SocialSecurityNumber FROM user WHERE UserID = ?", (self.doctorID,))
        doctor_ssn = self.cursor.fetchone()
        doctor_ssn = doctor_ssn[0] if doctor_ssn else "Unknown"

        self.cursor.execute("SELECT Address FROM user WHERE UserID = ?", (self.doctorID,))
        doctor_address = self.cursor.fetchone()
        doctor_address = doctor_address[0] if doctor_address else "Unknown"

        self.cursor.execute("SELECT openinghour FROM doctors WHERE doctorID = ?", (self.doctorID,))
        openinghour = self.cursor.fetchone()
        openinghour = openinghour[0] if openinghour else "Unknown"
        self.cursor.execute("SELECT closinghour FROM doctors WHERE doctorID = ?", (self.doctorID,))
        closinghour = self.cursor.fetchone()
        closinghour = closinghour[0] if closinghour else "Unknown"

        self.cursor.execute("SELECT PhoneNumber FROM user WHERE UserID = ?", (self.doctorID,))
        doctor_phone = self.cursor.fetchone()
        doctor_phone = doctor_phone[0] if doctor_phone else "Unknown"

        self.cursor.execute("SELECT Email FROM user WHERE UserID = ?", (self.doctorID,))
        doctor_mail = self.cursor.fetchone()
        doctor_mail = doctor_mail[0] if doctor_mail else "Unknown"

        name_label = ctk.CTkLabel(selection_frame, text=f"Name: {doctor_name}", font=("Arial", 12))
        name_label.place(x=20, y=50)

        surname_label = ctk.CTkLabel(selection_frame, text=f"Surname: {doctor_surname}", font=("Arial", 12))
        surname_label.place(x=20, y=70)

        ssn_label = ctk.CTkLabel(selection_frame, text=f"Social Security Number: {doctor_ssn}", font=("Arial", 12))
        ssn_label.place(x=20, y=90)

        address_label = ctk.CTkLabel(selection_frame, text=f"Address: {doctor_address}", font=("Arial", 12))
        address_label.place(x=20, y=110)

        businesshour_label = ctk.CTkLabel(selection_frame, text=f"Business hours: {openinghour} - {closinghour}", font=("Arial", 12))
        businesshour_label.place(x=20, y=130)

        phone_label = ctk.CTkLabel(selection_frame, text=f"Phone Number: {doctor_phone}", font=("Arial", 12))
        phone_label.place(x=20, y=150)

        email_label = ctk.CTkLabel(selection_frame, text=f"E-mail: {doctor_mail}", font=("Arial", 12))
        email_label.place(x=20, y=170)

    # Appointment per paziente 
    def appointment(self):
        for widget in self.appointment_frame.winfo_children():
            widget.destroy()

        # Frame for dropdowns
        self.app_frame = ctk.CTkFrame(self.appointment_frame, width=520, height=170, fg_color=self.c_frame)
        self.app_frame.place(x=20, y=20)

        select_label = ctk.CTkLabel(self.app_frame, text="Create a new appointment or edit an existing one:", font=("Arial",14), text_color=self.c_text)
        select_label.place(x=20, y=10)

        # Recupera info: 
        self.cursor.execute("""SELECT Datetime, Location FROM appointments WHERE PatientID = ? AND DoctorID = ? ORDER BY Datetime""", (self.user, self.doctorID))
        appointments = self.cursor.fetchall()

        # Crea mappa 
        self.appointment_map = {
            datetime : datetime
            for datetime, location in appointments
            }
        appointment_display_list = list(self.appointment_map.keys())

        # Appointment combobox
        self.selected_appointment = ctk.StringVar()
        self.appointment_combobox = ctk.CTkComboBox(self.app_frame, values="", variable=self.selected_appointment,
                                                    command=self.enableupdate_button, width=250, dropdown_fg_color="white", button_color=self.c_buttons, button_hover_color=self.c_buttons_hoover)
        self.appointment_combobox.place(x=250, y=50)
        self.appointment_combobox.configure(state="disabled")
        if appointment_display_list:
            self.appointment_combobox.configure(state="normal")
            self.appointment_combobox.configure(values=appointment_display_list)
        appointment_label = ctk.CTkLabel(self.app_frame, text="Select appointment:", font=("Arial",12))
        appointment_label.place(x=20, y=50)

         # Frame for additional notes 
        notes_frame = ctk.CTkFrame(self.appointment_frame, width=520, height=130, fg_color=self.c_frame)
        notes_frame.place(x=20, y=210)

        selectdate_label = ctk.CTkLabel(notes_frame, text="Select new date and location:", font=("Arial", 14), text_color=self.c_text)
        selectdate_label.place(x=20, y=10)

        # Select date and hour
        date_label = ctk.CTkLabel(notes_frame, text="New date:", font=("Arial",12))
        date_label.place(x=20, y=50)
        self.newdate_selection_entry = ctk.CTkEntry(notes_frame, placeholder_text="dd/mm/yyyy", width=100)
        self.newdate_selection_entry.place(x=120, y=50)

        hour_label = ctk.CTkLabel(notes_frame, text="New hour:", font=("Arial",12))
        hour_label.place(x=300, y=50)
        self.newhour_selection_entry = ctk.CTkEntry(notes_frame, placeholder_text="HH:MM", width=100)
        self.newhour_selection_entry.place(x=400, y=50)

        # Select location
        location_label = ctk.CTkLabel(notes_frame, text="New Location:", font=("Arial",12))
        location_label.place(x=20, y=90)
        self.location_selection_entry = ctk.CTkEntry(notes_frame, placeholder_text="Address", width=200)
        self.location_selection_entry.place(x=120, y=90)

        # Appointment buttons
        self.newappointment_button = ctk.CTkButton(self.appointment_frame, text="Create new appointment", command=self.newappointment_callback, width=520, fg_color=self.c_buttons, 
                                                   hover_color=self.c_buttons_hoover, text_color=self.c_buttons_text)
        self.newappointment_button.place(relx=0.5, y=400, anchor="n")

        # Button frame
        button_frame = ctk.CTkFrame(self.appointment_frame, fg_color="transparent")
        button_frame.place(relx=0.5, y=450, anchor="n")
        # Bottone "delete"
        self.delete_button = ctk.CTkButton(button_frame, text="Delete appointment", command=self.deleteappointment_callback, fg_color=self.c_buttons, 
                                           hover_color=self.c_buttons_hoover, text_color=self.c_buttons_text, width=250)
        self.delete_button.grid(row=0, column=0, padx=10, pady=0, sticky="e")
        self.delete_button.configure(state="disabled")
        # Bottone "update"
        self.update_button = ctk.CTkButton(button_frame, text="Update appointment", command=self.updateappointment_callback, fg_color=self.c_buttons, 
                                           hover_color=self.c_buttons_hoover, text_color=self.c_buttons_text, width=250)
        self.update_button.grid(row=0, column=1, padx=10, pady=0, sticky="w")
        self.update_button.configure(state="disabled")

        # Output label for confimation message
        self.outcome_label = ctk.CTkLabel(self.appointment_frame, text="", font=("Arial",14), width=600, height=30)
        self.outcome_label.place(relx=0.5, y=360, anchor="n")

    # Doctor's Notes
    def doctors_notes(self):
        for widget in self.notes_frame.winfo_children():
            widget.destroy()

        self.selection_frame = ctk.CTkFrame(self.notes_frame, width=515, height=250, fg_color=self.c_frame)
        self.selection_frame.place(x=20, y=20)

        notes_label = ctk.CTkLabel(self.selection_frame, text="Doctor's notes:", font=("Arial", 14), text_color=self.c_text)
        notes_label.place(x=20, y=10)

        # Selezione notes dal db
        self.cursor.execute("""SELECT NotesID, DateTime,Note FROM notes WHERE PatientID = ? AND DoctorID = ?
                            ORDER BY DateTime DESC""", (self.user, self.doctorID))
        notes = self.cursor.fetchall()
        # Mappa: DateTime -> Note
        self.notes_map = {
            datetime: note
            for notes_id, datetime, note in notes
        }

        # Lista delle date
        #notes_list = list(self.notes_map.keys())
        notes_list = [dt for _, dt, _ in notes]
        print(notes_list)
        

        #notes_list = [datetime.fromisoformat(str(dt)).strftime("%d/%m/%Y") for dt in self.notes_map.keys()]

        recent_note_label = ctk.CTkLabel(self.selection_frame, text="", font=("Arial",12))
        recent_note_label.place(x=20, y=40)
        other_notes_label = ctk.CTkLabel(self.selection_frame, text="", font=("Arial",12))
        other_notes_label.place(x=20, y=110)

        if notes_list: 

            recent = self.notes_map.get(notes_list[0])
            recent_note_label.configure(text="Most recent note:")
            recent_date_label = ctk.CTkLabel(self.selection_frame, text=f"({notes_list[0]})", font=("Arial",12))
            recent_date_label.place(x=20, y=60)
            recent_note = ctk.CTkTextbox(self.selection_frame, width=340, height=50, font=("Arial", 12), wrap="word")
            # long_text = "This is a very long text.\n" * 50 # prova testo lungo
            recent_note.insert("0.0", str(recent))
           

            # recent_note.insert("0.0", recent)
            recent_note.configure(state="disabled")  # Rende il testo non modificabile
            recent_note.place(x=150, y=40)

            if len(notes_list) == 1:
                other_notes_label.configure(text="No other notes found.")
            elif len(notes_list) >= 2:
                other_notes_label.configure(text="View other notes:", font=("Arial",14), text_color=self.c_text)
                select_note = ctk.CTkLabel(self.selection_frame, text="Select notes's date:", font=("Arial",12))
                select_note.place(x=20, y=140)
                combo_values = notes_list[1:]
                self.selected_note = ctk.StringVar()
                notes_combobox = ctk.CTkComboBox(self.selection_frame, values=combo_values, variable=self.selected_note, 
                                                 command=self.enable_view, width=150, dropdown_fg_color="white", 
                                                 button_color=self.c_buttons, button_hover_color=self.c_buttons_hoover)
                notes_combobox.place(x=150, y=140)
                self.view_button = ctk.CTkButton(self.selection_frame, text="View note", command=self.view_note_callback, width=170, fg_color=self.c_buttons, 
                                                 hover_color=self.c_buttons_hoover, text_color=self.c_buttons_text)
                self.view_button.place(x=320 ,y=140)
                self.view_button.configure(state="disabled")
                self.outcome_label = ctk.CTkLabel(self.selection_frame, text="", font=("Arial",14))
                self.outcome_label.place(relx=0.5, y=450, anchor="n")

        else:
            recent_note_label.configure(text="No notes found.")

    def enable_view(self, selected_note):
        selected_note = self.notes_map.get(selected_note)
        if not selected_note:
            self.outcome_label.configure(text="Select a note", text_color="red")
            return
        self.view_button.configure(state="normal")

    def view_note_callback(self):
        note_date = self.selected_note.get()
        note_text = self.notes_map.get(note_date)

        selected_note_label = ctk.CTkLabel(self.selection_frame, text=f"Note of {note_date}:", font=("Arial",12))
        selected_note_label.place(x=20, y=180)
        selected_note = ctk.CTkTextbox(self.selection_frame, width=340, height=50, font=("Arial", 12), wrap="word")
        # long_text = "This is a very long text.\n" * 50 # prova testo lungo
        selected_note.insert("0.0", note_text)
        selected_note.configure(state="disabled")
        selected_note.place(x=150, y=180)


    def submit_questionnaire(self):
        today = date.today().isoformat()  # serve: from datetime import datetime, date

        # Controllo se il questionario è già stato fatto
        self.cursor.execute("SELECT * FROM Questionnaire WHERE QuestionnaireDate = ? AND UserID = ?", (today, self.patientID))
        if self.cursor.fetchone():
            self.risultato_label.configure(
                text="The daily questionnaire has already been filled out..",
                text_color="red"
            )
            self.conn.close()
            return

        responses = [
            self.radio_var1.get(),
            self.radio_var2.get(),
            self.radio_var3.get(),
            self.radio_var4.get(),
            self.radio_var5.get(),
            self.radio_var6.get(),
            self.radio_var7.get(),
            self.radio_var8.get()
        ]

        # Controllo: tutte le risposte devono essere date
        if "" in responses:
            self.risultato_label.configure(
                text="Please answer all the questions.",
                text_color="red"
            )
            return
       
        subjectivequality = responses[0]
        sleeplatency =  responses[1]
        sleepduration =  responses[2]
        sleepdisturbances =  responses[3]
        medications =  responses[4]
        troubleawake =  responses[5]
        daynapduration = responses[6]
        screens30mins =  responses[7]

        # Calcolo punteggio
        total = sum(int(val) for val in responses)
        normalized = 100 - round((total / 24) * 100)

        self.risultato_label.configure(text=f"Score: {normalized}%", text_color="green")

        # Inserimento nel database
        self.cursor.execute("INSERT INTO Questionnaire (SleepScore, QuestionnaireDate, UserID, SubjectiveQuality, Sleeplatency, SleepDuration, SleepDisturbances,Medications,TroubleAwake, DayNapDuration, Screens30Mins) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                             (normalized, today,self.user,subjectivequality,sleeplatency,sleepduration,sleepdisturbances,medications,troubleawake,daynapduration,screens30mins))
        self.conn.commit()

        # Reset all radio button selections
        for var in [self.radio_var1, self.radio_var2, self.radio_var3, self.radio_var4,
                    self.radio_var5, self.radio_var6, self.radio_var7, self.radio_var8]:
            var.set("")

        
        # Reset all radio button selections
        for var in [self.radio_var1, self.radio_var2, self.radio_var3, self.radio_var4,
                    self.radio_var5, self.radio_var6, self.radio_var7, self.radio_var8]:
            var.set("")
            
        
        self.show_quest()
        self.quest_outcome_label.configure(text=f"Questionnaire completed - Score: {normalized}", text_color='green')
        self.quest_outcome_label.after(1500, lambda: self.quest_outcome_label.configure(text=""))



    def data_button_event(self):
            self.select_frame_by_name("data")
            self.show_parameters_selection()
        
    def show_parameters_selection(self):
            # Pulisci il frame prima di mostrare nuovi dati
            for widget in self.data_frame.winfo_children():
                widget.destroy()
            
            # # Titolo
            # title_label = ctk.CTkLabel(self.data_frame, text="Select Parameter to View", 
            #                         font=("Arial", 20, "bold"), text_color=self.c_text)
            # title_label.pack(pady=20)
            
            # # Frame per la selezione della data
            # date_frame = ctk.CTkFrame(self.data_frame, fg_color=self.c_frame)
            # date_frame.pack(pady=10, padx=20, fill="x")
            
            # # Selezione data
            # self.cursor.execute("SELECT DISTINCT SummaryDate FROM DataSummary WHERE PatientID = ? ORDER BY SummaryDate DESC", (self.user,))
            # dates = [row[0] for row in self.cursor.fetchall()]
            
            # date_label = ctk.CTkLabel(date_frame, text="Select Date:", font=("Arial", 14))
            # date_label.grid(row=0, column=0, padx=10, pady=5)
            
            # self.selected_date = ctk.StringVar()
            # date_combobox = ctk.CTkComboBox(date_frame, values=dates, variable=self.selected_date,
            #                             width=200, dropdown_fg_color="white", 
            #                             button_color=self.c_buttons, button_hover_color=self.c_buttons_hoover)
            # date_combobox.grid(row=0, column=1, padx=10, pady=5)
            
            # # Frame per i parametri
            # params_frame = ctk.CTkFrame(self.data_frame, fg_color=self.c_main)
            # params_frame.pack(pady=20, fill="both", expand=True)
            
            # # Crea i frame per i parametri
            # hr_frame = ctk.CTkFrame(params_frame, width=150, height=150, fg_color=self.c_frame, 
            #                     corner_radius=10)
            # hr_frame.grid(row=0, column=0, padx=20, pady=10)
            # hr_label = ctk.CTkLabel(hr_frame, text="Heart Rate", font=("Arial", 16))
            # hr_label.place(relx=0.5, rely=0.5, anchor="center")
            # hr_frame.bind("<Button-1>", lambda e: self.show_parameter_plot("HRPlotPath", "Heart Rate"))
            
            # bp_frame = ctk.CTkFrame(params_frame, width=150, height=150, fg_color=self.c_frame, 
            #                     corner_radius=10)
            # bp_frame.grid(row=0, column=1, padx=20, pady=10)
            # bp_label = ctk.CTkLabel(bp_frame, text="Blood Pressure", font=("Arial", 16))
            # bp_label.place(relx=0.5, rely=0.5, anchor="center")
            # bp_frame.bind("<Button-1>", lambda e: self.show_parameter_plot("BPPlotPath", "Blood Pressure"))
            
            # po2_frame = ctk.CTkFrame(params_frame, width=150, height=150, fg_color=self.c_frame, 
            #                         corner_radius=10)
            # po2_frame.grid(row=0, column=2, padx=20, pady=10)
            # po2_label = ctk.CTkLabel(po2_frame, text="Oxygen Saturation", font=("Arial", 16))
            # po2_label.place(relx=0.5, rely=0.5, anchor="center")
            # po2_frame.bind("<Button-1>", lambda e: self.show_parameter_plot("PO2PlotPath", "Oxygen Saturation"))
            # Titolo
            title_label = ctk.CTkLabel(self.data_frame, text="My Sleep Data", 
                                    font=("Arial", 20, "bold"), text_color=self.c_text)
            title_label.pack(pady=10)
            
            # Frame per la selezione della data
            date_frame = ctk.CTkFrame(self.data_frame, fg_color=self.c_frame)
            date_frame.pack(pady=10, padx=20, fill="x")
            
            # Selezione data
            self.cursor.execute("SELECT DISTINCT SummaryDate FROM DataSummary WHERE PatientID = ? ORDER BY SummaryDate DESC", (self.patientID,))
            dates = [row[0] for row in self.cursor.fetchall()]
            
            date_label = ctk.CTkLabel(date_frame, text="Select Date:", font=("Arial", 14))
            date_label.grid(row=0, column=0, padx=10, pady=5)
            
            self.selected_date = ctk.StringVar()
            date_combobox = ctk.CTkComboBox(date_frame, values=dates, variable=self.selected_date,
                                        command=self.update_data_display, width=200,
                                        dropdown_fg_color="white", button_color=self.c_buttons,
                                        button_hover_color=self.c_buttons_hoover)
            date_combobox.grid(row=0, column=1, padx=10, pady=5)

            


            
            # Frame principale per i dati
            self.data_display_frame = ctk.CTkFrame(self.data_frame, fg_color=self.c_main)
            self.data_display_frame.pack(pady=10, padx=20, fill="both", expand=True)
            
            # Mostra i dati se è presente almeno una data
            if dates:
                self.selected_date.set(dates[0])
                self.update_data_display()

    def update_data_display(self, event=None):
            # Pulisci il frame di visualizzazione
            for widget in self.data_display_frame.winfo_children():
                widget.destroy()
            
            selected_date = self.selected_date.get()
            if not selected_date:
                return
            
            # Recupera i dati dal database
            self.cursor.execute("""
                SELECT PO2Path, HRPath, BPPath, PO2PlotPath, HRPlotPath, BPPlotPath, 
                    FallAsleepTime, WakingUpTime
                FROM DataSummary 
                WHERE PatientID = ? AND SummaryDate = ?
            """, (self.patientID, selected_date))
            
            row = self.cursor.fetchone()
            if not row:
                no_data_label = ctk.CTkLabel(self.data_display_frame, text="No data available for selected date",
                                            font=("Arial", 14), text_color="red")
                no_data_label.pack(pady=50)
                return
            
            # Estrai i percorsi
            po2_path, hr_path, bp_path, po2_plot_path, hr_plot_path, bp_plot_path, fall_asleep, wake_up = row
            
            # Crea i tab per i diversi parametri
            tabview = ctk.CTkTabview(self.data_display_frame, fg_color=self.c_frame)
            tabview.pack(pady=10, padx=10, fill="both", expand=True)
            
            # Aggiungi tab per ciascun parametro
            tabview.add("Oxygen Saturation (pO2)")
            tabview.add("Heart Rate (HR)") 
            tabview.add("Blood Pressure (BP)")
            
            # Configura lo stile dei tab
            tabview.configure(segmented_button_selected_color=self.c_buttons,
                            segmented_button_selected_hover_color=self.c_buttons_hoover,
                            segmented_button_unselected_color=self.c_frame,
                            segmented_button_unselected_hover_color=self.c_buttons)
            
            # Funzione per creare il contenuto di un tab
            def create_tab_content(tab, data_path, plot_path, param_name, unit):
                # Frame per il grafico
                plot_frame = ctk.CTkFrame(tab, fg_color="white", height=250)
                plot_frame.pack(pady=10, padx=10, fill="both", expand=True)
                
                # Mostra l'immagine del grafico
                try:
                    img = ctk.CTkImage(Image.open(plot_path), size=(600, 250))
                    img_label = ctk.CTkLabel(plot_frame, image=img, text="")
                    img_label.image = img  # Mantieni un riferimento!
                    img_label.pack(fill="both", expand=True)
                except Exception as e:
                    error_label = ctk.CTkLabel(plot_frame, text=f"Error loading plot: {str(e)}", 
                                            text_color="red", font=("Arial", 12))
                    error_label.pack(pady=50)
                
                # Frame per la tabella
                table_frame = ctk.CTkFrame(tab, fg_color=self.c_frame)
                table_frame.pack(pady=10, padx=10, fill="both", expand=True)
                
                # Leggi i dati dal file
                try:
                    with open(data_path, 'r') as f:
                        lines = f.readlines()
                    times = lines[0].strip().split()
                    values = list(map(float, lines[1].strip().split()))
                    
                    # Filtra solo i dati durante il sonno
                    filtered_times, filtered_values = [], []
                    for t, v in zip(times, values):
                        time_obj = datetime.strptime(t, "%H:%M").time()
                        fall_asleep_obj = datetime.strptime(fall_asleep, "%H:%M").time()
                        wake_up_obj = datetime.strptime(wake_up, "%H:%M").time()
                        
                        if fall_asleep_obj <= wake_up_obj:
                            if fall_asleep_obj <= time_obj <= wake_up_obj:
                                filtered_times.append(t)
                                filtered_values.append(v)
                        else:  # caso in cui il sonno passa la mezzanotte
                            if time_obj >= fall_asleep_obj or time_obj <= wake_up_obj:
                                filtered_times.append(t)
                                filtered_values.append(v)
                    
                    # Crea la tabella
                    tree = tk.Treeview(table_frame, columns=("Time", "Value"), show="headings", height=6)
                    tree.heading("Time", text="Time")
                    tree.heading("Value", text=f"Value ({unit})")
                    tree.column("Time", width=150, anchor="center")
                    tree.column("Value", width=150, anchor="center")
                    
                    for t, v in zip(filtered_times, filtered_values):
                        tree.insert("", "end", values=(t, v))
                    
                    # Aggiungi scrollbar
                    scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
                    tree.configure(yscrollcommand=scrollbar.set)
                    
                    tree.pack(side="left", fill="both", expand=True)
                    scrollbar.pack(side="right", fill="y")
                    
                    # Statistiche
                    if filtered_values:
                        stats_frame = ctk.CTkFrame(tab, fg_color=self.c_frame)
                        stats_frame.pack(pady=5, padx=10, fill="x")
                        
                        avg = sum(filtered_values) / len(filtered_values)
                        min_val = min(filtered_values)
                        max_val = max(filtered_values)
                        
                        stats_text = (f"Statistics during sleep: Avg = {avg:.1f}{unit}, "
                                    f"Min = {min_val:.1f}{unit}, Max = {max_val:.1f}{unit}")
                        
                        stats_label = ctk.CTkLabel(stats_frame, text=stats_text, 
                                                font=("Arial", 12), text_color=self.c_text)
                        stats_label.pack()
                    
                except Exception as e:
                    error_label = ctk.CTkLabel(table_frame, text=f"Error loading data: {str(e)}", 
                                            text_color="red", font=("Arial", 12))
                    error_label.pack(pady=20)
            
            # Popola i tab
            create_tab_content(tabview.tab("Oxygen Saturation (pO2)"), po2_path, po2_plot_path, "pO2", "%")
            create_tab_content(tabview.tab("Heart Rate (HR)"), hr_path, hr_plot_path, "HR", "bpm")
            create_tab_content(tabview.tab("Blood Pressure (BP)"), bp_path, bp_plot_path, "BP", "mmHg")
    
    def data_button_event(self):
            self.select_frame_by_name("data")
            self.show_parameters_selection()
        
    def show_parameters_selection(self):
        # Pulisci il frame prima di mostrare nuovi dati
        for widget in self.data_frame.winfo_children():
            widget.destroy()

        # === INIZIO: Scrollable Frame ===
        canvas = tk.Canvas(self.data_frame, bg=self.c_main, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.data_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ctk.CTkFrame(canvas, fg_color=self.c_main)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux scroll up
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))   # Linux scroll down
        # === FINE: Scrollable Frame ===

        # # Titolo
        # title_label = ctk.CTkLabel(scrollable_frame, text="Select Parameter to View", 
        #                         font=("Arial", 20, "bold"), text_color=self.c_text)
        # title_label.pack(pady=20)

        # # Frame per la selezione della data
        # date_frame = ctk.CTkFrame(scrollable_frame, fg_color=self.c_frame)
        # date_frame.pack(pady=10, padx=10, fill="x")

         # Selezione data
        self.cursor.execute("SELECT DISTINCT SummaryDate FROM DataSummary WHERE PatientID = ? ORDER BY SummaryDate DESC", (self.patientID,))
        dates = [row[0] for row in self.cursor.fetchall()]

        # date_label = ctk.CTkLabel(date_frame, text="Select Date:", font=("Arial", 14))
        # date_label.grid(row=0, column=0, padx=10, pady=5)

        # self.selected_date = ctk.StringVar()
        # date_combobox = ctk.CTkComboBox(date_frame, values=dates, variable=self.selected_date,
        #                                 width=200, dropdown_fg_color="white", 
        #                                 button_color=self.c_buttons, button_hover_color=self.c_buttons_hoover)
        # date_combobox.grid(row=0, column=1, padx=10, pady=5)

        # # Frame per i parametri
        # params_frame = ctk.CTkFrame(scrollable_frame, fg_color=self.c_main)
        # params_frame.pack(pady=20, fill="both", expand=True)

        # # Crea i frame per i parametri
        # hr_frame = ctk.CTkFrame(params_frame, width=150, height=150, fg_color=self.c_frame, corner_radius=10)
        # hr_frame.grid(row=0, column=0, padx=20, pady=10)
        # hr_label = ctk.CTkLabel(hr_frame, text="Heart Rate", font=("Arial", 16))
        # hr_label.place(relx=0.5, rely=0.5, anchor="center")
        # hr_frame.bind("<Button-1>", lambda e: self.show_parameter_plot("HRPlotPath", "Heart Rate"))

        # bp_frame = ctk.CTkFrame(params_frame, width=150, height=150, fg_color=self.c_frame, corner_radius=10)
        # bp_frame.grid(row=0, column=1, padx=20, pady=10)
        # bp_label = ctk.CTkLabel(bp_frame, text="Blood Pressure", font=("Arial", 16))
        # bp_label.place(relx=0.5, rely=0.5, anchor="center")
        # bp_frame.bind("<Button-1>", lambda e: self.show_parameter_plot("BPPlotPath", "Blood Pressure"))

        # po2_frame = ctk.CTkFrame(params_frame, width=150, height=150, fg_color=self.c_frame, corner_radius=10)
        # po2_frame.grid(row=0, column=2, padx=20, pady=10)
        # po2_label = ctk.CTkLabel(po2_frame, text="Oxygen Saturation", font=("Arial", 16))
        # po2_label.place(relx=0.5, rely=0.5, anchor="center")
        # po2_frame.bind("<Button-1>", lambda e: self.show_parameter_plot("PO2PlotPath", "Oxygen Saturation"))

        # Secondo titolo
        title_label = ctk.CTkLabel(scrollable_frame, text="My Sleep Data", 
                                font=("Arial", 20, "bold"), text_color=self.c_text)
        title_label.pack(pady=10)

        # Nuovo frame selezione data
        date_frame = ctk.CTkFrame(scrollable_frame, fg_color=self.c_frame)
        date_frame.pack(pady=10, padx=10, fill="x")

        self.cursor.execute("SELECT DISTINCT SummaryDate FROM DataSummary WHERE PatientID = ? ORDER BY SummaryDate DESC", (self.patientID,))
        dates = [row[0] for row in self.cursor.fetchall()]

        date_label = ctk.CTkLabel(date_frame, text="Select Date:", font=("Arial", 14))
        date_label.grid(row=0, column=0, padx=10, pady=5)

        self.selected_date = ctk.StringVar()
        date_combobox = ctk.CTkComboBox(date_frame, values=dates, variable=self.selected_date,
                                        command=self.update_data_display, width=250,
                                        dropdown_fg_color="white", button_color=self.c_buttons,
                                        button_hover_color=self.c_buttons_hoover)
        date_combobox.grid(row=0, column=1, padx=10, pady=5)

        self.note_button = ctk.CTkButton(date_frame, text="", width=100, fg_color=self.c_frame, hover=False)
        self.note_button.grid(row=0, column=2, padx=20, pady=5)

        # Frame principale per i dati
        self.data_display_frame = ctk.CTkFrame(scrollable_frame, fg_color=self.c_main)
        self.data_display_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Mostra i dati se è presente almeno una data
        if dates:
            self.selected_date.set(dates[0])
            self.update_data_display()


    def update_data_display(self, event=None):
            # Pulisci il frame di visualizzazione
            for widget in self.data_display_frame.winfo_children():
                widget.destroy()
            
            selected_date = self.selected_date.get()
            if not selected_date:
                return
            
            # Recupera i dati dal database
            self.cursor.execute("""
                SELECT PO2Path, HRPath, BPPath, PO2PlotPath, HRPlotPath, BPPlotPath, 
                    FallAsleepTime, WakingUpTime
                FROM DataSummary 
                WHERE PatientID = ? AND SummaryDate = ?
            """, (self.user, selected_date))
            
            row = self.cursor.fetchone()
            if not row:
                no_data_label = ctk.CTkLabel(self.data_display_frame, text="No data available for selected date",
                                            font=("Arial", 14), text_color="red")
                no_data_label.pack(pady=50)
                return
            
            # Estrai i percorsi
            po2_path, hr_path, bp_path, po2_plot_path, hr_plot_path, bp_plot_path, fall_asleep, wake_up = row
            
            # Crea i tab per i diversi parametri
            tabview = ctk.CTkTabview(self.data_display_frame, fg_color=self.c_frame)
            tabview.pack(pady=10, padx=10, fill="both", expand=True)
            
            # Aggiungi tab per ciascun parametro
            tabview.add("Oxygen Saturation (pO2)")
            tabview.add("Heart Rate (HR)") 
            tabview.add("Blood Pressure (BP)")
            
            # Configura lo stile dei tab
            tabview.configure(segmented_button_selected_color=self.c_buttons,
                            segmented_button_selected_hover_color=self.c_buttons_hoover,
                            segmented_button_unselected_color=self.c_frame,
                            segmented_button_unselected_hover_color=self.c_buttons)
            
            # Funzione per creare il contenuto di un tab
            def create_tab_content(tab, data_path, plot_path, param_name, unit):
                # Frame per il grafico
                plot_frame = ctk.CTkFrame(tab, fg_color="white", height=250, width=460)
                plot_frame.pack(pady=10, padx=10, fill="both", expand=True)
                
                # Mostra l'immagine del grafico
                try:
                    img = ctk.CTkImage(Image.open(plot_path), size=(400, 250))
                    img_label = ctk.CTkLabel(plot_frame, image=img, text="")
                    img_label.image = img  # Mantieni un riferimento!
                    img_label.pack(fill="both", expand=True)
                except Exception as e:
                    error_label = ctk.CTkLabel(plot_frame, text=f"Error loading plot: {str(e)}", 
                                            text_color="red", font=("Arial", 12))
                    error_label.pack(pady=50)
                
                # Frame per la tabella
                table_frame = ctk.CTkFrame(tab, fg_color=self.c_frame)
                table_frame.pack(pady=10, padx=10, fill="both", expand=True)
                
                # Leggi i dati dal file
                try:
                    with open(data_path, 'r') as f:
                        lines = f.readlines()
                    times = lines[0].strip().split()
                    values = list(map(float, lines[1].strip().split()))
                    
                    # Filtra solo i dati durante il sonno
                    filtered_times, filtered_values = [], []
                    for t, v in zip(times, values):
                        time_obj = datetime.strptime(t, "%H:%M").time()
                        fall_asleep_obj = datetime.strptime(fall_asleep, "%H:%M").time()
                        wake_up_obj = datetime.strptime(wake_up, "%H:%M").time()
                        
                        if fall_asleep_obj <= wake_up_obj:
                            if fall_asleep_obj <= time_obj <= wake_up_obj:
                                filtered_times.append(t)
                                filtered_values.append(v)
                        else:  # caso in cui il sonno passa la mezzanotte
                            if time_obj >= fall_asleep_obj or time_obj <= wake_up_obj:
                                filtered_times.append(t)
                                filtered_values.append(v)
                    
                    # Crea la tabella
                    tree = ttk.Treeview(table_frame, columns=("Time", "Value"), show="headings", height=6)
                    tree.heading("Time", text="Time")
                    tree.heading("Value", text=f"Value ({unit})")
                    tree.column("Time", width=150, anchor="center")
                    tree.column("Value", width=150, anchor="center")
                    
                    for t, v in zip(filtered_times, filtered_values):
                        tree.insert("", "end", values=(t, v))
                    
                    # Aggiungi scrollbar
                    scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
                    tree.configure(yscrollcommand=scrollbar.set)
                    
                    tree.pack(side="left", fill="both", expand=True)
                    scrollbar.pack(side="right", fill="y")
                    
                    # Statistiche
                    if filtered_values:
                        stats_frame = ctk.CTkFrame(tab, fg_color=self.c_frame)
                        stats_frame.pack(pady=5, padx=10, fill="x")
                        
                        avg = sum(filtered_values) / len(filtered_values)
                        min_val = min(filtered_values)
                        max_val = max(filtered_values)
                        
                        stats_text = (f"Statistics during sleep: Avg = {avg:.1f}{unit}, "
                                    f"Min = {min_val:.1f}{unit}, Max = {max_val:.1f}{unit}")
                        
                        stats_label = ctk.CTkLabel(stats_frame, text=stats_text, 
                                                font=("Arial", 12), text_color=self.c_text)
                        stats_label.pack()
                    
                except Exception as e:
                    error_label = ctk.CTkLabel(table_frame, text=f"Error loading data: {str(e)}", 
                                            text_color="red", font=("Arial", 12))
                    error_label.pack(pady=20)
            
            # Popola i tab
            create_tab_content(tabview.tab("Oxygen Saturation (pO2)"), po2_path, po2_plot_path, "pO2", "%")
            create_tab_content(tabview.tab("Heart Rate (HR)"), hr_path, hr_plot_path, "HR", "bpm")
            create_tab_content(tabview.tab("Blood Pressure (BP)"), bp_path, bp_plot_path, "BP", "mmHg")









    def show_doc_parameters_selection(self):
        # Pulisci il frame prima di mostrare nuovi dati
        for widget in self.data_frame.winfo_children():
            widget.destroy()

        self.select_frame_by_name('data')  

        # === INIZIO: Scrollable Frame ===
        canvas = tk.Canvas(self.data_frame, bg=self.c_main, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.data_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ctk.CTkFrame(canvas, fg_color=self.c_main)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux scroll up
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))   # Linux scroll down
        # === FINE: Scrollable Frame ===

        # # Titolo
        # title_label = ctk.CTkLabel(scrollable_frame, text="Select Parameter to View", 
        #                         font=("Arial", 20, "bold"), text_color=self.c_text)
        # title_label.pack(pady=20)

        # # Frame per la selezione della data
        # date_frame = ctk.CTkFrame(scrollable_frame, fg_color=self.c_frame)
        # date_frame.pack(pady=10, padx=10, fill="x")

        # Selezione data
        self.cursor.execute("SELECT DISTINCT SummaryDate FROM DataSummary WHERE PatientID = ? ORDER BY SummaryDate DESC", (self.patientID,))
        dates = [row[0] for row in self.cursor.fetchall()]

        # date_label = ctk.CTkLabel(date_frame, text="Select Date:", font=("Arial", 14))
        # date_label.grid(row=0, column=0, padx=10, pady=5)

        # self.selected_date = ctk.StringVar()
        # date_combobox = ctk.CTkComboBox(date_frame, values=dates, variable=self.selected_date,
        #                                 width=200, dropdown_fg_color="white", 
        #                                 button_color=self.c_buttons, button_hover_color=self.c_buttons_hoover)
        # date_combobox.grid(row=0, column=1, padx=10, pady=5)

        # # Frame per i parametri
        # params_frame = ctk.CTkFrame(scrollable_frame, fg_color=self.c_main)
        # params_frame.pack(pady=20, fill="both", expand=True)

        # # Crea i frame per i parametri
        # hr_frame = ctk.CTkFrame(params_frame, width=150, height=150, fg_color=self.c_frame, corner_radius=10)
        # hr_frame.grid(row=0, column=0, padx=20, pady=10)
        # hr_label = ctk.CTkLabel(hr_frame, text="Heart Rate", font=("Arial", 16))
        # hr_label.place(relx=0.5, rely=0.5, anchor="center")
        # hr_frame.bind("<Button-1>", lambda e: self.show_parameter_plot("HRPlotPath", "Heart Rate"))

        # bp_frame = ctk.CTkFrame(params_frame, width=150, height=150, fg_color=self.c_frame, corner_radius=10)
        # bp_frame.grid(row=0, column=1, padx=20, pady=10)
        # bp_label = ctk.CTkLabel(bp_frame, text="Blood Pressure", font=("Arial", 16))
        # bp_label.place(relx=0.5, rely=0.5, anchor="center")
        # bp_frame.bind("<Button-1>", lambda e: self.show_parameter_plot("BPPlotPath", "Blood Pressure"))

        # po2_frame = ctk.CTkFrame(params_frame, width=150, height=150, fg_color=self.c_frame, corner_radius=10)
        # po2_frame.grid(row=0, column=2, padx=20, pady=10)
        # po2_label = ctk.CTkLabel(po2_frame, text="Oxygen Saturation", font=("Arial", 16))
        # po2_label.place(relx=0.5, rely=0.5, anchor="center")
        # po2_frame.bind("<Button-1>", lambda e: self.show_parameter_plot("PO2PlotPath", "Oxygen Saturation"))

        # Secondo titolo
        title_label = ctk.CTkLabel(scrollable_frame, text="My Sleep Data", 
                                font=("Arial", 20, "bold"), text_color=self.c_text)
        title_label.pack(pady=10)

        # Nuovo frame selezione data
        date_frame = ctk.CTkFrame(scrollable_frame, fg_color=self.c_frame)
        date_frame.pack(pady=10, padx=10, fill="x")

        self.cursor.execute("SELECT DISTINCT SummaryDate FROM DataSummary WHERE PatientID = ? ORDER BY SummaryDate DESC", (self.patientID,))
        dates = [row[0] for row in self.cursor.fetchall()]

        date_label = ctk.CTkLabel(date_frame, text="Select Date:", font=("Arial", 14))
        date_label.grid(row=0, column=0, padx=10, pady=5)

        self.selected_date = ctk.StringVar()
        date_combobox = ctk.CTkComboBox(date_frame, values=dates, variable=self.selected_date,
                                        command=self.update_doc_data_display, width=200,
                                        dropdown_fg_color="white", button_color=self.c_buttons,
                                        button_hover_color=self.c_buttons_hoover)
        date_combobox.grid(row=0, column=1, padx=10, pady=5)

        self.note_button = ctk.CTkButton(date_frame, text="Add note", command=self.add_note_callback, width=150, fg_color=self.c_buttons, 
                                                 hover_color=self.c_buttons_hoover, text_color=self.c_buttons_text)
        self.note_button.grid(row=0, column=2, padx=20, pady=5)

        # Frame principale per i dati
        self.data_display_frame = ctk.CTkFrame(scrollable_frame, fg_color=self.c_main)
        self.data_display_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Mostra i dati se è presente almeno una data
        if dates:
            self.selected_date.set(dates[0])
            self.update_doc_data_display()

    def add_note_callback(self):
        for widget in self.data_frame.winfo_children():
                widget.destroy()

        self.selection_frame = ctk.CTkFrame(self.data_frame, width=515, height=250, fg_color=self.c_frame)
        self.selection_frame.place(x=20, y=20)

        notes_label = ctk.CTkLabel(self.selection_frame, text="New note:", font=("Arial", 14), text_color=self.c_text)
        notes_label.place(x=20, y=10)

        

        

        self.recent_note = ctk.CTkTextbox(self.selection_frame, width=475, height=185, font=("Arial", 12), wrap="word")
        # long_text = "This is a very long text.\n" * 50 # prova testo lungo
        self.recent_note.place(x=20, y=40)

        
        self.view_button = ctk.CTkButton(self.data_frame, text="Save", command=self.save_note_callback, width=170, fg_color=self.c_buttons, 
                                            hover_color=self.c_buttons_hoover, text_color=self.c_buttons_text)
        self.view_button.place(relx=0.35 ,y=320)
        
        self.outcome_label = ctk.CTkLabel(self.data_frame, text="", font=("Arial",14))
        self.outcome_label.place(relx=0.5, y=450, anchor="n")
      

      
         

    def save_note_callback(self):

        ora = dt.date.today()
        note_text=self.recent_note.get("1.0", "end-1c")
        self.cursor.execute("""
        INSERT INTO notes (PatientID, DoctorID, Datetime, Note)
        VALUES (?, ?, ?, ?)
        """, (self.patientID, self.user, ora, note_text))

        self.conn.commit()
        self.outcome_label.configure(text="Note saved!", text_color='green')
        self.outcome_label.after(1000, lambda: self.outcome_label.configure(text=""))   
        self.recent_note.delete("1.0", "end")
        self.show_data()
        
        

    
        




    def update_doc_data_display(self, event=None):
            # Pulisci il frame di visualizzazione
            for widget in self.data_display_frame.winfo_children():
                widget.destroy()
            
            selected_date = self.selected_date.get()
            if not selected_date:
                return
            
            # Recupera i dati dal database
            self.cursor.execute("""
                SELECT PO2Path, HRPath, BPPath, PO2PlotPath, HRPlotPath, BPPlotPath, 
                    FallAsleepTime, WakingUpTime
                FROM DataSummary 
                WHERE PatientID = ? AND SummaryDate = ?
            """, (self.patientID, selected_date))
            
            row = self.cursor.fetchone()
            if not row:
                no_data_label = ctk.CTkLabel(self.data_display_frame, text="No data available for selected date",
                                            font=("Arial", 14), text_color="red")
                no_data_label.pack(pady=50)
                return
            
            # Estrai i percorsi
            po2_path, hr_path, bp_path, po2_plot_path, hr_plot_path, bp_plot_path, fall_asleep, wake_up = row
            
            # Crea i tab per i diversi parametri
            tabview = ctk.CTkTabview(self.data_display_frame, fg_color=self.c_frame)
            tabview.pack(pady=10, padx=10, fill="both", expand=True)
            
            # Aggiungi tab per ciascun parametro
            tabview.add("Oxygen Saturation (pO2)")
            tabview.add("Heart Rate (HR)") 
            tabview.add("Blood Pressure (BP)")
            
            # Configura lo stile dei tab
            tabview.configure(segmented_button_selected_color=self.c_buttons,
                            segmented_button_selected_hover_color=self.c_buttons_hoover,
                            segmented_button_unselected_color=self.c_frame,
                            segmented_button_unselected_hover_color=self.c_buttons)
            
            # Funzione per creare il contenuto di un tab
            def create_doc_tab_content(tab, data_path, plot_path, param_name, unit):
                # Frame per il grafico
                plot_frame = ctk.CTkFrame(tab, fg_color="white", height=250, width=420)
                plot_frame.pack(pady=10, padx=10, fill="both", expand=True)
                
                # Mostra l'immagine del grafico
                try:
                    img = ctk.CTkImage(Image.open(plot_path), size=(400, 250))
                    img_label = ctk.CTkLabel(plot_frame, image=img, text="")
                    img_label.image = img  # Mantieni un riferimento!
                    img_label.pack(fill="both", expand=True)
                except Exception as e:
                    error_label = ctk.CTkLabel(plot_frame, text=f"Error loading plot: {str(e)}", 
                                            text_color="red", font=("Arial", 12))
                    error_label.pack(pady=50)
                
                # Frame per la tabella
                table_frame = ctk.CTkFrame(tab, fg_color=self.c_frame)
                table_frame.pack(pady=10, padx=10, fill="both", expand=True)
                
                # Leggi i dati dal file
                try:
                    with open(data_path, 'r') as f:
                        lines = f.readlines()
                    times = lines[0].strip().split()
                    values = list(map(float, lines[1].strip().split()))
                    
                    # Filtra solo i dati durante il sonno
                    filtered_times, filtered_values = [], []
                    for t, v in zip(times, values):
                        time_obj = datetime.strptime(t, "%H:%M").time()
                        fall_asleep_obj = datetime.strptime(fall_asleep, "%H:%M").time()
                        wake_up_obj = datetime.strptime(wake_up, "%H:%M").time()
                        
                        if fall_asleep_obj <= wake_up_obj:
                            if fall_asleep_obj <= time_obj <= wake_up_obj:
                                filtered_times.append(t)
                                filtered_values.append(v)
                        else:  # caso in cui il sonno passa la mezzanotte
                            if time_obj >= fall_asleep_obj or time_obj <= wake_up_obj:
                                filtered_times.append(t)
                                filtered_values.append(v)
                    
                    # Crea la tabella
                    tree = ttk.Treeview(table_frame, columns=("Time", "Value"), show="headings", height=6)
                    tree.heading("Time", text="Time")
                    tree.heading("Value", text=f"Value ({unit})")
                    tree.column("Time", width=150, anchor="center")
                    tree.column("Value", width=150, anchor="center")
                    
                    for t, v in zip(filtered_times, filtered_values):
                        tree.insert("", "end", values=(t, v))
                    
                    # Aggiungi scrollbar
                    scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
                    tree.configure(yscrollcommand=scrollbar.set)
                    
                    tree.pack(side="left", fill="both", expand=True)
                    scrollbar.pack(side="right", fill="y")
                    
                    # Statistiche
                    if filtered_values:
                        stats_frame = ctk.CTkFrame(tab, fg_color=self.c_frame)
                        stats_frame.pack(pady=5, padx=10, fill="x")
                        
                        avg = sum(filtered_values) / len(filtered_values)
                        min_val = min(filtered_values)
                        max_val = max(filtered_values)
                        
                        stats_text = (f"Statistics during sleep: Avg = {avg:.1f}{unit}, "
                                    f"Min = {min_val:.1f}{unit}, Max = {max_val:.1f}{unit}")
                        
                        stats_label = ctk.CTkLabel(stats_frame, text=stats_text, 
                                                font=("Arial", 12), text_color=self.c_text)
                        stats_label.pack()
                    
                except Exception as e:
                    error_label = ctk.CTkLabel(table_frame, text=f"Error loading data: {str(e)}", 
                                            text_color="red", font=("Arial", 12))
                    error_label.pack(pady=20)
            
            # Popola i tab
            create_doc_tab_content(tabview.tab("Oxygen Saturation (pO2)"), po2_path, po2_plot_path, "pO2", "%")
            create_doc_tab_content(tabview.tab("Heart Rate (HR)"), hr_path, hr_plot_path, "HR", "bpm")
            create_doc_tab_content(tabview.tab("Blood Pressure (BP)"), bp_path, bp_plot_path, "BP", "mmHg")
        















    # FUNZIONI COMUNI A DOCTOR E PATIENT

    def select_frame_by_name(self, name):
        
        if self.user_role == "D":
            # set button color for selected button
            self.home_button.configure(fg_color=self.c_buttons_hoover if name == "home" else "transparent")
            self.doc_appointments_button.configure(fg_color=self.c_buttons_hoover if name == "doc_appointments" else "transparent")
            self.patients_button.configure(fg_color=self.c_buttons_hoover if name == "patients" else "transparent")
            self.profile_button.configure(fg_color=self.c_buttons_hoover if name == "profile" else "transparent")
            self.logout_button.configure(fg_color=self.c_buttons_hoover if name == "logout" else "transparent")

            # show selected frame
            if name == "home":
                self.home_frame.grid(row=0, column=1, sticky="nsew")
                self.content_frame.lower()
            else:
                self.home_frame.grid_forget()
            if name == "doc_appointments":
                self.doc_appointments_frame.grid(row=0, column=1, sticky="nsew")
                self.content_frame.lower()
            else:
                self.doc_appointments_frame.grid_forget()
            if name == "patients":
                self.patients_frame.grid(row=0, column=1, sticky="nsew")
            else:
                self.patients_frame.grid_forget()
            if name == "profile":
                self.profile_frame.grid(row=0, column=1, sticky="nsew")
                self.content_frame.lower()
            else:
                self.profile_frame.grid_forget()
            if name == "logout":
                self.logout_frame.grid(row=0, column=1, sticky="nsew")
                self.content_frame.lower()
            else:
                self.logout_frame.grid_forget()
            if name == "data":
                self.data_frame.grid(row=0, column=1, sticky="nsew")
                self.content_frame.lower()
            else:
                self.data_frame.grid_forget()    

        elif self.user_role == "P":
            self.home_button.configure(fg_color=self.c_buttons_hoover if name == "home" else "transparent")
            self.data_button.configure(fg_color=self.c_buttons_hoover if name == "data" else "transparent")
            self.notes_button.configure(fg_color=self.c_buttons_hoover if name == "notes" else "transparent")
            self.questionnaire_button.configure(fg_color=self.c_buttons_hoover if name == "questionnaire" else "transparent")
            self.doctor_button.configure(fg_color=self.c_buttons_hoover if name == "doctor" else "transparent")
            self.appointment_button.configure(fg_color=self.c_buttons_hoover if name == "appointment" else "transparent")
            self.profile_button.configure(fg_color=self.c_buttons_hoover if name == "profile" else "transparent")
            self.logout_button.configure(fg_color=self.c_buttons_hoover if name == "logout" else "transparent")

            # show selected frame
            if name == "home":
                self.home_frame.grid(row=0, column=1, sticky="nsew")
            else:
                self.home_frame.grid_forget()
            if name == "data":
                self.data_frame.grid(row=0, column=1, sticky="nsew")
            else:
                self.data_frame.grid_forget()
            if name == "notes":
                self.notes_frame.grid(row=0, column=1, sticky="nsew")
            else:
                self.notes_frame.grid_forget()
            if name == "questionnaire":
                self.questionnaire_frame.grid(row=0, column=1, sticky="nsew")
            else:
                self.questionnaire_frame.grid_forget()
            if name == "doctor":
                self.doctor_frame.grid(row=0, column=1, sticky="nsew")
            else:
                self.doctor_frame.grid_forget()
            if name == "appointment":
                self.appointment_frame.grid(row=0, column=1, sticky="nsew")
            else:
                self.appointment_frame.grid_forget()
            if name == "profile":
                self.profile_frame.grid(row=0, column=1, sticky="nsew")
            else:
                self.profile_frame.grid_forget()
            if name == "logout":
                self.logout_frame.grid(row=0, column=1, sticky="nsew")
            else:
                self.logout_frame.grid_forget()
    

    # MyProfile: doctor's and patient's profiles
    def personal_data(self):
        for widget in self.profile_frame.winfo_children():
            widget.destroy()
        
        selection_frame = ctk.CTkFrame(self.profile_frame, width=515, height=240, fg_color=self.c_frame)
        selection_frame.place(x=20, y=20)

        profile_label = ctk.CTkLabel(selection_frame, text="Personal data:", font=("Arial", 14), text_color=self.c_text)
        profile_label.place(x=20, y=10)

        self.cursor.execute("SELECT Name FROM user WHERE UserID = ?", (self.user,))
        self.name = self.cursor.fetchone()
        self.name = self.name[0] if self.name else "Unknown"

        self.cursor.execute("SELECT Surname FROM user WHERE UserID = ?", (self.user,))
        self.surname = self.cursor.fetchone()
        self.surname = self.surname[0] if self.surname else "Unknown"

        self.cursor.execute("SELECT BirthDate FROM user WHERE UserID = ?", (self.user,))
        self.bdate = self.cursor.fetchone()
        self.bdate = self.bdate[0] if self.bdate else "Unknown"

        self.cursor.execute("SELECT BirthPlace FROM user WHERE UserID = ?", (self.user,))
        self.bplace = self.cursor.fetchone()
        self.bplace = self.bplace[0] if self.bplace else "Unknown"

        self.cursor.execute("SELECT SocialSecurityNumber FROM user WHERE UserID = ?", (self.user,))
        self.ssn = self.cursor.fetchone()
        self.ssn = self.ssn[0] if self.ssn else "Unknown"

        self.cursor.execute("SELECT Address FROM user WHERE UserID = ?", (self.user,))
        self.address = self.cursor.fetchone()
        self.address = self.address[0] if self.address else "Unknown"

        self.cursor.execute("SELECT PhoneNumber FROM user WHERE UserID = ?", (self.user,))
        self.phone = self.cursor.fetchone()
        self.phone = self.phone[0] if self.phone else "Unknown"

        self.cursor.execute("SELECT Email FROM user WHERE UserID = ?", (self.user,))
        self.mail = self.cursor.fetchone()
        self.mail = self.mail[0] if self.mail else "Unknown"

        self.cursor.execute("SELECT Password FROM user WHERE UserID = ?", (self.user,))
        self.password = self.cursor.fetchone()
        self.password = self.password[0] if self.password else "Unknown"

        name_label = ctk.CTkLabel(selection_frame, text=f"Name: {self.name}", font=("Arial", 12))
        name_label.place(x=20, y=40)

        surname_label = ctk.CTkLabel(selection_frame, text=f"Surname: {self.surname}", font=("Arial", 12))
        surname_label.place(x=20, y=60)

        bdate_label = ctk.CTkLabel(selection_frame, text=f"Birth Date: {self.bdate}", font=("Arial", 12))
        bdate_label.place(x=20, y=80)

        bplace_label = ctk.CTkLabel(selection_frame, text=f"Birth Place: {self.bplace}", font=("Arial", 12))
        bplace_label.place(x=20, y=100)

        ssn_label = ctk.CTkLabel(selection_frame, text=f"Social Security Number: {self.ssn}", font=("Arial", 12))
        ssn_label.place(x=20, y=120)

        address_label = ctk.CTkLabel(selection_frame, text=f"", font=("Arial", 12))
        address_label.place(x=20, y=140)

        if self.user_role == "D":
            address_label.configure(text=f"Office Address: {self.address}", font=("Arial", 12))

            self.cursor.execute("SELECT openinghour FROM doctors WHERE doctorID = ?", (self.user,))
            self.openinghour = self.cursor.fetchone()
            self.openinghour = self.openinghour[0] if self.openinghour else "Unknown"
            self.cursor.execute("SELECT closinghour FROM doctors WHERE doctorID = ?", (self.user,))
            self.closinghour = self.cursor.fetchone()
            self.closinghour = self.closinghour[0] if self.closinghour else "Unknown"
            businesshour_label = ctk.CTkLabel(selection_frame, text=f"Business hours: {self.openinghour} - {self.closinghour}", font=("Arial", 12))
            businesshour_label.place(x=20, y=160)

        elif self.user_role == "P":
            address_label.configure(text=f"Residence Address: {self.address}", font=("Arial", 12))

            self.cursor.execute("SELECT Height FROM patient WHERE UserID = ?", (self.user,))
            self.height = self.cursor.fetchone()
            self.height = self.height[0] if self.height else "Unknown"
            self.cursor.execute("SELECT Weight FROM patient WHERE UserID = ?", (self.user,))
            self.weight = self.cursor.fetchone()
            self.weight = self.weight[0] if self.weight else "Unknown"
            heightweight_label = ctk.CTkLabel(selection_frame, text=f"Height: {self.height}, Weight: {self.weight}", font=("Arial", 12))
            heightweight_label.place(x=20, y=160)

            # Prescriptions 
            medication_frame = ctk.CTkFrame(self.profile_frame, width=515, height=120, fg_color=self.c_frame)
            medication_frame.place(x=20, y=280)
            medication_label = ctk.CTkLabel(medication_frame, text="Prescriptions:", font=("Arial", 14), text_color=self.c_text)
            medication_label.place(x=20, y=10)

            self.cursor.execute("""SELECT Drug,Dosage,Frequency,EndingDate FROM prescriptions WHERE PatientID = ? AND DoctorID = ?
                                ORDER BY EndingDate ASC""", (self.user,self.doctorID))
            self.medications_found = self.cursor.fetchall()

            medications_label = ctk.CTkLabel(medication_frame, text="Prescriptions: ", font=("Arial", 12))
            medications_label.place(x=20, y=40)

            medications = ctk.CTkTextbox(medication_frame, width=370, height=80, font=("Arial", 12), wrap="word")
            #long_text = "This is a very long text.\n" * 50 # prova testo lungo
            medications.place(x=130, y=20)

            today = date.today()
            self.medications_active = []
            for row in self.medications_found:
                ending_date_str = row[3]
                ending_date = date.fromisoformat(ending_date_str)
                if ending_date >= today:
                    self.medications_active.append(row)
            if not self.medications_active:
                medications.insert("0.0", "None")
                
            else:
                for drug, dosage, frequency, _ in self.medications_active:
                    text=f"{drug} {dosage} - {frequency}"
                    medications.insert("end", text + "\n")
                    
            print(self.medications_active) 
            medications.configure(state="disabled")       

            

        phone_label = ctk.CTkLabel(selection_frame, text=f"Phone Number: {self.phone}", font=("Arial", 12))
        phone_label.place(x=20, y=180)

        email_label = ctk.CTkLabel(selection_frame, text=f"E-mail: {self.mail}", font=("Arial", 12))
        email_label.place(x=20, y=200)

        # Buttons: modify personal data
        self.modify_button = ctk.CTkButton(self.profile_frame, text="Edit", command=self.modify_callback, width=520, fg_color=self.c_buttons, 
                                           hover_color=self.c_buttons_hoover, text_color=self.c_buttons_text) 
        self.modify_button.place(relx=0.5,  y=450, anchor="n")

        self.outcome_label = ctk.CTkLabel(self.profile_frame, text="", font=("Arial", 14))
        self.outcome_label.place(relx=0.5, y=350, anchor="n")

    # Modify MyProfile
    def modify_callback(self):
        for widget in self.profile_frame.winfo_children():
            widget.destroy()

        frame = ctk.CTkFrame(self.profile_frame, width=515, height=360, fg_color=self.c_frame)
        frame.place(x=20, y=20)

        update_label = ctk.CTkLabel(frame, text="Edit personal data:", font=("Arial", 14), text_color=self.c_text)
        update_label.place(x=20, y=10)

        selection_frame = ctk.CTkFrame(frame, width=515, height=355, fg_color=self.c_frame)
        selection_frame.place(relx=0.5, y=40, anchor="n")

        name_label = ctk.CTkLabel(selection_frame, text="Name:", font=("Arial", 14))
        name_label.grid(row=1, column=0, padx=10, pady=0, sticky="e")
        name_entry = ctk.CTkEntry(selection_frame, placeholder_text=f"{self.name}", width=200, height=20, font=("Arial", 14))
        name_entry.grid(row=1, column=1, padx=10, pady=0, sticky="w")
        name_entry.configure(state="readonly")

        surname_label = ctk.CTkLabel(selection_frame, text="Surname:", font=("Arial", 14))
        surname_label.grid(row=2, column=0, padx=10, pady=0, sticky="e")
        surname_entry = ctk.CTkEntry(selection_frame, placeholder_text=f"{self.surname}", width=200, height=20, font=("Arial", 14))
        surname_entry.grid(row=2, column=1, padx=10, pady=0, sticky="w")
        surname_entry.configure(state="readonly")

        bdate_label = ctk.CTkLabel(selection_frame, text="Birth Date:", font=("Arial", 14))
        bdate_label.grid(row=3, column=0, padx=10, pady=0, sticky="e")
        bdate_entry = ctk.CTkEntry(selection_frame, placeholder_text=f"{self.bdate}", width=200, height=20, font=("Arial", 14))
        bdate_entry.grid(row=3, column=1, padx=10, pady=0, sticky="w")
        bdate_entry.configure(state="readonly")

        bplace_label = ctk.CTkLabel(selection_frame, text="Birth Place:", font=("Arial", 14))
        bplace_label.grid(row=4, column=0, padx=10, pady=0, sticky="e")
        bplace_entry = ctk.CTkEntry(selection_frame, placeholder_text=f"{self.bplace}", width=200, height=20, font=("Arial", 14))
        bplace_entry.grid(row=4, column=1, padx=10, pady=0, sticky="w")
        bplace_entry.configure(state="readonly")

        ssn_label = ctk.CTkLabel(selection_frame, text="Social Security Number: ", font=("Arial", 14))
        ssn_label.grid(row=5, column=0, padx=10, pady=0, sticky="e")
        ssn_entry = ctk.CTkEntry(selection_frame, placeholder_text=f"{self.ssn}", width=200, height=20, font=("Arial", 14))
        ssn_entry.grid(row=5, column=1, padx=10, pady=0, sticky="w")
        ssn_entry.configure(state="readonly")

        address_label = ctk.CTkLabel(selection_frame, text="", font=("Arial", 14))
        address_label.grid(row=6, column=0, padx=10, pady=0, sticky="e")
        self.address_entry = ctk.CTkEntry(selection_frame, placeholder_text="Insert new address", width=200, height=20, font=("Arial", 14))
        self.address_entry.grid(row=6, column=1, padx=10, pady=0, sticky="w")

        if self.user_role == "D":
            address_label.configure(text="Office Address: ", font=("Arial", 14))

            openingh_label = ctk.CTkLabel(selection_frame, text="Opening hour: ", font=("Arial", 14))
            openingh_label.grid(row=7, column=0, padx=10, pady=0, sticky="e")
            self.openingh_entry = ctk.CTkEntry(selection_frame, placeholder_text="HH:MM", width=200, height=20, font=("Arial", 14))
            self.openingh_entry.grid(row=7, column=1, padx=10, pady=0, sticky="w")

            closingh_label = ctk.CTkLabel(selection_frame, text="Closing hour: ", font=("Arial", 14))
            closingh_label.grid(row=8, column=0, padx=10, pady=0, sticky="e")
            self.closingh_entry = ctk.CTkEntry(selection_frame, placeholder_text="HH:MM", width=200, height=20, font=("Arial", 14))
            self.closingh_entry.grid(row=8, column=1, padx=10, pady=0, sticky="w")

        elif self.user_role == "P":
            address_label.configure(text="Residence Address: ", font=("Arial", 14))

            height_label = ctk.CTkLabel(selection_frame, text="Height: ", font=("Arial", 14))
            height_label.grid(row=7, column=0, padx=10, pady=0, sticky="e")
            self.height_entry = ctk.CTkEntry(selection_frame, placeholder_text="Insert new height in cm", width=200, height=20, font=("Arial", 14))
            self.height_entry.grid(row=7, column=1, padx=10, pady=0, sticky="w")

            weight_label = ctk.CTkLabel(selection_frame, text="Weight: ", font=("Arial", 14))
            weight_label.grid(row=8, column=0, padx=10, pady=0, sticky="e")
            self.weight_entry = ctk.CTkEntry(selection_frame, placeholder_text="Insert new weight in kg", width=200, height=20, font=("Arial", 14))
            self.weight_entry.grid(row=8, column=1, padx=10, pady=0, sticky="w")

        phone_label = ctk.CTkLabel(selection_frame, text="Phone Number: ", font=("Arial", 14))
        phone_label.grid(row=9, column=0, padx=10, pady=0, sticky="e")
        self.phone_entry = ctk.CTkEntry(selection_frame, placeholder_text="Insert new phone number", width=200, height=20, font=("Arial", 14))
        self.phone_entry.grid(row=9, column=1, padx=10, pady=0, sticky="w")

        email_label = ctk.CTkLabel(selection_frame, text="E-mail: ", font=("Arial", 14))
        email_label.grid(row=10, column=0, padx=10, pady=0, sticky="e")
        self.email_entry = ctk.CTkEntry(selection_frame, placeholder_text="Insert new email", width=200, height=20, font=("Arial", 14))
        self.email_entry.grid(row=10, column=1, padx=10, pady=0, sticky="w")

        pass_label = ctk.CTkLabel(selection_frame, text="Password: ", font=("Arial", 14))
        pass_label.grid(row=11, column=0, padx=10, pady=0, sticky="e")
        self.pass_entry = ctk.CTkEntry(selection_frame, placeholder_text="Insert new password", width=200, height=20, font=("Arial", 14), show='*')
        self.pass_entry.grid(row=11, column=1, padx=10, pady=0, sticky="w")

        # buttons: confirm and back
        button_frame = ctk.CTkFrame(self.profile_frame, fg_color="transparent")
        button_frame.place(relx=0.5, y=450, anchor="n")
        self.confirm_button = ctk.CTkButton(button_frame, text="Confirm", command=self.update_callback, width=250, fg_color=self.c_buttons, 
                                            hover_color=self.c_buttons_hoover, text_color=self.c_buttons_text)
        self.confirm_button.grid(row=0, column=1, padx=10, pady=0, sticky="w")

        self.back_button = ctk.CTkButton(button_frame, text="Back", command=self.personal_data, width=250, fg_color=self.c_buttons, 
                                         hover_color=self.c_buttons_hoover, text_color=self.c_buttons_text)
        self.back_button.grid(row=0, column=0, padx=10, pady=0, sticky="e")

        self.error_label = ctk.CTkLabel(self.profile_frame, text="", font=("Arial", 14))
        self.error_label.place(relx=0.5, y=460, anchor="n")

    # Update MyProfile
    def update_callback(self):

        # address:
        new_address = self.address_entry.get()
        if new_address!="": 
          if new_address != self.address:
            self.cursor.execute("UPDATE user SET Address = ? WHERE UserID = ?", (new_address, self.user))

        # business hours
        if self.user_role == "D":
            new_open = self.openingh_entry.get()
            if new_open!="":
                if new_open != self.openinghour:
                    self.cursor.execute("UPDATE doctors SET openinghour = ? WHERE doctorID = ?", (new_open, self.user))
            new_close = self.closingh_entry.get()
            if new_close!="":
                if new_close!=self.closinghour:
                    self.cursor.execute("UPDATE doctors SET closinghour = ? WHERE doctorID = ?", (new_close, self.user))

        # height and weight
        elif self.user_role == "P":
            new_height = self.height_entry.get()
            if new_height!="":
                if new_height!=self.height:
                    self.cursor.execute("UPDATE patient SET Height = ? WHERE UserID = ?", (new_height, self.user))
            new_weight = self.weight_entry.get()
            if new_weight!="":
                if new_weight!=self.weight:
                    self.cursor.execute("UPDATE patient SET Weight = ? WHERE UserID = ?", (new_weight, self.user))

        # phone number:
        new_phone = self.phone_entry.get()
        if new_phone!="": 
          if new_phone!=self.phone:
            self.cursor.execute("UPDATE user SET PhoneNumber = ? WHERE UserID = ?", (new_phone, self.user))

        # mail:
        new_mail = self.email_entry.get()
        if new_mail!="": 
          if new_mail!=self.mail:
            self.cursor.execute("UPDATE user SET Email = ? WHERE UserID = ?", (new_mail, self.user))

        flag = 1
        # password
        new_pass = self.pass_entry.get()
        if new_pass!="":
          if new_pass!=self.password: 
            self.cursor.execute("UPDATE user SET Password = ? WHERE UserID = ?", (new_pass, self.user))
            flag = 1
          else: 
            self.error_label.configure(text="Password cannot be the same as before!", text_color="red")
            flag = 0
        
        if flag:
            self.conn.commit()
            self.personal_data()
            self.outcome_label.configure(text="Data updated!", text_color="green")

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()        
    
    def logout(self):
        for widget in self.logout_frame.winfo_children():
            widget.destroy()

        logout_label = ctk.CTkLabel(self.logout_frame, text="Do you really want to logout?", font=("Arial",20), text_color=self.c_text) 
        logout_label.place(relx=0.5,rely=0.5, anchor="center")

        # Button frame
        button_frame = ctk.CTkFrame(self.logout_frame, fg_color="transparent")
        button_frame.place(relx=0.5, y=360, anchor="n")
        # Bottone "confirm"
        self.confirm_logout_button = ctk.CTkButton(button_frame, text="Yes", command=self.confirmlogout_callback, fg_color=self.c_buttons, 
                                                   hover_color=self.c_buttons_hoover, text_color=self.c_buttons_text, width=250)
        self.confirm_logout_button.grid(row=0, column=0, padx=10, pady=0, sticky="e")
        # Bottone "deny"
        self.deny_logout_button = ctk.CTkButton(button_frame, text="No", command=self.denylogout_callback, fg_color=self.c_buttons, 
                                                hover_color=self.c_buttons_hoover, text_color=self.c_buttons_text, width=250)
        self.deny_logout_button.grid(row=0, column=1, padx=10, pady=0, sticky="w")


    def confirmlogout_callback(self):
        self.Login_gui()

    def denylogout_callback(self):
        self.select_frame_by_name("home")

    def close(self):
        self.conn.close()
    



      


if __name__ == "__main__":
    app = App()
    app.root.mainloop()
