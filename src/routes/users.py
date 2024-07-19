from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models.ModelUser import ModelUser
from models.entities.User import User
from flask_mysqldb import MySQL

users_bp = Blueprint('users', __name__)

# Base de datos
db = MySQL()

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        user=User(0,request.form['username'],request.form['password'])
        logged_user=ModelUser.login(db, user)

        if logged_user!=None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('vehicles.vehicles'))
            else:
                flash("password_invalid...")
                return render_template('auth/login.html')
        else:
            flash("user not found...")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@users_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))

@users_bp.route('/home')
def home():
    return render_template('home.html')
