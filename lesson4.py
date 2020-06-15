from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://danielzhang@localhost:5432/example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<User {self.id}, {self.name}>'


db.create_all()


@app.route('/')


def index():
    '''
    Index function
    '''
    person = User.query.first()
    # Add some stuff thru SQL into the table (i.e. INSERT into persons (name) 
    # VALUES ('daniel')
    # get the person!
    # Now, to get the name to show, you can restart the server
    # However, you can instead turn debug mode to on, which automatically
    # restarts it!
    # To set debug on, we do 'FLASK_DEBUG = true'
    # Now any times we make changes, it automatically is seen
    # We set this inline with our flask run command - FLASK_DEBUG=true flask
    # run
    return 'Hello ' + person.name + '!'


if __name__ == '__main__':
    app.run()
    # Remember, you use the model/table in the queries and stuff.

    print(User.query.all())