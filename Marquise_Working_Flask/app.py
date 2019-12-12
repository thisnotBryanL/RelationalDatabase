from flask import Flask, render_template, request, url_for, redirect, flash
#from TableSchema import *
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, Form
from wtforms.validators import InputRequired, Email, Length, ValidationError, AnyOf, DataRequired
from flask_bootstrap import Bootstrap
from flask_table import Table, Col,LinkCol

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'DontTellAnyone'

'''
# Configure db
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="hoangdieu72",
    database="GP"
)

myCursor = mydb.cursor()

createTables(myCursor)
'''

@app.route('/', methods=['GET', "POST"])
def index():
    if request.method == 'POST':
        if request.form['option'] == 'student':
            return redirect(url_for('studentInfo'))
        elif request.form['option'] == 'intern':
            return redirect(url_for('intern'))
        elif request.form['option'] == 'studentQuery':
            return redirect(url_for('studentQueryHomePage'))

        return 'success'
    return render_template('index.html')


@app.route('/studentInfo', methods=['GET', 'POST'])
def studentInfo():
    # create year options list
    year = [2000, 2001, 2002]
    for i in range(5):
        year.append(2003 + i)

    if request.method == 'POST':
        # fetch the form data
        userDetails = request.form
        s_id = userDetails['student_id']
        fName = userDetails['first_name']
        lname = userDetails['last_name']
        email = userDetails['email']
        semester = userDetails['adv_pr_semester']
        yr = userDetails['year']
        major_minor = userDetails['major_minor']
        grade = userDetails['grade']

        # Use Micah's function from User_Inputed_Data if possible. May need modification
        # insertIntoStudentInfo(s_id, lname, fName, email, semester, yr, major_minor, )

        '''
        myCursor.execute("INSERT INTO studentInfo(baylorID, lastName, firstName, emailAddress, ADV_PR_semester,"
                         "class, major_minor, ADV_PR_grade, ADV_PR_Year) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                         , (s_id, lname, fName, email, semester, className, major_minor, grade, yr))
        mydb.commit()
        myCursor.close()
        '''

        if request.form['submit_button'] == 'next':
            return redirect(url_for('intern'))
        elif request.form['submit_button'] == 'back':
            return redirect(url_for('index'))

    return render_template('studentInfo.html')


@app.route('/internship', methods=['GET', 'POST'])
def intern():
    # Data not being read into the DB yet..
    if request.method == 'POST':
        if request.form['submit_button'] == 'back':
            return redirect(url_for('index'))
        elif request.form['submit_button'] == 'next':
            return redirect(url_for('experience'))

    return render_template('internship.html')

@app.route('/internship/experience', methods=['GET','POST'])
def experience():
    return render_template('experience.html')


class StudentSearchForm(FlaskForm):
    choices = [('Baylor ID', 'Baylor ID'),
               ('Name', 'Name')]
    select = SelectField('Search for Student by:', choices=choices)
    search = StringField('Full Name or ID')




class Results(Table):
    id = Col('Baylor ID ')
    fname = Col('First Name ')
    lname = Col('Last Name ')
    email = Col('Email ')
    semester = Col('Semester' )
    yr = Col('Year ')
    major_minor = Col('Major ')
    grade = Col('Grade ')
    classN = Col('Class ')
    edit = LinkCol('Reviews', 'edit', url_kwargs=dict(id='id'))

class Item(object):
    def __init__(self, id, fname, lname, email,semester,yr,major_minor,grade,classN):
        self.id = id
        self.fname = fname
        self.lname = lname
        self.email = email
        self.semester = semester
        self.yr = yr
        self.major_minor = major_minor
        self.grade = grade
        self.classN = classN




@app.route('/studentQuery', methods=['GET', "POST"])
def studentQueryHomePage():
    search = StudentSearchForm()
    if request.method == 'POST':
        return search_results(search)
    return render_template('studentQueryHome.html', form=search)


@app.route('/studentQuery/results')
def search_results(search):
    results = []
    search_string = search.data['search']


    if search.data['search'] == 'Bryan':
        print("YAY")
        print(search.select.data)
        items = [Item('000000000', 'Bryan', 'Lee', 'Bryan_Lee@baylor.edu', 'Fall', '2019', 'PR', 'A', 'Class'),
                 Item('000000000', 'Bryan', 'Lee', 'Bryan_Lee@baylor.edu', 'Fall', '2019', 'PR', 'A', 'Class'),
                 Item('000000000', 'Bryan', 'Lee', 'Bryan_Lee@baylor.edu', 'Fall', '2019', 'PR', 'A', 'Class')]
        table = Results(items)

    #qry = db_session.query(Album)
    #results = qry.all()

    if results.__sizeof__() == 0:
        flash('No results found!')
        return redirect('/studentQuery')
    else:
        # display results
        table.border = True
        return render_template('results.html', table = table)


@app.route('/item/<int:id>', methods=['GET', 'POST'])
def edit(id):
    print('')



if __name__ == '__main__':
    app.run(debug=True)
