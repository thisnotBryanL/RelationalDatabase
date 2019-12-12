from flask import Flask, render_template, request, url_for, redirect, flash
from TableSchema import *
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, Form
from wtforms.validators import InputRequired, Email, Length, ValidationError, AnyOf, DataRequired
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'DontTellAnyone'

# Configure db
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password123",
    database="GP"
)

myCursor = mydb.cursor()

createTables(myCursor)

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
        className = userDetails['class']
        major_minor = userDetails['major_minor']
        grade = userDetails['grade']

        # Use Micah's function from User_Inputed_Data if possible. May need modification
        # insertIntoStudentInfo(s_id, lname, fName, email, semester, yr, major_minor, )

        myCursor.execute("INSERT INTO studentInfo(baylorID, lastName, firstName, emailAddress, ADV_PR_semester,"
                         "class, major_minor, ADV_PR_grade, ADV_PR_Year) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                         , (s_id, lname, fName, email, semester, className, major_minor, grade, yr))
        mydb.commit()
        myCursor.close()

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


class StudentSearchForm(Form):
    choices = [('Baylor ID', 'Baylor ID'),
               ('Name', 'Name')]
    select = SelectField('Search for Student by:', choices=choices)
    search = StringField('')


@app.route('/studentQuery', methods=['GET', "POST"])
def studentQueryHomePage():
    search = StudentSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('studentQueryHome.html', form=search)


@app.route('/studentQuery/results')
def search_results(search):
    results = []
    search_string = search.data['search']

    if search.data['search'] == 'Bryan':
        print("YAY")
    #qry = db_session.query(Album)
    #results = qry.all()

    if not results:
        flash('No results found!')
        return redirect('/studentQuery')
    else:
        # display results
        return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
