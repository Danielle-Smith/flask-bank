from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, Form, SubmitField, validators, ValidationError
from wtforms.validators import InputRequired
import marshmallow_sqlalchemy 
from flask_cors import CORS, cross_origin
from flask_bootstrap import Bootstrap
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, 'app.sqlite')


db = SQLAlchemy(app)
ma = Marshmallow(app)
Bootstrap(app)
CORS(app, resources='*')
# CORS(app)

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
@cross_origin()
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

# @app.route('/add-user', methods=['GET', 'POST'])
# @cross_origin()
# def add_user():
#     form = AddUserForm()

#     if form.validate_on_submit():
#         new_user = User(name=form.name.data, amount=form.amount.data)
#         db.session.add(new_user)
#         db.session.commit()

#         return '<h1>New user has been created!</h1>'

#     return render_template('add.html', form=form)

@app.route('/user/<id>', methods=["GET"])
@cross_origin()
def get_user(id):
    user = User.query.get(id)
    result = user_schema.dump(user)
    return result

# @app.route('/')
# @cross_origin()
# def home():
#     all_users = User.query.all()
#     result = users_schema.dump(all_users)
    
#     return render_template('home.html', names=result)

@app.route('/user-update/<id>', methods=['PATCH'])
def user_update(id):
    user = User.query.get(id)
    rqt = request.get_json(force=True)

    new_amount = rqt["amount"]
    user.amount = new_amount

    db.session.commit()
    print(user_schema.jsonify(user))
    return user_schema.jsonify(user)

if __name__ == '__main__':
    app.run(debug=True)



