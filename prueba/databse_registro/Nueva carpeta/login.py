# --- RUTA PARA MOSTRAR EL LOGIN ---
@app.route('/login')
def login_page():
    return render_template('login.html')

# --- RUTA QUE PROCESA EL LOGIN ---
@app.route('/validar_login', methods=['POST'])
def validar_login():
    # Flask recibe el FormData mediante request.form
    correo = request.form.get('usuario')
    password_escrita = request.form.get('password')

    try:
        db = get_db()
        # Usamos DictCursor para poder acceder como usuario['password_hash']
        cur = db.cursor(pymysql.cursors.DictCursor) 
        
        cur.execute("SELECT * FROM usuarios WHERE email = %s LIMIT 1", (correo,))
        usuario = cur.fetchone()
        db.close()

        if usuario:
            hash_almacenado = usuario['password_hash']
            
            # Convertir a bytes si es necesario
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