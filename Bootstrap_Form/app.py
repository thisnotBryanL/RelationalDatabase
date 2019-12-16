from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from flask_table import Table, Col,LinkCol
from wtforms import StringField, SelectField, IntegerField
from wtforms.validators import InputRequired, Email, Length, DataRequired, NumberRange
from flask_bootstrap import Bootstrap
from flask_bootstrap import Bootstrap
from Bootstrap_Form.TableSchema import reviewByStudent, basicInfo
from TableSchema import *
import mysql.connector
from Forms import *


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
print('done')

studentInfoList = []

# Create app
app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'DontTellAnyone'

# Create Classes for forms and web pages


executeList = [ ]
def executeInsert(sqlStatement, executeList, mycursor, mydb):
    print ("The execute list is", executeList)
    try:
        mycursor.execute(sqlStatement, executeList)
        del executeList[:]
        mydb.commit()
    except mysql.connector.Error as error:
        del executeList[:]
        print ("duplicate entry")
        flash ("Student with id #" + executeList[0] + " has already been entered")


def studentExecuteInsert(sqlStatement, executeList, mycursor, mydb):
    print ("The execute list is", executeList)
    try:
        mycursor.execute(sqlStatement, executeList)
    except mysql.connector.Error as error:
        print ("duplicate entry")
        flash ("Student with id #" + executeList[0] + " has already been entered")
    mydb.commit()
    del executeList[:]

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
        studentExecuteInsert(sql, executeList, mycursor,mydb)
       #END INSERT DATA
        # if request.form['option'] == 'home':
        #     return redirect(url_for('index'))
        # else:
        #     return 'Redirect'

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


@app.route('/item/<string:id>', methods=['GET', 'POST'])
def supervisorReviewLink(id):
    # Ask for YEAR of review
    types = SupervisorTypesForm()
    print('here')
    if request.method == 'POST':
        yearNum = types.data['year']

        if len(yearNum) == 4 and yearNum.isdigit():
            print(yearNum)
            # Query the Supervisor Reviews for the specific student using their BUID and Year
            # and add it to results
            studentInfoList.append(str(yearNum))
            SupervisorList = studentInfoList

            print(studentInfoList)
            print(SupervisorList)

            if types.data['types'] == "Midterm Qualtrics Survey":
                SupervisorList.append("midterm")

            elif types.data['types'] == "Midterm Site Visit":
                SupervisorList.append("site")

            elif types.data['types'] == "End-of-Term Qualtrics Survey":
                SupervisorList.append("site")

            print(types.data['types'])

            print ("SupervisorList", SupervisorList)
            results = supReviewType(mycursor, "idyear", SupervisorList)
            del studentInfoList[-1]
            SupervisorList.clear()

            if len(results) > 0:
                items = []
                for row in results:
                    instance = SupervisorReviewItem('', '', '')
                    instance.setValues(row)
                    items.append(instance)

                supervisorTable = SupervisorReviewsTable(items)
                supervisorTable.border = True
                return render_template('results.html', table=supervisorTable)
            else:
                flash('No results found!')
                return redirect(f'/item/{id}')
        else:
            flash('Please enter a 4 digit year!')
    return render_template('SupervisorTypes.html', form = types )

@app.route('/item1/<string:id>', methods=['GET', 'POST'])
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

            results = portfolioReview(mycursor, mydb, "idyear", PortfolioList)

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
                del studentInfoList[-1]
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
            print ("studentRList", studentRList)
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
                del studentInfoList[-1]
                return redirect(f'/item2/{id}')
        else:
            flash('Please enter a 4 digit year!')
    return render_template('yearForm.html' ,form=yearSearch)


@app.route('/reviewQuery', methods=['GET', "POST"])
def reviewQueryHomePage():
    search = ReviewSearchForm()
    if request.method == 'POST':
        return search_resultsForReview(search)
    return render_template('reviewQueryHome.html', form=search)

@app.route('/reviewQuery/results')
def search_resultsForReview(search):

    items = []
    if search.select.data == "Portfolio Review":
        queryResults = displayPortfolioReviews(mycursor, mydb)

        if len(queryResults) == 0:
            flash('No results found!')
        else:
            for row in queryResults:
                print (row)
                instance = PortfolioReviewItemAllStudents('', '', '', '', '', '', '', '')
                instance.setValues(row)
                items.append(instance)
            table = PortfolioReviewAllStudentsTable(items)
            table.border = True
            return render_template('results.html', table=table)

    elif search.select.data == "Student Review":
        queryResults = displayStudentReviews(mycursor, mydb)
        if len(queryResults) == 0:
            flash('No results found!')
        else:
            for row in queryResults:
                print (row)
                instance = StudentReviewItemAllStudents('', '', '', '', '', '', '')
                instance.setValues(row)
                items.append(instance)
            table = StudentReviewAllStudentsTable(items)
            table.border = True
            return render_template('results.html', table=table)
    else:
        exList = []
        if search.select.data == "Midterm Qualtrics Survey ":
            exList.append("midterm")

        elif search.select.data == "Midterm Site Visit":
            exList.append("site")

        elif search.select.data == "End-of-Term Qualtrics Survey":
            exList.append("site")

        print (search.select.data)

        queryResults = displayReviews(mycursor, mydb, exList)
        if len(queryResults) == 0:
            flash('No results found!')
        else:
            for row in queryResults:
                print (row)
                instance = StudentReviewItemAllStudents('', '', '', '', '', '', '')
                instance.setValues(row)
                items.append(instance)
            table = StudentReviewAllStudentsTable(items)
            table.border = True
            return render_template('results.html', table=table)
            return render_template('results.html', table=table)



    return redirect('/reviewQuery')



if __name__ == '__main__':
    app.run(debug=True)
