# -*- coding: utf-8 -*-
"""Banco de dados SQLite do FitNews: esquema e seed."""
import os
import secrets
import sqlite3
import time
import unicodedata

from data_exercises import EXERCISES

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fitnews.db")


def _sem_acento(texto):
    return "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )

SCHEMA = """
CREATE TABLE IF NOT EXISTS exercicios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    grupo TEXT NOT NULL,
    equipamento TEXT NOT NULL,
    nivel TEXT NOT NULL,
    contraindicado_para TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS planos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    sexo TEXT NOT NULL DEFAULT '',
    data_nascimento TEXT NOT NULL DEFAULT '',
    idade INTEGER NOT NULL DEFAULT 0,
    email TEXT NOT NULL DEFAULT '',
    telefone TEXT NOT NULL DEFAULT '',
    peso REAL,
    altura REAL,
    imc REAL,
    atividade TEXT NOT NULL DEFAULT 'moderado',
    nivel_treino TEXT NOT NULL DEFAULT 'iniciante',
    dias INTEGER NOT NULL DEFAULT 3,
    horario TEXT NOT NULL DEFAULT '',
    local TEXT NOT NULL DEFAULT 'academia',
    limitacoes TEXT NOT NULL DEFAULT '',
    focos TEXT NOT NULL DEFAULT '',
    observacoes TEXT NOT NULL DEFAULT '',
    personal_id INTEGER,
    anotacoes TEXT NOT NULL DEFAULT '',
    usuario_id INTEGER,
    token TEXT UNIQUE,
    dados_json TEXT NOT NULL DEFAULT '{}',
    criado_em TEXT NOT NULL DEFAULT (datetime('now', '-3 hours'))
);

CREATE TABLE IF NOT EXISTS personais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL,
    codigo TEXT NOT NULL UNIQUE,
    criado_em TEXT NOT NULL DEFAULT (datetime('now', '-3 hours'))
);

CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL,
    codigo_recup TEXT NOT NULL UNIQUE,
    criado_em TEXT NOT NULL DEFAULT (datetime('now', '-3 hours'))
);
"""

# Colunas adicionadas em bancos criados em versoes anteriores
MIGRACOES_PLANOS = [
    ("personal_id", "ALTER TABLE planos ADD COLUMN personal_id INTEGER"),
    ("anotacoes", "ALTER TABLE planos ADD COLUMN anotacoes TEXT NOT NULL DEFAULT ''"),
    ("usuario_id", "ALTER TABLE planos ADD COLUMN usuario_id INTEGER"),
    ("token", "ALTER TABLE planos ADD COLUMN token TEXT"),
]


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.executescript(SCHEMA)
    colunas = {r[1] for r in conn.execute("PRAGMA table_info(planos)")}
    for coluna, ddl in MIGRACOES_PLANOS:
        if coluna not in colunas:
            conn.execute(ddl)
    # Correcao unica: bancos criados antes desta versao gravavam UTC no servidor
    # (PythonAnywhere). Se a maquina esta em UTC, desloca os horarios ja gravados
    # para o horario de Brasilia (UTC-3). user_version garante que roda uma vez.
    if conn.execute("PRAGMA user_version").fetchone()[0] < 1:
        if time.timezone == 0:
            conn.execute("UPDATE planos SET criado_em = datetime(criado_em, '+3 hours')")
            conn.execute("UPDATE personais SET criado_em = datetime(criado_em, '+3 hours')")
        conn.execute("PRAGMA user_version = 1")
    # Reescrita ortografica: os nomes de exercicios agora sao gravados com
    # acentos. Bancos antigos guardam os mesmos nomes sem acento, entao a
    # migracao renomeia os registros e tambem os nomes dentro dos planos
    # ja salvos (dados_json). user_version = 2 garante que roda uma vez.
    if conn.execute("PRAGMA user_version").fetchone()[0] < 2:
        pares = {}
        for nome, _g, _e, _n, _c in EXERCISES:
            antigo = _sem_acento(nome)
            if antigo != nome:
                pares[antigo] = nome
        # Casos que nao diferem apenas por acento
        pares["Rosca scott"] = "Rosca Scott"
        pares["Donkey kick ( patada em quadrupedia )"] = \
            "Donkey kick ( patada em quatro apoios )"
        for antigo, novo in pares.items():
            ja_novo = conn.execute(
                "SELECT 1 FROM exercicios WHERE nome = ?", (novo,)
            ).fetchone()
            tem_antigo = conn.execute(
                "SELECT 1 FROM exercicios WHERE nome = ?", (antigo,)
            ).fetchone()
            if tem_antigo and not ja_novo:
                conn.execute(
                    "UPDATE exercicios SET nome = ? WHERE nome = ?", (novo, antigo)
                )
            conn.execute(
                "UPDATE planos SET dados_json = replace(dados_json, ?, ?)",
                ('"%s"' % antigo, '"%s"' % novo),
            )
        conn.execute("PRAGMA user_version = 2")
    # Privacidade: todo plano ganha um token secreto na URL e os planos
    # antigos ficam sem dono ate que o criador os salve na conta.
    if conn.execute("PRAGMA user_version").fetchone()[0] < 3:
        pendentes = conn.execute(
            "SELECT id FROM planos WHERE token IS NULL OR token = ''").fetchall()
        for r in pendentes:
            while True:
                token = secrets.token_urlsafe(9)
                if not conn.execute("SELECT 1 FROM planos WHERE token=?",
                                    (token,)).fetchone():
                    break
            conn.execute("UPDATE planos SET token=? WHERE id=?", (token, r["id"]))
        conn.execute("PRAGMA user_version = 3")
    total = conn.execute("SELECT COUNT(*) c FROM exercicios").fetchone()["c"]
    if total == 0:
        conn.executemany(
            "INSERT INTO exercicios (nome, grupo, equipamento, nivel, contraindicado_para)"
            " VALUES (?, ?, ?, ?, ?)",
            EXERCISES,
        )
    conn.commit()
    conn.close()
