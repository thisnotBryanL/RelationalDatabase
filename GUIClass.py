import mysql.connector
import tkinter as tk
from User_Inputed_Data import *

class PageOne:
    def destoryWindow(self, mycursor, mydb):
        self.upperFrame.destroy()
        self.middleFrame.destroy()
        #open next window
        PageTwo.__init__(self, mycursor, mydb)

    def __init__(self, mycursor, mydb):
        self.HEIGHT = 700
        self.WIDTH = 800

        # root window
        self.root = tk.Tk()

        self.canvas = tk.Canvas(self.root, height=self.HEIGHT, width=self.WIDTH)
        self.canvas.pack()

        #add background image
        self.bgImage = tk.PhotoImage(file = 'background5.png')
        self.bgLabel = tk.Label(self.root, image = self.bgImage)
        self.bgLabel.place(relwidth = 1, relheight = 1)

        #set up upper frame
        self.upperFrame = tk.Frame(self.root, bg = 'white', bd = 10, highlightbackground="#fbe1f2", highlightcolor="#fbe1f2", highlightthickness=5)
        self.upperFrame.place(relx = .1, rely = .05, relwidth = .8, relheight = .075)
        self.headerLabel = tk.Label(self.upperFrame, text = 'Student Information', font = 60)
        self.headerLabel.place(relx = .4, rely = .2)

        #set up middle frame
        self.middleFrame = tk.Frame(self.root, bg = 'white', bd = 10, highlightbackground="#fbe1f2", highlightcolor="#fbe1f2", highlightthickness=5)
        self.middleFrame.place(relx = .1, rely = .15, relwidth = .8, relheight = .6)

        #Get student ID
        self.idLabel = tk.Label(self.middleFrame, text = "Student ID", bg = '#e1fbfa' )
        self.idLabel.place(anchor = "w", relx = 0, rely = .1, relwidth = .30)
        self.idEntry = tk.Entry(self.middleFrame, bg = 'white')
        self.idEntry.place(anchor = "w", relx = .30, rely = .1, relwidth = .30)

        #Get last name
        self.lastnameLabel = tk.Label(self.middleFrame, text = "Last Name", bg = '#e1fbfa' )
        self.lastnameLabel.place(anchor = "w", relx = 0, rely = .3, relwidth = .30)
        self.lastnameEntry = tk.Entry(self.middleFrame, bg = 'white')
        self.lastnameEntry.place(anchor = "w", relx = .30, rely = .3, relwidth = .30)

        #Get first name
        self.firstnameLabel = tk.Label(self.middleFrame, text = "First Name", bg = '#e1fbfa' )
        self.firstnameLabel.place(anchor = "w", relx = 0, rely = .2, relwidth = .30)
        self.firstnameEntry = tk.Entry(self.middleFrame, bg = 'white')
        self.firstnameEntry.place(anchor = "w", relx = .30, rely = .2, relwidth = .30)

        #Get email address
        self.emailLabel = tk.Label(self.middleFrame, text = "Email Address", bg = '#e1fbfa' )
        self.emailLabel.place(anchor = "w", relx = 0, rely = .4, relwidth = .30)
        self.emailEntry = tk.Entry(self.middleFrame, bg = 'white')
        self.emailEntry.place(anchor = "w", relx = .30, rely = .4, relwidth = .30)


        #Get semester entering the program
        self.semesterLabel = tk.Label(self.middleFrame, text = "Semester Entering Program", bg = '#e1fbfa' )
        self.semesterLabel.place(anchor = "w", relx = 0, rely = .5, relwidth = .30)
        self.semesterEntry = tk.Entry(self.middleFrame, bg = 'white')
        self.semesterEntry.place(anchor = "w", relx = .3002, rely = .5, relwidth = .30)

        #Get Year
        self.yearLabel = tk.Label(self.middleFrame, text = "Year", bg = '#e1fbfa' )
        self.yearLabel.place(anchor = "w", relx = 0, rely = .6, relwidth = .30)
        self.yearEntry = tk.Entry(self.middleFrame, bg = 'white')
        self.yearEntry.place(anchor = "w", relx = .30, rely = .6, relwidth = .30)

        #Get class
        self.classLabel = tk.Label(self.middleFrame, text = "Class", bg = '#e1fbfa' )
        self.classLabel.place(anchor = "w", relx = 0, rely = .7, relwidth = .30)
        self.classEntry = tk.Entry(self.middleFrame, bg = 'white')
        self.classEntry.place(anchor = "w", relx = .30, rely = .7, relwidth = .30)

        #Get major or minor
        self.majorminorLabel = tk.Label(self.middleFrame, text = "Major or Minor", bg = '#e1fbfa' )
        self.majorminorLabel.place(anchor = "w", relx = 0, rely = .8, relwidth = .30)
        self.majorminorEntry = tk.Entry(self.middleFrame, bg = 'white')
        self.majorminorEntry.place(anchor = "w", relx = .30, rely = .8, relwidth = .30)

        #Get Grade
        self.gradeLabel = tk.Label(self.middleFrame, text = "Grade in Class", bg = '#e1fbfa' )
        self.gradeLabel.place(anchor = "w", relx = 0, rely = .9, relwidth = .30)
        self.gradeEntry = tk.Entry(self.middleFrame, bg = 'white')
        self.gradeEntry.place(anchor = "w", relx = .30, rely = .9, relwidth = .30)


        #Allow user to submit information, lambda is defined at runtime, redefines button each time it is clicked to get current
        #state of textbox
        self.button = tk.Button (self.middleFrame, text = "Submit", bg = 'red', fg = 'gray', font = 60,
                            command = lambda: [insertIntoStudentInfo(self.idEntry.get(), self.lastnameEntry.get(), self.firstnameEntry.get(), self.emailEntry.get(),
                                                            self.semesterEntry.get(), self.classEntry.get(), self.majorminorEntry.get(), self.gradeEntry.get(),
                                                                     self.yearEntry.get(), mycursor, mydb, self.middleFrame, self.upperFrame), self.destoryWindow(mycursor, mydb)])

        self.button.place (anchor = 's', rely = 1, relx = .5)

        self.root.mainloop()


class PageTwo:
    def destoryWindow(self, mycursor, mydb):
        self.upperFrame.destroy()
        self.middleFrame.destroy()
        #open next window

    #The window, background, and frames have been set up by the the first page, simply add internship information
    def __init__(self, mycursor, mydb):
        # set up upper frame
        self.upperFrame = tk.Frame(self.root, bg='white', bd=10, highlightbackground="#fbe1f2",
                                   highlightcolor="#fbe1f2", highlightthickness=5)
        self.upperFrame.place(relx=.1, rely=.05, relwidth=.8, relheight=.075)
        self.headerLabel = tk.Label(self.upperFrame, text='Internship', font=100)
        self.headerLabel.place(relx=.4, rely=.2)

        # set up middle frame
        self.middleFrame = tk.Frame(self.root, bg='white', bd=10, highlightbackground="#fbe1f2",
                                    highlightcolor="#fbe1f2", highlightthickness=5)
        self.middleFrame.place(relx=.1, rely=.15, relwidth=.8, relheight=.6)

        # Get company
        self.companyLabel = tk.Label(self.middleFrame, text="Company", bg='#e1fbfa')
        self.companyLabel.place(anchor="w", relx=0, rely=.05, relwidth=.30)
        self.companyEntry = tk.Entry(self.middleFrame, bg='white')
        self.companyEntry.place(anchor="w", relx=.30, rely=.05, relwidth=.30)

        # Get start month
        self.startmoLabel = tk.Label(self.middleFrame, text="Start Month", bg='#e1fbfa')
        self.startmoLabel.place(anchor="w", relx=0, rely=.14, relwidth=.30)
        self.startmoEntry = tk.Entry(self.middleFrame, bg='white')
        self.startmoEntry.place(anchor="w", relx=.30, rely=.14, relwidth=.30)

        # Get start year
        self.startyrLabel = tk.Label(self.middleFrame, text="Start Year", bg='#e1fbfa')
        self.startyrLabel.place(anchor="w", relx=0, rely=.23, relwidth=.30)
        self.startyrEntry = tk.Entry(self.middleFrame, bg='white')
        self.startyrEntry.place(anchor="w", relx=.30, rely=.23, relwidth=.30)

        # Get end month
        self.endmoLabel = tk.Label(self.middleFrame, text="End Month", bg='#e1fbfa')
        self.endmoLabel.place(anchor="w", relx=0, rely=.32, relwidth=.30)
        self.endmoEntry = tk.Entry(self.middleFrame, bg='white')
        self.endmoEntry.place(anchor="w", relx=.30, rely=.32, relwidth=.30)

        # Get end year
        self.endyrLabel = tk.Label(self.middleFrame, text="End Year", bg='#e1fbfa')
        self.endyrLabel.place(anchor="w", relx=0, rely=.41, relwidth=.30)
        self.endyrEntry = tk.Entry(self.middleFrame, bg='white')
        self.endyrEntry.place(anchor="w", relx=.3002, rely=.41, relwidth=.30)

        # Get Address
        self.addressLabel = tk.Label(self.middleFrame, text="Address", bg='#e1fbfa')
        self.addressLabel.place(anchor="w", relx=0, rely=.50, relwidth=.30)
        self.addressEntry = tk.Entry(self.middleFrame, bg='white')
        self.addressEntry.place(anchor="w", relx=.30, rely=.50, relwidth=.30)

        # Get phone number
        self.numberLabel = tk.Label(self.middleFrame, text="Number (123-456-789)", bg='#e1fbfa')
        self.numberLabel.place(anchor="w", relx=0, rely=.59, relwidth=.30)
        self.numberEntry = tk.Entry(self.middleFrame, bg='white')
        self.numberEntry.place(anchor="w", relx=.30, rely=.59, relwidth=.30)

        # Get total hours
        self.totHoursLabel = tk.Label(self.middleFrame, text="Total Hours", bg='#e1fbfa')
        self.totHoursLabel.place(anchor="w", relx=0, rely=.68, relwidth=.30)
        self.totHoursEntry = tk.Entry(self.middleFrame, bg='white')
        self.totHoursEntry.place(anchor="w", relx=.30, rely=.68, relwidth=.30)

        # Get ID
        self.idLabel = tk.Label(self.middleFrame, text="Student ID", bg='#e1fbfa')
        self.idLabel.place(anchor="w", relx=0, rely=.77, relwidth=.30)
        self.idEntry = tk.Entry(self.middleFrame, bg='white')
        self.idEntry.place(anchor="w", relx=.30, rely=.77, relwidth=.30)

        # Get supervisor name
        self.supLabel = tk.Label(self.middleFrame, text="Supervisor", bg='#e1fbfa')
        self.supLabel.place(anchor="w", relx=0, rely=.86, relwidth=.30)
        self.supEntry = tk.Entry(self.middleFrame, bg='white')
        self.supEntry.place(anchor="w", relx=.30, rely=.86, relwidth=.30)



        # Allow user to submit information, lambda is defined at runtime, redefines button each time it is clicked to get current
        # state of textbox
        self.button = tk.Button(self.middleFrame, text="Submit", bg='red', fg='gray', font=60,
                                command=lambda: [insertIntoInternship(self.companyEntry.get(), self.startmoEntry.get(), self.startyrEntry.get(), self.endmoEntry.get(),
                                                                       self.endyrEntry.get(), self.addressEntry.get(), self.numberEntry.get(),
                                                                       self.totHoursEntry.get(), self.idEntry.get(), self.supEntry.get(), mycursor, mydb, self.middleFrame,
                                                                       self.upperFrame), self.destoryWindow(mycursor, mydb)])

        self.button.place(anchor='s', rely=1, relx=.5)

        self.root.mainloop()
