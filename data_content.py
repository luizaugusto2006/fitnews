# -*- coding: utf-8 -*-
# Alongamentos, alimentacao e suplementos do FitNews

# Alongamento pos-treino por grupo muscular
# campos: nome, como_fazer, tempo, contraindicado_para
STRETCHES = {
    "peito": [
        {"nome": "Alongamento de peitoral na parede", "como": "Apoie o antebraço na parede com o braço a 90 graus e gire o tronco levemente para o lado oposto.", "tempo": "30s cada lado", "contra": "ombro"},
        {"nome": "Abertura de braços em pé", "como": "Entrelace as costas das mãos e estique os braços para trás, abrindo o peito.", "tempo": "30s", "contra": "ombro"},
        {"nome": "Alongamento de peitoral deitado", "como": "Deitado de costas, abra os braços em cruz e deixe os ombros relaxarem no chão.", "tempo": "40s", "contra": ""},
    ],
    "costas": [
        {"nome": "Postura da criança", "como": "Ajoelhado, sente sobre os calcanhares e estique os braços à frente no chão.", "tempo": "40s", "contra": "quadril"},
        {"nome": "Alongamento lombar em decúbito lateral", "como": "Deitado de lado, puxe o joelho em direção ao peito com as mãos.", "tempo": "30s cada lado", "contra": "quadril"},
        {"nome": "Gato camelo suave", "como": "Em quatro apoios, alterne levemente a curvatura da coluna, sem forçar.", "tempo": "10 repetições lentas", "contra": ""},
    ],
    "ombros": [
        {"nome": "Alongamento de ombro cruzado", "como": "Leve um braço cruzado sobre o peito e segure com a outra mão por 30s.", "tempo": "30s cada lado", "contra": ""},
        {"nome": "Tríceps na vertical", "como": "Dobre um braço por trás da cabeça e puxe o cotovelo com a mão oposta.", "tempo": "30s cada lado", "contra": ""},
        {"nome": "Alongamento de ombro com barbante", "como": "Segure uma toalha com as duas mãos por trás do corpo e leve o braço de cima para trás com leveza.", "tempo": "30s cada lado", "contra": "ombro"},
    ],
    "biceps": [
        {"nome": "Esticamento de bíceps na parede", "como": "Apoie a palma da mão na parede com o braço esticado e gire o corpo lentamente.", "tempo": "30s cada lado", "contra": "punho"},
        {"nome": "Alongamento de bíceps em pé", "como": "Estique o braço para trás com a palma virada para trás e incline o tronco levemente.", "tempo": "30s cada lado", "contra": ""},
    ],
    "triceps": [
        {"nome": "Tríceps esticado atrás da cabeça", "como": "Dobre o braço por trás da cabeça e puxe o cotovelo com a mão oposta.", "tempo": "30s cada lado", "contra": ""},
        {"nome": "Alongamento de tríceps na parede", "como": "Apoie a ponta do cotovelo na parede e deixe o tronco avançar suavemente.", "tempo": "30s cada lado", "contra": "ombro"},
    ],
    "quadriceps": [
        {"nome": "Quadríceps deitado com faixa", "como": "Deitado de lado ou de costas, puxe o calcanhar em direção ao glúteo usando uma faixa.", "tempo": "30s cada perna", "contra": ""},
        {"nome": "Quadríceps em pé", "como": "Em pé, puxe o calcanhar contra o glúteo segurando em uma parede.", "tempo": "30s cada perna", "contra": "joelho,quadril"},
    ],
    "posterior": [
        {"nome": "Isquiotibiais deitado com faixa", "como": "Deitado de costas, estique uma perna na vertical com o auxílio de uma faixa.", "tempo": "30s cada perna", "contra": ""},
        {"nome": "Isquiotibiais sentado", "como": "Sentado, estique as pernas e alcance os pés com leveza, sem forçar a coluna.", "tempo": "30s", "contra": "hernia_discal,bico_papagaio,coluna"},
        {"nome": "Postura do ajoelhado meio split", "como": "Em meio ajoelhado, empurre levemente o quadril para frente com a perna da frente esticada.", "tempo": "30s cada lado", "contra": "joelho,quadril"},
    ],
    "gluteo": [
        {"nome": "Piriforme deitado", "como": "Deitado de costas, cruze o joelho de um lado sobre a coxa do outro e puxe em direção ao peito.", "tempo": "30s cada lado", "contra": "quadril"},
        {"nome": "Alongamento de glúteo sentado", "como": "Sentado com as pernas cruzadas, incline o tronco para frente com a coluna reta.", "tempo": "30s", "contra": "quadril,hernia_discal,bico_papagaio"},
        {"nome": "Joelho ao peito em decúbito", "como": "Deitado de costas, puxe um joelho ao peito com as mãos.", "tempo": "30s cada lado", "contra": ""},
    ],
    "panturrilha": [
        {"nome": "Panturrilha na parede", "como": "Empurre o calcanhar no chão com uma perna atrás e o corpo inclinado na parede.", "tempo": "30s cada perna", "contra": ""},
        {"nome": "Panturrilha no degrau", "como": "Fique em um degrau e deixe o calcanhar descer abaixo do nível do pé.", "tempo": "30s", "contra": "tornozelo"},
    ],
    "core": [
        {"nome": "Cobra leve (extensão suave)", "como": "Deitado de bruços, apoie levemente as mãos e ergua o peito sem forçar a lombar.", "tempo": "20s", "contra": "hernia_discal,bico_papagaio"},
        {"nome": "Joelhos ao peito em decúbito", "como": "Deitado de costas, traga os dois joelhos ao peito e balance levemente.", "tempo": "30s", "contra": ""},
        {"nome": "Respiração diafragmática", "como": "Deitado de costas, inspire pelo nariz inflando a barriga e expire lentamente pela boca.", "tempo": "1 minuto", "contra": ""},
        {"nome": "Alongamento de coluna em decúbito lateral", "como": "Deitado de lado, traga os joelhos ao peito mantendo os ombros alinhados.", "tempo": "30s cada lado", "contra": "quadril"},
    ],
    "cardio": [
        {"nome": "Caminhada leve como volta à calma", "como": "Caminhe por 3 a 5 minutos reduzindo o ritmo gradualmente.", "tempo": "3-5 min", "contra": ""},
        {"nome": "Solta de pernas em pé", "como": "Balance levemente cada perna e depois as duas, relaxando músculos.", "tempo": "30s cada", "contra": ""},
        {"nome": "Alongamento geral de membros", "como": "Estique braços, pernas e tronco em posições confortáveis, sem rebotes.", "tempo": "30s cada região", "contra": ""},
    ],
    "mobilidade": [
        {"nome": "Rotação de quadril em pé", "como": "Em pé com apoio, faça rotações lentas de quadril para cada lado.", "tempo": "10 cada lado", "contra": ""},
        {"nome": "Círculos de ombro", "como": "Círculos amplos e lentos para frente e para trás.", "tempo": "10 cada direção", "contra": ""},
        {"nome": "Mobilidade de tornozelo", "como": "Apoie a frente do pé no chão e desloque o joelho à frente.", "tempo": "30s cada lado", "contra": "tornozelo"},
    ],
}

# Aquecimento geral (sempre) + ativações específicas por grupo
WARMUP_GENERAL = [
    "5 minutos de cardio leve (caminhada rápida, bicicleta ou marcha em lugar)",
    "Rotações de braços para frente e para trás (10 cada direção)",
    "Rotações de quadril em pé (10 cada lado)",
    "Mobilidade de tornozelo e joelho (10 cada lado)",
    "Elevação de joelhos alternados (10 cada perna)",
    "2 séries leves do primeiro exercício do treino (metade das repetições)",
]

WARMUP_ACTIVATION = {
    "peito": ["Rotações de ombro (10 cada direção)", "Flexão de braço leve no joelho (10 repetições)"],
    "costas": ["Gato camelo (10 repetições)", "Puxada leve na polia (15 repetições)"],
    "ombros": ["Círculos de ombro com halteres leves (12 cada direção)", "Face pull leve (15 repetições)"],
    "biceps": ["Rosca leve com halteres (15 repetições)", "Estiramento de braços (30s)"],
    "triceps": ["Extensão leve na polia (15 repetições)", "Rotação de punho (10 cada lado)"],
    "quadriceps": ["Ponte de glúteo (12 repetições)", "Cadeira extensora leve (12 repetições)"],
    "posterior": ["Cadeira flexora leve (12 repetições)", "Pull through sem carga (12 repetições)"],
    "gluteo": ["Ponte de glúteo (12 repetições)", "Abdução leve de quadril (12 cada lado)"],
    "panturrilha": ["Elevação de panturrilha leve (15 repetições)", "Marcha em lugar (1 min)"],
    "core": ["Respiração diafragmática (5 respirações)", "Dead bug (8 cada lado)"],
    "cardio": ["Caminhada progressiva (2 minutos)", "Mobilidade de quadril e tornozelo (1 min)"],
    "mobilidade": ["Caminhada leve (2 minutos)", "Círculos de braços e quadril (1 min)"],
}

# ------------------------------------------------------------------
# ALIMENTACAO
# ------------------------------------------------------------------
# Faixas por idade: <20, 20-29, 30-39, 40-49, 50-59, 60+
AGE_BANDS = [
    (0, 19, "<20"),
    (20, 29, "20-29"),
    (30, 39, "30-39"),
    (40, 49, "40-49"),
    (50, 59, "50-59"),
    (60, 120, "60+"),
]

NUTRITION_BANDS = {
    "<20": {
        "resumo": "Crescimento e desenvolvimento: priorize proteína de qualidade, cálcio e ferro. Nunca elimine grupos alimentares.",
        "proteina_g_kg": 1.6,
        "gordura_pct": 30,
        "refeicoes": [
            ("Café da manhã", "2 ovos mexidos + 1 fatia de pão integral + 1 fruta + 200ml de leite ou bebida de soja"),
            ("Lanche da manhã", "1 iogurte natural + 1 banana + 1 col. de aveia"),
            ("Almoço", "1 porção de arroz + 1 porção de feijão + 120g de frango grelhado + salada à vontade + 1 fruta"),
            ("Lanche da tarde", "Sanduíche integral com queijo branco + fruta + água"),
            ("Jantar", "1 porção de massa integral + 100g de carne magra ou legumes + salada"),
            ("Pós-treino (30-60 min)", "1 fruta + 1 punhado de castanhas ou 1 copo de leite com biscoito integral"),
        ],
        "atencao": "Adolescentes: não siga dietas restritivas. Priorize cálcio (leite, iogurte, queijo) e ferro (carne vermelha, feijão).",
    },
    "20-29": {
        "resumo": "Pico de massa muscular: base consistente de proteína em todas as refeições e hidratação de pelo menos 2 a 3 litros de água por dia.",
        "proteina_g_kg": 1.8,
        "gordura_pct": 28,
        "refeicoes": [
            ("Café da manhã", "3 ovos + pão integral + 1 fruta + café ou chá"),
            ("Lanche da manhã", "Fruta + 1 punhado de oleaginosas (amendoim, castanha)"),
            ("Almoço", "Arroz + feijão + 150g de proteína (frango, peixe, carne) + legumes + salada"),
            ("Pré-treino (1h antes)", "Banana + aveia ou tapioca com queijo"),
            ("Jantar", "Proteína magra + batata ou arroz + vegetais verdes"),
            ("Pós-treino", "Whey ou leite + fruta, ou uma refeição sólida"),
        ],
        "atencao": "Mantenha horários regulares e evite excesso de ultraprocessados e refrigerantes.",
    },
    "30-39": {
        "resumo": "Metabolismo começa a desacelerar: controle porções, mantenha fibra em alta e distribua proteína no dia todo.",
        "proteina_g_kg": 1.7,
        "gordura_pct": 28,
        "refeicoes": [
            ("Café da manhã", "Ovos mexidos com espinafre + fruta + café sem açúcar"),
            ("Lanche da manhã", "Iogurte natural + granola sem açúcar"),
            ("Almoço", "100g de arroz + feijão + 150g de proteína grelhada + salada com azeite"),
            ("Lanche da tarde", "Fruta + oleaginosas ou pão de queijo integral"),
            ("Jantar", "Sopa de legumes com frango desfiado ou omelete + salada"),
            ("Pós-treino", "Proteína (whey ou alimento) + carboidrato leve"),
        ],
        "atencao": "Reduza açúcar adicionado e álcool. Cuidado com sal: máximo de 5g por dia.",
    },
    "40-49": {
        "resumo": "Foco em saúde cardiovascular e manutenção de massa muscular: mais fibras, peixes gordurosos e legumes coloridos.",
        "proteina_g_kg": 1.7,
        "gordura_pct": 30,
        "refeicoes": [
            ("Café da manhã", "Papinha de aveia com frutas vermelhas + 1 ovo + café"),
            ("Lanche da manhã", "Fruta + 1 col. de sementes (chia, linhaça)"),
            ("Almoço", "Arroz integral opcional + feijão + 150g de proteína + salada variada"),
            ("Lanche da tarde", "Castanhas (30g) + fruta ou iogurte"),
            ("Jantar", "Proteína leve (peixe, frango) + legumes + sopa"),
            ("Pós-treino", "Leite, iogurte ou whey + fruta"),
        ],
        "atencao": "Atenção ao colesterol e pressão: prefira peixe 2 a 3x por semana, azeite e pouca gordura saturada.",
    },
    "50-59": {
        "resumo": "Prevenção de perda de massa muscular e ossos: proteína suficiente, cálcio, vitamina D e hidratação constante.",
        "proteina_g_kg": 1.8,
        "gordura_pct": 30,
        "refeicoes": [
            ("Café da manhã", "Ovos ou queijo branco + fruta + pão integral + café"),
            ("Lanche da manhã", "Iogurte com aveia ou fruta madura"),
            ("Almoço", "Proteína de qualidade (150g) + arroz + feijão + legumes cozidos"),
            ("Lanche da tarde", "Fruta + oleaginosas ou leite com biscoito integral"),
            ("Jantar", "Sopa nutritiva com legumes + proteína leve + salada"),
            ("Pós-treino", "Leite, queijo, iogurte ou whey para completar a proteína do dia"),
        ],
        "atencao": "Priorize cálcio (leite, queijo, sardinha) e vitamina D. Mastigue bem e hidrate-se mesmo sem sede.",
    },
    "60+": {
        "resumo": "Manutenção de funcionalidade e força: proteína distribuída, alimentos fáceis de mastigar e boa hidratação.",
        "proteina_g_kg": 1.8,
        "gordura_pct": 32,
        "refeicoes": [
            ("Café da manhã", "Ovos cozidos + pão integral + fruta amassada + café"),
            ("Lanche da manhã", "Iogurte ou leite + biscoito integral"),
            ("Almoço", "Carne ou frango macio + arroz + feijão + legumes bem cozidos"),
            ("Lanche da tarde", "Fruta sem casca dura + queijo branco ou coalhada"),
            ("Jantar", "Sopa cremosa de legumes com frango desfiado ou peixe"),
            ("Pós-treino / ceia", "Leite com colágeno ou iogurte, opcionalmente whey"),
        ],
        "atencao": "60+: aumente a densidade nutricional (calorias em pouco volume), B12 e água. Prefira alimentos macios se houver dificuldade de mastigação.",
    },
}

# ------------------------------------------------------------------
# SUPLEMENTOS
# ------------------------------------------------------------------
# Regra: base por idade + extras por foco + extras por limitacao
SUPPLEMENTS_BASE = {
    "<20": [
        ("Whey protein (ou alimento)", "1 dose (20-25g) após o treino, se não atingir a proteína da dieta", "Somente se a dieta for insuficiente; não substitui refeições."),
        ("Creatina monoidratada", "3g ao dia, todo dia (inclusive nos dias de descanso)", "Seguro em adolescentes treinados; prefira orientação de nutricionista."),
        ("Cálcio + Vitamina D", "500-600mg de cálcio + 1000 UI de D3 ao dia", "Importante no pico de massa óssea."),
    ],
    "20-29": [
        ("Whey protein", "1-2 doses (25-50g) por dia conforme a necessidade", "Conveniência para completar a proteína diária."),
        ("Creatina monoidratada", "3-5g ao dia", "Melhora força e desempenho; beba bastante água."),
        ("Multivitamínico", "1 dose pela manhã", "Cobertura basal; não substitui a alimentação."),
    ],
    "30-39": [
        ("Whey protein", "1-2 doses (25-50g) por dia", "Auxilia na recuperação muscular."),
        ("Creatina monoidratada", "3-5g ao dia", "Beneficia força, massa magra e função cerebral."),
        ("Ômega 3 (EPA/DHA)", "1-2g ao dia", "Saúde cardiovascular e anti-inflamatório."),
    ],
    "40-49": [
        ("Creatina monoidratada", "3-5g ao dia", "Apoia massa muscular e função cognitiva."),
        ("Ômega 3 (EPA/DHA)", "1-2g ao dia", "Com apoio à saúde cardiovascular."),
        ("Vitamina D3", "1000-2000 UI ao dia", "Principalmente em exposição solar baixa."),
        ("Whey protein", "1 dose (25-30g) ao dia", "Se a proteína alimentar estiver baixa."),
    ],
    "50-59": [
        ("Creatina monoidratada", "3-5g ao dia", "Ajuda na prevenção da perda muscular (sarcopenia)."),
        ("Cálcio + Vitamina D3", "500-600mg + 1000-2000 UI ao dia", "Saúde óssea."),
        ("Ômega 3 (EPA/DHA)", "1-2g ao dia", "Coração e articulações."),
        ("Whey protein", "1-2 doses (25-50g)", "Facilita atingir a meta de proteína."),
        ("Colágeno hidrolisado", "10-15g ao dia", "Articulações e tendões; melhor com vitamina C."),
    ],
    "60+": [
        ("Whey protein ou proteína de alta qualidade", "1-2 doses (25-50g) por dia", "Combate a sarcopenia; consulte nutricionista."),
        ("Vitamina B12", "1000 mcg 2-3x por semana (se orientado)", "Absorção reduzida com a idade."),
        ("Cálcio + Vitamina D3", "500-600mg + 1000-2000 UI ao dia", "Prevenção de osteoporose."),
        ("Ômega 3 (EPA/DHA)", "1-2g ao dia", "Cognição e saúde cardiovascular."),
        ("Creatina monoidratada", "3-5g ao dia", "Força e funcionalidade; avalie com médico se houver problemas renais."),
    ],
}

SUPPLEMENTS_FOCO = {
    "perda_peso": [("Cafeína pré-treino", "100-200mg 30-60 min antes (café forte serve)", "Não consumir após as 16h nem se houver pressão alta."),
                   ("Proteína (whey)", "1-2 doses ao dia", "Aumenta a saciedade e preserva massa magra no déficit.")],
    "definicao": [("Whey protein", "1-2 doses (25-50g)", "Mantém massa magra na definição."),
                  ("Ômega 3", "1-2g ao dia", "Saúde geral durante o ajuste calórico.")],
    "hipertrofia": [("Whey protein", "1-2 doses (25-50g)", "Complementa a proteína para ganho de massa."),
                    ("Creatina monoidratada", "3-5g ao dia", "Suporte a volume e intensidade."),
                    ("HMB (opcional)", "3g ao dia", "Apenas em casos de treino muito intenso ou catabolismo; validado de forma limitada.")],
    "fortalecimento": [("Creatina monoidratada", "3-5g ao dia", "Melhora força e potência."),
                       ("Whey protein", "1-2 doses", "Recuperação muscular.")],
    "resistencia": [("Eletrólitos", "1 porção em dias de treino longo (>60 min)", "Reposição de sais minerais."),
                    ("Cafeína", "100-200mg antes do treino", "Melhora o desempenho; não abusar."),
                    ("Ômega 3", "1-2g ao dia", "Recuperação geral.")],
    "bracos": [("Whey protein", "1-2 doses (25-50g)", "Suporte à hipertrofia de membros superiores."),
               ("Creatina monoidratada", "3-5g ao dia", "Volume e força.")],
    "peito": [("Whey protein", "1-2 doses", "Suporte à hipertrofia."),
              ("Creatina monoidratada", "3-5g ao dia", "Desempenho em supino e exercícios de peito.")],
    "costas": [("Whey protein", "1-2 doses", "Suporte à hipertrofia."),
               ("Creatina monoidratada", "3-5g ao dia", "Desempenho em puxadas e remadas.")],
    "ombros": [("Whey protein", "1-2 doses", "Suporte à hipertrofia."),
               ("Colágeno hidrolisado", "10g ao dia", "Apoio aos tendões do ombro (com vitamina C).")],
    "pernas": [("Creatina monoidratada", "3-5g ao dia", "Fortalece séries pesadas de pernas."),
               ("Whey protein", "1-2 doses", "Recuperação de grande massa muscular.")],
    "gluteos": [("Creatina monoidratada", "3-5g ao dia", "Suporte à progressão de carga."),
                ("Whey protein", "1-2 doses", "Hipertrofia de glúteos.")],
    "core": [("Whey protein", "1-2 doses", "Se a proteína estiver baixa.")],
    "mobilidade": [("Colágeno hidrolisado", "10g ao dia", "Articulações e tecido conjuntivo."),
                   ("Ômega 3", "1-2g ao dia", "Efeito anti-inflamatório.")],
    "postura": [("Magnésio", "200-400mg à noite", "Relaxamento muscular; consulte se usar medicamentos."),
                ("Ômega 3", "1-2g ao dia", "Saúde de articulações e músculos.")],
    "funcional": [("Whey protein", "1-2 doses", "Recuperação geral."),
                  ("Creatina monoidratada", "3-5g ao dia", "Versatilidade de desempenho.")],
}

SUPPLEMENTS_LIMIT = {
    "hernia_discal": [("Colágeno hidrolisado", "10-15g ao dia com vitamina C", "Suporte ao disco e tecido conjuntivo; não substitui tratamento."),
                      ("Vitamina D3", "1000-2000 UI ao dia", "Saúde óssea e muscular."),
                      ("Ômega 3", "1-2g ao dia", "Efeito anti-inflamatório.")],
    "bico_papagaio": [("Colágeno hidrolisado", "10-15g ao dia com vitamina C", "Suporte ao tecido conjuntivo da coluna."),
                      ("Vitamina D3", "1000-2000 UI ao dia", "Saúde óssea."),
                      ("Ômega 3", "1-2g ao dia", "Anti-inflamatório.")],
    "hernia_abdominal": [("Colágeno hidrolisado", "10-15g ao dia", "Suporte ao tecido conjuntivo."),
                         ("Vitamina D3", "1000-2000 UI", "Saúde geral e muscular.")],
    "joelho": [("Colágeno hidrolisado", "10-15g ao dia com vitamina C", "Cartilagem e tendões."),
               ("Ômega 3", "1-2g ao dia", "Anti-inflamatório articular."),
               ("Vitamina D3", "1000-2000 UI", "Saúde óssea.")],
    "coluna": [("Colágeno hidrolisado", "10-15g ao dia", "Tecido conjuntivo da coluna."),
               ("Magnésio", "200-400mg à noite", "Relaxamento muscular.")],
    "ombro": [("Colágeno hidrolisado", "10-15g ao dia", "Tendões do manguito rotador."),
              ("Ômega 3", "1-2g ao dia", "Anti-inflamatório.")],
    "punho": [("Colágeno hidrolisado", "10-15g ao dia", "Tendões e ligamentos."),
              ("Ômega 3", "1-2g ao dia", "Anti-inflamatório.")],
    "cardiaco": [("Ômega 3", "1-2g ao dia", "Saúde cardiovascular; somente com avaliação médica."),
                 ("Coenzima Q10", "100-200mg ao dia", "Frequente em usuários de estatinas; avalie com médico.")],
    "pressao": [("Magnésio", "200-400mg ao dia", "Pode ajudar na pressão; avalie com médico."),
                ("Ômega 3", "1-2g ao dia", "Saúde cardiovascular.")],
    "diabetes": [("Vitamina D3", "1000-2000 UI", "Metabolismo e imunidade."),
                 ("Cromo", "200-400 mcg ao dia", "Apoio ao metabolismo da glicose; avalie com médico."),
                 ("Ômega 3", "1-2g ao dia", "Saúde cardiovascular.")],
    "gravidez": [("Ácido fólico", "400-600 mcg ao dia", "Essencial na gestação; apenas com orientação médica."),
                 ("Ferro", "Conforme exame", "Somente se houver anemia e orientação do pré-natal."),
                 ("DHA/Ômega 3", "200-300mg ao dia", "Desenvolvimento fetal; somente com orientação médica.")],
}

# Exercicios evitados (exibidos no plano como aviso) - codigos de limitacao
LIMITATION_LABELS = {
    "hernia_discal": "Hérnia de disco",
    "bico_papagaio": "Bico de papagaio (protusão discal)",
    "hernia_abdominal": "Hérnia abdominal",
    "coluna": "Problemas na coluna",
    "joelho": "Problemas no joelho",
    "ombro": "Problemas no ombro",
    "punho": "Problemas no punho",
    "quadril": "Problemas no quadril",
    "tornozelo": "Problemas no tornozelo",
    "cervical": "Problemas cervicais",
    "cardiaco": "Condição cardíaca",
    "pressao": "Pressão alta",
    "diabetes": "Diabetes",
    "asma": "Asma",
    "gravidez": "Gestante",
    "pos_cirurgia": "Cirurgia recente",
}
