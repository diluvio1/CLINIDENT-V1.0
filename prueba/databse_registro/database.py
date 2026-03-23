from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pymysql
import bcrypt

app = Flask(__name__)
CORS(app)

# --- 1. CONFIGURACIÓN DE LA BASE DE DATOS ---
DB_CONFIG = {
    'host': 'localhost',
    'port': 3307,
    'user': 'root',
    'password': '',
    'database': 'clinident',
    'charset': 'utf8mb4'
}

def get_db():
    return pymysql.connect(**DB_CONFIG)

# --- 2. RUTAS DE NAVEGACIÓN (Páginas HTML) ---

@app.route('/')
def login_page():
    """Ahora el Login es la página inicial"""
    return render_template('login.html')

@app.route('/registro')
def registro_page():
    """Ruta para ir al formulario de registro"""
    return render_template('registro.html')

@app.route('/principal')
def principal():
    """Pantalla de éxito tras loguearse"""
    return "<h1>Bienvenido al Panel Principal de Clinident</h1>"

# --- 3. RUTAS DE LÓGICA (Procesamiento de datos) ---

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
                return "success"
            else:
                return "incorrecto"
        else:
            return "no_existe"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/registrar', methods=['POST'])
def registrar():
    datos = request.get_json()
    nombre = datos.get('nombre', '').strip()
    apellido = datos.get('apellido', '').strip()
    email = datos.get('email', '').strip()
    telefono = datos.get('telefono', '').strip()
    password = datos.get('password', '')

    hash_pass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        db = get_db()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO usuarios (nombre, apellido, email, telefono, password_hash) VALUES (%s,%s,%s,%s,%s)",
            (nombre, apellido, email, telefono, hash_pass)
        )
        db.commit()
        db.close()
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'msg': str(e)}), 500

# --- 4. EJECUCIÓN ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)