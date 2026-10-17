# -*- coding: utf-8 -*-
"""Smoke test do FitNews (executar: python test_site.py)"""
import re

from app import app

c = app.test_client()

print("== Rotas publicas ==")
for r in ["/", "/criar", "/planos", "/sobre", "/contato", "/admin"]:
    print(" ", r, c.get(r).status_code)

print("== Criar plano (hernia de disco + bico de papagaio) ==")
resp = c.post("/criar", data={
    "nome": "Teste Silva", "sexo": "masculino", "data_nascimento": "1990-05-10",
    "peso": "80", "altura": "175", "atividade": "moderado",
    "nivel_treino": "intermediario", "dias": "4", "horario": "manha",
    "local": "academia",
    "limitacoes": ["hernia_discal", "bico_papagaio"],
    "focos": ["pernas", "perda_peso", "core", "peito"], "aceite": "sim",
}, follow_redirects=True)
html = resp.get_data(as_text=True)
print("  status:", resp.status_code)

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
nomes = re.findall(r"<strong>([^<]+)</strong><br>", treino)
print("  exercicios do treino:", nomes)
assert falhas == 0, "EXERCICIO PERIGOSO NO TREINO!"

print("  + aquecimento/alongamento/alimentacao/suplementos:",
      "Aquecimento geral" in html, "Alongamento pós-treino" in html,
      "Alimentação sugerida" in html, "Suplementos sugeridos" in html)

print("== Editar foco (muda para bracos) ==")
resp2 = c.post("/plano/1/editar", data={
    "nome": "Teste Silva", "sexo": "masculino", "data_nascimento": "1990-05-10",
    "peso": "80", "altura": "175", "atividade": "moderado",
    "nivel_treino": "intermediario", "dias": "3", "horario": "manha",
    "local": "academia", "limitacoes": "hernia_discal",
    "focos": "bracos,peito", "aceite": "sim",
}, follow_redirects=True)
html2 = resp2.get_data(as_text=True)
m = re.search(r'id="aba-treino"(.*?)<!-- ============ AQUECIMENTO', html2, re.S)
treino2 = m.group(1) if m else ""
nomes2 = re.findall(r"<strong>([^<]+)</strong><br>", treino2)
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
r6 = c.post("/admin", data={"usuario": "admin", "senha": "fitnews2026"}, follow_redirects=True)
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

print()
print("TODOS OS TESTES PASSARAM" if falhas == 0 else "HOUVE FALHAS")
