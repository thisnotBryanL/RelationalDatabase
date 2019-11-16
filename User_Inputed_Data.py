import mysql.connector

#global variable allows us to update page
timeToUpdate = 0

def createTables(mycursor):
    mycursor.execute("CREATE TABLE IF NOT EXISTS StudentInfo(BaylorID CHAR (9),"
                     "lastName VARCHAR (30),"
                     "firstName VARCHAR (30),"
                     "emailAddress VARCHAR (30),"
                     "semester VARCHAR (30),"
                     "PRIMARY KEY (BaylorID))")


def insertIntoStudentInfo(idEntry, lastnameEntry, firstnameEntry, emailEntry, semesterEntry, mycursor, mydb, middleFrame, topFrame):
    print("The student id is", idEntry)
    print ("The last name is", lastnameEntry)
    print ("The first name is", firstnameEntry)
    print ("The email is", emailEntry)
    print ("The semester entering the program is", semesterEntry)

    try:
        sqlFormula = "INSERT INTO StudentInfo (BaylorID, lastName, firstName, emailAddress, semester) VALUES (%s, %s, %s, %s, %s)"
        mycursor.execute(sqlFormula, (idEntry, lastnameEntry, firstnameEntry, emailEntry, semesterEntry))
        mydb.commit()
    except mysql.connector.Error as error:
        print("could not be inserted")

    #Update frame to display new information
    Update(middleFrame, topFrame)


def Update (middleFrame, topFrame):
    for widget in middleFrame.winfo_children():
        widget.destroy()

    for widget in topFrame.winfo_children():
        widget.destroy()