from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import InputRequired, Email, Length, ValidationError, AnyOf, DataRequired
from flask_bootstrap import Bootstrap
from TableSchema import *
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

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'DontTellAnyone'

grade_list = [(0, '---'), (1, 'A'), (2, 'B'), (3, 'C'), (4, 'D'), (5, 'F')]
year_list = [(0, '---')]
for i in range(20):
    year_list.append((i+1, 2000 + i))

class StudentInfoForm(FlaskForm):
        student_id = StringField('student ID', validators=[InputRequired(), Length(9)])
        first_name = StringField('First Name', validators=[InputRequired()])
        last_name = StringField('Last Name', validators=[InputRequired()])
        email = StringField('email', validators=[InputRequired(), Email(message='Invalid email address')])
        Class = StringField('Class', validators=[InputRequired()])
        submit = SubmitField('Submit')

class StudentInfoForm2(FlaskForm):
    major_minor = SelectField('Major/Minor', [DataRequired()], choices=[(0, "---"), (1, 'major'), (2, 'minor')])
    ADV_PR_Semester = SelectField('ADV PR Semester', choices=[(0, '---'), (1, 'Fall'), (2, 'Spring')])
    ADV_PR_Year = SelectField('Year', choices=year_list)
    ADV_PR_Grade = SelectField('Grade', choices=grade_list)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = StudentInfoForm()
    form2 = StudentInfoForm2()
    if (form.validate_on_submit() and form2.major_minor.data != '0' and form2.ADV_PR_Semester.data != '0' and
        form2.ADV_PR_Grade.data != '0' and form2.ADV_PR_Year.data != '0'):
        print(form2.major_minor.data)
        return 'Redirect'
    return render_template('submit.html', form=form, form2=form2)


if __name__ == '__main__':
    app.run(debug=True)
