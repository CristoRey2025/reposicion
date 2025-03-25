from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)
app.secret_key = 'mi_clave_secreta'  # Necesaria para sesiones

# Conectar a la base de datos
def obtener_usuario(nombre_usuario):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", (nombre_usuario,))
    usuario = cursor.fetchone()
    conn.close()
    return usuario

# Vista de inicio de sesión
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        contraseña = request.form["contraseña"]
        usuario_db = obtener_usuario(usuario)
        
        if usuario_db and usuario_db[2] == contraseña:  # Contraseña correcta
            session['usuario'] = usuario
            return redirect(url_for("reporte"))
        else:
            return "Usuario o contraseña incorrectos"
    
    return render_template("login.html")

# Vista para mostrar el reporte y generar el PDF
@app.route("/reporte")
def reporte():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    # Generar el PDF
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, f"Reporte generado para {session['usuario']}")
    c.drawString(100, 735, "Aquí van los datos del reporte...")
    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer.getvalue()

if __name__ == "__main__":
    app.run(debug=True)
