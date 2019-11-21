import mysql.connector
import tkinter as tk
from GUI_code import *
from User_Inputed_Data import *

#connect to database
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "password123",
    database = "GP"
)
#initialize cursor of database
mycursor = mydb.cursor()

myCursor.execute("CREATE DATABASE IF NOT EXISTS Journalismdb")

myCursor.execute("CREATE TABLE IF NOT EXISTS student(class VARCHAR(255), major_minor VARCHAR(255),"
                 "ID VARCHAR(255), last_name VARCHAR(255), first_name VARCHAR(255), email VARCHAR(255),"
                 "ADV_PR_semester VARCHAR(255), ADV_PR_grade INT, primary key (ID))")

myCursor.execute("CREATE TABLE IF NOT EXISTS internship(company VARCHAR(255), start_month DATE,"
                 "start_year DATE, end_month DATE, end_year DATE, total_hours TIME,"
                 "address VARCHAR(255), phone_number VARCHAR(255), ID VARCHAR(255),"
                 "sup_name VARCHAR(255), primary key(ID, sup_name))")

myCursor.execute("CREATE TABLE IF NOT EXISTS supervisor(company VARCHAR(255), name VARCHAR(255),"
                 "title VARCHAR(255), email VARCHAR(255), primary key (email))")

# no primary key selected yet
myCursor.execute("CREATE TABLE IF NOT EXISTS portfolio_review(reviewer_name VARCHAR(255), "
                 "review_date DATE, student_ID VARCHAR(255), question_label VARCHAR(255))")

# no primary key selected yet
myCursor.execute("CREATE TABLE IF NOT EXISTS answers(student_ID VARCHAR(255), answer VARCHAR(255),"
                 "label VARCHAR(255), question VARCHAR(255))")

# no primary key selected yet
myCursor.execute("CREATE TABLE IF NOT EXISTS questions(label VARCHAR(255), question VARCHAR(255),"
                 "comments VARCHAR(255))")

# no primary key selected yet
myCursor.execute("CREATE TABLE IF NOT EXISTS review(review_type VARCHAR(255), supervisor_name VARCHAr(255),"
                 "student_ID VARCHAR(255), question_label VARCHAR(255))")
