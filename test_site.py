# -*- coding: utf-8 -*-
"""Smoke test do FitNews (executar: python test_site.py)"""
import re

import database
from app import app

c = app.test_client()

print("== Rotas publicas ==")
for r in ["/", "/criar", "/sobre", "/contato", "/admin"]:
    print(" ", r, c.get(r).status_code)
r = c.get("/planos")
print("  /planos (sem login) redireciona:", r.status_code == 302)
assert r.status_code == 302, "lista de planos vazou sem login!"

print("== Criar plano (hernia de disco + bico de papagaio) ==")
resp = c.post("/criar", data={
    "nome": "Teste Silva", "sexo": "masculino", "data_nascimento": "1990-05-10",
    "peso": "80", "altura": "175", "atividade": "moderado",
    "nivel_treino": "intermediario", "dias": "4", "horario": "manha",
    "local": "academia",
    "limitacoes": ["hernia_discal", "bico_papagaio"],
    "focos": ["pernas", "perda_peso", "core", "peito"], "aceite": "sim", "aceite_privacidade": "sim",
}, follow_redirects=True)
html = resp.get_data(as_text=True)
print("  status:", resp.status_code)

conn = database.get_db()
tok1 = conn.execute("SELECT token FROM planos WHERE nome='Teste Silva'"
                    " ORDER BY id LIMIT 1").fetchone()["token"]
conn.close()

m = re.search(r'id="aba-treino"(.*?)<!-- ============ AQUECIMENTO', html, re.S)
treino = m.group(1) if m else ""
m2 = re.search(r'class="evitados"(.*?)</details>', html, re.S)
evitados = m2.group(1) if m2 else ""

perigosos = ["Agachamento livre", "Levantamento terra", "Terra romeno", "Bom dia",
             "Remada curvada", "Abdominal tradicional", "Russian twist", "Burpee",
             "Mountain climber", "Hiperextensao", "Passada", "Agachamento sumo"]
print("  -- no painel de TREINO (deve ser ausente) --")
falhas = 0
for p in perigosos:
    dentro = p in treino
    print("   ", p, "NO TREINO!" if dentro else "ok")
    falhas += 1 if dentro else 0
print("  -- lista de BLOQUEADOS (deve conter) --")
for p in ["Agachamento livre", "Levantamento terra", "Bom dia", "Remada curvada",
          "Abdominal tradicional", "Russian twist", "Burpee"]:
    print("   ", p, "listado" if p in evitados else "NAO LISTADO")
nomes = re.findall(r"<strong>([^<]+)</strong>", treino)
print("  exercicios do treino:", nomes)
assert falhas == 0, "EXERCICIO PERIGOSO NO TREINO!"

print("  + aquecimento/alongamento/alimentacao/suplementos:",
      "Aquecimento geral" in html, "Alongamento pós-treino" in html,
      "Alimentação sugerida" in html, "Suplementos sugeridos" in html)

print("== Editar foco (muda para bracos) ==")
resp2 = c.post(f"/plano/{tok1}/editar", data={
    "nome": "Teste Silva", "sexo": "masculino", "data_nascimento": "1990-05-10",
    "peso": "80", "altura": "175", "atividade": "moderado",
    "nivel_treino": "intermediario", "dias": "3", "horario": "manha",
    "local": "academia", "limitacoes": "hernia_discal",
    "focos": "bracos,peito", "aceite": "sim", "aceite_privacidade": "sim",
}, follow_redirects=True)
html2 = resp2.get_data(as_text=True)
m = re.search(r'id="aba-treino"(.*?)<!-- ============ AQUECIMENTO', html2, re.S)
treino2 = m.group(1) if m else ""
nomes2 = re.findall(r"<strong>([^<]+)</strong>", treino2)
print("  status:", resp2.status_code, "| novos exercicios:", nomes2)
assert not any("Leg press" in n for n in nomes2), "foco antigo persistiu (pernas)"
assert any("Rosca" in n or "Supino" in n or "Triceps" in n for n in nomes2), "foco novo nao entrou"

print("== Validacoes ==")
r3 = c.post("/criar", data={"nome": "", "aceite": "nao"})
print("  form vazio volta com erro:", r3.status_code == 200 and "Informe seu nome" in r3.get_data(as_text=True))
r4 = c.get("/plano/9999")
print("  plano inexistente -> 404:", r4.status_code == 404)

print("== Admin ==")
r5 = c.post("/admin", data={"usuario": "admin", "senha": "errada"})
print("  senha errada:", "inválidos" in r5.get_data(as_text=True))
r6 = c.post("/admin", data={"usuario": "admin", "senha": "19160731"}, follow_redirects=True)
print("  login ok:", r6.status_code == 200 and "Painel administrativo" in r6.get_data(as_text=True))
r7 = c.get("/admin/exercicios")
print("  lista exercicios:", r7.status_code == 200)
r8 = c.post("/admin/exercicios/salvar", data={
    "nome": "Teste Exercicio", "grupo": "peito", "equipamento": "halteres",
    "nivel": "iniciante", "contraindicado_para": "ombro",
}, follow_redirects=True)
print("  criar exercicio:", "Teste Exercicio" in r8.get_data(as_text=True))
r9 = c.get("/admin/exercicios/1/editar")
print("  editar exercicio:", r9.status_code == 200)

print("== Personal trainer ==")
r = c.get("/personal")
print("  pagina login:", r.status_code == 200)
r = c.post("/personal", data={"acao": "criar", "nome": "Joao Personal",
                              "email": "joao@fit.com", "senha": "123456"},
           follow_redirects=True)
htmlp = r.get_data(as_text=True)
print("  cadastro -> painel:", "PAINEL DO PERSONAL" in htmlp)
m = re.search(r"(FIT-[A-Z0-9]{6})", htmlp)
codigo = m.group(1) if m else ""
print("  codigo gerado:", codigo or "AUSENTE")
assert codigo, "codigo de vinculo nao gerado"

# aluno cria plano informando o codigo
r = c.post("/criar", data={
    "nome": "Maria Aluna", "sexo": "feminino", "data_nascimento": "1995-03-03",
    "peso": "60", "altura": "165", "atividade": "leve", "nivel_treino": "iniciante",
    "dias": "3", "local": "casa", "focos": ["gluteos", "core"],
    "limitacoes": ["joelho"], "aceite": "sim",
    "aceite_privacidade": "sim", "personal_codigo": codigo,
}, follow_redirects=True)
print("  plano com codigo criado:", r.status_code == 200)

r = c.get("/personal/painel?q=Maria")
hp = r.get_data(as_text=True)
print("  busca por nome acha cliente:", "Maria Aluna" in hp)
r = c.get("/personal/painel?q=Zebedeu")
print("  busca sem resultado:", "Maria Aluna" not in r.get_data(as_text=True))

# codigo invalido bloqueia
r = c.post("/criar", data={
    "nome": "Teste", "sexo": "", "data_nascimento": "1990-01-01", "focos": ["peito"],
    "aceite": "sim", "aceite_privacidade": "sim", "personal_codigo": "FIT-XXXXXX",
}, follow_redirects=True)
print("  codigo invalido recusado:", "não encontrado" in r.get_data(as_text=True))

# anotacoes do personal
conn = database.get_db()
pid = conn.execute("SELECT id FROM planos WHERE nome='Maria Aluna'").fetchone()["id"]
conn.close()
r = c.post(f"/personal/plano/{pid}/anotacoes",
           data={"anotacoes": "Subir carga no supino. Cuidado com o joelho."},
           follow_redirects=True)
print("  anotacoes salvas:", "Subir carga no supino" in r.get_data(as_text=True))
print("  tag personal no plano:", "Personal: Joao Personal" in r.get_data(as_text=True))

# plano sem codigo -> vincular manualmente
r = c.post("/criar", data={
    "nome": "Bruno Solto", "sexo": "masculino", "data_nascimento": "1988-07-07",
    "focos": ["costas"], "aceite": "sim", "aceite_privacidade": "sim",
}, follow_redirects=True)
r = c.get("/personal/painel")
print("  plano solito listado:", "Bruno Solto" in r.get_data(as_text=True))
conn = database.get_db()
pid2 = conn.execute("SELECT id FROM planos WHERE nome='Bruno Solto'").fetchone()["id"]
conn.close()
r = c.post(f"/personal/plano/{pid2}/vincular", follow_redirects=True)
conn = database.get_db()
row2 = conn.execute("SELECT personal_id FROM planos WHERE id=?", (pid2,)).fetchone()
conn.close()
print("  vincular manual:", row2["personal_id"] is not None)

# novo plano pelo painel nasce vinculado
r = c.get("/personal/novo", follow_redirects=True)
print("  botao novo plano:", r.status_code == 200 and "vinculado automaticamente" in r.get_data(as_text=True))
r = c.post("/criar", data={
    "nome": "Carla Vinculada", "sexo": "feminino", "data_nascimento": "2001-01-01",
    "focos": ["ombros"], "aceite": "sim", "aceite_privacidade": "sim",
}, follow_redirects=True)
conn = database.get_db()
row = conn.execute("SELECT personal_id FROM planos WHERE nome='Carla Vinculada'").fetchone()
conn.close()
print("  novo plano ja vinculado:", row["personal_id"] is not None)

# logout / login
c.get("/personal/sair")
r = c.get("/personal/painel", follow_redirects=True)
print("  protegido apos logout:", "Acesse sua conta" in r.get_data(as_text=True))
r = c.post("/personal", data={"acao": "entrar", "email": "joao@fit.com", "senha": "123456"},
           follow_redirects=True)
print("  login ok:", "PAINEL DO PERSONAL" in r.get_data(as_text=True))

print("== Novas funcionalidades ==")
r = c.get("/privacidade")
print("  pagina privacidade:", r.status_code == 200 and "LGPD" in r.get_data(as_text=True))
r = c.post("/criar", data={"nome": "Sem Aceite", "data_nascimento": "1990-01-01",
                           "focos": ["peito"], "aceite": "sim"},
           follow_redirects=True)
print("  aceite privacidade obrigatorio:", "Política de Privacidade para gerar" in r.get_data(as_text=True))

r = c.get("/admin/exportar/planos")
print("  CSV planos:", r.status_code == 200 and "text/csv" in r.headers.get("Content-Type", ""))
r = c.get("/admin/exportar/exercicios")
print("  CSV exercicios:", r.status_code == 200 and "Supino" in r.get_data(as_text=True))

r = c.get(f"/plano/{tok1}/resumo")
print("  resumo 1 pagina:", r.status_code == 200 and "Resumo do treino" in r.get_data(as_text=True))

r = c.get(f"/plano/{tok1}/alternativas?grupo=peito")
alts = r.get_json()["alternativas"]
novo_ex = alts[0]["nome"] if alts else ""
print("  alternativas do mesmo grupo:", len(alts) > 0, "->", novo_ex)
r = c.post(f"/plano/{tok1}/trocar", data={"atual": "Supino reto com barra", "novo": novo_ex},
           follow_redirects=True)
hp = r.get_data(as_text=True)
print("  trocou exercicio:", novo_ex in hp and "<strong>Supino reto com barra</strong>" not in hp)

r = c.post(f"/plano/{tok1}/cargas", json={"itens": [{"nome": novo_ex, "carga": "40kg"}]})
print("  API cargas ok:", r.get_json().get("ok") is True)
r = c.get(f"/plano/{tok1}")
hp = r.get_data(as_text=True)
print("  carga visivel no plano:", 'value="40kg"' in hp)
print("  share/QR/timer no plano:", "btnWhats" in hp and "qrcode.min.js" in hp and "btn-timer" in hp)

r = c.get("/personal/painel?foco=gluteos")
hp = r.get_data(as_text=True)
print("  filtro por foco:", "Maria Aluna" in hp and "Bruno Solto" not in hp)
r = c.get("/personal/painel?lim=joelho")
hp = r.get_data(as_text=True)
print("  filtro por limitacao:", "Maria Aluna" in hp and "Bruno Solto" not in hp)
r = c.get("/personal/painel?q=Maria&foco=core")
print("  busca + filtro juntos:", "Maria Aluna" in r.get_data(as_text=True))

print("== Contas de usuario (Plano B) ==")
# /planos exige login
r = c.get("/planos")
print("  /planos sem login -> 302:", r.status_code == 302)
assert r.status_code == 302, "lista de planos vazou sem login!"

# cria um plano anonimo (sem dono)
c.post("/criar", data={
    "nome": "Conta Teste", "sexo": "feminino", "data_nascimento": "1992-05-05",
    "peso": "55", "altura": "160", "atividade": "moderado",
    "nivel_treino": "iniciante", "dias": "3", "local": "academia",
    "focos": ["core"], "aceite": "sim", "aceite_privacidade": "sim",
}, follow_redirects=True)
conn = database.get_db()
tok2 = conn.execute("SELECT token FROM planos WHERE nome='Conta Teste'"
                    " ORDER BY id DESC LIMIT 1").fetchone()["token"]
conn.close()

# plano sem conta pede para criar acesso
r = c.get(f"/plano/{tok2}")
hp = r.get_data(as_text=True)
print("  banner criar conta no plano:", "Plano sem conta" in hp and "Criar conta" in hp)
assert "Plano sem conta" in hp, "banner de conta ausente"

# cadastro liga o plano a conta + mostra codigo de recuperacao
r = c.post("/conta", data={"email": "dono@fitnews.com", "senha": "senhas12",
                           "senha2": "senhas12", "aceite": "sim", "plano": tok2})
hp = r.get_data(as_text=True)
m = re.search(r"(REC-[A-Z0-9]{6})", hp)
recup = m.group(1) if m else ""
print("  cadastro -> codigo de recuperacao:", recup or "AUSENTE")
assert recup, "codigo de recuperacao nao gerado"
conn = database.get_db()
dono = conn.execute("SELECT usuario_id FROM planos WHERE token=?",
                    (tok2,)).fetchone()
conn.close()
print("  plano ligado a conta:", dono["usuario_id"] is not None)
assert dono["usuario_id"] is not None, "plano nao anexado a conta"

# /planos mostra so os planos do dono
r = c.get("/planos")
hp = r.get_data(as_text=True)
print("  meus planos visiveis:", "Conta Teste" in hp)
print("  planos alheios fora:", "Bruno Solto" not in hp and "Maria Aluna" not in hp)
print("  nav logado mostra Sair:", "Sair" in hp)
assert "Conta Teste" in hp and "Bruno Solto" not in hp and "Maria Aluna" not in hp

# salva o plano antigo (sem dono) na conta
r = c.get(f"/plano/{tok1}")
print("  plano antigo oferece salvar:", "Salvar na minha conta" in r.get_data(as_text=True))
assert "Salvar na minha conta" in r.get_data(as_text=True)
r = c.post(f"/plano/{tok1}/salvar", follow_redirects=True)
conn = database.get_db()
d1 = conn.execute("SELECT usuario_id FROM planos WHERE token=?",
                  (tok1,)).fetchone()
conn.close()
print("  salvar na conta:", d1["usuario_id"] is not None)
assert d1["usuario_id"] is not None
r = c.get("/planos")
hp = r.get_data(as_text=True)
print("  dois planos na lista:", "Teste Silva" in hp and "Conta Teste" in hp)
assert "Teste Silva" in hp

# URL antiga por id sequencial nao abre mais
r = c.get("/plano/1")
print("  url antiga /plano/1 -> 404:", r.status_code == 404)
assert r.status_code == 404, "url antiga por id continuou funcionando!"

# logout devolve a protecao
c.get("/sair")
r = c.get("/planos")
print("  apos sair /planos -> 302:", r.status_code == 302)
assert r.status_code == 302

# recuperacao de senha com o codigo
r = c.post("/recuperar", data={"email": "dono@fitnews.com", "codigo": recup,
                               "senha": "novasenha"}, follow_redirects=True)
print("  recuperar -> senha alterada:", "Senha alterada" in r.get_data(as_text=True))
assert "Senha alterada" in r.get_data(as_text=True)
r = c.post("/entrar", data={"email": "dono@fitnews.com", "senha": "senhas12"},
           follow_redirects=True)
print("  senha antiga nao entra:", "inválidos" in r.get_data(as_text=True))
assert "inválidos" in r.get_data(as_text=True)
r = c.post("/entrar", data={"email": "dono@fitnews.com", "senha": "novasenha"},
           follow_redirects=True)
hp = r.get_data(as_text=True)
print("  senha nova entra:", r.status_code == 200 and "Conta Teste" in hp)
assert r.status_code == 200 and "Conta Teste" in hp
r = c.post("/recuperar", data={"email": "dono@fitnews.com", "codigo": "REC-ERRADO",
                               "senha": "outrasenha1"}, follow_redirects=True)
print("  codigo errado recusado:", "código de recuperação inválidos" in r.get_data(as_text=True))
assert "código de recuperação inválidos" in r.get_data(as_text=True)

# codigo digitado sem "REC-", em minusculas e com espacos tambem vale
codigo_simples = recup.replace("REC-", "").lower()
r = c.post("/recuperar", data={"email": "dono@fitnews.com",
                               "codigo": "  " + codigo_simples + " ",
                               "senha": "senhafina1"}, follow_redirects=True)
ok_flex = "Senha alterada" in r.get_data(as_text=True)
print("  codigo sem REC- / minusculo / com espacos:", ok_flex)
assert ok_flex, "codigo flexivel nao foi aceito"
r = c.post("/entrar", data={"email": "dono@fitnews.com", "senha": "senhafina1"},
           follow_redirects=True)
assert "Conta Teste" in r.get_data(as_text=True)
print("  login com a senha alterada pelo codigo flexivel: True")

# admin redefinir senha de quem perdeu o codigo de recuperacao
conn = database.get_db()
uid = conn.execute("SELECT id FROM usuarios WHERE email='dono@fitnews.com'"
                   ).fetchone()["id"]
conn.close()
r = c.post(f"/admin/usuario/{uid}/senha", data={"senha": "curta"},
           follow_redirects=True)
print("  admin: senha curta recusada:", "pelo menos 6 caracteres" in r.get_data(as_text=True))
assert "pelo menos 6 caracteres" in r.get_data(as_text=True)
r = c.get("/admin/painel")
print("  admin lista as contas:", "dono@fitnews.com" in r.get_data(as_text=True))
assert "dono@fitnews.com" in r.get_data(as_text=True)
r = c.post(f"/admin/usuario/{uid}/senha", data={"senha": "senhaadmin1"},
           follow_redirects=True)
print("  admin redefiniu a senha:", "redefinida" in r.get_data(as_text=True))
assert "redefinida" in r.get_data(as_text=True)
c.get("/sair")
r = c.post("/entrar", data={"email": "dono@fitnews.com", "senha": "senhaadmin1"},
           follow_redirects=True)
print("  login com a senha dada pelo admin:", "Conta Teste" in r.get_data(as_text=True))
assert "Conta Teste" in r.get_data(as_text=True)

print("== Data de nascimento digitada DD/MM/AAAA ==")
r = c.post("/criar", data={
    "nome": "Data Brasileira", "sexo": "outro", "data_nascimento": "15/07/1985",
    "peso": "70", "altura": "175", "atividade": "moderado",
    "nivel_treino": "iniciante", "dias": "3", "local": "academia",
    "focos": ["core"], "aceite": "sim", "aceite_privacidade": "sim",
}, follow_redirects=True)
hp = r.get_data(as_text=True)
print("  plano gerado:", r.status_code == 200 and "Data Brasileira" in hp)
assert r.status_code == 200 and "Data Brasileira" in hp
conn = database.get_db()
lin = conn.execute("SELECT data_nascimento, idade FROM planos WHERE nome='Data Brasileira'"
                   ).fetchone()
conn.close()
print("  salva como ISO:", lin["data_nascimento"] == "1985-07-15",
      "| idade:", lin["idade"])
assert lin["data_nascimento"] == "1985-07-15"
assert lin["idade"] and 10 <= lin["idade"] <= 100

print()
print("TODOS OS TESTES PASSARAM" if falhas == 0 else "HOUVE FALHAS")
