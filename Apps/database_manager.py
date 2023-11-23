# database_manager.py
import sqlite3
from datetime import datetime

idMunicipe = None
nomeMunicipe = ''
data_hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M")

def create_database():
    try:
        connection = sqlite3.connect("appprotoon.db")
        connection.close()
    except sqlite3.Error as e:
        print(f"Erro ao criar o banco de dados: {e}")

def create_table():
    create_database()
    connection = sqlite3.connect("appprotoon.db")
    cursor = connection.cursor()

    # Criação da tabela reclamacoes se não existir
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reclamacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idMunicipe INTEGER,
                nomeMunicipe TEXT,
                problema TEXT,
                bairro TEXT,
                rua TEXT,
                descricao TEXT,
                status TEXT,
                data_hora TEXT
            );
        """)
        
        # Criação da tabela municipes se não existir
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS municipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,                
                nome TEXT,
                email TEXT,
                senha TEXT,
                data_hora TEXT
            );
        """)
    except sqlite3.Error as e:
        print(f"Erro ao criar a tabela: {e}")
        
    connection.commit()
    connection.close()
    
def validar_login(email, senha):
    try:
        conn = sqlite3.connect('appprotoon.db')
        cursor = conn.cursor()

        # Use placeholders (?) para evitar SQL injection
        cursor.execute('SELECT * FROM municipes WHERE email = ? AND senha = ?', (email, senha))
        
        # Obtém o resultado da consulta
        resultado = cursor.fetchall()

        conn.close()

        # Verifica se há algum registro retornado pela consulta
        if resultado:
            nomeMunicipe = resultado[0][1]
            idMunicipe = resultado[0][0]            
            # Retorna o idMunicipe
            return idMunicipe, nomeMunicipe
        else:
            # Retorna None se não houver correspondência
            return None
    except sqlite3.Error as e:
        print(f"Erro ao validar login no banco de dados: {e}")
        return None    

def save_municipe(nome, email, senha, validate):
    
    if validate:    
        print(f"Nome: {nome}")
        print(f"Email: {email}")
        print(f"Senha: {senha}")
        print(f"Data e hora: {data_hora_atual}")
        
        try:
            # Criação do banco de dados e da tabela se não existirem
            create_database()
            create_table()
        
            # Estabeleça a conexão com o banco de dados (ou crie o banco se não existir)
            conn = sqlite3.connect('appprotoon.db')

            # Crie um cursor para executar operações no banco de dados
            cursor = conn.cursor()
            
            
            
            cursor.execute("INSERT INTO municipes (nome, email, senha, data_hora) VALUES (?, ?, ?, ?)",
                        (nome, email, senha, data_hora_atual))
            
            # Commit para salvar as alterações no banco de dados
            conn.commit()

            # Feche a conexão
            conn.close()
        except sqlite3.Error as e:
            print(f"Erro ao salvar no banco de dados: {e}")
            
def save_reclamacao(idMunicipe, nomeMunicipe, problema, bairro, rua, descricao, validate):
    
    if validate:
        
        print(f"Problema: {problema}")
        print(f"Bairro: {bairro}")
        print(f"Rua: {rua}")
        print(f"Descrição: {descricao}")
        print(f"Data e hora: {data_hora_atual}")
        
        print("idMunicipe:", idMunicipe)
        print("nomeMunicipe:", nomeMunicipe)
        
        try:
            create_database()
            create_table()
        
            conn = sqlite3.connect('appprotoon.db')

            cursor = conn.cursor()
            
            cursor.execute("INSERT INTO reclamacoes (idMunicipe, nomeMunicipe, problema, bairro, rua, descricao, status, data_hora) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        (idMunicipe, nomeMunicipe, problema, bairro, rua, descricao, 'Em Análise', data_hora_atual))
            
            conn.commit()

            conn.close()
        except sqlite3.Error as e:
            print(f"Erro ao salvar no banco de dados: {e}")
            
def get_reclamacoes(idMunicipe):
    try:

        conn = sqlite3.connect('appprotoon.db')
        cursor = conn.cursor()
        print(idMunicipe)

        # Verifica se há reclamações para o idMunicipe
        cursor.execute("SELECT * FROM reclamacoes WHERE idMunicipe = ?", (idMunicipe,))
        reclamacoes = cursor.fetchall()
        print(reclamacoes)

        conn.close()

        return reclamacoes
    except sqlite3.Error as e:
        print(f"Erro ao obter reclamações do banco de dados: {e}")
        return []
