# app.py
from flask import Flask, request, jsonify, render_template
from db import get_connection

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# 📌 Criar colaborador
@app.route('/colaboradores', methods=['POST'])
def criar_colaborador():
    data = request.json

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO colaboradores (nome, cpf, setor_id, funcao_id)
        VALUES (%s, %s, %s, %s)
        RETURNING id, nome, cpf
    """, (
        data['nome'],
        data['cpf'],
        data.get('setor_id'),
        data.get('funcao_id')
    ))

    novo = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    return jsonify(novo)

# 📌 Listar colaboradores
@app.route('/colaboradores', methods=['GET'])
def listar_colaboradores():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, nome, cpf FROM colaboradores")
    dados = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(dados)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)