# import mysql.connector
#
# #global variable allows us to update page
# timeToUpdate = 0
# #
# def createTables(mycursor):
#     mycursor.execute("CREATE TABLE IF NOT EXISTS StudentInfo(BaylorID CHAR (9),"
#                      "lastName VARCHAR (30),"
#                      "firstName VARCHAR (30),"
#                      "emailAddress VARCHAR (30),"
#                      "ADV_PR_semester VARCHAR (30),"
#                      "class VARCHAR (20),"
#                      "major_minor VARCHAR(5),"
#                      "ADV_PR_grade CHAR(1),"
#                      "ADV_PR_year CHAR(4),"
#                      "PRIMARY KEY (BaylorID))")
#
#     mycursor.execute("CREATE TABLE IF NOT EXISTS Internship(company VARCHAR (50),"
#                      "startMonth VARCHAR (15),"
#                      "startYear CHAR (4),"
#                      "endMonth VARCHAR (15),"
#                      "endYear CHAR (4),"
#                      "address VARCHAR(80),"
#                      "phoneNumber CHAR(11),"
#                      "totalHours INT,"
#                      "BaylorID CHAR(9),"
#                      "supervisorName VARCHAR(50),"
#                      "PRIMARY KEY (BaylorID, company, supervisorName),"
#                      "FOREIGN KEY (BaylorID) REFERENCES StudentInfo(BaylorID))")
#
#
# def insertIntoStudentInfo(idEntry, lastnameEntry, firstnameEntry, emailEntry, semesterEntry, classyr, major_minor, grade, year, mycursor, mydb, middleFrame, topFrame):
#     try:
#         sqlFormula = "INSERT INTO StudentInfo (BaylorID, lastName, firstName, emailAddress, ADV_PR_semester, class, major_minor, ADV_PR_grade, ADV_PR_year) " \
#                      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
#         mycursor.execute(sqlFormula, (idEntry, lastnameEntry, firstnameEntry, emailEntry, semesterEntry, classyr, major_minor, grade, year))
#         mydb.commit()
#     except mysql.connector.Error as error:
#         print("could not be inserted")
#
# def insertIntoInternship(companyEntry, startmoEntry, startyrEntry, endmoEntry, endyrEntry, addressEntry, numberEntry, totHoursEntry, idEntry, supNameEntry, mycursor, mydb, middleFrame, topFrame):
#     # print ("The company is", companyEntry)
#     # print ("The start month is", startmoEntry)
#     # print ("The start year is", startyrEntry)
#     # print ("The end month is", endmoEntry)
#     # print ("The end year is", endyrEntry)
#     # print ("The address is", addressEntry)
#     # print ("The number is", numberEntry)
#     # print ("The  total hours is", totHoursEntry)
#     # print ("The id is", idEntry)
#     # print ("The supervisor is", supNameEntry)
#
#     try:
#         sqlFormula = "INSERT INTO Internship (company, startMonth, startYear, endMonth, endYear, address, phoneNumber, totalHours, BaylorID, supervisorName) " \
#                      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
#         mycursor.execute(sqlFormula, (companyEntry, startmoEntry, startyrEntry, endmoEntry, endyrEntry, addressEntry, numberEntry, totHoursEntry, idEntry, supNameEntry))
#         mydb.commit()
#     except mysql.connector.Error as error:
#         print("could not be inserted")
