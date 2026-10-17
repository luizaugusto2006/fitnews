# -*- coding: utf-8 -*-
"""Gerador automático de plano de treino, alongamento, alimentacao e suplementos."""
import random

from data_content import (
    AGE_BANDS,
    NUTRITION_BANDS,
    STRETCHES,
    SUPPLEMENTS_BASE,
    SUPPLEMENTS_FOCO,
    SUPPLEMENTS_LIMIT,
    WARMUP_ACTIVATION,
    WARMUP_GENERAL,
)
from database import get_db

# ------------------------------------------------------------------
# Catalogos
# ------------------------------------------------------------------
LIMITACOES = [
    ("nenhuma", "Nenhuma limitação"),
    ("hernia_discal", "Hérnia de disco"),
    ("bico_papagaio", "Bico de papagaio (protusão discal)"),
    ("hernia_abdominal", "Hérnia abdominal / umbilical"),
    ("coluna", "Problemas na coluna (lombar / cervical)"),
    ("joelho", "Problemas no joelho"),
    ("ombro", "Problemas no ombro"),
    ("punho", "Problemas no punho"),
    ("quadril", "Problemas no quadril"),
    ("tornozelo", "Problemas no tornozelo"),
    ("cardiaco", "Condição cardíaca"),
    ("pressao", "Pressão alta"),
    ("diabetes", "Diabetes"),
    ("asma", "Asma"),
    ("gravidez", "Gestante"),
    ("pos_cirurgia", "Cirurgia recente (6 meses)"),
]

FOCOS = [
    ("bracos", "Braços (bíceps e tríceps)"),
    ("peito", "Peito"),
    ("costas", "Costas"),
    ("ombros", "Ombros"),
    ("pernas", "Pernas"),
    ("gluteos", "Glúteos"),
    ("core", "Abdômen / Core"),
    ("fortalecimento", "Fortalecimento geral"),
    ("perda_peso", "Perda de peso"),
    ("resistencia", "Resistência cardiovascular"),
    ("hipertrofia", "Hipertrofia (massa muscular)"),
    ("definicao", "Definição / Tonificação"),
    ("mobilidade", "Mobilidade e flexibilidade"),
    ("postura", "Melhora de postura"),
    ("funcional", "Treino funcional"),
]

FOCO_LABELS = dict(FOCOS)
LIMIT_LABELS = dict(LIMITACOES)

# Cada foco contribui com quais grupos musculares no treino
FOCO_GRUPOS = {
    "bracos": ["biceps", "triceps"],
    "peito": ["peito"],
    "costas": ["costas"],
    "ombros": ["ombros"],
    "pernas": ["quadriceps", "posterior", "panturrilha"],
    "gluteos": ["gluteo", "posterior"],
    "core": ["core"],
    "fortalecimento": ["peito", "costas", "ombros", "biceps", "triceps",
                       "quadriceps", "posterior", "gluteo", "core"],
    "perda_peso": ["cardio", "core"],
    "resistencia": ["cardio"],
    "hipertrofia": [],
    "definicao": ["cardio"],
    "mobilidade": ["mobilidade"],
    "postura": ["costas", "core", "mobilidade"],
    "funcional": ["core", "cardio", "gluteo"],
}

GRUPO_LABELS = {
    "peito": "Peito", "costas": "Costas", "ombros": "Ombros",
    "biceps": "Bíceps", "triceps": "Tríceps", "quadriceps": "Quadríceps",
    "posterior": "Posterior de coxa", "gluteo": "Glúteos",
    "panturrilha": "Panturrilha", "core": "Core / Abdômen",
    "cardio": "Cardio", "mobilidade": "Mobilidade",
}

GRUPO_ORDEM = ["peito", "costas", "ombros", "biceps", "triceps", "quadriceps",
               "posterior", "gluteo", "panturrilha", "core", "cardio", "mobilidade"]

NIVEL_ORDEM = {"iniciante": 0, "intermediario": 1, "avancado": 2}
EQUIP_CASA = ("peso_corporal", "halteres", "cardio")

ATIVIDADE_FATOR = {
    "sedentario": 1.2, "leve": 1.375, "moderado": 1.55,
    "intenso": 1.725, "muito_intenso": 1.9,
}
ATIVIDADE_LABELS = {
    "sedentario": "Sedentário (pouco ou nenhum exercício)",
    "leve": "Levemente ativo (exercício 1-3x/semana)",
    "moderado": "Moderado (exercício 3-5x/semana)",
    "intenso": "Intenso (exercício 6-7x/semana)",
    "muito_intenso": "Muito intenso (trabalho físico + treino diário)",
}

KCAL_BASE = {  # estimativas de TDEE para quem nao informou peso/altura (atividade moderada)
    "<20": (2400, 2000), "20-29": (2300, 1900), "30-39": (2200, 1800),
    "40-49": (2100, 1750), "50-59": (2000, 1650), "60+": (1900, 1600),
}


def faixa_idade(idade):
    for min_a, max_a, rotulo in AGE_BANDS:
        if min_a <= idade <= max_a:
            return rotulo
    return "20-29"


def parse_csv(texto):
    return [x.strip() for x in (texto or "").split(",") if x.strip()]


# ------------------------------------------------------------------
# Selecao de exercicios com bloqueio de contraindicacoes
# ------------------------------------------------------------------
def banco_exercicios(limitacoes, nivel_usuario=None, local="academia"):
    """Retorna exercicios permitidos (nenhum codigo bate com as limitacoes)."""
    conn = get_db()
    rows = conn.execute("SELECT * FROM exercicios ORDER BY id").fetchall()
    conn.close()
    permitidos, bloqueados = [], []
    limite_nivel = NIVEL_ORDEM.get(nivel_usuario or "iniciante", 0)
    for r in rows:
        proib = set(parse_csv(r["contraindicado_para"]))
        if proib & set(limitacoes):
            bloqueados.append(dict(r))
            continue
        if NIVEL_ORDEM.get(r["nivel"], 0) > limite_nivel:
            continue
        if local == "casa" and r["equipamento"] not in EQUIP_CASA:
            continue
        permitidos.append(dict(r))
    return permitidos, bloqueados


def contar_grupo(permitidos, grupo):
    return sum(1 for e in permitidos if e["grupo"] == grupo)


def escolher(permitidos, grupo, quantidade, usados, permitidos_todos=None):
    """Escolhe 'quantidade' exercicios do grupo, reutilizando os do plano anterior."""
    pool = [e for e in permitidos if e["grupo"] == grupo]
    escolhidos, nomes = [], set()

    # 1) mantem exercicios ja existentes no plano anterior (mesmo grupo)
    for nome in usados.get(grupo, []):
        if len(escolhidos) >= quantidade:
            break
        match = next((e for e in pool if e["nome"] == nome), None)
        if match and match["nome"] not in nomes:
            escolhidos.append(match)
            nomes.add(match["nome"])

    # 2) complementa com novos, na ordem do banco (deterministico)
    for e in pool:
        if len(escolhidos) >= quantidade:
            break
        if e["nome"] not in nomes:
            escolhidos.append(e)
            nomes.add(e["nome"])

    # 3) fallback: se o grupo ficou sem opcoes (equipamento/limitacao), usa o banco completo
    if len(escolhidos) < quantidade and permitidos_todos is not None:
        pool2 = [e for e in permitidos_todos if e["grupo"] == grupo]
        for e in pool2:
            if len(escolhidos) >= quantidade:
                break
            if e["nome"] not in nomes:
                escolhidos.append(e)
                nomes.add(e["nome"])
    return escolhidos


# ------------------------------------------------------------------
# Series / repeticoes / descanso
# ------------------------------------------------------------------
def esquema(focos, grupo, nivel):
    estilo = None
    for cand in ("perda_peso", "definicao", "resistencia", "fortalecimento", "hipertrofia"):
        if cand in focos:
            estilo = cand
            break

    if grupo == "cardio":
        if estilo in ("perda_peso", "definicao"):
            return {"series": 1, "reps": "30-40 min de ritmo moderado contínuo",
                    "descanso": "sem descanso intermediário"}
        if estilo == "resistencia":
            return {"series": 1, "reps": "20-30 min em ritmo alto (ou 8x 1min rápido / 1min leve)",
                    "descanso": "1 min entre blocos"}
        return {"series": 1, "reps": "15-20 min de aquecimento em ritmo leve",
                "descanso": "—"}
    if grupo == "mobilidade":
        return {"series": 1, "reps": "8-12 repetições lentas e controladas",
                "descanso": "—"}
    if grupo == "panturrilha":
        return {"series": 3, "reps": "12-15", "descanso": "45s"}

    if estilo == "perda_peso":
        return {"series": 3, "reps": "15-20", "descanso": "30-45s"}
    if estilo == "definicao":
        return {"series": 3, "reps": "12-15", "descanso": "45s"}
    if estilo == "resistencia":
        return {"series": 3, "reps": "20-25", "descanso": "30s"}
    if estilo == "fortalecimento":
        return {"series": 4, "reps": "6-8", "descanso": "90-120s"}
    if estilo == "hipertrofia":
        return {"series": 4, "reps": "8-12", "descanso": "60-90s"}
    if nivel == "avancado":
        return {"series": 4, "reps": "10-12", "descanso": "60-90s"}
    return {"series": 3, "reps": "10-12", "descanso": "60s"}


# ------------------------------------------------------------------
# Nutricao
# ------------------------------------------------------------------
def calcular_nutricao(dados):
    idade = dados.get("idade") or 25
    sexo = (dados.get("sexo") or "").lower()
    peso = dados.get("peso")
    altura = dados.get("altura")  # cm
    atividade = dados.get("atividade") or "moderado"
    focos = dados.get("focos") or []
    band = faixa_idade(idade)
    fator = ATIVIDADE_FATOR.get(atividade, 1.55)

    if peso and altura:
        bmr = 10 * peso + 6.25 * altura - 5 * idade + (5 if sexo.startswith("m") else -161)
        tdee = bmr * fator
        metodo = "fórmula de Mifflin-St Jeor (com seu peso e altura)"
    else:
        base = KCAL_BASE[band][0 if sexo.startswith("m") else 1]
        tdee = base * (fator / 1.55)
        metodo = "estimativa média por idade, sexo e nível de atividade"

    ajuste_txt = "Mantimento calórico para manutenção."
    if "perda_peso" in focos:
        tdee -= 400
        ajuste_txt = "Déficit calórico de ~400 kcal para perda de peso gradual (0,5 kg/semana)."
    elif "definicao" in focos:
        tdee -= 250
        ajuste_txt = "Déficit leve de ~250 kcal para definir sem perder massa magra."
    elif "hipertrofia" in focos:
        tdee += 250
        ajuste_txt = "Superávit leve de ~250 kcal para ganho de massa muscular."
    elif "fortalecimento" in focos:
        tdee += 200
        ajuste_txt = "Superávit leve de ~200 kcal para sustentar o ganho de força."

    piso = 1500 if sexo.startswith("m") else 1200
    tdee = max(tdee, piso)
    tdee = round(tdee / 10) * 10

    info = NUTRITION_BANDS[band]
    if peso:
        prot = round(peso * info["proteina_g_kg"])
    else:
        prot = round(tdee * 0.30 / 4)
    gord = round(tdee * info["gordura_pct"] / 100 / 9)
    carb = round((tdee - prot * 4 - gord * 9) / 4)
    carb = max(carb, 50)

    return {
        "faixa": band,
        "tdee": tdee,
        "metodo": metodo,
        "ajuste": ajuste_txt,
        "proteina": prot,
        "gordura": gord,
        "carboidrato": carb,
        "resumo": info["resumo"],
        "refeicoes": [list(r) for r in info["refeicoes"]],
        "atencao": info["atencao"],
        "agua": "ml por dia",
        "agua_l": round((peso * 35) / 1000, 1) if peso else 2.5,
    }


# ------------------------------------------------------------------
# Suplementos
# ------------------------------------------------------------------
def montar_suplementos(dados):
    band = faixa_idade(dados.get("idade") or 25)
    itens, vistos = [], set()

    def add(lista):
        for nome, dose, obs in lista:
            chave = nome.split(" (")[0].split(" -")[0].strip().lower()
            if chave in vistos:
                continue
            vistos.add(chave)
            itens.append({"nome": nome, "dose": dose, "obs": obs})

    add(SUPPLEMENTS_BASE.get(band, []))
    for f in dados.get("focos", []):
        add(SUPPLEMENTS_FOCO.get(f, []))
    for l in dados.get("limitacoes", []):
        add(SUPPLEMENTS_LIMIT.get(l, []))
    return {"faixa": band, "itens": itens}


# ------------------------------------------------------------------
# Geracao do plano completo
# ------------------------------------------------------------------
def gerar_plano(dados, anterior=None):
    limitacoes = [l for l in dados.get("limitacoes", []) if l != "nenhuma"]
    focos = dados.get("focos", [])
    nivel = dados.get("nivel_treino") or "iniciante"
    local = dados.get("local") or "academia"
    dias_qtd = int(dados.get("dias") or 3)

    permitidos, bloqueados = banco_exercicios(limitacoes, nivel, local)
    permitidos_todos, _ = banco_exercicios(limitacoes, None, local)

    # grupos musculares vindos dos focos
    grupos = []
    for f in focos:
        for g in FOCO_GRUPOS.get(f, []):
            if g not in grupos:
                grupos.append(g)
    if not grupos:  # nenhum foco com grupo (ex.: so hipertrofia) -> full body
        grupos = ["peito", "costas", "quadriceps", "posterior", "core"]
    grupos.sort(key=lambda g: GRUPO_ORDEM.index(g))

    # exercicios anteriores por grupo -> troca apenas o que mudou
    usados = {}
    if anterior:
        for dia in anterior.get("dias", []):
            for ex in dia.get("exercicios", []):
                usados.setdefault(ex["grupo"], []).append(ex["nome"])

    # distribui grupos nos dias (balanceado pela quantidade de exercicios disponiveis)
    pesos = {g: contar_grupo(permitidos, g) for g in grupos}
    buckets = [[] for _ in range(dias_qtd)]
    carga = [0] * dias_qtd
    for g in sorted(grupos, key=lambda x: (-pesos[x], GRUPO_ORDEM.index(x))):
        i = carga.index(min(carga))
        buckets[i].append(g)
        carga[i] += pesos[g]

    # monta os dias
    dias = []
    for idx, bucket in enumerate(buckets, start=1):
        if not bucket:
            bucket = ["cardio"]
        exercicios = []
        for g in bucket:
            qtd = 1 if g in ("panturrilha", "mobilidade", "cardio") else 2
            escolhidos = escolher(permitidos, g, qtd, usados, permitidos_todos)
            for e in escolhidos:
                eq = esquema(focos, g, nivel)
                exercicios.append({
                    "nome": e["nome"], "grupo": g, "grupo_label": GRUPO_LABELS.get(g, g),
                    "equipamento": e["equipamento"], "nivel": e["nivel"],
                    "series": eq["series"], "reps": eq["reps"], "descanso": eq["descanso"],
                })
        # sorteado no maximo para nao repetir sempre a mesma ordem visual
        rng = random.Random(dados.get("nome", "") + str(idx) + str(sorted(focos)))
        rng.shuffle(exercicios)

        # aquecimento especifico do dia
        ativacao = []
        for g in bucket:
            for a in WARMUP_ACTIVATION.get(g, []):
                if a not in ativacao:
                    ativacao.append(a)

        # alongamento pos-treino do dia (filtra contraindicacoes)
        pos = []
        for g in bucket:
            opcoes = [s for s in STRETCHES.get(g, []) if not (set(parse_csv(s["contra"])) & set(limitacoes))]
            for s in opcoes[:2]:
                pos.append({"grupo": GRUPO_LABELS.get(g, g), **s})

        dias.append({
            "titulo": f"Dia {chr(64 + idx)}",
            "grupos": [GRUPO_LABELS.get(g, g) for g in bucket],
            "grupos_cod": bucket,
            "exercicios": exercicios,
            "ativacao": ativacao,
            "alongamento_pos": pos,
        })

    # alongamento dinamico previo (geral + ativações)
    pre = [a for a in WARMUP_GENERAL[:5]]

    # exercicios evitados (aviso de seguranca)
    evitados = sorted({b["nome"] for b in bloqueados})

    nutri = calcular_nutricao(dados)
    supl = montar_suplementos(dados)

    return {
        "dias": dias,
        "aquecimento": WARMUP_GENERAL,
        "alongamento_pre": pre,
        "evitados": evitados,
        "limitacoes": limitacoes,
        "limitacoes_rotulos": [LIMIT_LABELS.get(l, l) for l in limitacoes],
        "focos": focos,
        "focos_rotulos": [FOCO_LABELS.get(f, f) for f in focos],
        "nutricao": nutri,
        "suplementos": supl,
        "aviso": ("Plano gerado automaticamente com base nas suas respostas. "
                  "Exercícios considerados de risco para as suas limitações foram excluídos. "
                  "Este conteúdo não substitui avaliação médica ou acompanhamento "
                  "profissional — procure um médico/fisioterapeuta e um educador físico "
                  "antes de iniciar."),
    }
