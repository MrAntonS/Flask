from flask import Flask, url_for, request
from flask import render_template, json, redirect, jsonify
from db_editor import DB, NewsModel, UsersModel, FriendsModel
from flask_restful import reqparse, abort, Api, Resource
from forms import LoginForm, SignInForm, AddNewsForm
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SECRET_KEY'] = 'VERY_SECRET_KEY'
database = 'FLASK.db'
session = {}


def check():
    if 'username' not in session:
        return True
    return False


@app.route('/')
@app.route('/index')
def index():
    if check(): return redirect('/login')
    
    users_model = UsersModel(db.get_connection())
    friends_model = FriendsModel(db.get_connection())
    
    friends_ids = list(map(lambda x: x[2],
                           friends_model.get_friends(session['user_id'])))
    
    news = []
    for friend_id in friends_ids:
        news += get_news(friend_id)

    if news:
        news = map(lambda x: [users_model.get_name(x[0]), x[1], x[2]], news)
    return render_template('index.html', username=session['username'],
                           news=news, session=session)


@app.route('/login', methods=["GET", "POST"])
def login(): 
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user_name = login_form.username.data
        password = login_form.password.data
        users_model = UsersModel(db.get_connection())
        
        pwd = users_model.get(user_name=user_name)
        if pwd and pwd[0]:
            if check_password_hash(pwd[2], password):
                session['username'] = user_name
                session['user_id'] = pwd[0]
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
        if not users_model.get(user_name=user_name):
            #Проверка на свободность логина
            
            user_id = users_model.insert(user_name, password)
            session['username'] = user_name
            session['user_id'] = user_id
            
            friends_model = FriendsModel(db.get_connection())
            friends_model.add_friend(1, user_id)
            friends_model.add_friend(user_id, 1)
            friends_model.add_friend(user_id, user_id)
            
            return redirect("/index") 
    return render_template("sign_in.html", title="Зарегестрироваться", form=sign_in_form)


@app.route("/friends_list")
def friends_list():
    if check(): return redirect('/login')
    
    friends_model = FriendsModel(db.get_connection())
    users_model = UsersModel(db.get_connection())
    friends_ids = friends_model.get_friends(session['user_id'])

    if friends_ids and str(session['user_id']) != "1":
        friends = map(lambda x: [users_model.get_name(x[2]), x[2]], friends_ids)
        return render_template("friends_list.html", title="Мои друзья", friends=friends, session=session)
    return render_template("friends_list.html", title="Мои друзья", friends=None, session=session)


@app.route("/remove_friend/<int:author_id>")
def remove_friend(author_id):
    if check(): return redirect('/login')
    
    friends_model = FriendsModel(db.get_connection())
    if friends_model.check_friendship(session["user_id"], author_id):
        if session['user_id'] != author_id and str(author_id) != "1":
            friends_model.remove_friend(session["user_id"], author_id)
    return redirect("/friends_list")


@app.route("/users_list")
def users_list():
    if check(): return redirect('/login')
    
    friends_model = FriendsModel(db.get_connection())
    users_model = UsersModel(db.get_connection())
    
    check_friendship = lambda x: not friends_model.check_friendship(session['user_id'], x)
    users_ids = users_model.get_all_ids()
    
    users = filter(check_friendship, users_ids)
    users = list(map(lambda x: [users_model.get_name(x), x], users))
    return render_template("users_list.html", title="С кем бы подружиться?", users=users, session=session)


@app.route("/add_friend/<int:author_id>")
def add_friend(author_id):
    if check(): return redirect('/login')
    
    friends_model = FriendsModel(db.get_connection())
    
    if not friends_model.check_friendship(session["user_id"], author_id):
        friends_model.add_friend(session["user_id"], author_id)
    return redirect("/users_list")


@app.route("/add_new", methods=["GET", "POST"])
def add_new():
    if check(): return redirect('/login')
    
    news_model = NewsModel(db.get_connection())
    news_form = AddNewsForm()
    
    if news_form.validate_on_submit():
        title = news_form.title.data
        content = news_form.content.data
        news_model.insert(title, content, session['user_id'])
        return redirect("/index")
    return render_template("add_new.html", title="Добавить новость", form=news_form, session=session)
  

@app.route("/del_news")
def del_news():
    if check(): return redirect('/login')
    
    user_model = UsersModel(db.get_connection())
    news_model = NewsModel(db.get_connection())
    lambda_for_jinja = lambda x: [x[1], user_model.get_name(x[3]), x[0]]
    if str(session['user_id']) == '1':
        news = list(map(lambda_for_jinja, news_model.get_all()))
    else:
        news = list(map(lambda_for_jinja, news_model.get_all(session['user_id'])))
    return render_template("del_news.html", title="Удалить новости", session=session, news=news)


@app.route("/del_news/<int:news_id>")
def del_new(news_id):
    if check(): return redirect('/login')
    
    news_model = NewsModel(db.get_connection())
    user_model = UsersModel(db.get_connection())
    new = news_model.get(news_id)
    
    if new:
        authors_id = new[3]
        if str(session["user_id"]) == "1" or int(session['user_id']) == authors_id:
            news_model.delete(news_id)
    return redirect("/del_news")


def get_news(user_id):
    news_model = NewsModel(db.get_connection())
    news = list(map(lambda x: [user_id, x[1], x[2]],
                    news_model.get_all(user_id)))
    return news


if __name__ == '__main__':
    db = DB(database)
    app.run(port=8080, host='127.0.0.1')
   