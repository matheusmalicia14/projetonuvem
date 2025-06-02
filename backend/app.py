from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
CORS(app)

# Dados de conexão com o RDS PostgreSQL
DB_HOST = 'postgres.c7pczpibkir2.us-east-1.rds.amazonaws.com'
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASSWORD = 'malicia1234'

def get_conn():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

@app.route("/api/filmes", methods=["GET"])
def listar_filmes():
    conn = get_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM filmes ORDER BY id")
    filmes = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(filmes)

@app.route("/api/filmes", methods=["POST"])
def adicionar_filme():
    novo = request.get_json()
    if not novo or "titulo" not in novo or "ano" not in novo:
        return jsonify({"erro": "Dados inválidos"}), 400
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO filmes (titulo, ano) VALUES (%s, %s) RETURNING id", (novo["titulo"], novo["ano"]))
    novo_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    novo["id"] = novo_id
    return jsonify(novo), 201

@app.route("/api/filmes/<int:id>", methods=["PUT"])
def atualizar_filme(id):
    dados = request.get_json()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE filmes SET titulo = %s, ano = %s WHERE id = %s",
                (dados.get("titulo"), dados.get("ano"), id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensagem": "Filme atualizado"})

@app.route("/api/filmes/<int:id>", methods=["DELETE"])
def deletar_filme(id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM filmes WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensagem": "Filme deletado"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
