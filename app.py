from flask import Flask, render_template, url_for, current_app, redirect
from flask import request, Request
from flask_sqlalchemy import SQLAlchemy


#url_for is for creating urls

app = Flask(__name__)

#To define where database is located
#//// is asbolute path, /// is relative path
db_name = 'example.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

#Initialize database
db = SQLAlchemy(app)

#Creating database table
class Example(db.Model):
    #Defining all fields
    _id = db.Column("id", db.Integer, primary_key=True)
    firstName = db.Column(db.String(200))
    lastName = db.Column(db.String(200))
    occupation = db.Column(db.String(200))
    company = db.Column(db.String(200))

    def __init__(self, firstName, lastName, occupation, company):
        self.firstName = firstName
        self.lastName = lastName
        self.occupation = occupation
        self.company = company

    #function to return something once a record is created
    def __repr__(self):
        return '<Record %r>' % self._id

#Creating database
with app.app_context():
    db.create_all()
    
#Create a route using @app.route('url_string_of_route', methods=[])
@app.route('/', methods=['GET', 'POST'])

#Create your function for the route
#Main page
def index():
    #Using POST method to retrieve input
    if request.method=="POST":
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        occupation = request.form['occupation']
        company = request.form['company']
        print(firstName, lastName, occupation)
        #Writing to the database
        new_record = Example(firstName=firstName, lastName=lastName, occupation=occupation, company=company)
        try:
            db.session.add(new_record)
            db.session.commit()
            return redirect('/')
        except:
            return ('There was an error.')
    else:
        return render_template('index.html')

#Retrieve all rows from database
@app.route('/display_data', methods=['GET', 'POST'])
def display_data():
    #Create a new list where all rows can be added as tuples.
    records_list = []
    #Get rows
    records = Example.query.all()
    #Unpack the database object to create tuples for each row and add to records_list
    for record in records:
        firstName = record.firstName
        lastName = record.lastName
        occupation = record.occupation
        company = record.company
        a_record = firstName, lastName, occupation, company
        records_list.append(a_record)
    print('This is the record list', records_list)
    #return records_list so it can be used in the HTML file
    return render_template('display_data.html', records_list=records_list)


if __name__ =="__main__":
    app.run(debug=True)
