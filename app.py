from flask import Flask, request, jsonify
import sqlite3 
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def init_db():
    with sqlite3.connect("database.db") as conn:
        conn.execute(
            """
                CREATE TABLE IF NOT EXISTS LIVROS(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                categoria TEXT NOT NULL,
                autor TEXT NOT NULL,
                imagem_url TEXT NOT NULL
                )
            """
        )

init_db()

@app.route("/")
def pagina_principal():
    return "<h1>Bem-vindos a minha API, espero que se orgulhem do meu desenvolvimento graças a VOCÊS!!</h1>"

@app.route("/doar", methods=["POST"])
def doar():
    dados = request.get_json()

    titulo = dados.get("titulo")
    categoria = dados.get("categoria")
    autor = dados.get("autor")
    imagem_url = dados.get("imagem_url")

    if not titulo or not categoria or not autor or not imagem_url:
        return jsonify({"erro": "TODOS OS CAMPOS SÃO OBRIGATÓRIOS"}), 400
    
    with sqlite3.connect("database.db") as conn:
        conn.execute(f"""
        INSERT INTO LIVROS (titulo, categoria, autor, imagem_url)
        VALUES ("{titulo}", "{categoria}", "{autor}", "{imagem_url}")
        """)
        conn.commit()

    return jsonify({"mensagem": "LIVRO CADRASTRADO COM SUCESSO!"}), 201

@app.route("/livros", methods=["GET"])
def livros_doados():

    with sqlite3.connect("database.db") as conn:
        livros = conn.execute("SELECT * FROM LIVROS").fetchall() 

        livros_formatados = []
        for item in livros:
            dicionario = {
                "id": item[0],
                "titulo": item[1],
                "categoria": item[2],
                "autor": item[3],
                "imagem_url": item[4]
            }

            livros_formatados.append(dicionario) 

    return jsonify(livros_formatados)

if __name__ == "__main__":
    app.run(debug=True)