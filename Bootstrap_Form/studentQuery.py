from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField
from flask_table import Table, Col,LinkCol
from flask import Flask, render_template, request, url_for, redirect, flash
from wtforms.validators import InputRequired, NumberRange, Length
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'DontTellAnyone'

class StudentSearchForm(FlaskForm):
    choices = [('Baylor ID', 'Baylor ID'),
               ('Name', 'Name')]
    select = SelectField('Search for Student by:', choices=choices)
    search = StringField('ID')
    firstName = StringField('First name')
    lastName = StringField('Last name')

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


class SuperVisorReviewItem(object):
    def __init__(self,question,answer,comment):
        self.question = question
        self.answer = answer
        self.comment = comment


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
    #Ask for YEAR of review

    #Query for the Portfolio Reviews for the specific student using their BUID


    results = [] #THE query information

    if len(results) == 0:
        return redirect(url_for('studentQueryHomePage'))
    else:
        flash('No results found!')
        return redirect('/studenQuery')

@app.route('/item2/<int:id>', methods=['GET', 'POST'])
def studentReviewLink(id):
    # Ask for YEAR of review

    #Query for the Student Reviews for the specific student using their BUID

    results = [] #THE query information

    if len(results) == 0:
        return redirect(url_for('studentQueryHomePage'))
    else:
        flash('No results found!')
        return redirect('/studenQuery')

'''

@app.route('studentQuery/results/reviews', methods=['GET','POST'])
def reviewsResultsPage():
'''

if __name__ == '__main__':
    app.run(debug=True)