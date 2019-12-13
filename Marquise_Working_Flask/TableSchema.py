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
#QUERY ANALYSIS

#BASIC INFO
#choice can equal: idTrue, nameTrue
def basicInfo(mycursor, mydb, choice, executeList):
    #if they enter id
    if choice == "idTrue":
        basicInfoBaylorID = """SELECT BaylorID, lastName, firstName, emailAddress, ADV_PR_semester, class, major_minor, ADV_PR_grade, ADV_PR_year
        FROM StudentInfo
        WHERE BaylorID = %s"""
    else:
        #if they enter name
        basicInfoName = """SELECT BaylorID, lastName, firstName, emailAddress, ADV_PR_semester, class, major_minor, ADV_PR_grade, ADV_PR_year
        FROM StudentInfo
        WHERE firstName = %s AND lastName = %s"""
"----------------------------------------------------------------------------------------------------------------------------------------------------------------"
#REVIEW FOR SPECIFIC TYPE
#IF REVIEW != PORTFOLIO
"""
this is how we will call the function in main
if choice != "portfolio":
    reviewType(mycursor, mydb, choice, executeList)"""
#choice can be id, name, idyear, nameyear
def reviewType(mycursor, mydb, choice, executeList):
    # id and no year
    if choice == "id":
        displayQReviewIDNoYear = """SELECT question, answer, comment 
        FROM SupervisorInternResponse, SupervisorInternReviewQ 
        WHERE baylorID = %s AND ReviewType = %s AND SupervisorInternResponse.startYear = SupervisorInternReviewQ.startYear AND SupervisorInternResponse.label = SupervisorInternReviewQ.label"""
        #name and no year
        displayQReviewnameNoYear = """SELECT question, answer, comment 
        FROM SupervisorInternResponse, StudentInfo, SupervisorInternReviewQ 
        WHERE firstName = %s AND lastName = %s AND ReviewType = %s 
        AND SupervisorInternResponse.baylorID = StudentInfo.BaylorID 
        AND SupervisorInternResponse.startYear = SupervisorInternReviewQ.startYear 
        AND SupervisorInternResponse.label = SupervisorInternReviewQ.label"""

    # name and no year
    if choice == "name":
        displayQReviewIDNoYear = """SELECT question, answer, comment 
        FROM SupervisorInternResponse, SupervisorInternReviewQ 
        WHERE firstName = %s AND lastName = %s AND ReviewType = %s AND SupervisorInternResponse.startYear = SupervisorInternReviewQ.startYear AND SupervisorInternResponse.label = SupervisorInternReviewQ.label"""
        #name and no year
        displayQReviewnameNoYear = """SELECT question, answer, comment 
        FROM SupervisorInternResponse, StudentInfo, SupervisorInternReviewQ 
        AND StudentInfo.BaylorID = SupervisorInternResponse.baylor ID
        WHERE firstName = %s AND lastName = %s AND ReviewType = %s 
        AND SupervisorInternResponse.baylorID = StudentInfo.BaylorID 
        AND SupervisorInternResponse.startYear = SupervisorInternReviewQ.startYear 
        AND SupervisorInternResponse.label = SupervisorInternReviewQ.label"""
        "----------------------------------------------------------------------------------------------------------------------------------------------------------------"
    #id and year
    if choice == "idyear":
        displayQReviewIDYear = """SELECT question, answer, comment 
        FROM SupervisorInternResponse, SupervisorInternReviewQ 
        WHERE baylorID = %s AND ReviewType = %s AND startYear = %s 
        AND SupervisorInternResponse.startYear = SupervisorInternReviewQ.startYear 
        AND SupervisorInternResponse.label = SupervisorInternReviewQ.label"""

    #name and year
    if choice == "nameyear":
        displayQReviewnameYear = """SELECT question, answer, comment 
        FROM SupervisorInternResponse, SupervisorInternReviewQ, StudentInfo
        WHERE firstName = %s AND lastName = %s AND ReviewType = %s AND startYear = %s 
        AND StudentInfo.BaylorID = SupervisorInternResponse.baylor ID
        AND SupervisorInternResponse.label = SupervisorInternReviewQ.label 
        AND SupervisorInternResponse.startYear = SupervisorInternReviewQ.startYear"""
        "----------------------------------------------------------------------------------------------------------------------------------------------------------------"
#IF REVIEW == PORTFOLIO
#id and no year
displayQReviewIDNoYear = """SELECT question, answer, comment 
FROM PortfolioReviewQ, PortfolioResponses 
WHERE baylorID = %s 
AND PortfolioReviewQ.startYear = PortfolioResponses.startYear 
AND PortfolioReviewQ.label = PortfolioResponses.label"""
#name and no year
displayQReviewnameNoYear = """SELECT question, answer, comment 
FROM PortfolioReviewQ, StudentInfo, PortfolioResponses 
WHERE firstName = %s AND lastName = %s 
AND PortfolioResponses.baylorID = StudentInfo.BaylorID 
AND PortfolioResponses.startYear = PortfolioReviewQ.startYear 
AND PortfolioResponses.label = PortfolioReviewQ.label"""
"----------------------------------------------------------------------------------------------------------------------------------------------------------------"
#id and year
displayQReviewIDYear = """SELECT question, answer, comment 
FROM PortfolioResponses, PortfolioReviewQ 
WHERE baylorID = %s AND startYear = %s 
AND PortfolioResponses.startYear = PortfolioReviewQ.startYear 
AND PortfolioResponses.label = PortfolioReviewQ.label"""

#name and year
displayQReviewnameYear = """SELECT question, answer, comment 
FROM PortfolioResponses, PortfolioReviewQ, StudentInfo
WHERE firstName = %s AND lastName = %s AND startYear = %s 
AND StudentInfo.BaylorID = SupervisorInternResponse.baylor ID
AND PortfolioResponses.startYear = PortfolioReviewQ.startYear 
AND PortfolioResponses.label = PortfolioReviewQ.label"""

"----------------------------------------------------------------------------------------------------------------------------------------------------------------"
#Reviews for specific year

#id
displayQReviewIDYear = """SELECT PortfolioReviewQ.question, PortfolioResponses.answer, PortfolioResponses.comment,
SupervisorInternReviewQ.question, SupervisorInternResponse.answer, SupervisorInternResponse.comment
FROM PortfolioResponses, PortfolioReviewQ, SupervisorInternResponse, SupervisorInternReviewQ  
WHERE baylorID = %s AND PortfolioResponses.startYear = %s AND SupervisorInternResponse.startYear = %s
AND PortfolioResponses.startYear = PortfolioReviewQ.startYear 
AND PortfolioResponses.label = PortfolioReviewQ.label 
AND SupervisorInternResponse.label = SupervisorInternReviewQ.label
AND SupervisorInternResponse.startYear = SupervisorInternReviewQ.startYear """

#name
displayQReviewIDYear = """SELECT PortfolioReviewQ.question, PortfolioResponses.answer, PortfolioResponses.comment,
SupervisorInternReviewQ.question, SupervisorInternResponse.answer, SupervisorInternResponse.comment
FROM PortfolioResponses, PortfolioReviewQ, SupervisorInternResponse, SupervisorInternReviewQ, StudentInfo 
WHERE firstName = %s AND lastName = %s AND PortfolioResponses.startYear = %s AND SupervisorInternResponse.startYear = %s
AND StudentInfo.BaylorID = PortfolioResponses.baylorID
AND PortfolioResponses.startYear = PortfolioReviewQ.startYear 
AND PortfolioResponses.label = PortfolioReviewQ.label 
AND SupervisorInternResponse.label = SupervisorInternReviewQ.label
AND SupervisorInternResponse.startYear = SupervisorInternReviewQ.startYear """

""""**************************************************************************************************************************************************************************************************"""

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
