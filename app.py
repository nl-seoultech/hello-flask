from flask import Flask, request, abort, jsonify
from sqlalchemy.exc import IntegrityError

from db import session, create_all
from user import User

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'hello world'


@app.route('/users/', methods=['POST'])
def create_users():
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    if email is None or password is None:
        abort(400)
    user = User(email=email, password=password)
    session.add(user)
    try:
        session.commit()
    except IntegrityError as e:
        session.rollback()
        abort(500)
    return jsonify(email=user.email)


@app.route('/login/', methods=['POST'])
def login():
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    users = session.query(User)\
            .filter(User.email == email)\
            .all()
    if not users:
        abort(404)
    user = users[0]
    if not user.confirm_password(password):
        abort(403)
    return jsonify(email=email, token=user.token)


@app.route('/users/<int:i>/', methods=['GET'])
def find_user(i):
    token = request.args.get('token', None)
    if token is None:
        abort(400)
    users = session.query(User)\
            .filter(User.id == i)\
            .all()
    if not users:
        abort(404)
    user = users[0]
    if not user.confirm_token(token):
        abort(403)
    return jsonify(id=user.id, email=user.email)


if __name__ == '__main__':
    app.run(debug=True)
