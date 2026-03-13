import customtkinter as ctk
from tkinter import messagebox, Toplevel, Listbox
import sqlite3
import hashlib
import re
from PIL import Image

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

conexion = sqlite3.connect("usuarios.db")
cursor = conexion.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT, apellido TEXT, correo TEXT UNIQUE, rol TEXT, password TEXT
)
""")
conexion.commit()

def validar_password(password):
    return len(password) >= 8 and re.search("[A-Z]", password) and \
           re.search("[a-z]", password) and re.search("[0-9]", password)

def cifrar(password):
    return hashlib.sha256(password.encode()).hexdigest()

def existe_admin():
    cursor.execute("SELECT * FROM usuarios WHERE rol='Administrador'")
    return cursor.fetchone()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión - Registro")
        self.geometry("900x650")
        self.resizable(False, False)

        self.admin_exists = existe_admin()

        try:
            img_path = r"C:\Users\MatDosuki\Documents\sena\Nueva carpeta\clini.png"
            self.bg_image = ctk.CTkImage(Image.open(img_path), size=(900, 650))
            self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
            self.bg_label.place(relx=0, rely=0)
        except:
            self.configure(fg_color="#E0E0E0")

        self.card = ctk.CTkFrame(self, corner_radius=20, fg_color="white")
        self.card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.45, relheight=0.85)

        titulo_texto = "Crear Usuario" if self.admin_exists else "Crear Administrador"
        self.lbl_titulo = ctk.CTkLabel(self.card, text=titulo_texto, font=("Helvetica", 22, "bold"))
        self.lbl_titulo.pack(pady=(25, 20))

        self.ent_nombre = self.crear_input("Nombre", "Nombre")
        self.ent_apellido = self.crear_input("Apellido", "Apellido")
        self.ent_correo = self.crear_input("Correo", "correo@ejemplo.com")

        if self.admin_exists:
            ctk.CTkLabel(self.card, text="Rol").pack(anchor="w", padx=45)
            self.combo_rol = ctk.CTkOptionMenu(self.card, values=["Recepcionista", "Odontólogo"])
            self.combo_rol.pack(fill="x", padx=45, pady=(0, 10))
        else:
            self.rol_fijo = "Administrador"

        self.ent_pass = self.crear_input("Contraseña", "********", show="*")
        self.ent_conf = self.crear_input("Confirmar", "********", show="*")

        self.btn_accion = ctk.CTkButton(self.card, text=titulo_texto,
                                       command=self.ejecutar_registro)
        self.btn_accion.pack(fill="x", padx=45, pady=(10, 5))

        if self.admin_exists:
            self.btn_ver = ctk.CTkButton(self.card, text="Ver usuarios registrados",
                                         command=self.ver_usuarios)
            self.btn_ver.pack(fill="x", padx=45, pady=5)

            self.btn_reset = ctk.CTkButton(self.card, text="Reiniciar Administrador",
                                           fg_color="red",
                                           command=self.reiniciar_admin)
            self.btn_reset.pack(fill="x", padx=45, pady=(5, 10))

    def crear_input(self, label, placeholder, show=""):
        ctk.CTkLabel(self.card, text=label).pack(anchor="w", padx=45)
        entry = ctk.CTkEntry(self.card, placeholder_text=placeholder, show=show)
        entry.pack(fill="x", padx=45, pady=(0, 10))
        return entry

    def ejecutar_registro(self):
        n, a, c = self.ent_nombre.get(), self.ent_apellido.get(), self.ent_correo.get()
        p, cf = self.ent_pass.get(), self.ent_conf.get()
        r = self.combo_rol.get() if self.admin_exists else "Administrador"

        if not all([n, a, c, p, cf]):
            messagebox.showerror("Error", "Complete todos los campos")
            return

        if p != cf:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return

        if not validar_password(p):
            messagebox.showerror("Error", "Contraseña débil")
            return

        try:
            cursor.execute("INSERT INTO usuarios VALUES (NULL,?,?,?,?,?)",
                           (n, a, c, r, cifrar(p)))
            conexion.commit()
            messagebox.showinfo("Éxito", "Usuario registrado")
            self.destroy()
            App().mainloop()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Correo ya existe")

    def reiniciar_admin(self):
        if messagebox.askyesno("Confirmar", "¿Eliminar Administrador?"):
            cursor.execute("DELETE FROM usuarios WHERE rol='Administrador'")
            conexion.commit()
            self.destroy()
            App().mainloop()

    def ver_usuarios(self):
        win = Toplevel(self)
        win.title("Usuarios registrados")
        win.geometry("400x400")

        cursor.execute("SELECT id,nombre,apellido,correo,rol FROM usuarios")
        datos = cursor.fetchall()

        lbl = ctk.CTkLabel(win, text=f"Total usuarios: {len(datos)}")
        lbl.pack(pady=5)

        lista = Listbox(win)
        lista.pack(fill="both", expand=True, padx=10, pady=5)

        for u in datos:
            lista.insert("end", f"{u[0]} - {u[1]} {u[2]} ({u[4]})")

        def editar():
            sel = lista.curselection()
            if not sel:
                return
            user = datos[sel[0]]

            edit = Toplevel(win)
            edit.title("Editar usuario")
            edit.geometry("300x300")

            en = ctk.CTkEntry(edit)
            en.insert(0, user[1])
            en.pack(pady=5)

            ea = ctk.CTkEntry(edit)
            ea.insert(0, user[2])
            ea.pack(pady=5)

            ec = ctk.CTkEntry(edit)
            ec.insert(0, user[3])
            ec.pack(pady=5)

            rol = ctk.CTkOptionMenu(edit, values=["Administrador","Recepcionista","Odontólogo"])
            rol.set(user[4])
            rol.pack(pady=5)

            def guardar():
                cursor.execute("""
                UPDATE usuarios SET nombre=?,apellido=?,correo=?,rol=? WHERE id=?
                """,(en.get(),ea.get(),ec.get(),rol.get(),user[0]))
                conexion.commit()
                messagebox.showinfo("Listo","Usuario actualizado")
                edit.destroy()
                win.destroy()

            ctk.CTkButton(edit,text="Guardar cambios",command=guardar).pack(pady=10)

        ctk.CTkButton(win, text="Editar usuario", command=editar).pack(pady=5)

if __name__ == "__main__":
    app = App()
    app.mainloop()