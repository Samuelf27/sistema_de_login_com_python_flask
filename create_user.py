import sqlite3
from flask_bcrypt import Bcrypt
from flask import Flask

app = Flask(__name__)
bcrypt = Bcrypt(app)

usuario = "admin"
senha = "1234"

senha_hash = bcrypt.generate_password_hash(senha).decode("utf-8")

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute(
    "INSERT INTO usuarios (usuario, senha) VALUES (?, ?)",
    (usuario, senha_hash)
)

conn.commit()
conn.close()

print("Usuário criado!")