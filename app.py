#! -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template, request, abort
from db import session, create_all
from user import User

from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('main.html', hello='Lorem ipsum')


@app.route('/login/', methods=['POST'])
def login():
    '''
    POST /login/
    username=admire93&password=foo

    200 OK
    {
      "email": "admire9@gmail.com"
    }
    '''
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    users = session.query(User)\
            .filter(User.email == email)\
            .all()
    if not users:
        abort(404)
    user = users[0]
    if not user.confirm_password(password):
        abort(404)
    return jsonify(email=email, token=user.token)


@app.route('/users/', methods=['GET'])
def find_users():
    users = session.query(User)\
            .all()
    print(users)
    return "Hello world"


@app.route('/users/<int:_id>/', methods=['GET'])
def find_user(_id):
    users = session.query(User)\
            .filter(User.id == _id)\
            .all()
    if not users:
        abort(404)
    user = users[0]
    token = request.args.get('token', None)
    if not user.confirm_token(token):
        abort(403)
    return jsonify(id=user.id, email=user.email)


@app.route('/users/', methods=['POST'])
def create_user():
    email = request.form.get('email', None) # 'admire9@gmail.com'
    password = request.form.get('password', None)
    '''
            user = User(name=me['name'], fb_id=me['id'])
            session.add(user)
            try:
                session.commit()
            except IntegrityError:
                session.rollback()
    '''
    user = User(email=email, password=password)
    session.add(user)
    if email is None or password is None:
        return jsonify(message='email, password must required')
    try:
        session.commit()
    except IntegrityError as e:
        session.rollback()
        abort(400)
    return jsonify(message='ok', email=user.email)



if __name__ == '__main__':
    app.run(debug=True)
