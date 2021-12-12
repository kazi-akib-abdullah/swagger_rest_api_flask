from flask import Flask, jsonify, request, make_response, redirect
import jwt
import datetime
from functools import wraps
from flask_swagger_ui import get_swaggerui_blueprint
from mysqlconnection import queryData


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Token is missing'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'],algorithms=['HS256'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(*args, **kwargs)
    return decorated

# class User(object):
#     def __init__(self, id, username, password):
#         self.id = id
#         self.username = username
#         self.password = password

#     def __str__(self):
#         return "User(id='%s')" % self.id

# users = [
#     User(1, 'user1', 'abcxyz'),
#     User(2, 'user2', 'abcxyz'),
# ]

# username_table = {u.username: u for u in users}
# userid_table = {u.id: u for u in users}

# def authenticate(username, password):
#     user = username_table.get(username, None)
#     if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
#         return user

# def identity(payload):
#     user_id = payload['identity']
#     return userid_table.get(user_id, None)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecret'

# jwt = JWT(app, authenticate, identity)

# @app.route('/unprotected')
# def unprotected():
#     return ''


# @app.route('/protected')
# @jwt_required()
# def protected():
#     # return ''
#     return '%s' % current_identity


# from routes import request_api

### swagger specific ###

### end swagger specific ###

@app.route('/protected')
@token_required
def protected():
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Seans-Python-Flask-REST-Boilerplate"
        }
    )
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
    return redirect("http://127.0.0.1:5000/swagger",code=302)

@app.route('/unprotected',methods=['GET'])
def unprotected():
    location = request.args.get('location')
    name = request.args.get('name')
    bedroom = request.args.get('bedroom')
    sleeps = request.args.get('sleeps')
    bathroom = request.args.get('bathroom')
    price = request.args.get('price')

    # if name == None:
    #     mapping = {"location":location}
    #     data = queryData(**mapping)
    #     print(name)
    #     print(location)
    #     print(data)
    #     return data
    # else:
    mapping = {"location":location, "name":name, "bedroom": bedroom, "sleeps": sleeps, "bathroom": bathroom, "price": price}
    data = queryData(**mapping)
    print(name, location,bedroom,sleeps,bathroom,price)
    # print(data)
    return data




@app.route('/')
def home():
    return redirect('http://127.0.0.1:5000/login', code=302)


@app.route('/login')
def login():
    auth = request.authorization
    if auth and auth.password == 'password':
        token = jwt.encode({'user': auth.username, 'exp' : datetime.datetime.utcnow()+datetime.timedelta(seconds=600)}, app.config['SECRET_KEY'])
        url = "http://127.0.0.1:5000/protected?token="f"{token}"
        return jsonify ({'token': token, 'token_verified_url': url})
    return make_response('Could not Verify!', 401, {'WWW-Authenticate': 'Basic realm = "Login Required"'})

if __name__ == '__main__':
    app.run(debug=False)