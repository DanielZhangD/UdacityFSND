from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#instantiate the application
app = Flask(__name__)
#standard way of creating a flask application

#Configuration Variable
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://danielzhang@localhost:5432/example'
#optionally, you can specify a dbapi by doing postgresql+psycopg2://... instead

#remove warning in interactive mode (i.e run python3)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#OPTIONAL - __repr__ for debugging


db = SQLAlchemy(app)
#Links instance of a database that we can interact with in SQLAlchemy in flask

#First, connect to a databse from our flask application
#To do this, we need a configuration variable ^ above

#Creating a db.model
class Person(db.Model):
    __tablename__ = 'persons'
    #make a tablename
    id = db.Column(db.Integer, primary_key = True)
    #column, with integer
    name = db.Column(db.String(), nullable = False)
    #This is a name, must be a string, and cannot be null
    #Generally, in a class, we need an 'init' method, but SQLAlchemy does this automatically

    #debugging
    def __repr__(self):
        return f'<Person ID: {self.id}, name: {self.name}>'

#Creates all tables that have been declared, *if they have not yet been created*
db.create_all()

#This is a python decorator, lets us tell the Flask application which endpoint to listen to for connections
@app.route('/')
#this is the homepage/root route

#Now we make a route handler
#When a client connects to the root route, we use index
def index():
    #Add some stuff thru SQL into the table (i.e. INSERT into persons (name) VALUES ('daniel')
    #get the person!
    person = Person.query.first()
    #Now, to get the name to show, you can restart the server
    #However, you can instead turn debug mode to on, which automatically restarts it!
    #To set debug on, we do 'FLASK_DEBUG = true'
    #Now any times we make changes, it automatically is seen
    #We set this inline with our flask run command - FLASK_DEBUG=true flask run
    return 'Hello ' + person.name + '!'
 

#FLASK_APP=flask-hello-app.py flask run - how we run
#ALTERNATIVELY
if __name__ == '__main__':
    app.run()

