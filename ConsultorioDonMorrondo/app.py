
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from models.entities import db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'consultorio_don_morrondo'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://USER:PASS@HOST/consultorio_don_morrondo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash("Credenciales incorrectas")
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        return render_template('admin.html')
    elif current_user.role == 'usuario1':
        return render_template('usuario1.html')
    elif current_user.role == 'usuario2':
        return render_template('usuario2.html')
    else:
        return render_template('usuario3.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
