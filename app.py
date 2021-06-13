from flask import Flask, render_template, jsonify, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, Form, SubmitField, validators, ValidationError
from wtforms.validators import InputRequired
import marshmallow_sqlalchemy
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://dpmsuznswdcjgh:2ceebb535e5463f883e4bb8ace666acacf2be7f7ba3c3b0f91f75b80dea2d1e1@ec2-3-233-7-12.compute-1.amazonaws.com:5432/d7ndet9b9sdb7f"


db = SQLAlchemy(app)
ma = Marshmallow(app)
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
@cross_origin()
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)


@app.route('/add-user', methods=['POST'])
@cross_origin()
def add_user():
    rqt = request.get_json(force=True)
    name = rqt["name"]
    amount = rqt["amount"]

    record = User(name, amount)
    db.session.add(record)
    db.session.commit()

    user = User.query.get(record.id)
    flash("User Added")
    return user_schema.jsonify(user)


@app.route('/user/<id>', methods=["GET"])
@cross_origin()
def get_user(id):
    user = User.query.get(id)
    result = user_schema.dump(user)
    return result


@app.route('/user-update/<id>', methods=['PATCH'])
def user_update(id):
    user = User.query.get(id)
    rqt = request.get_json(force=True)

    new_amount = rqt["amount"]
    user.amount = new_amount

    db.session.commit()
    print(user_schema.jsonify(user))
    return user_schema.jsonify(user)


@app.route('/delete-user/<id>', methods=['DELETE'])
@cross_origin()
def delete_user(id):
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    return jsonify('user deleted')


if __name__ == '__main__':
    app.run()
