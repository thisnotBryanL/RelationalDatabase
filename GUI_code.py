import mysql.connector
import tkinter as tk
from User_Inputed_Data import *

def firstPage(mycursor, mydb):
    HEIGHT = 700
    WIDTH = 800

    #root window
    root = tk.Tk()

    canvas = tk.Canvas(root, height = HEIGHT, width = WIDTH)
    canvas.pack()

    #add background image
    bgImage = tk.PhotoImage(file = 'background5.png')
    bgLabel = tk.Label(root, image = bgImage)
    bgLabel.place(relwidth = 1, relheight = 1)

    #set up upper frame
    upperFrame = tk.Frame(root, bg = 'white', bd = 10, highlightbackground="#fbe1f2", highlightcolor="#fbe1f2", highlightthickness=5)
    upperFrame.place(relx = .1, rely = .05, relwidth = .8, relheight = .075)
    headerLabel = tk.Label(upperFrame, text = 'Student Information', font = 60)
    headerLabel.place(relx = .4, rely = .2)

    #set up middle frame
    middleFrame = tk.Frame(root, bg = 'white', bd = 10, highlightbackground="#fbe1f2", highlightcolor="#fbe1f2", highlightthickness=5)
    middleFrame.place(relx = .1, rely = .15, relwidth = .8, relheight = .6)

    #Get student ID
    idLabel = tk.Label(middleFrame, text = "Student ID", bg = '#e1fbfa' )
    idLabel.place(anchor = "w", relx = 0, rely = .1, relwidth = .30)
    idEntry = tk.Entry(middleFrame, bg = 'white')
    idEntry.place(anchor = "w", relx = .30, rely = .1, relwidth = .30)

    #Get last name
    lastnameLabel = tk.Label(middleFrame, text = "Last Name", bg = '#e1fbfa' )
    lastnameLabel.place(anchor = "w", relx = 0, rely = .2, relwidth = .30)
    lastnameEntry = tk.Entry(middleFrame, bg = 'white')
    lastnameEntry.place(anchor = "w", relx = .30, rely = .2, relwidth = .30)

    #Get first name
    firstnameLabel = tk.Label(middleFrame, text = "First Name", bg = '#e1fbfa' )
    firstnameLabel.place(anchor = "w", relx = 0, rely = .3, relwidth = .30)
    firstnameEntry = tk.Entry(middleFrame, bg = 'white')
    firstnameEntry.place(anchor = "w", relx = .30, rely = .3, relwidth = .30)

    #Get email address
    emailLabel = tk.Label(middleFrame, text = "Email Address", bg = '#e1fbfa' )
    emailLabel.place(anchor = "w", relx = 0, rely = .4, relwidth = .30)
    emailEntry = tk.Entry(middleFrame, bg = 'white')
    emailEntry.place(anchor = "w", relx = .30, rely = .4, relwidth = .30)

    #Get semester entering the program
    semesterLabel = tk.Label(middleFrame, text = "Semester Entering Program", bg = '#e1fbfa' )
    semesterLabel.place(anchor = "w", relx = 0, rely = .5, relwidth = .30)
    semesterEntry = tk.Entry(middleFrame, bg = 'white')
    semesterEntry.place(anchor = "w", relx = .3002, rely = .5, relwidth = .3)

    #Allow user to submit information, lambda is defined at runtime, redefines button each time it is clicked to get current
    #state of textbox
    button = tk.Button (middleFrame, text = "Submit", bg = 'red', fg = 'gray', font = 60,
                        command = lambda: insertIntoStudentInfo(idEntry.get(), lastnameEntry.get(), firstnameEntry.get(), emailEntry.get(), semesterEntry.get(), mycursor, mydb, middleFrame,
                                                                upperFrame))



    button.place (anchor = 's', rely = .8, relx = .5)

    #delete canvas then create new one



    root.mainloop()