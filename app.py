# -*- coding: utf-8 -*-
"""FitNews - site de academia: gerador de treino, alimentacao e suplementos."""
import csv
import io
import json
import os
import secrets
import smtplib
import string
import sqlite3
import time
from datetime import date, datetime
from email.message import EmailMessage

from flask import (Flask, Response, abort, flash, jsonify, redirect,
                   render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from data_content import LIMITATION_LABELS
from database import get_db, init_db
from gerador import (ATIVIDADE_LABELS, EQUIP_LABELS, FOCOS, FOCO_LABELS,
                     GRUPO_LABELS, LIMITACOES, LIMIT_LABELS, NIVEL_LABELS,
                     banco_exercicios, gerar_plano)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "fitnews-dev-key-troque-em-producao")

ADMIN_USER = os.environ.get("ADMIN_USER", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "19160731")

SITE_URL = os.environ.get("SITE_URL", "https://fitnews.pythonanywhere.com").rstrip("/")

NIVEIS = [("iniciante", "Iniciante (nunca treinei ou até 6 meses)"),
          ("intermediario", "Intermediário (6 meses a 2 anos)"),
          ("avancado", "Avançado (mais de 2 anos)")]
ATIVIDADES = list(ATIVIDADE_LABELS.items())
HORARIOS = [("manha", "Manhã"), ("tarde", "Tarde"), ("noite", "Noite"),
            ("variado", "Variado / conforme a agenda")]


def _parse_data(valor):
    """Aceita AAAA-MM-DD (ISO) ou DD/MM/AAAA digitado pelo usuario."""
    valor = (valor or "").strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y"):
        try:
            return datetime.strptime(valor, fmt).date()
        except ValueError:
            continue
    return None


def calcular_idade(nasc):
    d = _parse_data(nasc)
    if not d:
        return None
    hoje = date.today()
    idade = hoje.year - d.year - ((hoje.month, hoje.day) < (d.month, d.day))
    return idade if 10 <= idade <= 100 else None


@app.template_global()
def data_brasil(valor):
    """AAAA-MM-DD -> DD/MM/AAAA (texto livre passa adiante)."""
    try:
        return date.fromisoformat((valor or "").strip()[:10]).strftime("%d/%m/%Y")
    except ValueError:
        return valor or ""


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
    nasc_bruto = form.get("data_nascimento", "").strip()
    nasc_data = _parse_data(nasc_bruto)
    nasc = nasc_data.isoformat() if nasc_data else nasc_bruto
    idade = calcular_idade(nasc_bruto)
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
# Contas de usuario (dono dos planos)
# ------------------------------------------------------------------
def usuario_logado():
    uid = session.get("usuario_id")
    if not uid:
        return None
    conn = get_db()
    row = conn.execute("SELECT * FROM usuarios WHERE id=?", (uid,)).fetchone()
    conn.close()
    if not row:
        session.pop("usuario_id", None)
        return None
    return dict(row)


def _gerar_token_plano():
    while True:
        token = secrets.token_urlsafe(9)
        conn = get_db()
        existe = conn.execute("SELECT 1 FROM planos WHERE token=?",
                              (token,)).fetchone()
        conn.close()
        if not existe:
            return token


def _gerar_codigo_recuperacao():
    # sem I, L, O, 0, 1 para nao gerar duvida de leitura (1 x I, 0 x O)
    alphabet = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"
    while True:
        codigo = "REC-" + "".join(secrets.choice(alphabet) for _ in range(6))
        conn = get_db()
        existe = conn.execute("SELECT 1 FROM usuarios WHERE codigo_recup=?",
                              (codigo,)).fetchone()
        conn.close()
        if not existe:
            return codigo


def _config_mail():
    """Credenciais via variaveis de ambiente ou arquivo local mail_secreto.py."""
    user = os.environ.get("MAIL_USER", "")
    senha = os.environ.get("MAIL_PASSWORD", "")
    if not user or not senha:
        try:
            import mail_secreto
            user = user or getattr(mail_secreto, "MAIL_USER", "")
            senha = senha or getattr(mail_secreto, "MAIL_PASSWORD", "")
        except Exception:
            pass
    return user, senha


def _enviar_email(para, assunto, corpo):
    """Envia pelo Gmail (unico SMTP liberado no PythonAnywhere free)."""
    user, senha = _config_mail()
    if not user or not senha:
        raise RuntimeError("MAIL_USER/MAIL_PASSWORD nao configurados")
    msg = EmailMessage()
    msg["From"] = os.environ.get("MAIL_FROM", user)
    msg["To"] = para
    msg["Subject"] = assunto
    msg.set_content(corpo)
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as servidor:
        servidor.starttls()
        servidor.login(user, senha)
        servidor.send_message(msg)


def _anexar_plano(token):
    """Liga um plano sem dono ao usuario da sessao."""
    uid = session.get("usuario_id")
    if not uid or not token:
        return False
    conn = get_db()
    cur = conn.execute(
        "UPDATE planos SET usuario_id=? WHERE token=? AND usuario_id IS NULL",
        (uid, token))
    conn.commit()
    conn.close()
    return cur.rowcount > 0


def _prox_seguro(valor):
    """Evita redirect para fora do site (open redirect)."""
    if valor and valor.startswith("/") and not valor.startswith("//"):
        return valor
    return url_for("listar_planos")


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
        token = _gerar_token_plano()
        conn = get_db()
        cur = conn.execute(
            "INSERT INTO planos (nome, sexo, data_nascimento, idade, email, telefone,"
            " peso, altura, imc, atividade, nivel_treino, dias, horario, local,"
            " limitacoes, focos, observacoes, personal_id, usuario_id, token, dados_json)"
            " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (dados["nome"], dados["sexo"], dados["data_nascimento"], dados["idade"],
             dados["email"], dados["telefone"], dados["peso"], dados["altura"],
             dados["imc"], dados["atividade"], dados["nivel_treino"], dados["dias"],
             dados["horario"], dados["local"], ",".join(dados["limitacoes"]),
             ",".join(dados["focos"]), dados["observacoes"], personal_id,
             session.get("usuario_id"), token,
             json.dumps(plano_json, ensure_ascii=False)),
        )
        conn.commit()
        conn.close()
        session.pop("personal_novo", None)
        return redirect(url_for("ver_plano", plano_token=token))
    if session.get("personal_novo"):
        flash("Novo plano: ele será vinculado automaticamente à sua conta de personal.", "ok")
    eu = usuario_logado()
    return render_template("criar.html", dados={"email": eu["email"]} if eu else {},
                           focos=FOCOS, limitacoes=LIMITACOES,
                           niveis=NIVEIS, atividades=ATIVIDADES, horarios=HORARIOS)


def _carregar_plano(plano_token):
    conn = get_db()
    row = conn.execute("SELECT * FROM planos WHERE token=?", (plano_token,)).fetchone()
    conn.close()
    if not row:
        abort(404)
    plano = dict(row)
    plano["dados"] = json.loads(plano["dados_json"])
    plano["limitacoes_lista"] = [x for x in (plano["limitacoes"] or "").split(",") if x]
    plano["focos_lista"] = [x for x in (plano["focos"] or "").split(",") if x]
    plano["nivel_treino_label"] = NIVEL_LABELS.get(plano["nivel_treino"],
                                                   plano["nivel_treino"])
    return plano


@app.route("/plano/<plano_token>")
def ver_plano(plano_token):
    plano = _carregar_plano(plano_token)
    personal_nome, sou_dono = None, False
    if plano.get("personal_id"):
        conn = get_db()
        row = conn.execute("SELECT nome FROM personais WHERE id=?",
                           (plano["personal_id"],)).fetchone()
        conn.close()
        personal_nome = row["nome"] if row else None
        sou_dono = session.get("personal_id") == plano["personal_id"]
    eu_usuario = usuario_logado()
    dono_usuario = bool(eu_usuario and plano.get("usuario_id") == eu_usuario["id"])
    return render_template(
        "plano.html", plano=plano, FOCO_LABELS=FOCO_LABELS,
        LIMIT_LABELS=LIMIT_LABELS, date=date,
        personal_nome=personal_nome, sou_dono=sou_dono,
        eu_usuario=eu_usuario, dono_usuario=dono_usuario,
        sem_conta=plano.get("usuario_id") is None,
        plano_url=url_for("ver_plano", plano_token=plano_token, _external=True))


@app.route("/plano/<plano_token>/resumo")
def plano_resumo(plano_token):
    plano = _carregar_plano(plano_token)
    return render_template("resumo.html", plano=plano, FOCO_LABELS=FOCO_LABELS,
                           LIMIT_LABELS=LIMIT_LABELS)


@app.route("/plano/<plano_token>/salvar", methods=["POST"])
def plano_salvar(plano_token):
    """Salva um plano sem dono na conta do usuario da sessao."""
    plano = _carregar_plano(plano_token)
    if not session.get("usuario_id"):
        return redirect(url_for("entrar", plano=plano_token))
    if plano["usuario_id"] == session.get("usuario_id"):
        flash("Este plano já está na sua conta.", "ok")
    elif plano["usuario_id"]:
        flash("Este plano já pertence a outra conta.", "erro")
    elif _anexar_plano(plano_token):
        flash("Plano salvo na sua conta! Ele agora aparece em Meus planos.", "ok")
    return redirect(url_for("ver_plano", plano_token=plano_token))


@app.route("/plano/<plano_token>/alternativas")
def plano_alternativas(plano_token):
    """Exercicios permitidos do mesmo grupo (ja filtrados pelas limitacoes)."""
    plano = _carregar_plano(plano_token)
    grupo = request.args.get("grupo", "")
    limitacoes = [l for l in plano["limitacoes_lista"] if l != "nenhuma"]
    permitidos, _ = banco_exercicios(limitacoes, plano["nivel_treino"], plano["local"])
    if not any(e["grupo"] == grupo for e in permitidos):
        permitidos, _ = banco_exercicios(limitacoes, None, plano["local"])
    usados = set()
    for dia in plano["dados"].get("dias", []):
        for e in dia.get("exercicios", []):
            usados.add(e["nome"])
    alts = [{"nome": e["nome"],
             "equipamento": EQUIP_LABELS.get(e["equipamento"],
                                             e["equipamento"].replace("_", " ")),
             "nivel": NIVEL_LABELS.get(e["nivel"], e["nivel"])}
            for e in permitidos if e["grupo"] == grupo and e["nome"] not in usados]
    return jsonify({"alternativas": alts[:12], "grupo": grupo})


def _salvar_dados(plano_id, dados):
    conn = get_db()
    conn.execute("UPDATE planos SET dados_json=? WHERE id=?",
                 (json.dumps(dados, ensure_ascii=False), plano_id))
    conn.commit()
    conn.close()


@app.route("/plano/<plano_token>/trocar", methods=["POST"])
def plano_trocar(plano_token):
    plano = _carregar_plano(plano_token)
    dados = plano["dados"]
    atual, novo = request.form.get("atual", ""), request.form.get("novo", "")
    alvo = None
    for dia in dados.get("dias", []):
        for e in dia.get("exercicios", []):
            if e["nome"] == atual:
                alvo = e
    if not alvo:
        flash("Exercício original não encontrado no plano.", "erro")
        return redirect(url_for("ver_plano", plano_token=plano_token))
    # valida o novo exercicio: existe, mesmo grupo e permitido para as limitacoes
    limitacoes = [l for l in plano["limitacoes_lista"] if l != "nenhuma"]
    permitidos, _ = banco_exercicios(limitacoes, plano["nivel_treino"], plano["local"])
    if not any(e["nome"] == novo and e["grupo"] == alvo["grupo"] for e in permitidos):
        permitidos, _ = banco_exercicios(limitacoes, None, plano["local"])
    escolhido = next((e for e in permitidos
                      if e["nome"] == novo and e["grupo"] == alvo["grupo"]), None)
    if not escolhido:
        flash("Esse exercício não está disponível para as suas limitações.", "erro")
        return redirect(url_for("ver_plano", plano_token=plano_token))
    usados = {e["nome"] for dia in dados.get("dias", [])
              for e in dia.get("exercicios", [])}
    if novo in usados and novo != atual:
        flash("Esse exercício já está no seu plano.", "erro")
        return redirect(url_for("ver_plano", plano_token=plano_token))
    alvo["nome"] = escolhido["nome"]
    alvo["equipamento"] = escolhido["equipamento"]
    alvo["nivel"] = escolhido["nivel"]
    alvo.pop("carga", None)
    _salvar_dados(plano["id"], dados)
    flash(f"Exercício trocado por: {novo}.", "ok")
    return redirect(url_for("ver_plano", plano_token=plano_token))


@app.route("/plano/<plano_token>/cargas", methods=["POST"])
def plano_cargas(plano_token):
    plano = _carregar_plano(plano_token)
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
    _salvar_dados(plano["id"], dados)
    return jsonify({"ok": True, "alterados": alterados})


@app.route("/planos")
def listar_planos():
    uid = session.get("usuario_id")
    if not uid:
        return redirect(url_for("entrar", prox="/planos"))
    conn = get_db()
    rows = conn.execute("SELECT id, token, nome, idade, focos, dias, criado_em"
                        " FROM planos WHERE usuario_id=? ORDER BY id DESC",
                        (uid,)).fetchall()
    conn.close()
    itens = []
    for r in rows:
        itens.append({
            "id": r["id"], "token": r["token"], "nome": r["nome"],
            "idade": r["idade"], "dias": r["dias"],
            "focos": ", ".join(FOCO_LABELS.get(f, f)
                               for f in (r["focos"] or "").split(",") if f),
            "criado_em": r["criado_em"],
        })
    return render_template("planos.html", itens=itens)


@app.route("/plano/<plano_token>/editar", methods=["GET", "POST"])
def editar_plano(plano_token):
    plano = _carregar_plano(plano_token)
    if request.method == "POST":
        dados, erros = ler_formulario(request.form)
        if erros:
            for e in erros:
                flash(e, "erro")
            return render_template("criar.html", dados=dados, focos=FOCOS,
                                   limitacoes=LIMITACOES, niveis=NIVEIS,
                                   atividades=ATIVIDADES, horarios=HORARIOS,
                                   edicao_token=plano_token)
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
             json.dumps(plano_json, ensure_ascii=False), plano["id"]),
        )
        conn.commit()
        conn.close()
        flash("Plano atualizado! Somente o que mudou foi substituído.", "ok")
        return redirect(url_for("ver_plano", plano_token=plano_token))
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
                           edicao_token=plano_token)


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
# Contas de usuario (entrar / criar / recuperar senha)
# ------------------------------------------------------------------
@app.route("/conta", methods=["GET", "POST"])
def conta():
    prox = request.args.get("prox", "")
    plano = request.args.get("plano", "")
    if request.method == "POST":
        plano = request.form.get("plano", "")
        prox = request.form.get("prox", "")
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        erros = []
        if "@" not in email or len(email) < 5:
            erros.append("Informe um e-mail válido.")
        if len(senha) < 6:
            erros.append("A senha precisa de pelo menos 6 caracteres.")
        if senha != request.form.get("senha2", ""):
            erros.append("As senhas não conferem.")
        if request.form.get("aceite") != "sim":
            erros.append("É preciso aceitar a Política de Privacidade.")
        if erros:
            for e in erros:
                flash(e, "erro")
            return render_template("conta.html", email=email, plano=plano, prox=prox)
        codigo = _gerar_codigo_recuperacao()
        conn = get_db()
        try:
            cur = conn.execute(
                "INSERT INTO usuarios (email, senha_hash, codigo_recup) VALUES (?,?,?)",
                (email, generate_password_hash(senha), codigo))
            conn.commit()
            session["usuario_id"] = cur.lastrowid
        except sqlite3.IntegrityError:
            conn.close()
            flash("Já existe uma conta com este e-mail.", "erro")
            return render_template("conta.html", email=email, plano=plano, prox=prox)
        except Exception:
            conn.close()
            flash("Erro ao criar conta. Tente novamente.", "erro")
            return render_template("conta.html", email=email, plano=plano, prox=prox)
        conn.close()
        _anexar_plano(plano)
        if plano:
            destino = url_for("ver_plano", plano_token=plano)
        else:
            destino = _prox_seguro(prox)
        return render_template("codigo_recuperacao.html", codigo=codigo,
                               destino=destino)
    if session.get("usuario_id"):
        return redirect(_prox_seguro(prox))
    return render_template("conta.html", plano=plano, prox=prox, email="")


@app.route("/entrar", methods=["GET", "POST"])
def entrar():
    prox = request.args.get("prox", "")
    plano = request.args.get("plano", "")
    if request.method == "POST":
        plano = request.form.get("plano", "")
        prox = request.form.get("prox", "")
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        conn = get_db()
        row = conn.execute("SELECT * FROM usuarios WHERE email=?",
                           (email,)).fetchone()
        conn.close()
        if row and check_password_hash(row["senha_hash"], senha):
            session["usuario_id"] = row["id"]
            _anexar_plano(plano)
            flash("Bem-vindo(a) de volta!", "ok")
            return redirect(_prox_seguro(prox))
        flash("E-mail ou senha inválidos.", "erro")
        return render_template("entrar.html", email=email, plano=plano, prox=prox)
    return render_template("entrar.html", plano=plano, prox=prox, email="")


@app.route("/sair")
def sair():
    session.pop("usuario_id", None)
    flash("Sessão encerrada.", "ok")
    return redirect(url_for("index"))


@app.route("/recuperar", methods=["GET", "POST"])
def recuperar():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        # ---- opcao 1: link enviado por e-mail ----
        if request.form.get("acao") == "enviar_link":
            conn = get_db()
            row = conn.execute("SELECT id FROM usuarios WHERE email=?",
                               (email,)).fetchone()
            if row:
                token = secrets.token_urlsafe(24)
                conn.execute("UPDATE usuarios SET reset_token=?, reset_expira=?"
                             " WHERE id=?",
                             (token, str(time.time() + 1800), row["id"]))
                conn.commit()
                link = f"{SITE_URL}/redefinir/{token}"
                try:
                    _enviar_email(
                        email, "Redefinir sua senha - FitNews",
                        "Ola!\n\nRecebemos um pedido para redefinir a senha da sua "
                        "conta no FitNews.\n\nPara escolher uma nova senha, abra o "
                        "link abaixo (valido por 30 minutos):\n\n"
                        f"{link}\n\n"
                        "Se nao foi voce, basta ignorar este email.\n"
                        "Se o link nao abrir, copie e cole o endereco no navegador.\n")
                except Exception:
                    app.logger.exception("Falha ao enviar email de recuperacao")
                    conn.close()
                    flash("Não foi possível enviar o e-mail agora. Tente de novo em "
                          "instantes ou use o código de recuperação.", "erro")
                    return render_template("recuperar.html", email=email, codigo="")
                conn.close()
            flash("Se existir uma conta com este e-mail, enviamos um link para "
                  "redefinir a senha. Confira a caixa de entrada e o spam.", "ok")
            return render_template("recuperar.html", email=email, codigo="")
        # ---- opcao 2: codigo REC mostrado no cadastro ----
        bruto = request.form.get("codigo", "")
        # aceita com/sem "REC-", maiusculas/minusculas e espacos
        limpo = "".join(ch for ch in bruto.upper() if ch.isascii() and ch.isalnum())
        if len(limpo) == 6:
            codigo = "REC-" + limpo
        elif len(limpo) == 9 and limpo.startswith("REC"):
            codigo = "REC-" + limpo[3:]
        else:
            codigo = limpo
        nova = request.form.get("senha", "")
        if len(nova) < 6:
            flash("A nova senha precisa de pelo menos 6 caracteres.", "erro")
            return render_template("recuperar.html", email=email, codigo=bruto)
        conn = get_db()
        row = conn.execute("SELECT id FROM usuarios WHERE email=? AND codigo_recup=?",
                           (email, codigo)).fetchone()
        if row:
            conn.execute("UPDATE usuarios SET senha_hash=? WHERE id=?",
                         (generate_password_hash(nova), row["id"]))
            conn.commit()
            conn.close()
            flash("Senha alterada! Entre com a nova senha.", "ok")
            return redirect(url_for("entrar"))
        conn.close()
        flash("E-mail ou código de recuperação inválidos. Confira o código "
              "exatamente como apareceu no cadastro (REC-...).", "erro")
        return render_template("recuperar.html", email=email, codigo=bruto)
    return render_template("recuperar.html", email="", codigo="")


@app.route("/redefinir/<token>", methods=["GET", "POST"])
def redefinir_senha(token):
    conn = get_db()
    row = conn.execute("SELECT id, reset_expira FROM usuarios WHERE reset_token=?",
                       (token,)).fetchone()
    valido = False
    if row:
        try:
            valido = time.time() <= float(row["reset_expira"])
        except (TypeError, ValueError):
            valido = False
    if not valido:
        conn.close()
        flash("Link inválido ou expirado. Solicite um novo em Recuperar senha.", "erro")
        return redirect(url_for("recuperar"))
    if request.method == "POST":
        nova = request.form.get("senha", "")
        if len(nova) < 6 or nova != request.form.get("senha2", ""):
            flash("As senhas precisam ter pelo menos 6 caracteres e conferir.", "erro")
        else:
            conn.execute("UPDATE usuarios SET senha_hash=?, reset_token=NULL,"
                         " reset_expira=NULL WHERE id=?",
                         (generate_password_hash(nova), row["id"]))
            conn.commit()
            conn.close()
            flash("Senha alterada! Entre com a nova senha.", "ok")
            return redirect(url_for("entrar"))
        conn.close()
        return render_template("redefinir.html", token=token)
    conn.close()
    return render_template("redefinir.html", token=token)


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
    sql = ("SELECT id, token, nome, idade, focos, limitacoes, criado_em FROM planos"
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

    sql2 = ("SELECT id, token, nome, focos, criado_em FROM planos"
            " WHERE personal_id IS NULL AND usuario_id IS NULL")
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
    token = None
    if ok:
        token = conn.execute("SELECT token FROM planos WHERE id=?",
                             (plano_id,)).fetchone()["token"]
    conn.close()
    flash("Anotações salvas." if ok else "Você não é o personal deste plano.", "ok" if ok else "erro")
    if token:
        return redirect(url_for("ver_plano", plano_token=token))
    return redirect(url_for("personal_painel"))


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
    planos = conn.execute("SELECT id, token, nome, criado_em FROM planos"
                          " ORDER BY id DESC LIMIT 20").fetchall()
    usuarios = conn.execute("SELECT id, email, criado_em FROM usuarios"
                            " ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("admin_painel.html", n_ex=n_ex, n_pl=n_pl, planos=planos,
                           usuarios=usuarios)


@app.route("/admin/usuario/<int:uid>/senha", methods=["POST"])
def admin_usuario_senha(uid):
    if not admin_requerido():
        return redirect(url_for("admin_login"))
    nova = request.form.get("senha", "")
    if len(nova) < 6:
        flash("A nova senha precisa de pelo menos 6 caracteres.", "erro")
    else:
        conn = get_db()
        conn.execute("UPDATE usuarios SET senha_hash=? WHERE id=?",
                     (generate_password_hash(nova), uid))
        conn.commit()
        conn.close()
        flash("Senha do usuário redefinida.", "ok")
    return redirect(url_for("admin_painel"))


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
                           LIMIT_LABELS=LIMITATION_LABELS, GRUPO_LABELS=GRUPO_LABELS,
                           EQUIP_LABELS=EQUIP_LABELS, NIVEL_LABELS=NIVEL_LABELS)


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
                           LIMIT_LABELS=LIMITATION_LABELS, GRUPO_LABELS=GRUPO_LABELS,
                           EQUIP_LABELS=EQUIP_LABELS, NIVEL_LABELS=NIVEL_LABELS)


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
