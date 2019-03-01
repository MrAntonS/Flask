from flask import Flask, url_for, request
from flask import render_template, json, redirect, jsonify
from db_editor import DB, NewsModel, UsersModel
from flask_restful import reqparse, abort, Api, Resource
from forms import LoginForm, SignInForm, AddNewsForm
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SECRET_KEY'] = 'VERY_SECRET_KEY'
database = 'FLASK.db'
session = {}


#Greeting page
@app.route('/')
@app.route('/index')
def index():
    if 'username' not in session:
        return redirect('/login')
    
    news = "NEWS"#NewsModel(db.get_connection()).get_all(session['user_id'])
    return render_template('index.html', username=session['username'],
                           news=news, session=session)


@app.route('/login', methods=["GET", "POST"])
def login(): 
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user_name = login_form.username.data
        password = login_form.password.data
        #print(user_name, password,sep="||")
        users_model = UsersModel(db.get_connection())
        pwd = users_model.get_pwd(user_name)
        print(pwd)
        if pwd and pwd[0]:
            if check_password_hash(pwd[2], password):
                session['username'] = user_name
                session['user_id'] = pwd[1]
        return redirect("/index")        
    return render_template('login.html', title='Авторизация', form=login_form)


@app.route('/logout')
def logout():
    session.pop('username',0)
    session.pop('user_id',0)
    return redirect('/login')
    

@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    sign_in_form = SignInForm()
    if sign_in_form.validate_on_submit():
        user_name = sign_in_form.username.data
        password = generate_password_hash(sign_in_form.password.data)
        users_model = UsersModel(db.get_connection())
        if not users_model.get_pwd(user_name):
            #Проверка на свободность логина
            users_model.insert(user_name, password)
            session['username'] = user_name
            session['user_id'] = password
            return redirect("/index") 
    return render_template("sign_in.html", title="Зарегестрироваться", form=sign_in_form)
parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('content', required=True)
parser.add_argument('user_id', required=True, type=int)


if __name__ == '__main__':
    db = DB(database)
    app.run(port=8080, host='127.0.0.1')
   