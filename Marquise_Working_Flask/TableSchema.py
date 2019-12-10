import mysql.connector

def createTables(mycursor):
    mycursor.execute("CREATE TABLE IF NOT EXISTS StudentInfo(BaylorID CHAR (9),"
                     "lastName VARCHAR (30),"
                     "firstName VARCHAR (30),"
                     "emailAddress VARCHAR (30),"
                     "ADV_PR_semester VARCHAR (30),"
                     "class VARCHAR (20),"
                     "major_minor VARCHAR(5),"
                     "ADV_PR_grade CHAR(1),"
                     "ADV_PR_year CHAR(4),"
                     "PRIMARY KEY (BaylorID))")

    mycursor.execute("CREATE TABLE IF NOT EXISTS Internship(company VARCHAR (50),"
                     "startMonth VARCHAR (15),"
                     "startYear CHAR (4),"
                     "endMonth VARCHAR (15),"
                     "endYear CHAR (4),"
                     "address VARCHAR(80),"
                     "phoneNumber CHAR(11),"
                     "totalHours INT,"
                     "BaylorID CHAR(9),"
                     "supervisorName VARCHAR(50),"
                     "PRIMARY KEY (BaylorID, company, supervisorName),"
                     #"FOREIGN KEY (supervisorName) REFERENCES Supervisor(supervisorName)," 
                     #"FOREIGN KEY (company) REFERENCES Supervisor(company,)"
                     #Supervisor has not yet been created so will have to alter Internship table after 
                     #Supervisor table has been created to add forteign key constraint
                     "FOREIGN KEY (BaylorID) REFERENCES StudentInfo(BaylorID))")

    mycursor.execute("CREATE TABLE IF NOT EXISTS Supervisor(company VARCHAR (50),"
                     "supervisorName VARCHAR (50),"
                     "title VARCHAR (20),"
                     "email VARCHAR (30),"
                     "UNIQUE (supervisorName),"
                     #made supervisorName unique so other tables could reference it
                     #I don't think it should be a problem, though it may be possible
                     #that mult students have the same supervisor It's unlikely
                     "PRIMARY KEY (email))")
                     #"FOREIGN KEY (company) REFERENCES Internship(company))")

    mycursor.execute("CREATE TABLE IF NOT EXISTS Questions(label VARCHAR (50),"
                     "question VARCHAR (255),"
                     "comments VARCHAR (255),"
                     "startYear CHAR (4),"
                     "PRIMARY KEY (question))")
                     #made question, label composite instead of just label as pk so label could be referenced
                    #from Review


    mycursor.execute("CREATE TABLE IF NOT EXISTS Review(reviewType VARCHAR (50),"
                     "supervisorName VARCHAR (50),"
                     #added question so questionLabel could reference label from Questions
                     "question VARCHAR (255),"
                     "baylorID CHAR (9),"
                     "questionLabel VARCHAR (50),"
                     "PRIMARY KEY (reviewType, supervisorName, baylorID, questionLabel),"
                     "FOREIGN KEY (baylorID) REFERENCES StudentInfo(BaylorID),"
                     #"FOREIGN KEY (questionLabel) REFERENCES Questions(label),"
                     "FOREIGN KEY (supervisorName) REFERENCES Supervisor(supervisorName))")


    mycursor.execute("CREATE TABLE IF NOT EXISTS Answers(baylorID CHAR (9),"
                     "answer VARCHAR (255),"
                     "label VARCHAR (255),"
                     "question VARCHAR (255),"
                     "PRIMARY KEY (baylorID, answer, question),"
                     "FOREIGN KEY (baylorID) REFERENCES StudentInfo(BaylorID),"
                     "FOREIGN KEY (question) REFERENCES Questions(question))")


    #mycursor.execute("ALTER TABLE Internship ADD FOREIGN KEY (company, supervisorName) REFERENCES Supervisor(company, supervisorName)")



def insertIntoStudentInfo(idEntry, lastnameEntry, firstnameEntry, emailEntry, semesterEntry, classyr, major_minor, grade, year, mycursor, mydb, middleFrame, topFrame):
    try:
        sqlFormula = "INSERT INTO StudentInfo (BaylorID, lastName, firstName, emailAddress, ADV_PR_semester, class, major_minor, ADV_PR_grade, ADV_PR_year) " \
                     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        mycursor.execute(sqlFormula, (idEntry, lastnameEntry, firstnameEntry, emailEntry, semesterEntry, classyr, major_minor, grade, year))
        mydb.commit()
    except mysql.connector.Error as error:
        print("could not be inserted")

def insertIntoInternship(companyEntry, startmoEntry, startyrEntry, endmoEntry, endyrEntry, addressEntry, numberEntry, totHoursEntry, idEntry, supNameEntry, mycursor, mydb, middleFrame, topFrame):
    # print ("The company is", companyEntry)
    # print ("The start month is", startmoEntry)
    # print ("The start year is", startyrEntry)
    # print ("The end month is", endmoEntry)
    # print ("The end year is", endyrEntry)
    # print ("The address is", addressEntry)
    # print ("The number is", numberEntry)
    # print ("The  total hours is", totHoursEntry)
    # print ("The id is", idEntry)
    # print ("The supervisor is", supNameEntry)

    try:
        sqlFormula = "INSERT INTO Internship (company, startMonth, startYear, endMonth, endYear, address, phoneNumber, totalHours, BaylorID, supervisorName) " \
                     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        mycursor.execute(sqlFormula, (companyEntry, startmoEntry, startyrEntry, endmoEntry, endyrEntry, addressEntry, numberEntry, totHoursEntry, idEntry, supNameEntry))
        mydb.commit()
    except mysql.connector.Error as error:
        print("could not be inserted")
