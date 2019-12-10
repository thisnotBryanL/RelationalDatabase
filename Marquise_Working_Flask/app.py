from flask import Flask, render_template, request, url_for, redirect
import mysql.connector
from TableSchema import *

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
