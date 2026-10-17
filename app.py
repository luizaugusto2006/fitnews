# -*- coding: utf-8 -*-
"""FitNews - site de academia: gerador de treino, alimentacao e suplementos."""
import json
import os
from datetime import date

from flask import (Flask, abort, flash, redirect, render_template, request,
                   session, url_for)

from data_content import LIMITATION_LABELS
from database import get_db, init_db
from gerador import (ATIVIDADE_LABELS, FOCOS, FOCO_LABELS, LIMITACOES,
                     LIMIT_LABELS, gerar_plano)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "fitnews-dev-key-troque-em-producao")

ADMIN_USER = os.environ.get("ADMIN_USER", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "fitnews2026")

NIVEIS = [("iniciante", "Iniciante (nunca treinei ou até 6 meses)"),
          ("intermediario", "Intermediário (6 meses a 2 anos)"),
          ("avancado", "Avançado (mais de 2 anos)")]
ATIVIDADES = list(ATIVIDADE_LABELS.items())
HORARIOS = [("manha", "Manhã"), ("tarde", "Tarde"), ("noite", "Noite"),
            ("variado", "Variado / conforme a agenda")]


def calcular_idade(nasc):
    try:
        d = date.fromisoformat(nasc)
    except ValueError:
        return None
    hoje = date.today()
    idade = hoje.year - d.year - ((hoje.month, hoje.day) < (d.month, d.day))
    return idade if 10 <= idade <= 100 else None


def _multi_vals(form, campo):
    """Aceita varios checkboxes ou uma string unica separada por virgulas."""
    valores = []
    for v in form.getlist(campo):
        valores.extend([x.strip() for x in v.split(",") if x.strip()])
    return list(dict.fromkeys(valores))


def ler_formulario(form):
    focos = _multi_vals(form, "focos")
    limitacoes = _multi_vals(form, "limitacoes")
    if "nenhuma" in limitacoes and len(limitacoes) > 1:
        limitacoes = ["nenhuma"]
    nasc = form.get("data_nascimento", "")
    idade = calcular_idade(nasc)
    peso = form.get("peso", type=float) or None
    altura = form.get("altura", type=float) or None
    imc = round(peso / ((altura / 100) ** 2), 1) if peso and altura and altura > 0 else None
    dados = {
        "nome": form.get("nome", "").strip(),
        "email": form.get("email", "").strip(),
        "telefone": form.get("telefone", "").strip(),
        "sexo": form.get("sexo", ""),
        "data_nascimento": nasc,
        "idade": idade,
        "peso": peso,
        "altura": altura,
        "imc": imc,
        "atividade": form.get("atividade", "moderado"),
        "nivel_treino": form.get("nivel_treino", "iniciante"),
        "dias": int(form.get("dias", 3) or 3),
        "horario": form.get("horario", ""),
        "local": form.get("local", "academia"),
        "limitacoes": limitacoes,
        "focos": focos,
        "observacoes": form.get("observacoes", "").strip(),
    }
    erros = []
    if not dados["nome"] or len(dados["nome"]) < 2:
        erros.append("Informe seu nome.")
    if not idade:
        erros.append("Informe uma data de nascimento válida (idade entre 10 e 100 anos).")
    if not focos:
        erros.append("Selecione pelo menos um foco/objetivo.")
    if form.get("aceite") != "sim":
        erros.append("É preciso aceitar o aviso de segurança para gerar o plano.")
    return dados, erros


# ------------------------------------------------------------------
# Paginas publicas
# ------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/criar", methods=["GET", "POST"])
def criar():
    if request.method == "POST":
        dados, erros = ler_formulario(request.form)
        if erros:
            for e in erros:
                flash(e, "erro")
            return render_template("criar.html", dados=dados, focos=FOCOS,
                                   limitacoes=LIMITACOES, niveis=NIVEIS,
                                   atividades=ATIVIDADES, horarios=HORARIOS)
        plano_json = gerar_plano(dados)
        conn = get_db()
        cur = conn.execute(
            "INSERT INTO planos (nome, sexo, data_nascimento, idade, email, telefone,"
            " peso, altura, imc, atividade, nivel_treino, dias, horario, local,"
            " limitacoes, focos, observacoes, dados_json)"
            " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (dados["nome"], dados["sexo"], dados["data_nascimento"], dados["idade"],
             dados["email"], dados["telefone"], dados["peso"], dados["altura"],
             dados["imc"], dados["atividade"], dados["nivel_treino"], dados["dias"],
             dados["horario"], dados["local"], ",".join(dados["limitacoes"]),
             ",".join(dados["focos"]), dados["observacoes"], json.dumps(plano_json, ensure_ascii=False)),
        )
        pid = cur.lastrowid
        conn.commit()
        conn.close()
        return redirect(url_for("ver_plano", plano_id=pid))
    return render_template("criar.html", dados={}, focos=FOCOS, limitacoes=LIMITACOES,
                           niveis=NIVEIS, atividades=ATIVIDADES, horarios=HORARIOS)


def _carregar_plano(plano_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM planos WHERE id=?", (plano_id,)).fetchone()
    conn.close()
    if not row:
        abort(404)
    plano = dict(row)
    plano["dados"] = json.loads(plano["dados_json"])
    plano["limitacoes_lista"] = [x for x in (plano["limitacoes"] or "").split(",") if x]
    plano["focos_lista"] = [x for x in (plano["focos"] or "").split(",") if x]
    return plano


@app.route("/plano/<int:plano_id>")
def ver_plano(plano_id):
    plano = _carregar_plano(plano_id)
    return render_template("plano.html", plano=plano, FOCO_LABELS=FOCO_LABELS,
                           LIMIT_LABELS=LIMIT_LABELS, date=date)


@app.route("/planos")
def listar_planos():
    conn = get_db()
    rows = conn.execute("SELECT id, nome, idade, focos, dias, criado_em FROM planos"
                        " ORDER BY id DESC").fetchall()
    conn.close()
    itens = []
    for r in rows:
        itens.append({
            "id": r["id"], "nome": r["nome"], "idade": r["idade"], "dias": r["dias"],
            "focos": ", ".join(FOCO_LABELS.get(f, f)
                               for f in (r["focos"] or "").split(",") if f),
            "criado_em": r["criado_em"],
        })
    return render_template("planos.html", itens=itens)


@app.route("/plano/<int:plano_id>/editar", methods=["GET", "POST"])
def editar_plano(plano_id):
    plano = _carregar_plano(plano_id)
    if request.method == "POST":
        dados, erros = ler_formulario(request.form)
        if erros:
            for e in erros:
                flash(e, "erro")
            return render_template("criar.html", dados=dados, focos=FOCOS,
                                   limitacoes=LIMITACOES, niveis=NIVEIS,
                                   atividades=ATIVIDADES, horarios=HORARIOS,
                                   edicao_id=plano_id)
        plano_json = gerar_plano(dados, anterior=plano["dados"])
        conn = get_db()
        conn.execute(
            "UPDATE planos SET nome=?, sexo=?, data_nascimento=?, idade=?, email=?,"
            " telefone=?, peso=?, altura=?, imc=?, atividade=?, nivel_treino=?, dias=?,"
            " horario=?, local=?, limitacoes=?, focos=?, observacoes=?, dados_json=?"
            " WHERE id=?",
            (dados["nome"], dados["sexo"], dados["data_nascimento"], dados["idade"],
             dados["email"], dados["telefone"], dados["peso"], dados["altura"],
             dados["imc"], dados["atividade"], dados["nivel_treino"], dados["dias"],
             dados["horario"], dados["local"], ",".join(dados["limitacoes"]),
             ",".join(dados["focos"]), dados["observacoes"],
             json.dumps(plano_json, ensure_ascii=False), plano_id),
        )
        conn.commit()
        conn.close()
        flash("Plano atualizado! Somente o que mudou foi substituído.", "ok")
        return redirect(url_for("ver_plano", plano_id=plano_id))
    # GET: preenche o formulario com os dados atuais
    d = plano
    dados = {
        "nome": d["nome"], "email": d["email"], "telefone": d["telefone"],
        "sexo": d["sexo"], "data_nascimento": d["data_nascimento"], "peso": d["peso"],
        "altura": d["altura"], "atividade": d["atividade"],
        "nivel_treino": d["nivel_treino"], "dias": d["dias"], "horario": d["horario"],
        "local": d["local"], "limitacoes": plano["limitacoes_lista"],
        "focos": plano["focos_lista"], "observacoes": d["observacoes"],
        "aceite": "sim",
    }
    return render_template("criar.html", dados=dados, focos=FOCOS,
                           limitacoes=LIMITACOES, niveis=NIVEIS,
                           atividades=ATIVIDADES, horarios=HORARIOS,
                           edicao_id=plano_id)


@app.route("/sobre")
def sobre():
    return render_template("sobre.html")


@app.route("/contato")
def contato():
    return render_template("contato.html")


# ------------------------------------------------------------------
# Admin simples (CRUD)
# ------------------------------------------------------------------
def admin_requerido():
    return session.get("admin") is True


@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if (request.form.get("usuario") == ADMIN_USER and
                request.form.get("senha") == ADMIN_PASSWORD):
            session["admin"] = True
            return redirect(url_for("admin_painel"))
        flash("Usuário ou senha inválidos.", "erro")
    return render_template("admin_login.html")


@app.route("/admin/sair")
def admin_sair():
    session.pop("admin", None)
    return redirect(url_for("index"))


@app.route("/admin/painel")
def admin_painel():
    if not admin_requerido():
        return redirect(url_for("admin_login"))
    conn = get_db()
    n_ex = conn.execute("SELECT COUNT(*) c FROM exercicios").fetchone()["c"]
    n_pl = conn.execute("SELECT COUNT(*) c FROM planos").fetchone()["c"]
    planos = conn.execute("SELECT id, nome, criado_em FROM planos ORDER BY id DESC"
                          " LIMIT 20").fetchall()
    conn.close()
    return render_template("admin_painel.html", n_ex=n_ex, n_pl=n_pl, planos=planos)


@app.route("/admin/exercicios")
def admin_exercicios():
    if not admin_requerido():
        return redirect(url_for("admin_login"))
    busca = request.args.get("q", "")
    conn = get_db()
    if busca:
        rows = conn.execute("SELECT * FROM exercicios WHERE nome LIKE ? OR grupo LIKE ?"
                            " ORDER BY grupo, nome", (f"%{busca}%", f"%{busca}%")).fetchall()
    else:
        rows = conn.execute("SELECT * FROM exercicios ORDER BY grupo, nome").fetchall()
    conn.close()
    return render_template("admin_exercicios.html", itens=rows, busca=busca,
                           LIMIT_LABELS=LIMITATION_LABELS)


@app.route("/admin/exercicios/salvar", methods=["POST"])
def admin_exercicio_salvar():
    if not admin_requerido():
        return redirect(url_for("admin_login"))
    f = request.form
    nome = f.get("nome", "").strip()
    grupo = f.get("grupo", "").strip()
    equip = f.get("equipamento", "").strip()
    nivel = f.get("nivel", "iniciante")
    contra = ",".join(x.strip() for x in f.getlist("contraindicado_para") if x.strip())
    if not nome or not grupo:
        flash("Nome e grupo são obrigatórios.", "erro")
        return redirect(url_for("admin_exercicios"))
    conn = get_db()
    ex_id = f.get("id", "")
    try:
        if ex_id:
            conn.execute("UPDATE exercicios SET nome=?, grupo=?, equipamento=?, nivel=?,"
                         " contraindicado_para=? WHERE id=?",
                         (nome, grupo, equip, nivel, contra, int(ex_id)))
        else:
            conn.execute("INSERT INTO exercicios (nome, grupo, equipamento, nivel,"
                         " contraindicado_para) VALUES (?,?,?,?,?)",
                         (nome, grupo, equip, nivel, contra))
        conn.commit()
        flash("Exercício salvo.", "ok")
    except Exception:
        flash("Já existe um exercício com esse nome.", "erro")
    finally:
        conn.close()
    return redirect(url_for("admin_exercicios"))


@app.route("/admin/exercicios/<int:ex_id>/excluir", methods=["POST"])
def admin_exercicio_excluir(ex_id):
    if not admin_requerido():
        return redirect(url_for("admin_login"))
    conn = get_db()
    conn.execute("DELETE FROM exercicios WHERE id=?", (ex_id,))
    conn.commit()
    conn.close()
    flash("Exercício excluído.", "ok")
    return redirect(url_for("admin_exercicios"))


@app.route("/admin/exercicios/<int:ex_id>/editar")
def admin_exercicio_editar(ex_id):
    if not admin_requerido():
        return redirect(url_for("admin_login"))
    conn = get_db()
    row = conn.execute("SELECT * FROM exercicios WHERE id=?", (ex_id,)).fetchone()
    conn.close()
    if not row:
        abort(404)
    return render_template("admin_exercicio_form.html", ex=row,
                           LIMIT_LABELS=LIMITATION_LABELS)


@app.route("/admin/planos/<int:plano_id>/excluir", methods=["POST"])
def admin_plano_excluir(plano_id):
    if not admin_requerido():
        return redirect(url_for("admin_login"))
    conn = get_db()
    conn.execute("DELETE FROM planos WHERE id=?", (plano_id,))
    conn.commit()
    conn.close()
    flash("Plano excluído.", "ok")
    return redirect(url_for("admin_painel"))


@app.template_filter("idade_label")
def idade_label(valor):
    return f"{valor} anos" if valor else "—"


init_db()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
