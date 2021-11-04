from flask import Flask,request,render_template
import random
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
data = {}

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)


class Login(db.Model):
    __tablename__ = 'login'
    user_name = db.Column(db.Text,primary_key=True)
    password = db.Column(db.Text)

    def __init__(self,user_name,password):
        self.user_name = user_name
        self.password = password

    def __repr__(self):
        pass



@app.route("/")
def home_page():
    return render_template("index.html")

@app.route("/",methods=['POST'])
def home_post():
    original_url = request.form.get('link')
    if request.form.get('link') == "" or request.form.get('link')=="http//:  " or request.form.get('link')== None:
        return render_template("index.html")
    ls = ['a','b','c','d','e','f','g','h','i','j','k','l','m','p','r','q','A','B','C','D']
    shorter_url = ''.join(random.sample(ls,5))
    data[shorter_url] = original_url
    return render_template("index.html",shurl=shorter_url)



@app.route("/history")
def history_page():
    return render_template("history.html",data = data)

@app.route("/short/<url>")
def fun(url):
    if url in data:
        return "Redirecting to {}".format(data[url])
    return "Not Found"

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register",methods=['POST','GET'])
def register():
    if request.method == "POST":
        user_name = request.form.get('un')
        password = request.form.get('ps')
        new_user = Login(user_name,password)
        db.session.add(new_user)
        db.session.commit()
        return render_template("login.html")

    return render_template("register.html")

@app.route('/login')
def login_page():
    username = request.form.get('username')
    pasword = request.form.get('password')
    user = Login.query.filter_by(name=username).first()
    pword = Login.query.filter_by(name=pasword).first()
    if user == username and pasword == pword:
        return render_template("index.html")

    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
