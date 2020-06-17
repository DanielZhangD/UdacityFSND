from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import sys
# TO RUN THIS, WE DO $ FLASK_APP=app.py FLASK_DEBUG=true flask run

# create application (named after our file)
app = Flask(__name__)
# connect flask to db
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://danielzhang@localhost:5432/todoapp'
# remember to manually create the db 
# createdb
# make our database
db = SQLAlchemy(app)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

db.create_all()

# whenever something happens at route todos/create, we do this stuff
@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        #we want to get the json instead of the old stuff
        description = request.get_json()['description']
        #it comes as a dictionary
        #we have a default empty string in case nothing comes in
        #let's make a new todo object with description
        todo = Todo(description=description)
        db.session.add(todo)
        # add as pending change
        db.session.commit()
        # commit the change
        body['description'] = todo.description
        #this way, we don't need to access todo.description after closing the connection
        #therefore, we circumvent the expiry
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort (400)
    else: 
        return jsonify(body)

# we've chosen post as our user data method
#The index is the controller - tells the the user should view next, and what the model to do
@app.route('/') 
def index():
    # this is like column and etc,
    # Now we pass in the data from our database
    return render_template('index.html', data=Todo.query.all())
    # let's have a template!
    # fukin pylint REEEEE (render_template is fine, but pylint doesn't
    # recognize imported variables)
    # You can pass in variables into 'render_template'
    # Flask processes HTML templates with Jinja/ jinja2 to replace template
    # strings
    # View uses the render_template, model accesses todo.query.all