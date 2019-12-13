from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from flask_table import Table, Col,LinkCol
from flask import Flask, render_template, request, url_for, redirect, flash
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
    edit = LinkCol('Reviews', 'edit', url_kwargs=dict(id='id'))

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


@app.route('/item/<int:id>', methods=['GET', 'POST'])
def edit(id):
    #Query the Reviews for the specific student using their BUID

    results = [] #THE query information

    if len(results) == 0:
        return redirect(url_for('studentQueryHomePage'))
    else:
        flash('No results found!')
        return redirect('/studenQuery')



@app.route('studentQuery/results/reviews', methods=['GET','POST'])
def reviewsResultsPage():

if __name__ == '__main__':
    app.run(debug=True)