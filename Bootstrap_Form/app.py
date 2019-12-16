from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from flask_table import Table, Col,LinkCol
from wtforms import StringField, SelectField, IntegerField
from wtforms.validators import InputRequired, Email, Length, DataRequired, NumberRange
from flask_bootstrap import Bootstrap
from flask_bootstrap import Bootstrap
from Bootstrap_Form.TableSchema import reviewByStudent, basicInfo
from Bootstrap_Form.TableSchema import reviewByStudent, basicInfo
from TableSchema import *
from Bootstrap_Form.Forms import *
import mysql.connector

#connect to database
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "hoangdieu72",
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
        elif request.form['option'] == 'Look up Review By Label':
            return redirect(url_for('questionSearchPage'))
        elif request.form['option'] == 'Enter Student Information':
            return redirect(url_for('studentInfo'))
        elif request.form['option'] == 'Enter Supervisor Information':
            return redirect(url_for('supervisorInfo'))
        elif request.form['option'] == 'Enter Internship Information':
            return redirect(url_for('internshipInfo'))
        elif request.form['option'] == 'Review Questions':
            return redirect(url_for('ReviewQ'))
        elif request.form['option'] == 'Look up Review Questions':
            return redirect(url_for('REAL_Question_search_page'))
    return render_template('index.html')


######################## INFORMATION INPUT FORMS ########################

@app.route('/input_student_info', methods=['GET', 'POST'])
def studentInfo():
    executeList = []
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
        executeList.append(form2.data['Class'])
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
    executeList = []
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
    executeList = []
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
        print ("the execute list is", executeList)

        sql = "INSERT INTO Internship (`supervisorEmail`, `startMonth`, `startYear`, `endMonth`, `endYear`, `address`, `phoneNumber`, `totalHours`, `BaylorID`)" \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

        mycursor.execute(sql, executeList)
        mydb.commit()
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
    studentInfoList = []
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
    print (str(id))
    # Ask for YEAR of review
    types = SupervisorTypesForm()
    print('here')
    exList = []
    exList.append(str(id))
    if request.method == 'POST':
        yearNum = types.data['year']

        if len(yearNum) == 4 and yearNum.isdigit():
            print(yearNum)
            # Query the Supervisor Reviews for the specific student using their BUID and Year
            # and add it to results
            exList.append(str(yearNum))
            print(exList)

            if types.data['types'] == "Midterm Qualtrics Survey":
                exList.append("midterm")
                exList.append("midterm")


            elif types.data['types'] == "Midterm Site Visit":
                exList.append("site")
                exList.append("site")


            elif types.data['types'] == "End-of-Term Qualtrics Survey":
                exList.append("endterm")
                exList.append("endterm")


            print(types.data['types'])

            print ("SupervisorList", exList)
            results = supReviewType(mycursor, "idyear", exList)

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

        elif len(yearNum) != 4 and yearNum.isdigit():
            flash('Please enter a 4 digit year or leave year field blank!')
        else:
            if types.data['types'] == "Midterm Qualtrics Survey":
                exList.append("midterm")
                exList.append("midterm")


            elif types.data['types'] == "Midterm Site Visit":
                exList.append("site")
                exList.append("site")


            elif types.data['types'] == "End-of-Term Qualtrics Survey":
                exList.append("endterm")
                exList.append("endterm")

            print(types.data['types'])

            print("SupervisorList", exList)
            results = supReviewType(mycursor, "id", exList)

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

    return render_template('SupervisorTypes.html', form = types )

@app.route('/item3/<string:id>', methods=['GET', 'POST'])
def yearLink(id):
    print (str(id))
    # Ask for YEAR of review
    year = YearSearchForm()
    print('here')
    exList = []
    exList.append(str(id))
    if request.method == 'POST':
        yearNum = year.data['year']

        if len(yearNum) == 4 and yearNum.isdigit():
            print(yearNum)
            # Query the Supervisor Reviews for the specific student using their BUID and Year
            # and add it to results
            exList.append(str(yearNum))
            exList.append(str(yearNum))
            print ("exList is", exList)

            supResults = displayReviewForStudent(mycursor, "sup", exList)
            items = []
            if len(supResults) > 0:
                for row in supResults:
                    instance = IDReviewPerYearItem('', '', '', '')
                    instance.setValues(row)
                    items.append(instance)

            studentResults = displayReviewForStudent(mycursor, "student", exList)
            if len(studentResults) > 0:
                for row in studentResults:
                    row = list(row)
                    #append a space so we can list the review type as "student"
                    row.append("student")
                    print (row)
                    instance = IDReviewPerYearItem('', '', '', '')
                    instance.setValues(row)
                    items.append(instance)

            portfolioResults = displayReviewForStudent (mycursor, "portfolio", exList)
            if len(portfolioResults) > 0:
                for row in portfolioResults:
                    row = list(row)
                    #append a space so we can list the review type as "student"
                    row.append("portfolio")
                    print (row)
                    instance = IDReviewPerYearItem('', '', '', '')
                    instance.setValues(row)
                    items.append(instance)

            if len(supResults) > 0 or len(studentResults) > 0 or len(portfolioResults) > 0:
                supervisorTable = IDReviewPerYearTable(items)
                supervisorTable.border = True
                return render_template('results.html', table=supervisorTable)

            else:
                flash('No results found!')
                return redirect(f'/item3/{id}')
        else:
            flash('Please enter a 4 digit year!')
    return render_template('yearForm.html', form = year )

@app.route('/item1/<string:id>', methods=['GET', 'POST'])
def portfolioReviewLink(id):
    # Ask for YEAR of review
    yearSearch = YearSearchForm()
    print('here')
    exList = []
    exList.append(str(id))
    if request.method == 'POST':
        yearNum = yearSearch.data['year']

        if len(yearNum) == 4 and yearNum.isdigit():
            print(yearNum)
            # Query the Portfolio Reviews for the specific student using their BUID and Year
            # and add it to results
            exList.append(str(yearNum))
            print ("list:", exList)

            results = portfolioReview(mycursor, mydb, "idyear", exList)

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
        elif len(yearNum) != 4 and yearNum.isdigit():
            flash('Please enter a 4 digit year!')
        else:
            print ("list:", exList)

            results = portfolioReview(mycursor, mydb, "id", exList)

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
    return render_template('yearForm.html' ,form=yearSearch)

@app.route('/item2/<string:id>', methods=['GET', 'POST'])
def studentReviewLink(id):
    # Ask for YEAR of review
    yearSearch = YearSearchForm()
    exList = []
    exList.append(str(id))
    print('here')
    if request.method == 'POST':
        yearNum = yearSearch.data['year']

        if len(yearNum) == 4 and yearNum.isdigit():
            print(yearNum)
            # Query the Supervisor Reviews for the specific student using their BUID and Year
            # and add it to results
            exList.append(str(yearNum))
            print ("studentRList", exList)
            results = reviewByStudent(mycursor, mydb, "idyear", exList)

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
        elif len(yearNum) != 4 and yearNum.isdigit():
            flash('Please enter a 4 digit year or leave the year field blank!')
        else:
            print ("studentRList", exList)
            results = reviewByStudent(mycursor, mydb, "id", exList)

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
            exList.append("midterm")


        elif search.select.data == "Midterm Site Visit":
            exList.append("site")
            exList.append("site")


        elif search.select.data == "End-of-Term Qualtrics Survey":
            exList.append("site")
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



    return redirect('/reviewQuery')

# @app.route('/ReviewAnalysis', methods=['GET', "POST"])
# def GetLabel():
#     search = GetLabelForm()
#     if request.method == 'POST':
#         executeList = []
#         #label = search.data['label']
#         reviewType = search.data['reviewType']
#         startYear = int(search.data['startYear']) - 1
#         startYear = "20" + str(startYear)
#         endYear = int(search.data['endYear']) - 1
#         endYear = "20" + str(endYear)
#         executeList.append(startYear)
#         executeList.append(endYear)
#
#         if reviewType == "Portfolio Review":
#             print("the executeList is", executeList)
#             sql = "SELECT label FROM PortfolioReviewQ WHERE startYear BETWEEN %s AND %s"
#             mycursor.execute(sql, executeList)
#             results = mycursor.fetchall()
#             print ("IN HERE")
#
#         elif reviewType == "Student Review":
#             sql = "SELECT label FROM StudentReviewQ WHERE startYear BETWEEN %s AND %s"
#             mycursor.execute(sql, executeList)
#             results = mycursor.fetchall()
#
#         else:
#             if reviewType == "Midterm Qualtrics Survey":
#                 executeList.append("midterm")
#
#             elif reviewType == "Midterm Site Visit":
#                 executeList.append("site")
#
#             elif reviewType == "End-of-Term Qualtrics Survey":
#                 executeList.append("site")
#
#             sql = "SELECT label FROM SupervisorInternReviewQ WHERE startYear BETWEEN %s AND %s AND reviewType = %s"
#             mycursor.execute(sql, executeList)
#             results = mycursor.fetchall()
#
#         if len(results) == 0:
#             flash('No results found!')
#             return redirect(f'/item5/{id}')
#         else:
#             items = []
#             for row in results:
#                 instance = LabelItem( " ", " ", " ")
#                 row = list(row)
#                 if reviewType == "Portfolio Review":
#                     row.append("Portfolio")
#
#                 if reviewType == "Student Review":
#                     row.append("Student")
#                 instance.setValues(row)
#                 items.append(row)
#
#             table = LabelTable(items)
#             table.border = True
#             return render_template('results.html', table=table)
#
#
#             return redirect("/ReviewAnalysis/LabelPage'")
#     return render_template('reviewAnalysis.html', form=search)
#
# @app.route('/ReviewAnalysis/LabelPage', methods=['GET', "POST"])
# def LabelPage():
#     search = LabelChoice()
#     search.lbl = []
#     return render_template("labelchoices.html", form = search)
#

# add this <string:label> to the route when done
# it will take question label
@app.route('/studentAnswersMultipleChoice/', methods=['GET', 'POST'])
def studentMultipleChoiceAnswerPage():
    form = studentResponsesMultipleChoiceForm()
    # form.multipleChoiceAnswers.choices = ['QUERY TUPLE RESULTS HERE']
    selectChoices = [('1', 'BAD'), ('2', 'Okay'), ('3', 'Good')]

    form.multipleChoiceAnswers.choices = selectChoices
    if request.method == 'POST':
        print('SUBMIT BUTTON HAS BEEN PRESSED WITH ANSWER CHOICE: ', form.multipleChoiceAnswers.data)

    return render_template('multipleChoiceAnswerForm.html', form=form)




@app.route('/searchLabels/', methods=['GET', 'POST'])
def questionSearchPage():
    form = GetLabelForm()
    if request.method == 'POST':
        return search_results_Questions(form)

    return render_template('getLabelFormV2.html', form=form)


@app.route('/searchLabels/results')
def search_results_Questions(form):
    results = []

    executeList = []
    # label = search.data['label']
    reviewType = form.reviewType.data
    startYear = int(form.startYear.data) - 1
    startYear = "20" + str(startYear)
    endYear = int(form.endYear.data) - 1
    endYear = "20" + str(endYear)
    executeList.append(startYear)
    executeList.append(endYear)

    if reviewType == "Portfolio Review":
        print("the executeList is", executeList)
        sql = "SELECT label FROM PortfolioReviewQ WHERE startYear BETWEEN %s AND %s"
        mycursor.execute(sql, executeList)
        results = mycursor.fetchall()
        print("IN HERE")

    elif reviewType == "Student Review":
        sql = "SELECT label FROM StudentReviewQ WHERE startYear BETWEEN %s AND %s"
        mycursor.execute(sql, executeList)
        results = mycursor.fetchall()

    else:
        if reviewType == "Midterm Qualtrics Survey":
            executeList.append("midterm")

        elif reviewType == "Midterm Site Visit":
            executeList.append("site")

        elif reviewType == "End-of-Term Qualtrics Survey":
            executeList.append("site")

        sql = "SELECT label FROM SupervisorInternReviewQ WHERE startYear BETWEEN %s AND %s AND reviewType = %s"
        mycursor.execute(sql, executeList)
        results = mycursor.fetchall()

#
    if len(results) == 0:
        flash('No results found!')
        return redirect('/searchLabels/')
    else:
        items = []
        for row in results:
            instance = LabelItem(" ", " ")
            row = list(row)
            if reviewType == "Portfolio Review":
                row.append("Portfolio")

            if reviewType == "Student Review":
                row.append("Student")

            print ("the row is", row)
            instance.setValues(row)
            items.append(instance)

        table = QuestionsResults(items)
        table.border = True
        return render_template('results.html', table=table)


@app.route('/LabelItem/<string:id>', methods=['GET', 'POST'])
def answerLink(id):
    print(id)

    """
    If count(*) is greater than one then relocate to multiple choice answer page

    else 
    relocate to short answer page
    """
    # form = studentResponsesMultipleChoiceForm()
    # # form.multipleChoiceAnswers.choices = ['QUERY TUPLE RESULTS HERE']
    # selectChoices = [('1', 'BAD'), ('2', 'Okay'), ('3', 'Good')]
    #
    # form.multipleChoiceAnswers.choices = selectChoices
    # if request.method == 'POST':
    #     print('SUBMIT BUTTON HAS BEEN PRESSED WITH ANSWER CHOICE: ', form.multipleChoiceAnswers.data)
    #
    # return render_template('multipleChoiceAnswerForm.html', form=form)
    return id


@app.route('/searchQuestions/', methods=['GET', 'POST'])
def REAL_Question_search_page():
    form = searchQuestions()
    if request.method == 'POST':
        return newSearchResults(form)

    return render_template('questionSearchPage.html', form=form)


@app.route('/searchQuestions/results')
def newSearchResults(form):
    results = []
    print('Here?')

    if len(results) > 0:
        flash('No results found!')
        return redirect('/searchQuestions/')
    else:
        print('HEre')
        items = [QuestionItem('This is a question', 'this is a label', 'this is a start year')]
        table = ACTUALQuestionsResults(items)
        table.border = True
        return render_template('results.html', table=table)


@app.route('/answerItem/<string:id>/<string:year>', methods=['GET', 'POST'])
def answerLinkv2(id, year):
    print(id)
    print(year)

    """
    If count(*) is greater than one then relocate to multiple choice answer page

    else 
    relocate to short answer page
    """
    form = studentResponsesMultipleChoiceForm()
    # form.multipleChoiceAnswers.choices = ['QUERY TUPLE RESULTS HERE']
    selectChoices = [('1', 'BAD'), ('2', 'Okay'), ('3', 'Good')]

    form.multipleChoiceAnswers.choices = selectChoices
    if request.method == 'POST':
        print('SUBMIT BUTTON HAS BEEN PRESSED WITH ANSWER CHOICE: ', form.multipleChoiceAnswers.data)

    return render_template('multipleChoiceAnswerForm.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
