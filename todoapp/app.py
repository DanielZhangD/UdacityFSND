from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import sys
from flask_migrate import Migrate

# TO RUN THIS, WE DO $ FLASK_APP=app.py FLASK_DEBUG=true flask run

# create application (named after our file)
app = Flask(__name__)
# connect flask to db
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://danielzhang@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# remember to manually create the db 
# createdb
# make our database
db = SQLAlchemy(app)

# this sets up the flask database migration commands
migrate = Migrate(app, db)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    # it's a new part of the db!
    completed = db.Column(db.Boolean, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable = False)
    def __repr__(self):
        return f'<Todo {self.id} {self.description}, list {self.list_id}>'

# this below command was needed to sync models - unneeded with migrations
# db.create_all()

class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(), nullable=False)
    #TodoList is the parent, Todo is the child
    todos = db.relationship('Todo', backref = 'list', cascade = 'all, delete-orphan')
    #We need to create a migration so that we have a new TodoList model
    def __repr__(self):
        return f'<TodoList {self.id} {self.name}>'


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
        body['id'] = todo.id
        body['description'] = todo.description
        body['completed'] = todo.completed
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

#we have a todo id inside of <todo_id>, which becomes avaibale to us.
@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    try:
        completed = request.get_json()['completed']
        print('completed', completed)
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))

@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    try:
        Todo.query.filter_by(id=todo_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({ 'success': True })

# we've chosen post as our user data method
#The index is the controller - tells the the user should view next, and what the model to do
@app.route('/lists/<list_id>') 
def get_list_todos(list_id):
    # this is like column and etc,
    # Now we pass in the data from our database
    return render_template('index.html', 
    lists=TodoList.query.all(), 
    active_list = TodoList.query.get(list_id),
    todos=Todo.query.filter_by(list_id=list_id).order_by('id').all()) 
     # let's have a template!
    # You can pass in variables into 'render_template'
    # Flask processes HTML templates with Jinja/ jinja2 to replace template
    # strings
    # View uses the render_template, model accesses todo.query.all

#home page route, but we're gonna redirect
@app.route('/')
def index():
    #this shit hate spaces - no space between list_id and = and 1 
    return redirect(url_for('get_list_todos', list_id=1))