import mysql.connector

def createTables(mycursor):
    """"*************************************************************************************************"""
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

    mycursor.execute("CREATE TABLE IF NOT EXISTS Supervisor(company VARCHAR (50),"
                     "supervisorName VARCHAR (50)," #seperate to first last
                     "title VARCHAR (20),"
                     "email VARCHAR (30),"
                     "PRIMARY KEY (email))")

    mycursor.execute("CREATE TABLE IF NOT EXISTS Internship(supervisorEmail VARCHAR (30),"
                     "startMonth VARCHAR (15),"
                     "startYear CHAR (4),"
                     "endMonth VARCHAR (15),"
                     "endYear CHAR (4),"
                     "address VARCHAR(80),"
                     "phoneNumber CHAR(11),"
                     "totalHours INT,"
                     "BaylorID CHAR(9),"
                     #"supervisorName VARCHAR(50)," #supervisorName and company replaced with SupervisorEmail
                     "PRIMARY KEY (BaylorID, supervisorEmail),"
                     #Supervisor has not yet been created so will have to alter Internship table after 
                     #to add supervisorEmail foreign constraint
                     "FOREIGN KEY (supervisorEmail) REFERENCES Supervisor(email),"
                     "FOREIGN KEY (BaylorID) REFERENCES StudentInfo(BaylorID))")
    """"*************************************************************************************************"""

    mycursor.execute("CREATE TABLE IF NOT EXISTS SupervisorInternReviewQ(label VARCHAR (50),"
                     "question VARCHAR (255),"
                     "reviewType VARCHAR (30),"
                     "startYear CHAR (4),"
                     "PRIMARY KEY (label, startYear, reviewType))")

    mycursor.execute("CREATE TABLE IF NOT EXISTS SupervisorInternAnswerChoices(label VARCHAR (50),"
                     "startYear CHAR (4),"
                     "reviewType VARCHAR (30),"
                     "answerChoiceLabel VARCHAR (255),"
                     "value INT DEFAULT NULL," #answerchoices can have a value associated with them
                     "FOREIGN KEY (label, startYear, reviewType) REFERENCES SupervisorInternReviewQ(label, startYear, reviewType),"
                     "PRIMARY KEY (label, startYear, reviewType, answerChoiceLabel))")

    mycursor.execute("CREATE TABLE IF NOT EXISTS SupervisorInternResponse(label VARCHAR (50),"
                     "startYear CHAR (4),"
                     "reviewType VARCHAR (30),"
                     "supervisorEmail VARCHAR (30),"
                     "baylorID CHAR (9),"
                     "answer VARCHAR (255),"
                     "comment VARCHAR (255),"
                     "FOREIGN KEY (supervisorEmail) REFERENCES Supervisor(email),"
                     "FOREIGN KEY (BaylorID) REFERENCES StudentInfo(BaylorID),"
                     "FOREIGN KEY (label, startYear, reviewType) REFERENCES SupervisorInternReviewQ(label, startYear, reviewType),"
                     "PRIMARY KEY (label, startYear, reviewType, supervisorEmail))")
    """"*************************************************************************************************"""

    mycursor.execute("CREATE TABLE IF NOT EXISTS StudentReviewQ(label VARCHAR (50),"
                     "question VARCHAR (255),"
                     "startYear CHAR (4),"
                     "PRIMARY KEY (label, startYear))")

    mycursor.execute("CREATE TABLE IF NOT EXISTS StudentAnswerChoices(label VARCHAR (50),"
                     "startYear CHAR (4),"
                     "answerChoiceLabel VARCHAR (255),"
                     "value INT DEFAULT NULL," #answerchoices can have a value associated with them
                     "FOREIGN KEY (label, startYear) REFERENCES StudentReviewQ(label, startYear),"
                     "PRIMARY KEY (label, startYear, answerChoiceLabel))")

    mycursor.execute("CREATE TABLE IF NOT EXISTS StudentResponse(label VARCHAR (50),"
                     "startYear CHAR (4),"
                     "supervisorEmail VARCHAR (30),"
                     "baylorID CHAR (9),"
                     "answer VARCHAR (255),"
                     "comment VARCHAR (255),"
                     "FOREIGN KEY (supervisorEmail) REFERENCES Supervisor(email),"
                     "FOREIGN KEY (BaylorID) REFERENCES StudentInfo(BaylorID),"
                     "FOREIGN KEY (label, startYear) REFERENCES StudentReviewQ(label, startYear),"
                     "PRIMARY KEY (label, startYear, supervisorEmail))")
    """"*************************************************************************************************"""
    mycursor.execute("CREATE TABLE IF NOT EXISTS PortfolioReviewQ(label VARCHAR (50),"
                     "question VARCHAR (255),"
                     "startYear CHAR (4),"
                     "PRIMARY KEY (label, startYear))")

    #will need to ask user for number of answer choices
    mycursor.execute("CREATE TABLE IF NOT EXISTS PortfolioAnswerChoices(label VARCHAR (50),"
                     "startYear CHAR (4),"
                     "answerChoiceLabel VARCHAR (255),"
                     "value INT DEFAULT NULL," #answerchoices can have a value associated with them
                     "FOREIGN KEY (label, startYear) REFERENCES PortfolioReviewQ(label, startYear),"
                     "PRIMARY KEY (label, startYear, answerChoiceLabel))")

    mycursor.execute("CREATE TABLE IF NOT EXISTS PortfolioResponses(label VARCHAR (50),"
                     "startYear CHAR (4),"
                     "baylorID CHAR (9),"
                     "answer VARCHAR (255),"
                     "comment VARCHAR (255),"
                     "dateOfReview DATE,"
                     "reviewerName VARCHAR (50),"
                     "FOREIGN KEY (BaylorID) REFERENCES StudentInfo(BaylorID),"
                     "FOREIGN KEY (label, startYear) REFERENCES PortfolioReviewQ(label, startYear),"
                     "PRIMARY KEY (label, startYear, ReviewerName, baylorID))")
    """"*************************************************************************************************"""




#get the basic student info
#if they enter id
basicInfoBaylorID = """SELECT BaylorID, lastName, firstName, emailAddress, ADV_PR_semester, class, major_minor, ADV_PR_grade, ADV_PR_year
FROM StudentInfo
WHERE BaylorID = %s"""
#if they enter name
basicInfoName = """SELECT BaylorID, lastName, firstName, emailAddress, ADV_PR_semester, class, major_minor, ADV_PR_grade, ADV_PR_year
FROM StudentInfo
WHERE firstName = %s AND lastName = %s"""

#ask user for which type of review they would like
#if review type is Qualtrics
#ask user if it is midterm or endterm
#ask if they want to enter the year as well, if no:
displayQReviewIDNoYear = "SELECT answer, comment FROM QualtricsReview WHERE reviewTime = %s AND BaylorID = %s"
displayQReviewnameNoYear = """SELECT answer, comment 
FROM QualtricsReview, StudentInfo 
WHERE reviewTime = %s AND firstName = %s AND lastName = %s AND QualtricsReview.baylorID = StudentInfo.baylorID"""
#if yes:
displayQReviewIDYear = "SELECT answer, comment FROM QualtricsReview WHERE reviewTime = %s AND BaylorID = %s AND syear = %s"
displayQReviewnameYear = """SELECT answer, comment 
FROM QualtricsReview, StudentInfo 
WHERE reviewTime = %s AND firstName = %s AND lastName = %s AND QualtricsReview.baylorID = StudentInfo.baylorID AND year = %s"""

#if review type is midTermSiteReview
#ask if they want to enter the year as well, if no:
displayMReviewIDNoYear = "SELECT answer, comment FROM midTermSiteReview WHERE BaylorID = %s"
displayMReviewnameNoYear = """SELECT answer, comment 
FROM midTermSiteReview, StudentInfo 
WHERE firstName = %s AND lastName = %s AND midTermSiteReview.baylorID = StudentInfo.baylorID"""
#if yes:
displayMReviewIDYear = "SELECT answer, comment FROM midTermSiteReview WHERE BaylorID = %s AND syear = %s"
displayMReviewnameYear = """SELECT answer, comment 
FROM midTermSiteReview, StudentInfo 
WHERE reviewTime = %s AND firstName = %s AND lastName = %s AND midTermSiteReview.baylorID = StudentInfo.baylorID AND year = %s"""
#


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
