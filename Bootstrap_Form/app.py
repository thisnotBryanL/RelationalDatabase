from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from flask_table import Table, Col,LinkCol
from wtforms import StringField, SelectField, IntegerField
from wtforms.validators import InputRequired, Email, Length, DataRequired, NumberRange
from flask_bootstrap import Bootstrap
from Bootstrap_Form.TableSchema import reviewType, reviewByStudent, basicInfo
from TableSchema import *
import mysql.connector


#connect to database
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "BUboxtop2020",
    database = "testdb"
)

#initialize cursor of database
mycursor = mydb.cursor()

# Create Tables if they do not exist
createTables(mycursor)
print('done')

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
        elif request.form['option'] == 'Review Questions':
            return redirect(url_for('ReviewQ'))
    return render_template('index.html')


######################## INFORMATION INPUT FORMS ########################

@app.route('/input_student_info', methods=['GET', 'POST'])
def studentInfo():
    form = StudentInfoForm()
    form2 = StudentInfoForm2()
    if (form.validate_on_submit() and form2.major_minor.data != '0' and form2.ADV_PR_Semester.data != '0' and
        form2.ADV_PR_Grade.data != '0' and form2.ADV_PR_Year.data != '0'):
       #insert data into database
        majororminor = " "
        if form2.data['major_minor'] == '1':
           majororminor = "major"
        else:
            majororminor = "minor"

        semester = " "
        if form2.data['ADV_PR_Semester'] == '1':
           semester = "Fall"
        else:
           semester = "Spring"

        grade = " "
        if form2.data['ADV_PR_Grade'] == '1':
           grade = "A"
        elif form2.data['ADV_PR_Grade'] == '2':
           grade = "B"
        elif form2.data['ADV_PR_Grade'] == '3':
           grade = "C"
        elif form2.data['ADV_PR_Grade'] == '4':
           grade = "D"
        elif form2.data['ADV_PR_Grade'] == '5':
           grade = "F"

        year = " "
        year = int(form2.data['ADV_PR_Year']) - 1
        yr = "20" + str(year)

        executeList.append(form.data['student_id'])
        executeList.append(form.data['last_name'])
        executeList.append(form.data['first_name'])
        executeList.append(form.data['email'])
        executeList.append(semester)
        executeList.append(form.data['Class'])
        executeList.append(majororminor)
        executeList.append(grade)
        executeList.append(yr)


        print ("the executeList is", executeList)
        sql = "INSERT INTO StudentInfo (`BaylorID`, `lastName`, `firstName`, `emailAddress`, `ADV_PR_semester`, `class`, `major_minor`, `ADV_PR_grade`, `ADV_PR_year`)" \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        executeInsert(sql, executeList, mycursor,mydb)
       #END INSERT DATA
        # if request.form['option'] == 'home':
        #     return redirect(url_for('index'))
        # else:
        #     return 'Redirect'
    # if trueorfalse == False:
    #     error1 = "Student with ID #" + executeList[0] + " has already been inserted'\n'" \
    #                                                     "If you would like to update their information, please go to the update page"
    #
    #     return render_template('submit.html', form=form, form2=form2, error=error)
    # else:
    return render_template('submit.html', form=form, form2=form2)

@app.route('/input_supervisor_info', methods=['GET', 'POST'])
def supervisorInfo():
    form = SupervisorInfoForm()
    if form.validate_on_submit():
        executeList.append(form.data["company"])
        executeList.append(form.data["first_name"] + " " + form.data["last_name"])
        executeList.append(form.data["title"])
        executeList.append(form.data["email"])
        sql = "INSERT INTO Supervisor (`company`, `supervisorName`, `title`, `email`) VALUES (%s, %s, %s, %s)"
        executeInsert(sql, executeList, mycursor, mydb)

        # if request.form['option'] == 'home':
        #     return redirect(url_for('index'))
        # else:
        #     return 'Successfully submitted supervisor information!'
    return render_template('supervisor.html', form=form)

@app.route('/input_internship_info', methods=['GET', 'POST'])
def internshipInfo():
    form = InternshipInfoForm()
    form2 = InternshipInfoForm2()
    if form.validate_on_submit():
        executeList.append(form.data['email'])
        month = " "
        m = form2.data['startMonth']
        for (index, mon) in month_list:
            if str(index) == m:
                month = mon
                break
        executeList.append(month)
        year = " "
        y = form2.data['startYear']
        for (index, yr) in year_list:
            if str(index) == y:
                year = yr
                break
        executeList.append(str(year))
        month = " "
        m = form2.data['endMonth']
        for (index, mon) in month_list:
            if str(index) == m:
                month = mon
                break
        executeList.append(month)
        year = " "
        y = form2.data['endYear']
        for (index, yr) in year_list:
            if str(index) == y:
                year = yr
                break
        executeList.append(str(year))
        executeList.append(form.data['address'])
        executeList.append(form.data['phone'])
        executeList.append(form.data['tot_hours'])
        executeList.append(form.data['buID'])

        sql = "INSERT INTO Internship (`supervisorEmail`, `startMonth`, `startYear`, `endMonth`, `endYear`, `address`, `phoneNumber`, `totalHours`, `BaylorID`)" \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        executeInsert(sql, executeList, mycursor, mydb)

        # if request.form['option'] == 'home':
        #     return redirect(url_for('index'))
        # else:
        #     return 'Successfully submitted internship information!'
    return render_template('internship.html', form=form, form2=form2)

@app.route('/ReviewQ_info', methods=['GET', 'POST'])
def ReviewQ():
    # form = SupervisorInternReviewQForm()
    # form2 = SupervisorInternReviewQForm2()
    form = ReviewQuestions()
    # if form.validate_on_submit():
#        if request.form['option'] == 'home':
#            return redirect(url_for('index'))
#        else:
#             return 'Successfully submitted Review information!'
    if form.review_list.data == '1':
        return redirect(url_for('PortfolioRevQ'))
    elif form.review_list.data == '2':
        return redirect(url_for('SupInternRevQ'))
    elif form.review_list.data == '3':
        return redirect(url_for('StudentRevQ'))
    return render_template('ReviewQuestions.html', form=form)

@app.route('/ReviewQ_info/Student_Review_Questions', methods=['GET','POST'])
def StudentRevQ():
    form = Student_PortfolioReviewQForm()
    form2 = Student_PortfolioReviewQForm2()
    if form.validate_on_submit():
        return redirect(url_for('ReviewQ'))
    return render_template('Student_PortfolioReviewQ.html', form=form, form2=form2, header='Student')

@app.route('/ReviewQ_info/Supervisor_Intern_Review_Questions', methods=['GET','POST'])
def SupInternRevQ():
    form = SupervisorInternReviewQForm()
    form2 = SupervisorInternReviewQForm2()
    if form.validate_on_submit():
        return redirect(url_for('ReviewQ'))
    return render_template('SupervisorInternReviewQ.html', form=form, form2=form2)

@app.route('/ReviewQ_info/Portfolio_Review_Questions', methods=['GET','POST'])
def PortfolioRevQ():
    form = Student_PortfolioReviewQForm()
    form2 = Student_PortfolioReviewQForm2()
    if form.validate_on_submit():
        return redirect(url_for('ReviewQ'))
    return render_template('Student_PortfolioReviewQ.html', form=form, form2=form2, header='Portfolio')


######################## SUDENT QUERY DATA ########################

@app.route('/studentQuery', methods=['GET', "POST"])
def studentQueryHomePage():
    del studentInfoList [:]
    search = StudentSearchForm()
    if request.method == 'POST':
        if(search.select.data == "Baylor ID"):
            if len(search.search.data) == 9 and search.search.data.isdigit():
                return search_results(search)
            else:
                flash('ID must be 9 digits')
        elif (search.select.data == "Name"):
            if len(search.firstName.data) > 0 and len(search.lastName.data) > 0:
                return search_results(search)
            else:
                flash('Please enter both first and last name')
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
            studentInfoList.append(str(id))
            studentInfoList.append(str(yearNum))
            SuperVisorList = studentInfoList


            print(studentInfoList)
            print(SuperVisorList)

            results = reviewType(mycursor, mydb, "SUPidyear", SuperVisorList)

            # Clears the list after use, or else append will keep appending
            # if back button is pushed
            studentInfoList.clear()
            SuperVisorList.clear()

            if len(results) > 0:
                items = []
                for row in results:
                    instance = SuperVisorReviewItem('', '', '')
                    instance.setValues(row)
                    items.append(instance)

                superVisorTable = SuperVisorReviewsTable(items)
                superVisorTable.border = True
                return render_template('results.html', table=superVisorTable)
            else:
                flash('No results found!')
                return redirect(f'/item/{id}')
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

            if len(results) > 0:
                items = []
                for row in results:
                    instance = PortfolioReviewItem('', '', '', '')
                    instance.setValues(row)
                    items.append(instance)

                portfolioReviewTable = PortfolioReviewTable(items)
                portfolioReviewTable.border = True
                return render_template('results.html', table=portfolioReviewTable)
            else:
                flash('No results found!')
                return redirect(f'/item1/{id}')
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
                return redirect(f'/item2/{id}')
        else:
            flash('Please enter a 4 digit year!')
    return render_template('yearForm.html' ,form=yearSearch)


@app.route('/reviewQuery', methods=['GET', "POST"])
def reviewQueryHomePage():
    search = ReviewSearchForm()
    if request.method == 'POST':
        if (len(search.searchID.data) > 0):
            if len(search.searchID.data) == 9 and search.search.data.isdigit():
                return search_resultsForReview(search)
            else:
                flash('ID must be 9 digits')
        return search_resultsForReview(search)
    return render_template('reviewQueryHome.html', form=search)

@app.route('/reviewQuery/results')
def search_resultsForReview(search):
    results = []
    choice = " "
    stringf = " "

    if search.select.data == "Review1":
        print("REVIEW 1")
        choice = "idTrue"
        #Query the Review
        '''
        search_string = search.data['search']
        results.append(search_string)
        stringf = search_string
        studentInfoList.append(stringf)
        '''

        #elif statements for the other review types

        #elif statement if BU ID was included


    queryResults = []
    print(len(queryResults))

    if len(queryResults) == 0:
        flash('No results found!')


    ''''
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
        '''
    return redirect('/reviewQuery')



if __name__ == '__main__':
    app.run(debug=True)
