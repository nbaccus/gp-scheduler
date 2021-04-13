# gp-scheduler
small project to design an patient/gp login GUI
=======================
Files inluded:
gp_app_scheduler.py
gp_database.py
gp_pratice.sql

=======================

1) gp_app_scheduler.py creates GUI for a user (doctor or 
patient) to log in/add themselves to GP system. They can 
view and make appointments. Uses gp_database module which 
contains functions to access the GP database.

2) The database in the code is on a local server and you 
will need to replace the host name, username and password. 
The database is gp_practice.sql
3) Modules that need to be installed separately:
	tkcalendar
	mysqlconnector

4) Once the above is installed, to execute program run 
gp_app_scheduler.py.

=======================

(This program was inspired by a prompt (found below) and 
modifiying: 
https://github.com/karan/Projects#classes

"Patient / Doctor Scheduler - Create a patient class and a 
doctor class. Have a doctor that can handle multiple 
patients and setup a scheduling program where a doctor can 
only handle 16 patients during an 8 hr work day." )

