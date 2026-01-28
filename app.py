from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models.entities import db, User, Paciente, HistoriaClinica

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev_key_123'

# -----------------------
# BASE DE DATOS
# -----------------------
# DESARROLLO (SQLite)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///consultorio.db'

# PRODUCCIÓN (PythonAnywhere - MySQL)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql+pymysql://USUARIO:CLAVE@USUARIO.mysql.pythonanywhere-services.com/consultorio_don_morrondo'
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# -----------------------
# LOGIN
# -----------------------
@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    user = User.query.filter_by(
        username=request.form['username'],
        password=request.form['password']
    ).first()

    if user:
        login_user(user)
        return redirect(url_for('dashboard'))

    flash('Credenciales incorrectas')
    return redirect(url_for('index'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# -----------------------
# DASHBOARD
# -----------------------
@app.route('/dashboard')
@login_required
def dashboard():
    return redirect(url_for('listar_pacientes'))


# -----------------------
# CREAR PACIENTE + HISTORIA
# -----------------------
@app.route('/pacientes/nuevo', methods=['GET', 'POST'])
@login_required
def crear_paciente():
    if current_user.role not in ['admin', 'usuario1']:
        flash('No tenés permiso para crear pacientes')
        return redirect(url_for('listar_pacientes'))

    if request.method == 'POST':
        try:
            paciente = Paciente(
                nombre=request.form['nombre'],
                apellido=request.form['apellido']
            )

            historia = HistoriaClinica(
                diagnostico=request.form['diagnostico'],
                observaciones=request.form['observaciones']
            )

            paciente.historia_clinica = historia
            db.session.add(paciente)
            db.session.commit()

            flash('Paciente creado correctamente')
            return redirect(url_for('listar_pacientes'))

        except Exception:
            db.session.rollback()
            flash('Error al crear paciente')

    return render_template('paciente_form.html')


# -----------------------
# LISTAR PACIENTES
# -----------------------
@app.route('/pacientes')
@login_required
def listar_pacientes():
    pacientes = Paciente.query.filter_by(eliminado=False).all()
    return render_template('pacientes.html', pacientes=pacientes)


# -----------------------
# EDITAR PACIENTE
# -----------------------
@app.route('/pacientes/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_paciente(id):
    if current_user.role not in ['admin', 'usuario2']:
        flash('No tenés permiso para editar pacientes')
        return redirect(url_for('listar_pacientes'))

    paciente = Paciente.query.get_or_404(id)

    if request.method == 'POST':
        try:
            paciente.nombre = request.form['nombre']
            paciente.apellido = request.form['apellido']
            paciente.historia_clinica.diagnostico = request.form['diagnostico']
            paciente.historia_clinica.observaciones = request.form['observaciones']

            db.session.commit()
            flash('Paciente actualizado correctamente')
            return redirect(url_for('listar_pacientes'))

        except Exception:
            db.session.rollback()
            flash('Error al actualizar paciente')

    return render_template(
        'paciente_form.html',
        paciente=paciente,
        editando=True
    )


# -----------------------
# VER HISTORIA CLÍNICA (READ ONLY)
# -----------------------
@app.route('/pacientes/ver/<int:id>')
@login_required
def ver_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    return render_template('paciente_detalle.html', paciente=paciente)


# -----------------------
# BAJA LÓGICA
# -----------------------
@app.route('/pacientes/eliminar/<int:id>')
@login_required
def eliminar_paciente(id):
    if current_user.role != 'admin':
        flash('Solo el administrador puede eliminar')
        return redirect(url_for('listar_pacientes'))

    paciente = Paciente.query.get_or_404(id)
    paciente.eliminado = True
    db.session.commit()

    flash('Paciente eliminado')
    return redirect(url_for('listar_pacientes'))


# -----------------------
# MAIN
# -----------------------
if __name__ == '__main__':
    app.run(debug=True)
