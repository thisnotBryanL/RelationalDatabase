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

#Create Tables if they do not exist
createTables(mycursor)

#get student information
firstPage(mycursor, mydb)
#Create Tables and Insert data