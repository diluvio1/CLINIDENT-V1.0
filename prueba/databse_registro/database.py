from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pymysql
import bcrypt

app = Flask(__name__)
CORS(app)

# --- 1. CONFIGURACIÓN DE LA BASE DE DATOS ---
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',
    'database': 'clinident',
    'charset': 'utf8mb4'
}

def get_db():
    return pymysql.connect(**DB_CONFIG)

# --- 2. RUTAS DE NAVEGACIÓN ---

@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/registro')
def registro_page():
    return render_template('registro.html')

@app.route('/agenda')
def agenda():
    return render_template('agenda.html')

@app.route('/odontologo')
def odontologo():
    return render_template('odontologo.html')

@app.route('/facturacion')
def facturacion():
    return render_template('facturacion.html')

@app.route('/odontologoagenda')
def odontologoagenda():
    return render_template('odontologoagenda.html')

@app.route('/historial')
def historial():
    return render_template('historial.html')

@app.route('/index')
def registrar_atencion():
    return render_template('index.html')



# --- 3. RUTAS DE LÓGICA ---

@app.route('/validar_login', methods=['POST'])
def validar_login():
    correo = request.form.get('usuario')
    password_escrita = request.form.get('password')

    try:
        db = get_db()
        cur = db.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT * FROM usuarios WHERE email = %s LIMIT 1", (correo,))
        usuario = cur.fetchone()
        db.close()

        if usuario:
            hash_almacenado = usuario['password_hash']
            if isinstance(hash_almacenado, str):
                hash_almacenado = hash_almacenado.encode('utf-8')

            if bcrypt.checkpw(password_escrita.encode('utf-8'), hash_almacenado):
                rol = usuario['rol']

                if rol in [3, 4]:
                    redirect_url = '/agenda'
                elif rol in [1, 2]:
                    redirect_url = '/odontologo'
                else:
                    redirect_url = '/principal'  # Los otros roles por ahora van aquí

                return jsonify({
                    'status': 'success',
                    'rol': rol,
                    'nombre': usuario['nombre'],
                    'redirect': redirect_url
                })
            else:
                return jsonify({'status': 'error', 'msg': 'incorrecto'})
        else:
            return jsonify({'status': 'error', 'msg': 'no_existe'})

    except Exception as e:
        return jsonify({'status': 'error', 'msg': str(e)})


@app.route('/registrar', methods=['POST'])
def registrar():
    datos = request.get_json()
    nombre   = datos.get('nombre', '').strip()
    apellido = datos.get('apellido', '').strip()
    email    = datos.get('email', '').strip()
    telefono = datos.get('telefono', '').strip()
    password = datos.get('password', '')
    rol      = datos.get('rol', 4)

    if rol not in [1, 2, 3, 4]:
        rol = 4

    hash_pass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        db = get_db()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO usuarios (nombre, apellido, email, telefono, password_hash, rol) VALUES (%s,%s,%s,%s,%s,%s)",
            (nombre, apellido, email, telefono, hash_pass, rol)
        )
        db.commit()
        db.close()
        return jsonify({'status': 'success'})

    except Exception as e:
        return jsonify({'status': 'error', 'msg': str(e)}), 500


# --- 4. EJECUCIÓN ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)