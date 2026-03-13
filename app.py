from flask import Flask, render_template, request, session, redirect
from flask_bcrypt import Bcrypt
import sqlite3

app = Flask(__name__)
app.secret_key = "segredo"

bcrypt = Bcrypt(app)


def conectar():
    return sqlite3.connect("database.db")


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def verificar_login():

    usuario = request.form["usuario"]
    senha = request.form["senha"]

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE usuario=?", (usuario,))
    user = cursor.fetchone()

    conn.close()

    if user:

        senha_hash = user[2]

        if bcrypt.check_password_hash(senha_hash, senha):
            session["usuario"] = usuario
            return redirect("/dashboard")

    return "Usuário ou senha incorretos"


@app.route("/dashboard")
def dashboard():

    if "usuario" not in session:
        return redirect("/")

    return render_template("dashboard.html")


@app.route("/logout")
def logout():

    session.pop("usuario", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)