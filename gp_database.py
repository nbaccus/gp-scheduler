#!/usr/bin/env python3

"""
Created on 13/04/21

@author: nbaccus

Collection of functions to access and manipulate GP database
of patients/doctors and appointments. To be used with gp_app_scheduler

"""

import mysql.connector


def add_appointee(mydb, name, dob, postcode, person_type):
    """ ====== Adds current person into database ====== """
    my_cursor0 = mydb.cursor()
    my_cursor0.execute("SELECT * FROM appointees WHERE APPname = %s AND APPdob = %s "
                       "AND APPpostcode = %s", (name, dob, postcode))
    if my_cursor0.fetchone() is None:
        my_cursor = mydb.cursor()
        query = "INSERT INTO appointees (APPname, APPtype, APPdob, APPpostcode) VALUES ( %s, %s, %s, %s)"
        val = (str(name), person_type, dob, postcode)
        my_cursor.execute(query, val)
        print(my_cursor.rowcount, "record inserted.")
        my_cursor.close()
    else:
        print("Appointee already exists.")
        raise Exception("User already exists")
    my_cursor0.close()
    mydb.commit()


def add_appointments(mydb, date, doctorID, patientID):
    if check_availability(mydb, date, doctorID, patientID):
        my_cursor=mydb.cursor()
        query = "INSERT INTO appointments (APMdate, APMstaff, APMpatient) VALUES (%s, %s, %s)"
        values = (date, doctorID, patientID)
        my_cursor.execute(query, values)
        print(my_cursor.rowcount, "appointment inserted.")
        my_cursor.close()


def get_person_ID(mydb, name, dob, postcode, person_type):
    my_cursor = mydb.cursor()
    query = "SELECT APPID FROM appointees WHERE APPname=%s AND APPdob=%s AND APPpostcode=%s AND APPtype=%s"
    values = (name, dob, postcode, person_type)
    my_cursor.execute(query, values)
    my_result = my_cursor.fetchone()[0]
    my_cursor.close()
    return my_result


def get_person_info(mydb, person_id):
    my_cursor=mydb.cursor()
    query="SELECT APPname, APPdob, APPpostcode, APPtype FROM appointees where APPID="+str(person_id)
    my_cursor.execute(query)
    my_result=my_cursor.fetchall()
    result_list=[]
    for result in my_result:
        result_list.append(result)
    my_cursor.close()
    return result_list


def view_appointments(mydb):

    # ====== Prints the appointments database ======
    my_cursor = mydb.cursor()
    my_cursor.execute("SElECT * FROM appointments")
    my_result = my_cursor.fetchall()
    for result in my_result:
        print(result)

    my_cursor.close()


def view_appointees(mydb, person_type):

    # ====== returns the appointees table as a list of tuples, by person_type (doctor=0, patient=1) ======
    my_cursor = mydb.cursor()
    query="SElECT * FROM appointees where APPtype ="+str(person_type)
    my_cursor.execute(query)
    my_result = my_cursor.fetchall()
    print([i[0] for i in my_cursor.description])
    result_list = []
    for result in my_result:
        row = ()
        for item in result:
            row += (str(item),)
        result_list.append(row)
    my_cursor.close()
    return result_list


def check_availability(mydb, date, doctor_ID, patient_ID=False):
    # checks if time slot (date) is available with a particular doctor.
    # if patient ID is provided, checks if patient and doctor are both available.
    if not patient_ID:
        my_cursor2 = mydb.cursor()
        query = "SELECT * FROM appointments WHERE APMdate= %s AND APMstaff = %s"
        values = (date, doctor_ID)
        my_cursor2.execute(query, values)
        result2 = my_cursor2.fetchone()
        my_cursor2.close()
        if result2 is None:
            print("Time slot is available.")
            return True
        else:
            print("Time slot is not available.")
    else:
        my_cursor = mydb.cursor()
        query = "SELECT * FROM appointments WHERE APMdate= %s AND APMstaff = %s AND APMpatient = %s"
        values = (date, doctor_ID, patient_ID)
        my_cursor.execute(query, values)
        result = my_cursor.fetchone()
        my_cursor.close()
        if result is None:
            print("Time slot is available.")
            return True
        else:
            print("Time slot is not available.")
    return False


def get_my_appointments(mydb, person_type, person_ID):
    # Retrieves a doctor's or patient's appointment list
    my_cursor = mydb.cursor()
    if person_type == 0:
        col = "APMstaff"
    else:
        col = "APMpatient"
    query = "SELECT * FROM appointments where "+col+"="+str(person_ID)
    my_cursor.execute(query)
    my_result = my_cursor.fetchall()
    app_date = []

    staff_id = []
    patient_id = []
    if my_cursor.rowcount < 1:
        msg = "You currently have no appointments booked"
    else:
        msg = "Your appointment dates are:"

        for result in my_result:
            app_date.append(result[1])
            staff_id.append(result[2])
            patient_id.append(result[3])


    my_cursor.close()
    return msg, app_date, staff_id, patient_id


def connect_to_database(hostname, user, password, database):
    # connects to database
    try:
        mydb = mysql.connector.connect(
            host=str(hostname),
            user=str(user),
            password=str(password),
            database=str(database)
        )
        print("Database connected successfully")
        return mydb
    except:
        print("Database not connected")

