from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

filmes = [
    {"id": 1, "titulo": "Matrix", "ano": 1999},
    {"id": 2, "titulo": "Interestelar", "ano": 2014}
]

@app.route("/api/filmes", methods=["GET"])
def listar_filmes():
    return jsonify(filmes)

@app.route("/api/filmes", methods=["POST"])
def adicionar_filme():
    novo = request.json
    novo["id"] = filmes[-1]["id"] + 1 if filmes else 1
    filmes.append(novo)
    return jsonify(novo), 201

@app.route("/api/filmes/<int:id>", methods=["PUT"])
def atualizar_filme(id):
    for filme in filmes:
        if filme["id"] == id:
            dados = request.json
            filme.update(dados)
            return jsonify(filme)
    return jsonify({"erro": "Filme não encontrado"}), 404

@app.route("/api/filmes/<int:id>", methods=["DELETE"])
def deletar_filme(id):
    global filmes
    filmes = [f for f in filmes if f["id"] != id]
    return jsonify({"mensagem": "Filme deletado"})

if __name__ == "__main__":
    app.run(debug=True)
