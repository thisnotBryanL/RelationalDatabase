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
                     "phoneNumber CHAR(10),"
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
                     "PRIMARY KEY (label, startYear, supervisorEmail, baylorID))")
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
        basicInfoBaylorID = """SELECT * 
        FROM StudentInfo 
        WHERE BaylorID = %s"""

        mycursor.execute(basicInfoBaylorID, executeList)
        basicInfoResults = mycursor.fetchall()
        return basicInfoResults

    else:
        #if they enter name
        basicInfoName = """SELECT BaylorID, lastName, firstName, emailAddress, ADV_PR_semester, class, major_minor, ADV_PR_grade, ADV_PR_year
        FROM StudentInfo
        WHERE firstName = %s AND lastName = %s"""

        mycursor.execute(basicInfoName, executeList)
        basicInfoResults = mycursor.fetchall()
        return basicInfoResults
"----------------------------------------------------------------------------------------------------------------------------------------------------------------"
#REVIEW FOR SPECIFIC TYPE
#IF REVIEW != PORTFOLIO
"""
this is how we will call the function in main
if reviewType != "portfolio" and reviewType != "reviewByStudent":
    reviewType(mycursor, mydb, choice, executeList)"""
#choice can be id, name, idyear, nameyear
def supReviewType(mycursor, choice, executeList):
    # id and no year
    if choice == "id":
        displayQReviewIDNoYear = """SELECT SupervisorInternReviewQ.question, SupervisorInternResponse.answer, SupervisorInternResponse.comment
FROM SupervisorInternResponse, SupervisorInternReviewQ
WHERE baylorID = %s AND SupervisorInternReviewQ.reviewType = %s AND SupervisorInternResponse.ReviewType = %s
AND SupervisorInternResponse.startYear = SupervisorInternReviewQ.startYear AND SupervisorInternResponse.label = SupervisorInternReviewQ.label"""

        mycursor.execute(displayQReviewIDNoYear, executeList)
        reviewresults = mycursor.fetchall()
        return reviewresults

    # "----------------------------------------------------------------------------------------------------------------------------------------------------------------"
    #id and year
    if choice == "idyear":
        displayQReviewIDYear = """SELECT SupervisorInternReviewQ.question, SupervisorInternResponse.answer, comment
        FROM SupervisorInternResponse, SupervisorInternReviewQ
        WHERE baylorID = %s AND SupervisorInternResponse.startYear = %s AND SupervisorInternResponse.reviewType = %s AND SupervisorInternReviewQ.reviewType = %s
        AND SupervisorInternResponse.startYear = SupervisorInternReviewQ.startYear
        AND SupervisorInternResponse.label = SupervisorInternReviewQ.label"""

        mycursor.execute(displayQReviewIDYear, executeList)
        reviewresults = mycursor.fetchall()
        return reviewresults

# "----------------------------------------------------------------------------------------------------------------------------------------------------------------"
# IF REVIEW == PORTFOLIO
# """
# #choice can be id, name, idyear, nameyear
def portfolioReview(mycursor, mydb, choice, executeList):
    # #id and no year
    if choice == "id":
        displayQReviewIDNoYear = """SELECT question, answer, comment, reviewerName
        FROM PortfolioReviewQ, PortfolioResponses
        WHERE baylorID = %s
        AND PortfolioReviewQ.startYear = PortfolioResponses.startYear
        AND PortfolioReviewQ.label = PortfolioResponses.label"""

        mycursor.execute(displayQReviewIDNoYear, executeList)
        reviewresults = mycursor.fetchall()
        return reviewresults

    # id and year
    if choice == "idyear":
        displayQReviewIDNoYear = """SELECT question, answer, comment, reviewerName
        FROM PortfolioReviewQ, PortfolioResponses
        WHERE baylorID = %s and PortfolioResponses.startYear = %s
        AND PortfolioReviewQ.startYear = PortfolioResponses.startYear
        AND PortfolioReviewQ.label = PortfolioResponses.label"""


        mycursor.execute(displayQReviewIDNoYear, executeList)
        reviewresults = mycursor.fetchall()
        return reviewresults

# "----------------------------------------------------------------------------------------------------------------------------------------------------------------"
# #IF REVIEW == reviewByStudent
# # choice can be id, name, idyear, nameyear
def reviewByStudent(mycursor, mydb, choice, executeList):
    # id and no year
    if choice == "id":
        displayQReviewIDNoYear = """SELECT question, answer, comment
        FROM StudentReviewQ, StudentResponse
        WHERE baylorID = %s
        AND StudentReviewQ.startYear = StudentResponse.startYear
        AND StudentReviewQ.label = StudentResponse.label"""

        mycursor.execute(displayQReviewIDNoYear, executeList)
        reviewresults = mycursor.fetchall()
        return reviewresults

#
#
    # id and year
    if choice == "idyear":
        displayQReviewIDNoYear = """SELECT question, answer, comment
        FROM StudentReviewQ, StudentResponse
        WHERE baylorID = %s and StudentResponse.startYear = %s
        AND StudentReviewQ.startYear = StudentResponse.startYear
        AND StudentReviewQ.label = StudentResponse.label"""

        mycursor.execute(displayQReviewIDNoYear, executeList)
        reviewresults = mycursor.fetchall()
        return reviewresults

# "----------------------------------------------------------------------------------------------------------------------------------------------------------------"
# #Reviews for specific year of specific student
def displayReviewForStudent(mycursor, choice, executeList):
        if choice == "sup":
            displayQReviewIDYear = """SELECT SupervisorInternReviewQ.question, SupervisorInternResponse.answer, SupervisorInternResponse.comment, SupervisorInternReviewQ.reviewType
FROM SupervisorInternResponse, SupervisorInternReviewQ
WHERE baylorID = %s AND SupervisorInternReviewQ.startYear = %s AND SupervisorInternResponse.startYear = %s
AND SupervisorInternResponse.startYear = SupervisorInternReviewQ.startYear AND SupervisorInternResponse.label = SupervisorInternReviewQ.label AND
SupervisorInternReviewQ.reviewType = SupervisorInternResponse.reviewType"""

            mycursor.execute(displayQReviewIDYear, executeList)
            reviewresults = mycursor.fetchall()
            return reviewresults

        elif choice == "student":
            displayQReviewIDYear = """SELECT StudentReviewQ.question, StudentResponse.answer, StudentResponse.comment
    FROM StudentReviewQ, StudentResponse
    WHERE baylorID = %s AND StudentResponse.startYear = %s AND StudentReviewQ.startYear = %s 
    AND StudentReviewQ.startYear = StudentResponse.startYear
    AND StudentReviewQ.label = StudentResponse.label"""

            mycursor.execute(displayQReviewIDYear, executeList)
            reviewresults = mycursor.fetchall()
            return reviewresults

        elif choice == "portfolio":
            displayQReviewIDYear = """SELECT PortfolioReviewQ.question, PortfolioResponses.answer, PortfolioResponses.comment
    FROM PortfolioReviewQ, PortfolioResponses
    WHERE baylorID = %s AND PortfolioResponses.startYear = %s AND PortfolioReviewQ.startYear = %s AND 
	PortfolioReviewQ.startYear = PortfolioResponses.startYear
    AND PortfolioReviewQ.label = PortfolioResponses.label"""

        mycursor.execute(displayQReviewIDYear, executeList)
        reviewresults = mycursor.fetchall()
        return reviewresults

""""**************************************************************************************************************************************************************************************************"""
#ask for certain type of reviews
"""if reviewType = "Portfolio":
    displayPortfolioReviews(mycursor, mydb, choice, executeList)"""
def displayPortfolioReviews(mycursor, mydb):
    displayAllPortfolio = """SELECT firstName, lastName, StudentInfo.BaylorID,
    PortfolioReviewQ.question, PortfolioResponses.answer, PortfolioResponses.comment,
    PortfolioReviewQ.startYear, reviewerName
    FROM StudentInfo, PortfolioReviewQ, PortfolioResponses
    WHERE StudentInfo.BaylorID = PortfolioResponses.baylorID
    AND PortfolioReviewQ.startYear = PortfolioResponses.startYear
    AND PortfolioReviewQ.label = PortfolioResponses.label"""

    mycursor.execute(displayAllPortfolio)
    reviewresults = mycursor.fetchall()
    return reviewresults


# "----------------------------------------------------------------------------------------------------------------------------------------------------------------"
# """if reviewType = "Student":
#     displayStudentReviews(mycursor, mydb, choice, executeList)"""
def displayStudentReviews(mycursor, mydb):
    displayAllStudent = """SELECT firstName, lastName, StudentInfo.BaylorID,
    StudentReviewQ.question, StudentResponse.answer, StudentResponse.comment,
    StudentResponse.startYear
    FROM StudentInfo, StudentReviewQ, StudentResponse
    WHERE StudentInfo.BaylorID = StudentResponse.baylorID
    AND StudentReviewQ.startYear = StudentResponse.startYear
    AND StudentReviewQ.label = StudentResponse.label"""

    mycursor.execute(displayAllStudent)
    reviewresults = mycursor.fetchall()
    return reviewresults
#
#
# "----------------------------------------------------------------------------------------------------------------------------------------------------------------"
#review types can be midterm, endterm, site
def displayReviews(mycursor, mydb, executeList):
    displayReviews = """SELECT firstName, lastName, StudentInfo.BaylorID,
    SupervisorInternReviewQ.question, SupervisorInternResponse.answer, SupervisorInternResponse.comment,
    SupervisorInternResponse.startYear
    FROM StudentInfo, SupervisorInternReviewQ, SupervisorInternResponse
    WHERE SupervisorInternResponse.reviewType = %s AND SupervisorInternReviewQ.reviewType = %s
    AND StudentInfo.BaylorID = SupervisorInternResponse.baylorID
    AND SupervisorInternReviewQ.startYear = SupervisorInternResponse.startYear
    AND SupervisorInternReviewQ.label = SupervisorInternResponse.label"""

    mycursor.execute(displayReviews, executeList)
    reviewresults = mycursor.fetchall()
    return reviewresults


""""**************************************************************************************************************************************************************************************************"""
# #certain question label for certain review type of certain year range

def displayForSpecificLabelSup(mycursor, executeList):
    #by year
    #if answer is short answer
    displayReviewsY = """SELECT SupervisorInternReviewQ.question, SupervisorInternResponse.label, SupervisorInternResponse.answer,
    COUNT(*) as number__of_times_answer_was_chosen
    FROM SupervisorInternReviewQ, SupervisorInternResponse, SupervisorInternAnswerChoices
    WHERE SupervisorInternAnswerChoices.reviewType = %s
	AND SupervisorInternReviewQ.reviewType = %s
    AND SupervisorInternResponse.reviewType = %s
    AND SupervisorInternAnswerChoices.label = %s
	AND SupervisorInternReviewQ.label = %s
    AND SupervisorInternResponse.label = %s
    AND SupervisorInternReviewQ.startYear = SupervisorInternResponse.startYear
    AND SupervisorInternAnswerChoices.startYear = SupervisorInternReviewQ.startYear
    AND SupervisorInternAnswerChoices.startYear BETWEEN %s AND %s
	GROUP BY SupervisorInternReviewQ.question, SupervisorInternResponse.label, SupervisorInternResponse.answer"""

    mycursor.execute(displayReviewsY, executeList)
    reviewresults = mycursor.fetchall()
    return reviewresults

def displayForSpecificLabelSupAgg(mycursor, executeList):
    #aggregate
    #if answer is multiple choice
    displayReviewsA = """SELECT StudentResponse.label, question, StudentResponse.answer,
    COUNT(answer) as number__of_times_answer_was_chosen
    FROM StudentReviewQ, StudentResponse, StudentAnswerChoices
    WHERE StudentAnswerChoices.label = %s AND StudentResponse.label = %s AND StudentReviewQ.label = %s
    AND StudentAnswerChoices.answerChoiceLabel = StudentResponse.answer
    AND StudentAnswerChoices.startYear = StudentResponse.startYear
    AND StudentAnswerChoices.startYear = StudentReviewQ.startYear
    AND StudentReviewQ.label = StudentResponse.label
    AND StudentAnswerChoices.label = StudentResponse.label
    AND StudentAnswerChoices.startYear BETWEEN %s and %s
    GROUP BY question, StudentResponse.label, StudentResponse.answer"""

    mycursor.execute(displayReviewsA, executeList)
    reviewresults = mycursor.fetchall()
    return reviewresults
#
#     #number__of_times_answer_was_chosen > 1, display it for both queries
# "----------------------------------------------------------------------------------------------------------------------------------------------------------------"
# """elif reviewType == "Student":
#     #questionLabel, startYear, endYear
#     displayForSpecificLabelStudent(mycursor, mydb, executeList)"""
def displayForSpecificLabelStudent(mycursor, executeList):
     #by year
    displayReviewsY = """SELECT StudentResponse.label, question, StudentResponse.answer,
    COUNT(answer) as number__of_times_answer_was_chosen
    FROM StudentReviewQ, StudentResponse, StudentAnswerChoices
    WHERE StudentAnswerChoices.label = %s AND StudentResponse.label = %s AND StudentReviewQ.label = %s
    AND StudentAnswerChoices.answerChoiceLabel = StudentResponse.answer
    AND StudentAnswerChoices.startYear = StudentResponse.startYear
    AND StudentAnswerChoices.startYear = StudentReviewQ.startYear
    AND StudentReviewQ.label = StudentResponse.label
    AND StudentAnswerChoices.label = StudentResponse.label
    AND StudentAnswerChoices.startYear BETWEEN %s and %s
    GROUP BY question, StudentResponse.label, StudentResponse.answer"""

    mycursor.execute(displayReviewsY, executeList)
    resultsByYear = mycursor.fetchall()
    return resultsByYear
#
#     #aggregate
#     displayReviewsA = """SELECT StudentResponse.label, StudentResponse.answer
#     COUNT(*) as number__of_times_answer_was_chosen
#     FROM StudentReviewQ, StudentResponse, StudentAnswerChoices,
#     WHERE StudentAnswerChoices.label = %s AND StudentAnswerChoices.startYear BETWEEN %s and %s
#     AND StudentAnswerChoices.startYear = StudentResponse.startYear
#     AND StudentReviewQ.label = StudentResponse.label
#     AND StudentAnswerChoices.label = StudentResponse.label
#     AND StudentAnswerChoices.startYear = StudentReviewQ.label
#     GROUP BY  StudentResponse.answer"""
#
#     mycursor.execute(displayReviewsA, (questionlabel, startyear, endyear))
#     mydb.commit()
#     resultsAggregate = mycursor.fetchall()
#
#
#     #number__of_times_answer_was_chosen > 1, display it for both queries
# #ask for certain review label of
#
# "----------------------------------------------------------------------------------------------------------------------------------------------------------------"
def displayForSpecificLabelPortfolio(mycursor, executeList):
    #by year
    displayReviewsY = """SELECT question, PortfolioResponses.label, PortfolioResponses.answer,
        COUNT(*) as number__of_times_answer_was_chosen
        FROM PortfolioReviewQ, PortfolioResponses, PortfolioAnswerChoices
        WHERE PortfolioAnswerChoices.label = %s AND PortfolioResponses.label = %s AND PortfolioReviewQ.label = %s
        AND PortfolioAnswerChoices.startYear = PortfolioResponses.startYear
        AND PortfolioAnswerChoices.startYear = PortfolioReviewQ.startYear
        AND PortfolioReviewQ.label = PortfolioResponses.label
        AND PortfolioAnswerChoices.label = PortfolioReviewQ.label
        AND PortfolioAnswerChoices.startYear BETWEEN %s and %s
        GROUP BY PortfolioResponses.label, question, PortfolioResponses.answer"""

    mycursor.execute(displayReviewsY, executeList)
    resultsByYear = mycursor.fetchall()
    return resultsByYear

#
#     #aggregate
#     displayReviewsA = """SELECT PortfolioResponses.label, PortfolioResponses.answer
#     COUNT(*) as number__of_times_answer_was_chosen
#     FROM PortfolioReviewQ, PortfolioResponses, PortfolioAnswerChoices,
#     WHERE PortfolioAnswerChoices.label = %s AND PortfolioAnswerChoices.startYear BETWEEN %s and %s
#     AND PortfolioAnswerChoices.startYear = PortfolioResponses.startYear
#     AND PortfolioReviewQ.label = PortfolioResponses.label
#     AND PortfolioAnswerChoices.label = PortfolioResponses.label
#     AND PortfolioAnswerChoices.startYear = PortfolioReviewQ.label
#     GROUP BY  PortfolioResponses.answer"""
#
#     mycursor.execute(displayReviewsA, (questionlabel, startyear, endyear))
#     mydb.commit()
#     resultsAggregate = mycursor.fetchall()
#
#