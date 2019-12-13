from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from flask_table import Table, Col,LinkCol
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import InputRequired, Email, Length, DataRequired
from flask_bootstrap import Bootstrap


from Bootstrap_Form.TableSchema import createTables
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

# Create app
app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'DontTellAnyone'

# Create Classes for forms and web pages

class StudentInfoForm(FlaskForm):
    student_id = StringField('student ID', validators=[InputRequired(), Length(9)])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email address')])
    Class = StringField('Class', validators=[InputRequired()])

class StudentInfoForm2(FlaskForm):
    grade_list = [(0, '---'), (1, 'A'), (2, 'B'), (3, 'C'), (4, 'D'), (5, 'F')]
    year_list = [(0, '---')]
    for i in range(20):
        year_list.append((i + 1, 2000 + i))
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

class StudentReviewItem(object):
    def __init__(self,question,answer,comment):
        self.question = question
        self.answer = answer
        self.comment = comment


class PortfolioReviewItem(object):
    def __init__(self,question,answer,comment,reviewerName):
        self.question = question
        self.answer = answer
        self.comment = comment
        self.reviewerName = reviewerName

class Item(object):
    def __init__(self, id, fname, lname, email,semester,yr,major_minor,grade,classYear):
        self.id = id
        self.fname = fname
        self.lname = lname
        self.email = email
        self.semester = semester
        self.yr = yr
        self.major_minor = major_minor
        self.grade = grade
        self.classYear = classYear

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
    return render_template('index.html')


######################## INFORMATION INPUT FORMS ########################
@app.route('/input_student_info', methods=['GET', 'POST'])
def studentInfo():
    form = StudentInfoForm()
    form2 = StudentInfoForm2()
    if (form.validate_on_submit() and form2.major_minor.data != '0' and form2.ADV_PR_Semester.data != '0' and
        form2.ADV_PR_Grade.data != '0' and form2.ADV_PR_Year.data != '0'):
        return 'Redirect'
    return render_template('submit.html', form=form, form2=form2)

@app.route('/input_supervisor_info', methods=['GET', 'POST'])
def supervisorInfo():
    form = SupervisorInfoForm()
    if form.validate_on_submit():
        return 'Successfully submitted supervisor information!'
    return render_template('supervisor.html', form=form)


######################## SUDENT QUERY DATA ########################

@app.route('/studentQuery', methods=['GET', "POST"])
def studentQueryHomePage():
    search = StudentSearchForm()
    if request.method == 'POST':
        return search_results(search)
    return render_template('studentQueryHome.html', form=search)


@app.route('/studentQuery/results')
def search_results(search):
    results = []

    if search.select.data == "Baylor ID":
        print("BUID")
        #Query the BU ID
        search_string = search.data['search']

    else:
        print("BUNAME")
        firstNameSearch = search.data['firstName']
        lastNameSearch = search.data['lastName']

    if search.data['search'] == 'Bryan Lee':
        items = [Item('000000000', 'Bryan', 'Lee', 'Bryan_Lee@baylor.edu', 'Fall', '2019', 'PR', 'A', 'SR'),
                 Item('000000000', 'Bryan', 'Lee', 'Bryan_Lee@baylor.edu', 'Fall', '2019', 'PR', 'A', 'SR'),
                 Item('111111111', 'Bryan', 'Lee', 'Bryan_Lee@baylor.edu', 'Fall', '2019', 'PR', 'A', 'SR')]
        table = Results(items)
        table.border = True
        return render_template('results.html', table=table)
    #qry = db_session.query(Album)
    #results = qry.all()

    if len(results) == 0:
        flash('No results found!')
        return redirect('/studentQuery')
    else:
        # display results
        #table.border = True
        return render_template('results.html', table = table)

@app.route('/studentQuery/results/reviews/year', methods=['GET','POST'])
def SearchYearHomePage():
    yearSearch = YearSearchForm()
    if request.method == 'POST' and yearSearch.validate_on_submit():
        return SearchYear(yearSearch)
    return render_template('yearForm.html', form=yearSearch)

def SearchYear(search):
    yearEntered = search.data['year']




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

            results = [PortfolioReviewItem('QUESTION 1', 'ANSWER1',
                                            'This is a commnt that is supposed to be kind of l'
                                            'ong to see how this would fit in to the table '
                                            'lol hahahahahahha hehehehehe hohohohohohohho')]  # THE query information

            portfolioReviewTable = PortfolioReviewTable(results)
            portfolioReviewTable.border = True

            if len(results) > 0:
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

            results = [StudentReviewItem('QUESTION 1', 'ANSWER1',
                                            'This is a commnt that is supposed to be kind of l'
                                            'ong to see how this would fit in to the table '
                                            'lol hahahahahahha hehehehehe hohohohohohohho')]  # THE query information

            studentReviewTable = StudentReviewTable(results)
            studentReviewTable.border = True

            if len(results) > 0:
                return render_template('results.html', table=studentReviewTable)
            else:
                flash('No results found!')
                return redirect(url_for('studentQueryHomePage'))
        else:
            flash('Please enter a 4 digit year!')
    return render_template('yearForm.html' ,form=yearSearch)


if __name__ == '__main__':
    app.run(debug=True)
