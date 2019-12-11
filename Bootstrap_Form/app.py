from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import InputRequired, Email, Length, ValidationError, AnyOf, DataRequired
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'DontTellAnyone'

nolist = 'Please Select...'

def your_validator(form, field):
    if field.data == '0':
        print("Field.data does = 0")
        raise ValidationError('Please select a value')


grade_list = [(0, 'Pleae Select..'), (1, 'A'), (2, 'B'), (3, 'C'), (4, 'D'), (5, 'F')]
#grade_list_validate = [(1, 'A'), (2, 'B'), (3, 'C'), (4, 'D'), (5, 'F')]

year_list = [(0, 'Please Select..')]
#year_list_validate = []
for i in range(20):
    year_list.append((i, 2000 + i))
#    year_list_validate.append((2000 + i))


class StudentInfoForm(FlaskForm):
    student_id = StringField('student ID', validators=[InputRequired(), Length(9)])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email address')])
#    ADV_PR_Semester = SelectField('ADV PR Semester', choices=[(0, 'Please Select..'), (1, 'Fall'), (2, 'Spring')])
    Class = StringField('Class', validators=[InputRequired()])
    major_minor = SelectField('Major/Minor', choices=[(None, "---"), (1, 'major'), (2, 'minor')], default=None,
                              validators=[AnyOf(['minor', 'major'])])
#    ADV_PR_Grade = SelectField('Grade', choices=grade_list)
#    ADV_PR_Year = SelectField('Year', choices=year_list)
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = StudentInfoForm()
    if form.validate_on_submit():
        return 'Form Successfully submitted!'
    print(form.validate_on_submit())
    return render_template('submit.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
