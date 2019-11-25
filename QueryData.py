import mysql.connector
import tkinter as tk
import GUIClass
from User_Inputed_Data import *

def main():
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
    firstpage = GUIClass.PageOne(mycursor, mydb)
    #Create Tables and Insert data

main()
