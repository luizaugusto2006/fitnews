# -*- coding: utf-8 -*-
"""FitNews - site de academia: gerador de treino, alimentacao e suplementos."""
import csv
import io
import json
import os
import secrets
import string
import sqlite3
from datetime import date

from flask import (Flask, Response, abort, flash, jsonify, redirect,
                   render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from data_content import LIMITATION_LABELS
from database import get_db, init_db
from gerador import (ATIVIDADE_LABELS, FOCOS, FOCO_LABELS, LIMITACOES,
                     LIMIT_LABELS, banco_exercicios, gerar_plano)

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
        "personal_codigo": (form.get("personal_codigo", "") or "").strip().upper(),
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
    if form.get("aceite_privacidade") != "sim":
        erros.append("É preciso aceitar a Política de Privacidade para gerar o plano.")
    return dados, erros


# ------------------------------------------------------------------
# Paginas publicas
# ------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


def _buscar_personal_por_codigo(codigo):
    if not codigo:
        return None
    conn = get_db()
    row = conn.execute("SELECT id FROM personais WHERE codigo=?",
                       (codigo.upper(),)).fetchone()
    conn.close()
    return row["id"] if row else None


@app.route("/criar", methods=["GET", "POST"])
def criar():
    if request.method == "POST":
        dados, erros = ler_formulario(request.form)
        # vinculo com personal: codigo informado OU personal logado que abriu o form
        personal_id = None
        if dados.get("personal_codigo"):
            personal_id = _buscar_personal_por_codigo(dados["personal_codigo"])
            if personal_id is None:
                erros.append("Código do personal não encontrado. Confira o código ou deixe em branco.")
        if not erros and session.get("personal_novo"):
            personal_id = session["personal_novo"]
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
            " limitacoes, focos, observacoes, personal_id, dados_json)"
            " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (dados["nome"], dados["sexo"], dados["data_nascimento"], dados["idade"],
             dados["email"], dados["telefone"], dados["peso"], dados["altura"],
             dados["imc"], dados["atividade"], dados["nivel_treino"], dados["dias"],
             dados["horario"], dados["local"], ",".join(dados["limitacoes"]),
             ",".join(dados["focos"]), dados["observacoes"], personal_id,
             json.dumps(plano_json, ensure_ascii=False)),
        )
        pid = cur.lastrowid
        conn.commit()
        conn.close()
        session.pop("personal_novo", None)
        return redirect(url_for("ver_plano", plano_id=pid))
    if session.get("personal_novo"):
        flash("Novo plano: ele será vinculado automaticamente à sua conta de personal.", "ok")
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
    personal_nome, sou_dono = None, False
    if plano.get("personal_id"):
        conn = get_db()
        row = conn.execute("SELECT nome FROM personais WHERE id=?",
                           (plano["personal_id"],)).fetchone()
        conn.close()
        personal_nome = row["nome"] if row else None
        sou_dono = session.get("personal_id") == plano["personal_id"]
    return render_template("plano.html", plano=plano, FOCO_LABELS=FOCO_LABELS,
                           LIMIT_LABELS=LIMIT_LABELS, date=date,
                           personal_nome=personal_nome, sou_dono=sou_dono,
                           plano_url=url_for("ver_plano", plano_id=plano_id,
                                             _external=True))


@app.route("/plano/<int:plano_id>/resumo")
def plano_resumo(plano_id):
    plano = _carregar_plano(plano_id)
    return render_template("resumo.html", plano=plano, FOCO_LABELS=FOCO_LABELS,
                           LIMIT_LABELS=LIMIT_LABELS)


@app.route("/plano/<int:plano_id>/alternativas")
def plano_alternativas(plano_id):
    """Exercicios permitidos do mesmo grupo (ja filtrados pelas limitacoes)."""
    plano = _carregar_plano(plano_id)
    grupo = request.args.get("grupo", "")
    limitacoes = [l for l in plano["limitacoes_lista"] if l != "nenhuma"]
    permitidos, _ = banco_exercicios(limitacoes, plano["nivel_treino"], plano["local"])
    if not any(e["grupo"] == grupo for e in permitidos):
        permitidos, _ = banco_exercicios(limitacoes, None, plano["local"])
    usados = set()
    for dia in plano["dados"].get("dias", []):
        for e in dia.get("exercicios", []):
            usados.add(e["nome"])
    alts = [{"nome": e["nome"], "equipamento": e["equipamento"].replace("_", " "),
             "nivel": e["nivel"]}
            for e in permitidos if e["grupo"] == grupo and e["nome"] not in usados]
    return jsonify({"alternativas": alts[:12], "grupo": grupo})


def _salvar_dados(plano_id, dados):
    conn = get_db()
    conn.execute("UPDATE planos SET dados_json=? WHERE id=?",
                 (json.dumps(dados, ensure_ascii=False), plano_id))
    conn.commit()
    conn.close()


@app.route("/plano/<int:plano_id>/trocar", methods=["POST"])
def plano_trocar(plano_id):
    plano = _carregar_plano(plano_id)
    dados = plano["dados"]
    atual, novo = request.form.get("atual", ""), request.form.get("novo", "")
    alvo = None
    for dia in dados.get("dias", []):
        for e in dia.get("exercicios", []):
            if e["nome"] == atual:
                alvo = e
    if not alvo:
        flash("Exercício original não encontrado no plano.", "erro")
        return redirect(url_for("ver_plano", plano_id=plano_id))
    # valida o novo exercicio: existe, mesmo grupo e permitido para as limitacoes
    limitacoes = [l for l in plano["limitacoes_lista"] if l != "nenhuma"]
    permitidos, _ = banco_exercicios(limitacoes, plano["nivel_treino"], plano["local"])
    if not any(e["nome"] == novo and e["grupo"] == alvo["grupo"] for e in permitidos):
        permitidos, _ = banco_exercicios(limitacoes, None, plano["local"])
    escolhido = next((e for e in permitidos
                      if e["nome"] == novo and e["grupo"] == alvo["grupo"]), None)
    if not escolhido:
        flash("Esse exercício não está disponível para as suas limitações.", "erro")
        return redirect(url_for("ver_plano", plano_id=plano_id))
    usados = {e["nome"] for dia in dados.get("dias", [])
              for e in dia.get("exercicios", [])}
    if novo in usados and novo != atual:
        flash("Esse exercício já está no seu plano.", "erro")
        return redirect(url_for("ver_plano", plano_id=plano_id))
    alvo["nome"] = escolhido["nome"]
    alvo["equipamento"] = escolhido["equipamento"]
    alvo["nivel"] = escolhido["nivel"]
    alvo.pop("carga", None)
    _salvar_dados(plano_id, dados)
    flash(f"Exercício trocado por: {novo}.", "ok")
    return redirect(url_for("ver_plano", plano_id=plano_id))


@app.route("/plano/<int:plano_id>/cargas", methods=["POST"])
def plano_cargas(plano_id):
    plano = _carregar_plano(plano_id)
    dados = plano["dados"]
    payload = request.get_json(silent=True) or {}
    itens = payload.get("itens", [])
    nomes = {e["nome"] for dia in dados.get("dias", [])
             for e in dia.get("exercicios", [])}
    alterados = 0
    for item in itens:
        nome = str(item.get("nome", ""))[:120]
        carga = str(item.get("carga", ""))[:40]
        if nome not in nomes:
            continue
        for dia in dados.get("dias", []):
            for e in dia.get("exercicios", []):
                if e["nome"] == nome:
                    if carga:
                        e["carga"] = carga
                    else:
                        e.pop("carga", None)
                    alterados += 1
    _salvar_dados(plano_id, dados)
    return jsonify({"ok": True, "alterados": alterados})


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
        "aceite": "sim", "aceite_privacidade": "sim",
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


@app.route("/privacidade")
def privacidade():
    return render_template("privacidade.html")


# ------------------------------------------------------------------
# Personal trainer
# ------------------------------------------------------------------
def personal_logado():
    pid = session.get("personal_id")
    if not pid:
        return None
    conn = get_db()
    row = conn.execute("SELECT * FROM personais WHERE id=?", (pid,)).fetchone()
    conn.close()
    return dict(row) if row else None


def _gerar_codigo():
    alphabet = string.ascii_uppercase + string.digits
    while True:
        codigo = "FIT-" + "".join(secrets.choice(alphabet) for _ in range(6))
        conn = get_db()
        existe = conn.execute("SELECT 1 FROM personais WHERE codigo=?", (codigo,)).fetchone()
        conn.close()
        if not existe:
            return codigo


@app.route("/personal", methods=["GET", "POST"])
def personal():
    if personal_logado():
        return redirect(url_for("personal_painel"))
    if request.method == "POST":
        f = request.form
        acao = f.get("acao", "entrar")
        if acao == "criar":
            nome = f.get("nome", "").strip()
            email = f.get("email", "").strip().lower()
            senha = f.get("senha", "")
            if len(nome) < 2 or "@" not in email or len(senha) < 6:
                flash("Preencha nome, e-mail válido e senha com pelo menos 6 caracteres.", "erro")
                return render_template("personal_login.html", aba="criar", nome=nome, email=email)
            conn = get_db()
            try:
                cur = conn.execute(
                    "INSERT INTO personais (nome, email, senha_hash, codigo)"
                    " VALUES (?,?,?,?)",
                    (nome, email, generate_password_hash(senha), _gerar_codigo()),
                )
                conn.commit()
                session["personal_id"] = cur.lastrowid
                flash(f"Conta criada! Seu código de vínculo é {conn.execute('SELECT codigo FROM personais WHERE id=?', (cur.lastrowid,)).fetchone()['codigo']}. Compartilhe com seus alunos.", "ok")
            except sqlite3.IntegrityError:
                flash("Já existe uma conta com este e-mail.", "erro")
            except Exception:
                flash("Erro ao criar conta. Tente novamente.", "erro")
            finally:
                conn.close()
            return redirect(url_for("personal_painel"))
        # entrar
        email = f.get("email", "").strip().lower()
        senha = f.get("senha", "")
        conn = get_db()
        row = conn.execute("SELECT * FROM personais WHERE email=?", (email,)).fetchone()
        conn.close()
        if row and check_password_hash(row["senha_hash"], senha):
            session["personal_id"] = row["id"]
            flash(f"Bem-vindo(a), {row['nome']}!", "ok")
            return redirect(url_for("personal_painel"))
        flash("E-mail ou senha inválidos.", "erro")
        return render_template("personal_login.html", aba="entrar", email=email)
    return render_template("personal_login.html", aba=request.args.get("aba", "entrar"))


@app.route("/personal/sair")
def personal_sair():
    session.pop("personal_id", None)
    session.pop("personal_novo", None)
    flash("Sessão encerrada.", "ok")
    return redirect(url_for("index"))


@app.route("/personal/painel")
def personal_painel():
    eu = personal_logado()
    if not eu:
        return redirect(url_for("personal"))
    q = (request.args.get("q", "") or "").strip()
    foco = request.args.get("foco", "") or ""
    lim = request.args.get("lim", "") or ""
    conn = get_db()
    sql = ("SELECT id, nome, idade, focos, limitacoes, criado_em FROM planos"
           " WHERE personal_id=?")
    params = [eu["id"]]
    if q:
        sql += " AND nome LIKE ?"
        params.append(f"%{q}%")
    if foco:
        sql += " AND focos LIKE ?"
        params.append(f"%{foco}%")
    if lim:
        sql += " AND limitacoes LIKE ?"
        params.append(f"%{lim}%")
    sql += " ORDER BY id DESC"
    meus = [dict(r) for r in conn.execute(sql, params).fetchall()]

    sql2 = "SELECT id, nome, focos, criado_em FROM planos WHERE personal_id IS NULL"
    params2 = []
    if q:
        sql2 += " AND nome LIKE ?"
        params2.append(f"%{q}%")
    if foco:
        sql2 += " AND focos LIKE ?"
        params2.append(f"%{foco}%")
    if lim:
        sql2 += " AND limitacoes LIKE ?"
        params2.append(f"%{lim}%")
    sql2 += " ORDER BY id DESC LIMIT 50"
    sem_vinculo = [dict(r) for r in conn.execute(sql2, params2).fetchall()]

    n_clientes = conn.execute(
        "SELECT COUNT(DISTINCT nome) c FROM planos WHERE personal_id=?",
        (eu["id"],)).fetchone()["c"]
    n_planos = len(meus)
    conn.close()
    return render_template("personal_painel.html", eu=eu, meus=meus,
                           sem_vinculo=sem_vinculo, q=q, foco=foco, lim=lim,
                           n_clientes=n_clientes, n_planos=n_planos,
                           FOCO_LABELS=FOCO_LABELS, LIMIT_LABELS=LIMIT_LABELS,
                           FOCOS=FOCOS, LIMITACOES=LIMITACOES)


@app.route("/personal/novo")
def personal_novo():
    if not personal_logado():
        return redirect(url_for("personal"))
    session["personal_novo"] = session["personal_id"]
    return redirect(url_for("criar"))


@app.route("/personal/plano/<int:plano_id>/vincular", methods=["POST"])
def personal_vincular(plano_id):
    eu = personal_logado()
    if not eu:
        return redirect(url_for("personal"))
    conn = get_db()
    conn.execute("UPDATE planos SET personal_id=? WHERE id=? AND personal_id IS NULL",
                 (eu["id"], plano_id))
    conn.commit()
    conn.close()
    flash("Plano vinculado à sua conta.", "ok")
    return redirect(url_for("personal_painel"))


@app.route("/personal/plano/<int:plano_id>/desvincular", methods=["POST"])
def personal_desvincular(plano_id):
    eu = personal_logado()
    if not eu:
        return redirect(url_for("personal"))
    conn = get_db()
    conn.execute("UPDATE planos SET personal_id=NULL WHERE id=? AND personal_id=?",
                 (plano_id, eu["id"]))
    conn.commit()
    conn.close()
    flash("Plano desvinculado.", "ok")
    return redirect(url_for("personal_painel"))


@app.route("/personal/plano/<int:plano_id>/anotacoes", methods=["POST"])
def personal_anotacoes(plano_id):
    eu = personal_logado()
    if not eu:
        return redirect(url_for("personal"))
    texto = request.form.get("anotacoes", "").strip()
    conn = get_db()
    cur = conn.execute("UPDATE planos SET anotacoes=? WHERE id=? AND personal_id=?",
                       (texto, plano_id, eu["id"]))
    conn.commit()
    ok = cur.rowcount > 0
    conn.close()
    flash("Anotações salvas." if ok else "Você não é o personal deste plano.", "ok" if ok else "erro")
    return redirect(url_for("ver_plano", plano_id=plano_id))


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


def _csv_response(nome_arquivo, cabecalho, linhas):
    buf = io.StringIO()
    escritor = csv.writer(buf)
    escritor.writerow(cabecalho)
    escritor.writerows(linhas)
    dados = "\ufeff" + buf.getvalue()  # BOM para o Excel abrir em UTF-8
    return Response(dados, mimetype="text/csv; charset=utf-8", headers={
        "Content-Disposition": f"attachment; filename={nome_arquivo}"})


@app.route("/admin/exportar/planos")
def admin_exportar_planos():
    if not admin_requerido():
        return redirect(url_for("admin_login"))
    conn = get_db()
    rows = conn.execute(
        "SELECT id, nome, sexo, idade, email, telefone, peso, altura, imc,"
        " atividade, nivel_treino, dias, local, limitacoes, focos, criado_em"
        " FROM planos ORDER BY id").fetchall()
    conn.close()
    linhas = [[r["id"], r["nome"], r["sexo"], r["idade"], r["email"], r["telefone"],
               r["peso"], r["altura"], r["imc"], r["atividade"], r["nivel_treino"],
               r["dias"], r["local"], r["limitacoes"], r["focos"], r["criado_em"]]
              for r in rows]
    return _csv_response("fitnews_planos.csv",
                         ["id", "nome", "sexo", "idade", "email", "telefone", "peso",
                          "altura", "imc", "atividade", "nivel", "dias", "local",
                          "limitacoes", "focos", "criado_em"], linhas)


@app.route("/admin/exportar/exercicios")
def admin_exportar_exercicios():
    if not admin_requerido():
        return redirect(url_for("admin_login"))
    conn = get_db()
    rows = conn.execute(
        "SELECT id, nome, grupo, equipamento, nivel, contraindicado_para"
        " FROM exercicios ORDER BY grupo, nome").fetchall()
    conn.close()
    linhas = [[r["id"], r["nome"], r["grupo"], r["equipamento"], r["nivel"],
               r["contraindicado_para"]] for r in rows]
    return _csv_response("fitnews_exercicios.csv",
                         ["id", "nome", "grupo", "equipamento", "nivel",
                          "contraindicado_para"], linhas)


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
