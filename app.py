from flask import Flask, render_template, request, url_for
import mysql.connector

app = Flask(__name__)

# Configure db
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="BUboxtop2020",
    database="testdb"
)
#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = 'BUboxtop2020'
#app.config['MYSQL_DB'] = 'testdb'

#mysql = MySQL(app)
myCursor = mydb.cursor()


@app.route('/', methods=['GET',"POST"])
def index():
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


        myCursor.execute("INSERT INTO studentInfo(baylorID, lastName, firstName, emailAddress, ADV_PR_semester,"
                         "class, major_minor, ADV_PR_grade, ADV_PR_Year) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                         ,(s_id, lname, fName, email, semester, className, major_minor,grade, yr))
        mydb.commit()
        myCursor.close()
        return 'success'
    return render_template('index.html')




if __name__ == '__main__':
    app.run(debug=True)
