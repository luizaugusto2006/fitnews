# -*- coding: utf-8 -*-
"""Banco de dados SQLite do FitNews: esquema e seed."""
import os
import sqlite3

from data_exercises import EXERCISES

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fitnews.db")

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
    dados_json TEXT NOT NULL DEFAULT '{}',
    criado_em TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);
"""


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.executescript(SCHEMA)
    total = conn.execute("SELECT COUNT(*) c FROM exercicios").fetchone()["c"]
    if total == 0:
        conn.executemany(
            "INSERT INTO exercicios (nome, grupo, equipamento, nivel, contraindicado_para)"
            " VALUES (?, ?, ?, ?, ?)",
            EXERCISES,
        )
    conn.commit()
    conn.close()
