from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from flask_table import Table, Col,LinkCol
from wtforms import StringField, SelectField, IntegerField
from wtforms.validators import InputRequired, Email, Length, DataRequired, NumberRange
from flask_bootstrap import Bootstrap
from TableSchema import *
import mysql.connector


#connect to database
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "password123",
    database = "GP"
)

#initialize cursor of database
mycursor = mydb.cursor()

# Create Tables if they do not exist
createTables(mycursor)

studentInfoList = []

# Create app
app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'DontTellAnyone'

# Create Classes for forms and web pages
year_list = [(0, '---')]
for i in range(20):
    year_list.append((i + 1, 2000 + i))

month_list = [(0,'---'), (1, 'JAN'), (2,'FEB'), (3,'MAR'), (4,'APR'), (5,'MAY'), (6,'JUN'),
            (7,'JUL'), (8, 'AUG'), (9, 'SEP'), (10, 'OCT'), (11, 'NOV'), (12, 'DEC')]

class createInsertIntoStudentList():
    def __init__ (self, student_id, first_name, last_name, email, Class ):
        self.executeList = [" "] * 5
        self.executeList[0] = student_id
        self.executeList[2] = first_name
        self.executeList[1] = last_name
        self.executeList[3] = email
        self.executeList[4] = Class

    def getExecuteList(self):
        return self.executeList

        # sql = "INSERT INTO StudentInfo (`BaylorID`, `lastName`, `firstName`, `emailAddress`, `class`)" \
        #       "VALUES (%s, %s, %s, %s, %s)"
        # mycursor.execute(sql, self.executeList)
        # mycursor.execute("insert into PortfolioResponses values('photo', '2018', '123456789', 'saw the skyline', 'how observational', '2019-05-01', 'Julius Caesar')")
        #
        # mydb.commit

StudentInfoFormExecuteList = [ ]
class StudentInfoForm(FlaskForm):
    student_id = StringField('student ID', validators=[InputRequired(), Length(9)])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email address')])
    Class = StringField('Class', validators=[InputRequired()])

    instance = createInsertIntoStudentList (student_id, first_name, last_name, email, Class)
    StudentInfoFormExecuteList = instance.getExecuteList()


class StudentInfoForm2(FlaskForm):
    grade_list = [(0, '---'), (1, 'A'), (2, 'B'), (3, 'C'), (4, 'D'), (5, 'F')]

    major_minor = SelectField('Major/Minor', [DataRequired()], choices=[(0, "---"), (1, 'major'), (2, 'minor')])
    ADV_PR_Semester = SelectField('ADV PR Semester', choices=[(0, '---'), (1, 'Fall'), (2, 'Spring')])
    ADV_PR_Year = SelectField('Year', choices=year_list)
    ADV_PR_Grade = SelectField('Grade', choices=grade_list)

class StudentSearchForm(FlaskForm):
    choices = [('Baylor ID', 'Baylor ID'),
               ('Name', 'Name')]
    select = SelectField('Search for Student by:', choices=choices)
    search = StringField('ID')
    firstName = StringField('First name')
    lastName = StringField('Last name')

class SupervisorInfoForm(FlaskForm):
    company = StringField('Company', validators=[InputRequired()])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    title = StringField('Title', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email address')])

class InternshipInfoForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email address')])
    address = StringField('Address', validators=[InputRequired()])
    phone = StringField('Phone Number', validators=[InputRequired()])
    tot_hours = IntegerField('Total Hours', validators=[InputRequired()])
    buID = StringField('Student ID', validators=[InputRequired(), Length(9)])

class InternshipInfoForm2(FlaskForm):
    startMonth = SelectField('Start Month', choices=month_list)
    startYear = SelectField('Start Year', choices=year_list)
    endMonth = SelectField('Start Month', choices=month_list)
    endYear = SelectField('Start Year', choices=year_list)

class SupervisorInternReviewQForm(FlaskForm):
    label = StringField('Label', validators=[InputRequired()])
    question = StringField('Question', validators=[InputRequired()])
    review_type = StringField('Review Type', validators=[InputRequired()])

class SupervisorInternReviewQForm2(FlaskForm):
    startYear = SelectField('Start Year', choices=year_list)




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
    supervisorReviewLink = LinkCol('Supervisor Reviews', 'supervisorReviewLink', url_kwargs=dict(id='id'))
    portfolioReviewLink = LinkCol('Portfolio Reviews', 'portfolioReviewLink', url_kwargs=dict(id='id'))
    studentReviewLink = LinkCol('Student Reviews', 'studentReviewLink', url_kwargs=dict(id='id'))


class SuperVisorReviewsTable(Table):
    question = Col('Questions')
    answer = Col('Answers')
    comment = Col('Comments')

class PortfolioReviewTable(Table):
    question = Col('Questions')
    answer = Col('Answers')
    comment = Col('Comments')
    reviewerName = Col('Reviewer Name')

class StudentReviewTable(Table):
    question = Col('Questions')
    answer = Col('Answers')
    comment = Col('Comments')

class SuperVisorReviewItem(object):
    def __init__(self,question,answer,comment):
        self.question = question
        self.answer = answer
        self.comment = comment

    def setValues(self,list):
        self.question = list[0]
        self.answer = list[1]
        self.comment = list[2]

class StudentReviewItem(object):
    def __init__(self,question,answer,comment):
        self.question = question
        self.answer = answer
        self.comment = comment

    def setValues(self,list):
        self.question = list[0]
        self.answer = list[1]
        self.comment = list[2]


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

class YearSearchForm(FlaskForm):
    year = StringField('Enter Year:')


@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        if request.form['option'] == 'Look Up Student Information':
            return redirect(url_for('studentQueryHomePage'))
        elif request.form['option'] == 'Enter Student Information':
            return redirect(url_for('studentInfo'))
        elif request.form['option'] == 'Enter Supervisor Information':
            return redirect(url_for('supervisorInfo'))
        elif request.form['option'] == 'Enter Internship Information':
            return redirect(url_for('internshipInfo'))
        elif request.form['option'] == 'Supervisor\'s Intern Review Quesitons':
            return redirect(url_for('SupInternReviewInfo'))
    return render_template('index.html')


######################## INFORMATION INPUT FORMS ########################
@app.route('/input_student_info', methods=['GET', 'POST'])
def studentInfo():
    form = StudentInfoForm()
    print ("The execute list is", StudentInfoFormExecuteList)

    form2 = StudentInfoForm2()
    if (form.validate_on_submit() and form2.major_minor.data != '0' and form2.ADV_PR_Semester.data != '0' and
        form2.ADV_PR_Grade.data != '0' and form2.ADV_PR_Year.data != '0'):
        if request.form['option'] == 'home':
            print ("The execute list is", StudentInfoFormExecuteList)
            return redirect(url_for('index'))
        else:
            return 'Redirect'
    return render_template('submit.html', form=form, form2=form2)

@app.route('/input_supervisor_info', methods=['GET', 'POST'])
def supervisorInfo():
    form = SupervisorInfoForm()
    if form.validate_on_submit():
        if request.form['option'] == 'home':
            return redirect(url_for('index'))
        else:
            return 'Successfully submitted supervisor information!'
    return render_template('supervisor.html', form=form)

@app.route('/input_internship_info', methods=['GET', 'POST'])
def internshipInfo():
    form = InternshipInfoForm()
    form2 = InternshipInfoForm2()
    if form.validate_on_submit():
        if request.form['option'] == 'home':
            return redirect(url_for('index'))
        else:
            return 'Successfully submitted internship information!'
    return render_template('internship.html', form=form, form2=form2)

@app.route('/input_SupervisorInternReviewQ_info', methods=['GET', 'POST'])
def SupInternReviewInfo():
    form = SupervisorInternReviewQForm()
    form2 = SupervisorInternReviewQForm2()
    if form.validate_on_submit():
#        if request.form['option'] == 'home':
#            return redirect(url_for('index'))
#        else:
            return 'Successfully submitted Review information!'
    return render_template('SupervisorInternReviewQ.html', form=form, form2=form2)

######################## SUDENT QUERY DATA ########################

@app.route('/studentQuery', methods=['GET', "POST"])
def studentQueryHomePage():
    del studentInfoList [:]
    search = StudentSearchForm()
    if request.method == 'POST':
        return search_results(search)
    return render_template('studentQueryHome.html', form=search)


@app.route('/studentQuery/results')
def search_results(search):
    results = []
    choice = " "
    stringf = " "

    if search.select.data == "Baylor ID":
        print("BUID")
        choice = "idTrue"
        #Query the BU ID
        search_string = search.data['search']
        results.append(search_string)
        stringf = search_string
        studentInfoList.append(stringf)

    else:
        print("BUNAME")
        firstNameSearch = search.data['firstName']
        lastNameSearch = search.data['lastName']
        choice = "nameTrue"
        results.append(firstNameSearch)
        results.append(lastNameSearch)
        stringf = firstNameSearch + " " + lastNameSearch
        studentInfoList.append(firstNameSearch)
        studentInfoList.append(lastNameSearch)



    queryResults = []
    queryResults = basicInfo(mycursor, mydb, choice, results)
    print("query results", queryResults)

    if len(queryResults) == 0:
        flash('No results found!')
        return redirect('/studentQuery')


    elif search.data['search'] == stringf:
        items = []
        for row in queryResults:
            instance = Item('', '', '', '', '', '', '', '', '')
            instance.setValues(row)
            items.append(instance)
        table = Results(items)
        table.border = True
        return render_template('results.html', table=table)

    elif search.data['firstName'] == firstNameSearch and search.data['lastName'] == lastNameSearch:
        items = []
        for row in queryResults:
            instance = Item('', '', '', '', '', '', '', '', '')
            instance.setValues(row)
            items.append(instance)
        table = Results(items)
        table.border = True
        return render_template('results.html', table=table)


@app.route('/item/<int:id>', methods=['GET', 'POST'])
def supervisorReviewLink(id):
    # Ask for YEAR of review
    yearSearch = YearSearchForm()
    print('here')
    if request.method == 'POST':
        yearNum = yearSearch.data['year']

        if len(yearNum) == 4 and yearNum.isdigit():
            print(yearNum)
            # Query the Supervisor Reviews for the specific student using their BUID and Year
            # and add it to results
            studentInfoList.append(str(yearNum))
            studentReviewLink = studentInfoList
            print ("student review", studentInfoList)

            #reviewType(mycursor, mydb, "idyear", executeList)
            results = [SuperVisorReviewItem('QUESTION 1', 'ANSWER1',
                                            'This is a commnt that is supposed to be kind of l'
                                            'ong to see how this would fit in to the table '
                                            'lol hahahahahahha hehehehehe hohohohohohohho')]  # THE query information

            superVisorTable = SuperVisorReviewsTable(results)
            superVisorTable.border = True

            if len(results) > 0:
                return render_template('results.html', table=superVisorTable)
            else:
                flash('No results found!')
                return redirect(url_for('studentQueryHomePage'))
        else:
            flash('Please enter a 4 digit year!')
    return render_template('yearForm.html' ,form=yearSearch)

@app.route('/item1/<int:id>', methods=['GET', 'POST'])
def portfolioReviewLink(id):
    # Ask for YEAR of review
    yearSearch = YearSearchForm()
    print('here')
    if request.method == 'POST':
        yearNum = yearSearch.data['year']

        if len(yearNum) == 4 and yearNum.isdigit():
            print(yearNum)
            # Query the Portfolio Reviews for the specific student using their BUID and Year
            # and add it to results
            studentInfoList.append(str(yearNum))
            PortfolioList = studentInfoList
            print ("list:", PortfolioList)
            results = reviewType(mycursor, mydb, "idyear", PortfolioList)
            print (results)

            # results = [PortfolioReviewItem('QUESTION 1', 'ANSWER1',
            #                                 'This is a commnt that is supposed to be kind of l'
            #                                 'ong to see how this would fit in to the table '
            #                                 'lol hahahahahahha hehehehehe hohohohohohohho')]  # THE query information

            # portfolioReviewTable = PortfolioReviewTable(results)
            # portfolioReviewTable.border = True

            if len(results) > 0:
                items = []
                for row in results:
                    instance = PortfolioReviewItem('', '', '', ' ')
                    instance.setValues(row)
                    items.append(instance)

                portfolioReviewTable = PortfolioReviewTable(items)
                portfolioReviewTable.border = True
                return render_template('results.html', table=portfolioReviewTable)
            else:
                flash('No results found!')
                return redirect(url_for('studentQueryHomePage'))
        else:
            flash('Please enter a 4 digit year!')
    return render_template('yearForm.html' ,form=yearSearch)

@app.route('/item2/<int:id>', methods=['GET', 'POST'])
def studentReviewLink(id):
    # Ask for YEAR of review
    yearSearch = YearSearchForm()
    print('here')
    if request.method == 'POST':
        yearNum = yearSearch.data['year']

        if len(yearNum) == 4 and yearNum.isdigit():
            print(yearNum)
            # Query the Supervisor Reviews for the specific student using their BUID and Year
            # and add it to results
            studentInfoList.append(str(yearNum))
            studentRList = studentInfoList
            results = reviewByStudent(mycursor, mydb, "idyear", studentRList)

            # results = [StudentReviewItem('QUESTION 1', 'ANSWER1',
            #                                 'This is a commnt that is supposed to be kind of l'
            #                                 'ong to see how this would fit in to the table '
            #                                 'lol hahahahahahha hehehehehe hohohohohohohho')]  # THE query information

            if len(results) > 0:
                items = []
                for row in results:
                    instance = StudentReviewItem('', '', ' ')
                    instance.setValues(row)
                    items.append(instance)
                    studentReviewTable = StudentReviewTable(items)
                    studentReviewTable.border = True
                return render_template('results.html', table=studentReviewTable)
            else:
                flash('No results found!')
                return redirect(url_for('studentQueryHomePage'))
        else:
            flash('Please enter a 4 digit year!')
    return render_template('yearForm.html' ,form=yearSearch)


if __name__ == '__main__':
    app.run(debug=True)
