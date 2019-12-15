from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from flask_table import Table, Col,LinkCol
from wtforms import StringField, SelectField, IntegerField
from wtforms.validators import InputRequired, Email, Length, DataRequired, NumberRange
from flask_bootstrap import Bootstrap
from flask_bootstrap import Bootstrap

year_list = [(0, '---')]
for i in range(20):
    year_list.append((i + 1, 2000 + i))

month_list = [(0,'---'), (1, 'JAN'), (2,'FEB'), (3,'MAR'), (4,'APR'), (5,'MAY'), (6,'JUN'),
            (7,'JUL'), (8, 'AUG'), (9, 'SEP'), (10, 'OCT'), (11, 'NOV'), (12, 'DEC')]

class SupervisorTypesForm(FlaskForm):
    types = SelectField('Supervisor Review:', choices = [('Midterm Qualtrics Survey', 'Midterm Qualtrics Survey'),
                                                        ('Midterm Site Visit', 'Midterm Site Visit'),
                                                        ('End-of-Term Qualtrics Survey', 'End-of-Term Qualtrics Survey')])
    year = StringField('Enter Year:')

class StudentInfoForm(FlaskForm):
    student_id = StringField('student ID', validators=[InputRequired(), Length(9)])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email address')])


class StudentInfoForm2(FlaskForm):
    grade_list = [(0, '---'), (1, 'A'), (2, 'B'), (3, 'C'), (4, 'D'), (5, 'F')]
    class_list = [(0, '---'), (1, 'Freshman'), (2, 'Sophomore'), (3, 'Junior'), (4, 'Senior')]

    Class = SelectField('Classifcation', choices=class_list)
    major_minor = SelectField('Major or Minor', [DataRequired()], choices=[(0, "---"), (1, 'major'), (2, 'minor')])
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
    choices = [('Portfolio Review', 'Portfolio Review'),
               ('Student Review', 'Student Review'),
               ('Midterm Qualtrics Survey ', 'Midterm Qualtrics Survey'),
               ('Midterm Site Visit', 'Midterm Site Visit'),
               ('End-of-Term Qualtrics Survey','End-of-Term Qualtrics Survey')]

    select = SelectField('Search by:', choices=choices)

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
    review_type = StringField('Review Type', validators=[InputRequired()])

class SupervisorInternReviewQForm2(FlaskForm):
    startYear = SelectField('Start Year', choices=year_list)

class YearSearchForm(FlaskForm):
    year = StringField('Enter Year:')

#********************************************************************************************************************************************

class Results(Table):
    id = Col('Baylor ID ')
    fname = Col('First Name ')
    lname = Col('Last Name ')
    email = Col('Email ')
    semester = Col('Semester' )
    yr = Col('Year ')
    major_minor = Col('Major ')
    grade = Col('Grade ')
    classYear = Col('Class')
    supervisorReviewLink = LinkCol('Supervisor Reviews', 'supervisorReviewLink', url_kwargs=dict(id ='id'))
    portfolioReviewLink = LinkCol('Portfolio Reviews', 'portfolioReviewLink', url_kwargs=dict(id='id'))
    studentReviewLink = LinkCol('Student Reviews', 'studentReviewLink', url_kwargs=dict(id='id'))

#********************************************************************************************************************************************
class PortfolioReviewTable(Table):
    question = Col('Questions')
    answer = Col('Answers')
    comment = Col('Comments')
    reviewerName = Col('Reviewer Name')

class PortfolioReviewItem(object):
    def __init__(self,question,answer,comment,reviewerName):
        self.question = question
        self.answer = answer
        self.comment = comment
        self.reviewerName = reviewerName

    def setValues(self,list):
        self.question = list[0]
        self.answer = list[1]
        self.comment = list[2]
        self.reviewerName = list[3]
#********************************************************************************************************************************************
class StudentReviewTable(Table):
    question = Col('Questions')
    answer = Col('Answers')
    comment = Col('Comments')

class StudentReviewItem(object):
    def __init__(self,question,answer,comment):
        self.question = question
        self.answer = answer
        self.comment = comment

    def setValues(self,list):
        self.question = list[0]
        self.answer = list[1]
        self.comment = list[2]
#********************************************************************************************************************************************
class StudentReviewAllStudentsTable(Table):
    fname = Col('First Name')
    lname = Col('Last Name')
    sid = Col('Student ID')
    question = Col('Question')
    answer = Col('Answer')
    comment = Col('Comment')
    yr = Col('Year')

class StudentReviewItemAllStudents(object):
    def __init__(self, fname, lname, sid, question, answer, comment, yr):
        self.fname = fname
        self.lname = lname
        self.sid = sid
        self.question = question
        self.answer = answer
        self.comment = comment
        self.yr = yr

    def setValues(self, list):
        self.fname = list[0]
        self.lname = list[1]
        self.sid = list[2]
        self.question = list[3]
        self.answer = list[4]
        self.comment = list[5]
        self.yr = list[6]


#********************************************************************************************************************************************
class PortfolioReviewAllStudentsTable(Table):
    fname = Col('First Name')
    lname = Col('Last Name')
    sid = Col('Student ID')
    question = Col('Question')
    answer = Col('Answer')
    comment = Col('Comment')
    yr = Col('Year')
    revname = Col('Reviewer Name')

class PortfolioReviewItemAllStudents(object):
    def __init__(self, fname, lname, sid, question, answer, comment, yr, revname):
        self.fname = fname
        self.lname = lname
        self.sid = sid
        self.question = question
        self.answer = answer
        self.comment = comment
        self.yr = yr
        self.revname = revname

    def setValues(self, list):
        self.fname = list[0]
        self.lname = list[1]
        self.sid = list[2]
        self.question = list[3]
        self.answer = list[4]
        self.comment = list[5]
        self.yr = list[6]
        self.revname = list[7]
#********************************************************************************************************************************************

class SupervisorReviewItem(object):
    def __init__(self,question,answer,comment):
        self.question = question
        self.answer = answer
        self.comment = comment

    def setValues(self,list):
        self.question = list[0]
        self.answer = list[1]
        self.comment = list[2]

class SupervisorReviewsTable(Table):
    question = Col('Questions')
    answer = Col('Answers')
    comment = Col('Comments')
#********************************************************************************************************************************************


class Item(object):
    def __init__(self, id, fname, lname, email, semester, yr, major_minor, grade, classYear):
        self.id = id
        self.fname = fname
        self.lname = lname
        self.email = email
        self.semester = semester
        self.yr = yr
        self.major_minor = major_minor
        self.grade = grade
        self.classYear = classYear

    def setValues (self, list):
        self.id = list[0]
        self.fname = list[2]
        self.lname = list[1]
        self.email = list[3]
        self.semester = list[4]
        self.yr = list[8]
        self.major_minor = list[6]
        self.grade = list[7]
        self.classn = list[5]




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