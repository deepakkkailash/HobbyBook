from flask import Blueprint,request,redirect,url_for
from Models import User
auth = Blueprint('auth',__name__)


@auth.route('/login',methods=["POST"])
def login():
    formdata = request.form
    username,password = [formdata.get('username'),formdata.get('password').encode('utf-8')]
    if(User.loginuser(username,password)==200):
        return redirect(url_for('views.homepage'))
    else:
        return redirect(url_for('views.index'))


@auth.route('/signup',methods=["POST"])
def signup():
    formdata = request.form
    username,password, name = [formdata.get('username'),formdata.get('password').encode('utf-8'),formdata.get('name')]
    if (User.signupuser(username, password,name) == 200):
        return redirect(url_for('views.homepage'))
    else:
        return redirect(url_for('views.index'))
