# gp-scheduler
Patient/GP login GUI
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
![gp_app_scheduler_screenshot1](https://user-images.githubusercontent.com/80896538/114599337-df420d80-9c8a-11eb-8bed-09dfcaeac12b.jpg)
![gp_app_scheduler_screenshot3](https://user-images.githubusercontent.com/80896538/114599425-fb45af00-9c8a-11eb-81d8-b61efd5aed85.jpg)



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

