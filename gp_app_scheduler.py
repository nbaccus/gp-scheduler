#!/usr/bin/env python3

"""
Created on 13/04/21

@author: nbaccus

This program allows patients and doctors to either log into the system,
or add themselves if they don't exist. They can view and make appointments,
up to one month in advance. (Doctors can only view their appointments.)

"""

from datetime import datetime
from datetime import timedelta
from datetime import date
import gp_database
from tkcalendar import DateEntry
from tkinter import constants
from tkinter import messagebox
try:
    import tkinter as tk
except:
    import Tkinter as tk

try:
    from tkinter import ttk

except:
    import ttk

# ----global variables needed----

test_variable = "On"
patient_identification = ""
user_type = ""
dr_identification = ""

# ----database credentials----
db_hostname = "localhost"
db_username = "root"
db_password = ""

# ==================== miscellaneous functions ====================
# =================================================================

def raise_frame(frame):
    """
    raises a frame to the top of a tkinter window
    :param frame: frame to be raised
    :return: nothing
    """
    frame.tkraise()


def create_frames(frames_dict, num_of_frames):
    """
    generates x number of frames

    :param frames_dict: empty dictionary to contain frames
    :param num_of_frames: x number of frames to generate
    :return: frame dictionary
    :rtype: dictionary
    """
   
    if frames_dict is None:
        frames_dict = {}
    for i in range(1, num_of_frames+1):
        # creates frames for each page
        frame_name = "f"+str(i)
        frame = tk.Frame(root)
        frames_dict[frame_name] = frame
        frame.grid(row=0, column=0, sticky="nsew")


def create_time_slots(time_slots):
    """
    Creates a list of time slots from 9:00 to 17:00, excluding 13:00-14:00,
    with duration 15 minutes.
    :param time_slots : empty list to contain time slots
    :return: time_slots
    :rtype: list
    """
  
    if time_slots is None:
        time_slots = []
    opening_time = datetime.today().replace(hour=9, minute=0)
    closing_time = opening_time + timedelta(hours=8)
    current_time = opening_time

    while current_time <= closing_time:
        time_slots.append(datetime.strftime(current_time, '%H:%M'))
        current_time = current_time + timedelta(minutes=15)
    remove_time = ['13:00', '13:15', '13:30', '13:45']
    for time in remove_time:
        time_slots.remove(time)
    return time_slots


def get_details(details_dict, name, dob, postcode, person_type ):
    """
    Stores user details from tkinter button
    :param details_dict: empty dictionary to contain user details
    :param name: name of person
    :param dob: date of birth
    :type dob: datetime object
    :param postcode: postcode
    :param person_type: 0 for doctors, 1 for patients
    :type person_type: int
    :return: dictionary with user details
    """

    if details_dict is None:
        details_dict = {}
    details_dict["name"] = name.title()
    details_dict["dob"] = dob
    details_dict["postcode"] = postcode.upper().replace(" ", "")
    details_dict["person_type"] = person_type
    global patient_identification
    global user_type
    global dr_identification
    user_type = 0

    try:
        mydb = gp_database.connect_to_database("localhost", "root", "", "gp_practice")
        person_ID = gp_database.get_person_ID(mydb, details_dict["name"], details_dict["dob"], details_dict["postcode"],
                                              details_dict["person_type"])
        if person_type == 1:
            user_type = 1
            patient_identification = person_ID
        else:
            dr_identification=person_ID
    except:
        messagebox.showerror("Error", "Details entered for user are incorrect. Please go back and re-enter.")

    return details_dict


def get_app_details(date, doctor, time):
    """
    Stores info when user is making a new appointment.
    :param date: date of app
    :param doctor: preferred doctor
    :param time: time of app
    :return: dictionary with app details
    """
    global app_info
    app_info = {'time': time, 'date': date, 'doctor': doctor}


def convert_date(appointment_date):
    """
    convert datetime object to string
    :param appointment_date: date to be converted
    :return: date as string
    """
    appointment = datetime.strftime(appointment_date, '%d %A %Y at %H:%M')
    return appointment


# ==================== database functions ====================
# ============================================================

def view_app(frame, backframe, details):
    """
    Retrieves appointments from database for user and prints on screen.
    Throws error box if user details are incorrect.
    :param frame : current frame
    :param backframe : previous frame
    :param details : non empty dictionary containing user name, dob, postcode and person_type"""


    try:
        mydb = gp_database.connect_to_database(db_hostname, db_username, db_password, "gp_practice")
        person_ID = gp_database.get_person_ID(mydb, details["name"], details["dob"], details["postcode"], details["person_type"])
        msg, app_list, staff_id_list, patient_id_list = gp_database.get_my_appointments(mydb, details["person_type"], person_ID)
        staff_name = []
        patient_name = []

        for i in range(0,len(staff_id_list)):
            staff_id = staff_id_list[i]
            patient_id = patient_id_list[i]
            staff_name.append(gp_database.get_person_info(mydb, staff_id)[0][0])
            patient_name.append(gp_database.get_person_info(mydb, patient_id)[0][0])
        mydb.close()

        for widget in frame.winfo_children():
            widget.destroy()
        view_app_label = tk.Text(frame, bg="gainsboro")
        view_app_label.pack()
        view_app_label.configure(font=("Arial", 12))
        view_app_label.config(state=tk.NORMAL)
        view_app_label.insert(constants.INSERT, msg + "\n")
        if len(app_list) != 0:
            for i in range(0, len(app_list)):
                app_time = convert_date(app_list[i])
                view_app_label.insert(constants.INSERT, app_time + " - Dr."+staff_name[i]+" with "+patient_name[i] + "\n")
        view_app_label.see(constants.INSERT)
        view_app_label.config(state=tk.DISABLED)
        tk.Button(frame, text="Go back", command=lambda: raise_frame(backframe)).pack()
    except:
        messagebox.showerror("Error", "Details entered for user are incorrect. Please go back and re-enter.")


def add_new_person_to_db(details):
    """
    Adds new user to database. Throws error if user already exists.
    :param details : non empty list of user details written by get_details and determine_person
    """
    try:
        mydb = gp_database.connect_to_database(db_hostname, db_username, db_password, "gp_practice")
        gp_database.add_appointee(mydb, details["name"], details["dob"], details["postcode"], details["person_type"])
        mydb.close()
    except:
        messagebox.showerror("Error", "This user already exists.")


def get_available_doctors(date, time, available_doctors):
    """
    Returns a dictionary of doctors who are available for an appointment based on user-selected time and date.
    Gets information from make_appointment_page_date
    :param date: specified date of appointment
    :param time: specified time of appointment
    :parma available_doctors: empty list to contain result
    :return: available_doctors. key=doctor name, value=doctor ID
    :rtype: dictionary
    """
    date = datetime.strptime(date,"%d/%m/%Y").date()
    time = datetime.strptime(time,'%H:%M').time()
    time_slot = datetime.combine(date,time)
    mydb = gp_database.connect_to_database(db_hostname, db_username, db_password, "gp_practice")
    doctors = gp_database.view_appointees(mydb, 0)
    if available_doctors is None:
        available_doctors = {}
    for person in doctors:
        if gp_database.check_availability(mydb,time_slot,person[0]):
            available_doctors[person[1]] = person[0]
    mydb.close()
    return available_doctors


# ==================== tkinter functions ====================
# ===========================================================

def main_menu(frame, nextframe1, nextframe2):
    """
    Main menu when tkinter window is opened.
    :param frame= current frame
    :param nextframe1 = frame for existing user
    :param nextframe2 = frame for non-existing user """
    tk.Label(frame, text="Welcome!", font=("Arial", 12, 'bold')).pack()
    tk.Label(frame, text="Are you an existing patient/doctor?").pack()
    tk.Button(frame, text="Yes", command=lambda: raise_frame(nextframe1)).pack()
    tk.Button(frame, text="No", command=lambda: raise_frame(nextframe2)).pack()


def add_new_person_page(frame, nextframe1, backframe):
    """
    asks user to add their details
    :param frame: current frame
    :param nextframe1: next frame
    :param backframe : previous frame to main menu
    """
    tk.Label(frame, text="Would you like to add your details?").pack()
    tk.Button(frame, text="Continue", command=lambda: raise_frame(nextframe1)).pack()
    tk.Button(frame, text="Go back to main menu", command=lambda: raise_frame(backframe)).pack()


def print_my_var(eventobj):
    global drop_down_time
    drop_down_time = eventobj


def make_appointment_page_date(frame, nextframe, nextframe2, nextframe3,  backframe):
    """
    Asks user to enter details for a new appointment. Once entered, asks user to
    select an available doctor and submit.
    :param frame: current frame
    :param nextframe: next frame - choose preferred doctor
    :param nextframe2: frame for checking details of appointment
    :param nextframe3: frame for confirmation of appointment
    :param backframe: main menu
    """
    tk.Label(frame, text="Please choose a date.").pack()
    cal = DateEntry(frame, locale = "en_UK", date_pattern = "dd/mm/yyyy", showweeknumbers=False, font="Arial 10", width=12, background='grey',
                    foreground='white', borderwidth=2, mindate=date.today(), maxdate=date.today() + timedelta(365/12))
    cal.pack(padx=10, pady=10)
    tk.Label(frame, text="Choose appointment time.").pack()
    time_slots = []
    create_time_slots(time_slots)
    default_text = tk.StringVar(frame)
    default_text.set("Select time:")
    app_time = tk.OptionMenu(frame, default_text, *time_slots, command= print_my_var)
    app_time.pack()
    tk.Button(frame, text="Submit", command=lambda: [get_app_details(cal.get(),"", drop_down_time)
        ,preferred_doctor(nextframe, nextframe2, nextframe3,frame, backframe), raise_frame(nextframe)]).pack()

    tk.Button(frame, text="Go back to main menu", command=lambda: raise_frame(backframe)).pack()


def preferred_doctor(frame, nextframe, nextframe2, backframe, mainmenuframe):
    """
    Displays a drop down list of available doctors, if any, based on user selected
    appointment time.

    :param frame: current frame
    :param nextframe: next frame to view appointment details before submitting
    :param nextframe2: frame to confirm appointment
    :param backframe: frame to go back and re-enter details
    :param mainmenuframe: main menu frame
    """
    for widget in frame.winfo_children():
        widget.destroy()
    dr_dict={}
    get_available_doctors(app_info["date"], app_info["time"], dr_dict)
    dr_names=list(dr_dict.keys())

    label = tk.Label(frame, text="The available doctors for your chosen time slot are:")
    label.pack()
    default_text = tk.StringVar(frame)
    default_text.set("Select")
    try:
        dr_pref = tk.OptionMenu(frame, default_text, *dr_names)
        dr_pref.pack()

        tk.Button(frame, text="Submit",
                  command=lambda: [confirm_add_appointment(nextframe, nextframe2, frame, mainmenuframe, default_text.get(), dr_dict), raise_frame(nextframe)]).pack()
    except:
        msg='There are no available doctors'
        tk.Label(frame, text=msg).pack()

    button = tk.Button(frame, text="Go back", command=lambda: raise_frame(backframe))
    button.pack()


def confirm_add_appointment(frame,nextframe, backframe, mainmenuframe, dr_name,dr_dict):
    """
    Page to show user the new appointment details before submitting.
    :param frame: current frame
    :param nextframe: next frame to show confirmation and make appointment
    :param backframe: back frame to change preferred doctor
    :param mainmenuframe: main menu frame
    :param dr_name: Name of chosen doctor
    :param dr_dict: popluated dictionary containing all doctor IDs and corresponding names
    """
    for widget in frame.winfo_children():
        widget.destroy()
    app_info['doctor'] = dr_name
    app_info['doctor ID'] = dr_dict[dr_name]
    confirm_app_label = tk.Text(frame, bg="gainsboro")
    confirm_app_label.pack()
    confirm_app_label.configure(font=("Arial", 12))
    confirm_app_label.config(state=tk.NORMAL)
    confirm_app_label.insert(constants.INSERT, "Your appointment details are:" + "\n")
    for key,value in app_info.items():
        msg= key.title()+" : "+str(value)
        if key != 'doctor ID':
            confirm_app_label.insert(constants.INSERT, msg + "\n")
    confirm_app_label.insert(constants.INSERT, "Are these details correct?" + "\n")
    confirm_app_label.see(constants.INSERT)
    confirm_app_label.config(state=tk.DISABLED)

    tk.Button(frame, text="Confirm", command=lambda: [add_appointment_to_db(nextframe, mainmenuframe),raise_frame(nextframe)]).pack()
    tk.Button(frame, text="Go back", command=lambda: raise_frame(backframe)).pack()

def add_appointment_to_db(frame, mainmenuframe):
    """
    Adds new appointment to database. Throws error if user is a doctor - doctors cannot book
    appointments with another doctor currently.
    :param frame: current frame
    :param mainmenuframe: main menu frame
    """
    mydb = gp_database.connect_to_database("localhost", "root", "", "gp_practice")
    global patient_identification

    if dr_identification != "":
        messagebox.showerror("Error", "You cannot book an appointment with another doctor.")
    try:
        patient_ID = patient_identification
        date = datetime.strptime(app_info['date'], "%d/%m/%Y").date()
        time = datetime.strptime(app_info['time'], '%H:%M').time()
        time_slot = datetime.combine(date, time)
        gp_database.add_appointments(mydb, time_slot, app_info['doctor ID'], patient_ID)
        for widget in frame.winfo_children():
            widget.destroy()
        tk.Label(frame, text="Appointment added! Thank you.").pack()
        tk.Button(frame, text="Main Menu", command=lambda: raise_frame(mainmenuframe)).pack()
    except:
        messagebox.showerror("Error", "You cannot book an appointment with another doctor.")



def determine_person(frame, backframe, nextframe2, details, exists):
    """
    Gets user details. Depending on if user exists, directs to different frames.
    :param frame: current frame
    :param backframe: previous frame (main menu)
    :param nextframe2: next frame if user exists
    :param details: empty dictionary to store user details
    :param exists: True if user exists
    :type exists: boolean
    """

    tk.Label(frame, text="Please enter your details and press submit").pack()

    tk.Label(frame, text="Are you a patient?").pack()
    var = tk.IntVar()
    tk.Checkbutton(frame,text="Yes", variable=var).pack()

    tk.Label(frame, text="What is your postcode?").pack()
    inputpostcode = tk.Entry(frame)
    inputpostcode.pack()

    tk.Label(frame, text="What is your name?").pack()
    inputname=tk.Entry(frame)
    inputname.pack()

    tk.Label(frame, text="What is your date of birth?").pack()
    cal = DateEntry(frame, locale="en_UK", date_pattern="dd/mm/yyyy",showweeknumbers=False, font="Arial 10", width=12, background='grey',
                    foreground='white', borderwidth=2, maxdate=date.today())
    cal.pack(padx=10, pady=10)
    if exists:
        tk.Button(frame, text="Submit", command=lambda: [
            get_details(details, inputname.get(), cal.get_date(), inputpostcode.get(), var.get()),
            raise_frame(nextframe2)]).pack()
    else:
      tk.Button(frame, text="Submit", command= lambda: [add_new_person_to_db(get_details(details,
                                                          inputname.get(),cal.get_date(), inputpostcode.get(),var.get())), raise_frame(nextframe2)]).pack()

    tk.Button(frame, text="Go back to main menu", command=lambda: raise_frame(backframe)).pack()
    inputpostcode.delete(0, constants.END)
    inputname.delete(0,constants.END)


def submit_confirmation(frame, backframe, exists,  nextframe=None,):
    """
    frame to confirm that user has submitted details.
    :param frame: current frame
    :param backframe: main menu frame
    :param exists: True if user exists in database
    :param nextframe: None if user exists
    """
    tk.Label(frame, text="Information submitted. Thank you").pack()
    if exists and nextframe is not None:
        tk.Button(frame, text="Continue", command=lambda: raise_frame(nextframe)).pack()
    tk.Button(frame, text="Go back to main menu", command=lambda: raise_frame(backframe)).pack()


def person_menu(frame, nextframe1, nextframe2, backframe):
    """
    Main menu once user is logged in
    :param frame: current frame
    :param nextframe1: next frame to view appointments
    :param nextframe2: next frame to make appointments
    :param backframe: main menu frame
    """
    tk.Label(frame, text="Appointments menu").pack()
    tk.Button(frame, text="View appointments", command= lambda: [view_app(nextframe1, frame, details), raise_frame(nextframe1)]).pack()
    tk.Button(frame, text="Make an appointment", command= lambda: raise_frame(nextframe2)).pack()
    tk.Button(frame, text="Go back to main menu", command= lambda: raise_frame(backframe)).pack()


# ==================== script ====================
# ================================================
frames = {}
details = {}
app_info = {}

# create tkinter window and frames
root = tk.Tk()
create_frames(frames, 12)

main_menu(frames["f1"], frames["f2"], frames["f3"])

# adds new person
add_new_person_page(frames["f3"], frames["f4"], frames["f1"])
determine_person(frames["f4"],frames["f1"], frames["f5"], details, False)
submit_confirmation(frames["f5"], frames["f1"],False)

# gets existing user details and brings up menu
determine_person(frames["f2"], frames["f1"], frames["f6"], details, True)
submit_confirmation(frames["f6"], frames["f1"], True, frames["f7"])
person_menu(frames["f7"], frames["f8"], frames["f9"], frames["f1"])
make_appointment_page_date(frames["f9"], frames["f10"], frames["f11"], frames["f12"], frames["f1"])

# bring up main menu and start tkinter window
raise_frame(frames["f1"])
root.mainloop()
