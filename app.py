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
                link_Da_Imagem TEXT NOT NULL
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
    link_Da_Imagem = dados.get("link_Da_Imagem")

    if not titulo or not categoria or not autor or not link_Da_Imagem:
        return jsonify({"erro": "TODOS OS CAMPOS SÃO OBRIGATÓRIOS"}), 400
    
    with sqlite3.connect("database.db") as conn:
        conn.execute(f"""
        INSERT INTO LIVROS (titulo, categoria, autor, link_Da_Imagem)
        VALUES ("{titulo}", "{categoria}", "{autor}", "{link_Da_Imagem}")
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
                "link_Da_Imagem": item[4]
            }

            livros_formatados.append(dicionario) 

    return jsonify(livros_formatados)

if __name__ == "__main__":
    app.run(debug=True)