from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from flask_table import Table, Col,LinkCol
from wtforms import StringField, SelectField, IntegerField
from wtforms.validators import InputRequired, Email, Length, DataRequired, NumberRange
from flask_bootstrap import Bootstrap
from Bootstrap_Form.TableSchema import reviewType, reviewByStudent, basicInfo
from TableSchema import *

# Create Classes for forms and web pages
year_list = [(0, '---')]
for i in range(20):
    year_list.append((i + 1, 2000 + i))

month_list = [(0,'---'), (1, 'JAN'), (2,'FEB'), (3,'MAR'), (4,'APR'), (5,'MAY'), (6,'JUN'),
            (7,'JUL'), (8, 'AUG'), (9, 'SEP'), (10, 'OCT'), (11, 'NOV'), (12, 'DEC')]

executeList = [ ]
def executeInsert(sqlStatement, executeList, mycursor, mydb):
    print ("The execute list is", executeList)
    try:
        mycursor.execute(sqlStatement, executeList)
        mydb.commit()
    except mysql.connector.Error as error:
        print ("duplicate entry")
    mydb.commit()
    del executeList[:]



class StudentInfoForm(FlaskForm):
    student_id = StringField('student ID', validators=[InputRequired(), Length(9)])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email address')])
    Class = StringField('Class', validators=[InputRequired()])


class StudentInfoForm2(FlaskForm):
    grade_list = [(0, '---'), (1, 'A'), (2, 'B'), (3, 'C'), (4, 'D'), (5, 'F')]

    major_minor = SelectField('Major/Minor', [DataRequired()], choices=[(0, "---"), (1, 'major'), (2, 'minor')])
    ADV_PR_Semester = SelectField('ADV PR Semester', choices=[(0, '---'), (1, 'Fall'), (2, 'Spring')])
    ADV_PR_Year = SelectField('Year', choices=year_list)
    ADV_PR_Grade = SelectField('Grade', choices=grade_list)

class StudentSearchForm(FlaskForm):
    choices = [('Baylor ID', 'Baylor ID'),
               ('Name', 'Name')]
    select = SelectField('Search by:', choices=choices)
    search = StringField('ID')
    firstName = StringField('First name')
    lastName = StringField('Last name')


class ReviewSearchForm(FlaskForm):
    choices = [('Review1', 'Review1'),
               ('Review2', 'Review2'),
               ('Review3', 'Review3'),
               ('Review4', 'Review4')]

    select = SelectField('Search by:', choices=choices)
    searchID = StringField('ID')


class SupervisorInfoForm(FlaskForm):
    company = StringField('Company', validators=[InputRequired()])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    title = StringField('Title', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email address')])

class InternshipInfoForm(FlaskForm):
    email = StringField('Supervisor Email', validators=[InputRequired(), Email(message='Invalid email address')])
    address = StringField('Company Address', validators=[InputRequired()])
    phone = StringField('Phone Number', validators=[InputRequired()])
    tot_hours = IntegerField('Total Hours', validators=[InputRequired()])
    buID = StringField('Student ID', validators=[InputRequired(), Length(9)])

class InternshipInfoForm2(FlaskForm):
    startMonth = SelectField('Start Month', choices=month_list)
    startYear = SelectField('Start Year', choices=year_list)
    endMonth = SelectField('End Month', choices=month_list)
    endYear = SelectField('End Year', choices=year_list)

class SupervisorInternReviewQForm(FlaskForm):
    label = StringField('Label', validators=[InputRequired()])
    question = StringField('Question', validators=[InputRequired()])

class SupervisorInternReviewQForm2(FlaskForm):
    startYear = SelectField('Start Year', choices=year_list)
    review_type = SelectField('Review Type', choices=[(0,'---'), (1,'Midterm Qualtrics Survey'), (2,'Midterm Site Visit'),
                                                      (3,'End-of-Term Qualtrics Survey')])

class Student_PortfolioReviewQForm(FlaskForm):
    label = StringField('Label', validators=[InputRequired()])
    question = StringField('Question', validators=[InputRequired()])

class Student_PortfolioReviewQForm2(FlaskForm):
    startYear = SelectField('Start Year', choices=year_list)

class ReviewQuestions(FlaskForm):
    review_list = SelectField('Review Question Option', choices=[(0,'---'), (1,'Portfolio Review'),
                                                                 (2,'Supervisor Intern Review'),
                                                                 (3,'Student Review')])