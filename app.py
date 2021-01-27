from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, Form, SubmitField, validators, ValidationError
from wtforms.validators import InputRequired
import marshmallow_sqlalchemy 
from flask_cors import CORS
from flask_bootstrap import Bootstrap
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, 'app.sqlite')


db = SQLAlchemy(app)
ma = Marshmallow(app)
Bootstrap(app)
CORS(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    amount = db.Column(db.Float)

    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

class UserSchema(ma.Schema):
    class Meta: 
        fields = ("id", "name", "amount")

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class AddUserForm(FlaskForm):
    name = StringField('name', validators=[InputRequired()])
    amount = DecimalField('amount', validators=[InputRequired()])

@app.route('/users', methods=["GET"])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    form = AddUserForm()

    if form.validate_on_submit():
        new_user = User(name=form.name.data, amount=form.amount.data)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created!</h1>'

    return render_template('add.html', form=form)

@app.route('/')
def home():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    
    return render_template('home.html', names=result)

@app.route('/add-amount/<id>', methods=['GET', 'POST'])
def add_amount(id):
    user = User.query.get(id)
    result = user_schema.dump(user)
    return render_template('account.html', name=result)


# @app.route('/sub-amount')
# def sub_amount():

if __name__ == '__main__':
    app.run(debug=True)



