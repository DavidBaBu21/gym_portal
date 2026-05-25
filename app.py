from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime
from flask_migrate import Migrate



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gym.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ------------------ MODELOS ------------------

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    rutinas = db.relationship('Rutina', backref='usuario', lazy=True)
    progresos = db.relationship('Progreso', backref='usuario', lazy=True)

class GrupoMuscular(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    ejercicios = db.relationship('Ejercicio', backref='grupo', lazy=True)

class Ejercicio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    archivo = db.Column(db.String(100), nullable=True)  # nombre del PNG
    repeticiones = db.Column(db.String(50), nullable=True)
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupo_muscular.id'), nullable=False)


class Rutina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    dia_semana = db.Column(db.String(20), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    ejercicios = db.relationship('EjercicioRutina', backref='rutina', lazy=True)

class EjercicioRutina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rutina_id = db.Column(db.Integer, db.ForeignKey("rutina.id"), nullable=False)
    ejercicio_id = db.Column(db.Integer, db.ForeignKey("ejercicio.id"), nullable=False)

    series = db.Column(db.Integer, nullable=False, default=3)
    repeticiones = db.Column(db.Integer, nullable=False, default=10)
    descanso = db.Column(db.Integer, nullable=False, default=60)  # segundos
    calentamiento = db.Column(db.Boolean, default=False)

    ejercicio = db.relationship("Ejercicio")

class Progreso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    peso_levantado = db.Column(db.Integer, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

with app.app_context():
    db.create_all()

# ------------------ RUTAS ------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        password = request.form["password"]

        user = Usuario.query.filter_by(usuario=usuario, password=password).first()

        if user:
            # Aquí decides a dónde redirigir
            if user.usuario == "David" and user.password == "12345":
                return redirect(url_for("coach"))   # Coach va a su panel
            else:
                return redirect(url_for("menu", usuario=usuario))  # Usuarios normales al menú
        else:
            return "Usuario o contraseña incorrectos"

    return render_template("login.html")


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        usuario = request.form["usuario"]
        password = request.form["password"]
        nuevo_usuario = Usuario(usuario=usuario, password=password)
        db.session.add(nuevo_usuario)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("registro.html")

@app.route("/menu/<usuario>")
def menu(usuario):
    return render_template("menu.html", usuario=usuario)

@app.route("/rutinas")
def rutinas():
    rutinas = Rutina.query.all()
    return render_template("rutinas.html", rutinas=rutinas)

@app.route("/rutina_hoy/<usuario>")
def rutina_hoy(usuario):
    user = Usuario.query.filter_by(usuario=usuario).first()
    if not user:
        return "Usuario no encontrado"

    dias = ["lunes","martes","miércoles","jueves","viernes","sábado","domingo"]
    dia_actual = dias[datetime.today().weekday()]

    rutina = Rutina.query.filter_by(usuario_id=user.id, dia_semana=dia_actual).first()
    if not rutina:
        return f"No hay rutina asignada para {dia_actual}"

    return render_template("rutina_hoy.html", rutina=rutina)

@app.route("/progreso")
def progreso():
    progresos = Progreso.query.all()
    datos = [
        {"fecha": p.fecha.strftime("%Y-%m-%d"), "peso_levantado": p.peso_levantado}
        for p in progresos
    ]
    return render_template("progreso.html", progresos=datos)

@app.route("/logout")
def logout():
    return redirect(url_for("home"))

# ------------------ CREAR DATOS DE PRUEBA ------------------

@app.route("/crear_datos")
def crear_datos():
    usuario = Usuario.query.filter_by(usuario="david").first()
    if not usuario:
        usuario = Usuario(usuario="david", password="1234")
        db.session.add(usuario)
        db.session.commit()

    # Crear grupos musculares
    pecho = GrupoMuscular(nombre="pecho")
    biceps = GrupoMuscular(nombre="biceps")
    triceps = GrupoMuscular(nombre="triceps")
    db.session.add_all([pecho, biceps, triceps])
    db.session.commit()

    # Crear ejercicios
    press_banca = Ejercicio(nombre="Press banca", repeticiones="4x10", grupo=pecho)
    flexiones = Ejercicio(nombre="Flexiones", repeticiones="3x15", grupo=pecho)
    curl_biceps = Ejercicio(nombre="Curl bíceps", repeticiones="3x12", grupo=biceps)
    extension_triceps = Ejercicio(nombre="Extensión polea", repeticiones="3x12", grupo=triceps)
    db.session.add_all([press_banca, flexiones, curl_biceps, extension_triceps])
    db.session.commit()

    # Crear rutina y asignar ejercicios
    rutina = Rutina(nombre="Rutina de Pecho", dia_semana="lunes", usuario_id=usuario.id)
    db.session.add(rutina)
    db.session.commit()

    db.session.add_all([
        EjercicioRutina(rutina_id=rutina.id, ejercicio_id=press_banca.id),
        EjercicioRutina(rutina_id=rutina.id, ejercicio_id=flexiones.id),
        EjercicioRutina(rutina_id=rutina.id, ejercicio_id=curl_biceps.id),
        EjercicioRutina(rutina_id=rutina.id, ejercicio_id=extension_triceps.id),
    ])
    db.session.commit()

    # Progreso
    progreso = Progreso(fecha=date.today(), peso_levantado=80, usuario_id=usuario.id)
    db.session.add(progreso)
    db.session.commit()

    return "Datos de prueba creados"


@app.route("/crear_ejercicios")
def crear_ejercicios():
    # Lista de grupos musculares (agregamos "pierna")
    grupos = [
        "pecho","espalda","hombros","biceps","triceps",
        "antebrazos","abdomen","gluteos","cuadriceps",
        "isquiotibiales","pantorrillas","pierna"
    ]
    objetos = {}
    for g in grupos:
        gm = GrupoMuscular.query.filter_by(nombre=g).first()
        if not gm:
            gm = GrupoMuscular(nombre=g)
            db.session.add(gm)
            db.session.commit()
        objetos[g] = gm

    # Diccionario de ejercicios por grupo (nombre + archivo PNG)
    ejercicios_por_grupo = {
        "pecho": [
            ("Press banca","press_banca.png"),
            ("Press inclinado","press_inclinado.png"),
            ("Aperturas mancuernas","aperturas_mancuernas.png"),
            ("Cruce polea","cruce_polea.png"),
            ("Flexiones","flexiones.png"),
        ],
        "espalda": [
            ("Dominadas","dominadas.png"),
            ("Jalón pecho polea","jalon_pecho_polea.png"),
            ("Remo barra","remo_barra.png"),
            ("Remo mancuernas","remo_mancuernas.png"),
            ("Peso muerto","peso_muerto.png"),
            # Nuevos
            ("Pull over","pull_over.png"),
            ("Remo T en máquina","remo_t.png"),
            ("Remo en polea baja","remo_polea_baja.png"),
            ("Vuelos posteriores","vuelos_posteriores.png"),
        ],
        "hombros": [
            ("Press militar","press_militar.png"),
            ("Elevaciones laterales","elevaciones_laterales.png"),
            ("Elevaciones frontales","elevaciones_frontales.png"),
            ("Face pulls","face_pulls.png"),
            ("Press Arnold","press_arnold.png"),
        ],
        "biceps": [
            ("Curl barra recta","curl_barra_recta.png"),
            ("Curl mancuernas","curl_mancuernas.png"),
            ("Curl martillo","curl_martillo.png"),
            ("Curl concentrado","curl_concentrado.png"),
            ("Curl polea baja","curl_polea_baja.png"),
        ],
        "triceps": [
            ("Fondos paralelas","fondos_paralelas.png"),
            ("Extensión polea cuerda","extensión_polea_cuerda.png"),
            ("Press francés barra","press_frances_barra.png"),
            ("Patada tríceps","patada_triceps.png"),
            ("Flexiones diamante","flexiones_diamante.png"),
        ],
        "antebrazos": [
            ("Curl muñeca","curl_muñeca.png"),
            ("Curl invertido","curl_invertido.png"),
            ("Farmer’s walk","farmers_walk.png"),
            ("Extensiones muñeca","extensiones_muñeca_mancuerna.png"),
            ("Dominadas invertidas","dominadas_invertidas.png"),
        ],
        "abdomen": [
            ("Crunch abdominal","crunch_abdominal.png"),
            ("Plancha","plancha.png"),
            ("Elevación piernas","elevacion_piernas.png"),
            ("Russian twists","rusian_twists.png"),
            ("AB wheel","ab_wheel.png"),
        ],
        "gluteos": [
            ("Hip thrust","hip_thrust.png"),
            ("Sentadilla sumo","sentadilla_sumo.png"),
            ("Peso muerto rumano","peso_muerto_rumano.png"),
            ("Puente glúteos","puente_gluteos.png"),
            ("Step ups","step_ups.png"),
        ],
        "cuadriceps": [
            ("Sentadilla barra","sentadilla_barra.png"),
            ("Prensa pierna","prensa_pierna.png"),
            ("Zancadas","sancadas.png"),
            ("Extensión pierna máquina","extension_pierna_maquina.png"),
            ("Sentadilla frontal","sentadilla_frontal.png"),
        ],
        "isquiotibiales": [
            ("Curl pierna máquina","curl_pierna_maquina.png"),
            ("Buenos días barra","buenos_dias_barra.png"),
            ("Glute ham raise","glute_ham_raise.png"),
            ("Sentadilla búlgara","sentadilla_bulgara.png"),
            ("Peso muerto rumano","peso_muerto_rumano.png"),
        ],
        "pantorrillas": [
            ("Elevación talones pie","elevacion_talones_pie.png"),
            ("Elevación talones sentado","elevacion_talones_sentado.png"),
            ("Saltos pliométricos","saltos.png"),
            ("Farmer’s walk puntillas","farmers_walk.png"),
            ("Correr pendiente","correr_pendiente.png"),
            # Nuevo
            ("Pantorrilla en máquina","pantorrilla_maquina.png"),
        ],
        "pierna": [
            ("Abductores en máquina","abductores_maquina.png"),
            ("Femorales en máquina","femorales_maquina.png"),
        ],
    }

    # Insertar ejercicios en la base de datos
    for grupo, lista in ejercicios_por_grupo.items():
        gm = objetos.get(grupo)
        if gm:
            for nombre, archivo in lista:
                existente = Ejercicio.query.filter_by(nombre=nombre, grupo=gm).first()
                if not existente:
                    db.session.add(Ejercicio(nombre=nombre, archivo=archivo, grupo=gm))

    db.session.commit()
    return "Ejercicios creados/actualizados correctamente"



@app.route("/ver_ejercicios")
def ver_ejercicios():
    ejercicios = Ejercicio.query.all()
    salida = "<h1>Ejercicios en la base</h1><ul>"
    for e in ejercicios:
        salida += f"<li>{e.nombre} — archivo: {e.archivo} — repeticiones: {e.repeticiones}</li>"
    salida += "</ul>"
    return salida

@app.route("/limpiar_ejercicios")
def limpiar_ejercicios():
    Ejercicio.query.delete()
    db.session.commit()
    return "Ejercicios eliminados"
# Página principal del coach: lista de usuarios
@app.route("/coach")
def coach():
    usuarios = Usuario.query.all()
    return render_template("coach.html", usuarios=usuarios)

# Ver rutinas de un usuario y asignar ejercicios
@app.route("/coach/<int:usuario_id>", methods=["GET", "POST"])
def coach_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    ejercicios = Ejercicio.query.all()
    dias = ["lunes","martes","miércoles","jueves","viernes","sábado","domingo"]

    if request.method == "POST":
        nombre_rutina = request.form["nombre"]
        dia_semana = request.form["dia"]
        seleccionados = request.form.getlist("ejercicios")

        rutina = Rutina(nombre=nombre_rutina, dia_semana=dia_semana, usuario_id=usuario.id)
        db.session.add(rutina)
        db.session.commit()

        for ejercicio_id in seleccionados:
            er = EjercicioRutina(rutina_id=rutina.id, ejercicio_id=int(ejercicio_id))
            db.session.add(er)
        db.session.commit()

        return redirect(url_for("coach_usuario", usuario_id=usuario.id))

    # ordenar rutinas por día de la semana
    rutinas = sorted(
        Rutina.query.filter_by(usuario_id=usuario.id).all(),
        key=lambda r: dias.index(r.dia_semana)
    )

    return render_template("coach_usuario.html", usuario=usuario, rutinas=rutinas, ejercicios=ejercicios, dias=dias)


@app.route("/coach/eliminar_rutina/<int:rutina_id>", methods=["POST"])
def eliminar_rutina(rutina_id):
    rutina = Rutina.query.get_or_404(rutina_id)
    EjercicioRutina.query.filter_by(rutina_id=rutina.id).delete()
    db.session.delete(rutina)
    db.session.commit()
    return redirect(url_for("coach_usuario", usuario_id=rutina.usuario_id))

@app.route("/crear_coach")
def crear_coach():
    coach = Usuario.query.filter_by(usuario="David").first()
    if not coach:
        coach = Usuario(usuario="David", password="12345")
        db.session.add(coach)
        db.session.commit()
    return "Coach creado"

@app.route("/coach/editar_rutina/<int:rutina_id>", methods=["POST"])
def editar_rutina(rutina_id):
    rutina = Rutina.query.get_or_404(rutina_id)

    # actualizar nombre y día
    rutina.nombre = request.form["nombre"]
    rutina.dia_semana = request.form["dia"]

    # limpiar ejercicios anteriores
    EjercicioRutina.query.filter_by(rutina_id=rutina.id).delete()

    # agregar nuevos con parámetros extra
    seleccionados = request.form.getlist("ejercicios")
    for ejercicio_id in seleccionados:
        series = int(request.form.get(f"series_{ejercicio_id}", 3))
        reps = int(request.form.get(f"reps_{ejercicio_id}", 10))
        descanso = int(request.form.get(f"descanso_{ejercicio_id}", 60))
        calentamiento = f"calentamiento_{ejercicio_id}" in request.form

        er = EjercicioRutina(
            rutina_id=rutina.id,
            ejercicio_id=int(ejercicio_id),
            series=series,
            repeticiones=reps,
            descanso=descanso,
            calentamiento=calentamiento
        )
        db.session.add(er)

    db.session.commit()
    return redirect(url_for("coach_usuario", usuario_id=rutina.usuario_id))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
