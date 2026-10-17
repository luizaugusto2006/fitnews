# -*- coding: utf-8 -*-
# Alongamentos, alimentacao e suplementos do FitNews

# Alongamento pos-treino por grupo muscular
# campos: nome, como_fazer, tempo, contraindicado_para
STRETCHES = {
    "peito": [
        {"nome": "Alongamento de peitoral na parede", "como": "Apoie o antebraco na parede com o braco a 90 graus e gire o tronco levemente para o lado oposto.", "tempo": "30s cada lado", "contra": "ombro"},
        {"nome": "Abertura de bracos em pe", "como": "Entrelace as costas das maos e estique os bracos para tras, abrindo o peito.", "tempo": "30s", "contra": "ombro"},
        {"nome": "Alongamento de peitoral deitado", "como": "Deitado de costas, abra os bracos em cruz e deixe os ombros relaxarem no chao.", "tempo": "40s", "contra": ""},
    ],
    "costas": [
        {"nome": "Postura da crianca", "como": "Ajoelhado, sente sobre os calcanhares e estique os bracos a frente no chao.", "tempo": "40s", "contra": "quadril"},
        {"nome": "Alongamento lombar em decubito lateral", "como": "Deitado de lado, puxe o joelho em direcao ao peito com as maos.", "tempo": "30s cada lado", "contra": "quadril"},
        {"nome": "Gato camelo suave", "como": "Em quadrupedia, alterne levemente a curvatura da coluna sem forcac", "tempo": "10 repeticoes lentas", "contra": ""},
    ],
    "ombros": [
        {"nome": "Alongamento de ombro cruzado", "como": "Leve um braco cruzado sobre o peito e segure com a outra mao por 30s.", "tempo": "30s cada lado", "contra": ""},
        {"nome": "Triceps na vertical", "como": "Dobre um braco por tras da cabeca e puxe o cotovelo com a mao oposta.", "tempo": "30s cada lado", "contra": ""},
        {"nome": "Alongamento de ombro com barbante", "como": "Segure uma toalha com as duas maos por tras do corpo e leve o braco de cima para tras com leveza.", "tempo": "30s cada lado", "contra": "ombro"},
    ],
    "biceps": [
        {"nome": "Esticamento de biceps na parede", "como": "Apoie a palma da mao na parede com o braco esticado e gire o corpo lentamente.", "tempo": "30s cada lado", "contra": "punho"},
        {"nome": "Alongamento de biceps em pe", "como": "Estique o braco para tras com a palma virada para tras e incline o tronco levemente.", "tempo": "30s cada lado", "contra": ""},
    ],
    "triceps": [
        {"nome": "Triceps esticado atras da cabeca", "como": "Dobre o braco por tras da cabeca e puxe o cotovelo com a mao oposta.", "tempo": "30s cada lado", "contra": ""},
        {"nome": "Alongamento de triceps na parede", "como": "Apoie a ponta do cotovelo na parede e deixe o tronco avancar suavemente.", "tempo": "30s cada lado", "contra": "ombro"},
    ],
    "quadriceps": [
        {"nome": "Quadriceps deitado com faixa", "como": "Deitado de lado ou de costas, puxe o calcanhar em direcao ao gluteo usando uma faixa.", "tempo": "30s cada perna", "contra": ""},
        {"nome": "Quadriceps em pe", "como": "Em pe, puxe o calcanhar contra o gluteo segurando em uma parede.", "tempo": "30s cada perna", "contra": "joelho,quadril"},
    ],
    "posterior": [
        {"nome": "Isquiotibiais deitado com faixa", "como": "Deitado de costas, estique uma perna na vertical com o auxilio de uma faixa.", "tempo": "30s cada perna", "contra": ""},
        {"nome": "Isquiotibiais sentado", "como": "Sentado, estique as pernas e alcance os pes com leveza, sem forcac a coluna.", "tempo": "30s", "contra": "hernia_discal,bico_papagaio,coluna"},
        {"nome": "Postura do ajoelhado meio split", "como": "Em meio ajoelhado, empurre levemente o quadril para frente com a perna da frente esticada.", "tempo": "30s cada lado", "contra": "joelho,quadril"},
    ],
    "gluteo": [
        {"nome": "Piriforme deitado", "como": "Deitado de costas, cruze o joelho de um lado sobre a coxa do outro e puxe em direcao ao peito.", "tempo": "30s cada lado", "contra": "quadril"},
        {"nome": "Alongamento de gluteo sentado", "como": "Sentado com as pernas cruzadas, incline o tronco para frente com a coluna reta.", "tempo": "30s", "contra": "quadril,hernia_discal,bico_papagaio"},
        {"nome": "Joelho ao peito em decubito", "como": "Deitado de costas, puxe um joelho ao peito com as maos.", "tempo": "30s cada lado", "contra": ""},
    ],
    "panturrilha": [
        {"nome": "Panturrilha na parede", "como": "Empurre o calcanhar no chao com uma perna atras e o corpo inclinado na parede.", "tempo": "30s cada perna", "contra": ""},
        {"nome": "Panturrilha no degrau", "como": "Fique em um degrau e deixe o calcanhar descer abaixo do nivel do pe.", "tempo": "30s", "contra": "tornozelo"},
    ],
    "core": [
        {"nome": "Cobra leve ( extensao suave )", "como": "Deitado de bruços, apoie levemente as maos e ergua o peito sem forcar a lombar.", "tempo": "20s", "contra": "hernia_discal,bico_papagaio"},
        {"nome": "Joelhos ao peito em decubito", "como": "Deitado de costas, traga os dois joelhos ao peito e balancar levemente.", "tempo": "30s", "contra": ""},
        {"nome": "Respiracao diafragmatica", "como": "Deitado de costas, inspire pelo nariz inflando a barriga e expire lentamente pela boca.", "tempo": "1 minuto", "contra": ""},
        {"nome": "Alongamento de coluna em decubito lateral", "como": "Deitado de lado, traga os joelhos ao peito mantendo os ombros alinhados.", "tempo": "30s cada lado", "contra": "quadril"},
    ],
    "cardio": [
        {"nome": "Caminhata leve como volta a calma", "como": "Caminhe por 3 a 5 minutos reduzindo o ritmo gradualmente.", "tempo": "3-5 min", "contra": ""},
        {"nome": "Solta de pernas em pe", "como": "Balance levemente cada perna e depois as duas, relaxando musculos.", "tempo": "30s cada", "contra": ""},
        {"nome": "Alongamento geral de membros", "como": "Estique bracos, pernas e tronco em posicoes confortaveis, sem rebotes.", "tempo": "30s cada regiao", "contra": ""},
    ],
    "mobilidade": [
        {"nome": "Rotacao de quadril em pe", "como": "Em pe com apoio, faca rotacoes lentas de quadril para cada lado.", "tempo": "10 cada lado", "contra": ""},
        {"nome": "Circulos de ombro", "como": "Circulos amplos e lentos para frente e para tras.", "tempo": "10 cada direcao", "contra": ""},
        {"nome": "Mobilidade de tornozelo", "como": "Apoie a frente do pe no chao e desloque o joelho a frente.", "tempo": "30s cada lado", "contra": "tornozelo"},
    ],
}

# Aquecimento geral (sempre) + ativações especificas por grupo
WARMUP_GENERAL = [
    "5 minutos de cardio leve (caminhada rapida, bicicleta ou marcha em lugar)",
    "Rotacoes de bracos para frente e para tras (10 cada direcao)",
    "Rotacoes de quadril em pe (10 cada lado)",
    "Mobilidade de tornozelo e joelho (10 cada lado)",
    "Elevacao de joelhos alternados (10 cada perna)",
    "2 series leves do primeiro exercicio do treino (metade das repeticoes)",
]

WARMUP_ACTIVATION = {
    "peito": ["Rotacoes de ombro (10 cada direcao)", "Flexao de braco leve no joelho (10 repeticoes)"],
    "costas": ["Gato camelo (10 repeticoes)", "Puxada leve na polia (15 repeticoes)"],
    "ombros": ["Circulos de ombro com halteres leves (12 cada direcao)", "Face pull leve (15 repeticoes)"],
    "biceps": ["Rosca leve com halteres (15 repeticoes)", "Estiramento de bracos (30s)"],
    "triceps": ["Extensao leve na polia (15 repeticoes)", "Rotacao de punho (10 cada lado)"],
    "quadriceps": ["Ponte de gluteo (12 repeticoes)", "Cadeira extensora leve (12 repeticoes)"],
    "posterior": ["Cadeira flexora leve (12 repeticoes)", "Pull through sem carga (12 repeticoes)"],
    "gluteo": ["Ponte de gluteo (12 repeticoes)", "Abducao leve de quadril (12 cada lado)"],
    "panturrilha": ["Elevacao de panturrilha leve (15 repeticoes)", "Marcha em lugar (1 min)"],
    "core": ["Respiracao diafragmatica (5 respiracoes)", "Dead bug (8 cada lado)"],
    "cardio": ["Caminhada progressiva (2 minutos)", "Mobilidade de quadril e tornozelo (1 min)"],
    "mobilidade": ["Caminhada leve (2 minutos)", "Circulos de bracos e quadril (1 min)"],
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
        "resumo": "Crescimento e desenvolvimento: priorize proteina de qualidade, calcio e ferro. Nunca elimine grupos alimentares.",
        "proteina_g_kg": 1.6,
        "gordura_pct": 30,
        "refeicoes": [
            ("Cafe da manha", "2 ovos mexidos + 1 fatia de pao integral + 1 fruta + 200ml de leite ou bebida de soja"),
            ("Lanche da manha", "1 iogurte natural + 1 banana + 1 col. de aveia"),
            ("Almoco", "1 porcao de arroz + 1 porcao de feijao + 120g de frango grelhado + salada a vontade + 1 fruta"),
            ("Lanche da tarde", "Sanduiche integral com queijo branco + fruta + agua"),
            ("Jantar", "1 porcao de massa integral + 100g de carne magra ou legumes + salada"),
            ("Pos-treino (30-60 min)", "1 fruta + 1 punhado de castanhas ou 1 copo de leite com biscoito integral"),
        ],
        "atencao": "Adolescentes: nao siga dietas restritivas. Priorize calcio (leite, iogurte, queijo) e ferro (carne vermelha, feijao).",
    },
    "20-29": {
        "resumo": "Pico de massa muscular: base consistente de proteina em todas as refeicoes e hidratacao de pelo menos 2 a 3 litros de agua por dia.",
        "proteina_g_kg": 1.8,
        "gordura_pct": 28,
        "refeicoes": [
            ("Cafe da manha", "3 ovos + pao integral + 1 fruta + cafe ou cha"),
            ("Lanche da manha", "Fruta + 1 punhado de oleaginosas (amendoim, castanha)"),
            ("Almoco", "Arroz + feijao + 150g de proteina (frango, peixe, carne) + legumes + salada"),
            ("Pre-treino (1h antes)", "Banana + aveia ou tapioca com queijo"),
            ("Jantar", "Proteina magra + batata ou arroz + vegetais verdes"),
            ("Pos-treino", "Whey ou leite + fruta, ou uma refeicao solida"),
        ],
        "atencao": "Mantenha horarios regulares e evite excesso de ultraprocessados e refrigerantes.",
    },
    "30-39": {
        "resumo": "Metabolismo comeca a desacelerar: controle porcoes, mantenha fibra em alta e distribua proteina no dia todo.",
        "proteina_g_kg": 1.7,
        "gordura_pct": 28,
        "refeicoes": [
            ("Cafe da manha", "Ovos mexidos com espinafre + fruta + cafe sem acucar"),
            ("Lanche da manha", "Iogurte natural + granola sem acucar"),
            ("Almoco", "100g de arroz + feijao + 150g de proteina grelhada + salada com azeite"),
            ("Lanche da tarde", "Fruta + oleaginosas ou pao de queijo integral"),
            ("Jantar", "Sopa de legumes com frango desfiado ou omelete + salada"),
            ("Pos-treino", "Proteina (whey ou alimento) + carboidrato leve"),
        ],
        "atencao": "Reduza acucar adicionado e alcool. Cuidado com sal: maximo de 5g por dia.",
    },
    "40-49": {
        "resumo": "Foco em saude cardiovascular e manutencao de massa muscular: mais fibras, peixes gordurosos e legumes coloridos.",
        "proteina_g_kg": 1.7,
        "gordura_pct": 30,
        "refeicoes": [
            ("Cafe da manha", "Papinha de aveia com frutas vermelhas + 1 ovo + cafe"),
            ("Lanche da manha", "Fruta + 1 col. de sementes (chia, linhaça)"),
            ("Almoco", "Arroz integral opcional + feijao + 150g de proteina + salada variada"),
            ("Lanche da tarde", "Castanhas (30g) + fruta ou iogurte"),
            ("Jantar", "Proteina leve (peixe, frango) + legumes + sopa"),
            ("Pos-treino", "Lebite, iogurte ou whey + fruta"),
        ],
        "atencao": "Atencao ao colesterol e pressao: prefira peixe 2 a 3x por semana, azeite e pouca gordura saturada.",
    },
    "50-59": {
        "resumo": "Prevencao de perda de massa muscular e ossos: proteina suficiente, calcio, vitamina D e hidratacao constante.",
        "proteina_g_kg": 1.8,
        "gordura_pct": 30,
        "refeicoes": [
            ("Cafe da manha", "Ovos ou queijo branco + fruta + pao integral + cafe"),
            ("Lanche da manha", "Iogurte com aveia ou fruta madura"),
            ("Almoco", "Proteina de qualidade (150g) + arroz + feijao + legumes cozidos"),
            ("Lanche da tarde", "Fruta + oleaginosas ou leite com biscoito integral"),
            ("Jantar", "Sopa nutritiva com legumes + proteina leve + salada"),
            ("Pos-treino", "Leite, queijo, iogurte ou whey para completar proteina do dia"),
        ],
        "atencao": "Priorize calcio (leite, queijo, sardinha) e vitamina D. Mastigue bem e hidrate-se mesmo sem sede.",
    },
    "60+": {
        "resumo": "Manutencao de funcionalidade e forca: proteina distribuida, alimentos faceis de mastigar e boa hidratacao.",
        "proteina_g_kg": 1.8,
        "gordura_pct": 32,
        "refeicoes": [
            ("Cafe da manha", "Ovos cozidos + pao integral + fruta amassada + cafe"),
            ("Lanche da manha", "Iogurte ou leite + biscoito integral"),
            ("Almoco", "Carne ou frango macio + arroz + feijao + legumes bem cozidos"),
            ("Lanche da tarde", "Fruta sem casca dura + queijo branco ou coalhada"),
            ("Jantar", "Sopa crematica de legumes com frango desfiado ou peixe"),
            ("Pos-treino / ceia", "Leite com colageno ou iogurte, opcionalmente whey"),
        ],
        "atencao": "60+ : aumente a densidade nutricional (calorias em pouco volume), B12 e agua. Prefira alimentos macios se houver dificuldade de mastigacao.",
    },
}

# ------------------------------------------------------------------
# SUPLEMENTOS
# ------------------------------------------------------------------
# Regra: base por idade + extras por foco + extras por limitacao
SUPPLEMENTS_BASE = {
    "<20": [
        ("Whey protein (ou alimento)", "1 dose (20-25g) apos o treino, se nao atingir a proteina da dieta", "Somente se a dieta for insuficiente; nao substitui refeicoes."),
        ("Creatina monoidratada", "3g ao dia, todo dia (inclusive nos dias de descanso)", "Seguro em adolescentes treinados; prefira orientacao de nutricionista."),
        ("Calcio + Vitamina D", "500-600mg de calcio + 1000 UI de D3 ao dia", "Importante no pico de massa ossea."),
    ],
    "20-29": [
        ("Whey protein", "1-2 doses (25-50g) por dia conforme a necessidade", "Conveniencia para completar a proteina diaria."),
        ("Creatina monoidratada", "3-5g ao dia", "Melhora forca e desempenho; beba bastante agua."),
        ("Multivitaminico", "1 dose pela manha", "Cobertura basal, nao substitui alimentacao."),
    ],
    "30-39": [
        ("Whey protein", "1-2 doses (25-50g) por dia", "Auxilia na recuperacao muscular."),
        ("Creatina monoidratada", "3-5g ao dia", "Beneficia forca, massa magra e funcao cerebral."),
        ("Omga 3 (EPA/DHA)", "1-2g ao dia", "Saude cardiovascular e anti-inflamatorio."),
    ],
    "40-49": [
        ("Creatina monoidratada", "3-5g ao dia", "Apoia massa muscular e funcao cognitiva."),
        ("Omga 3 (EPA/DHA)", "1-2g ao dia", "Com apoio a saude cardiovascular."),
        ("Vitamina D3", "1000-2000 UI ao dia", "Principalmente em exposicao solar baixa."),
        ("Whey protein", "1 dose (25-30g) ao dia", "Se a proteina alimentar estiver baixa."),
    ],
    "50-59": [
        ("Creatina monoidratada", "3-5g ao dia", "Ajud na prevencao da perda muscular (sarcopenia)."),
        ("Calcio + Vitamina D3", "500-600mg + 1000-2000 UI ao dia", "Saude ossea."),
        ("Omga 3 (EPA/DHA)", "1-2g ao dia", "Coraacao e articulacoes."),
        ("Whey protein", "1-2 doses (25-50g)", "Facilita atingir a meta de proteina."),
        ("Colageno hidrolisado", "10-15g ao dia", "Articulacoes e tendoes; melhor com vitamina C."),
    ],
    "60+": [
        ("Whey protein ou proteina de alta qualidade", "1-2 doses (25-50g) por dia", "Combate a sarcopenia; consulte nutricionista."),
        ("Vitamina B12", "1000 mcg 2-3x por semana (se orientado)", "Absorcao reduzida com a idade."),
        ("Calcio + Vitamina D3", "500-600mg + 1000-2000 UI ao dia", "Prevencao de osteoporose."),
        ("Omga 3 (EPA/DHA)", "1-2g ao dia", "Cognicao e cardiovascular."),
        ("Creatina monoidratada", "3-5g ao dia", "Forca e funcionalidade; avalie com medico se houver problemas renais."),
    ],
}

SUPPLEMENTS_FOCO = {
    "perda_peso": [("Cafeina pre-treino", "100-200mg 30-60 min antes (cafe forte serve)", "Nao consumir apos as 16h nem se houver pressao alta."),
                   ("Proteina (whey)", "1-2 doses ao dia", "Aumenta a saciedade e preserva massa magra no deficit.")],
    "definicao": [("Whey protein", "1-2 doses (25-50g)", "Mantem massa magra na definicao."),
                  ("Omga 3", "1-2g ao dia", "Saude geral durante o ajuste calorico.")],
    "hipertrofia": [("Whey protein", "1-2 doses (25-50g)", "Complementa a proteina para ganho de massa."),
                    ("Creatina monoidratada", "3-5g ao dia", "Suporte a volume e intensidade."),
                    ("HMB (opcional)", "3g ao dia", "Apenas em casos de treino muito intenso ou catabolismo; validado de forma limitada.")],
    "fortalecimento": [("Creatina monoidratada", "3-5g ao dia", "Melhora forca e potencia."),
                       ("Whey protein", "1-2 doses", "Recuperacao muscular.")],
    "resistencia": [("Eletrólitos", "1 porcao em dias de treino longo (>60 min)", "Reposicao de sais minerais."),
                    ("Cafeina", "100-200mg antes do treino", "Melhora o desempenho; nao abusar."),
                    ("Omga 3", "1-2g ao dia", "Recuperacao geral.")],
    "bracos": [("Whey protein", "1-2 doses (25-50g)", "Suporte a hipertrofia de membros superiores."),
               ("Creatina monoidratada", "3-5g ao dia", "Volume e forca.")],
    "peito": [("Whey protein", "1-2 doses", "Suporte a hipertrofia."),
              ("Creatina monoidratada", "3-5g ao dia", "Desempenho em supino e exercicios de peito.")],
    "costas": [("Whey protein", "1-2 doses", "Suporte a hipertrofia."),
               ("Creatina monoidratada", "3-5g ao dia", "Desempenho em puxadas e remadas.")],
    "ombros": [("Whey protein", "1-2 doses", "Suporte a hipertrofia."),
               ("Colageno hidrolisado", "10g ao dia", "Apoio a tendoes do ombro (com vitamina C).")],
    "pernas": [("Creatina monoidratada", "3-5g ao dia", "Fortalece series pesadas de pernas."),
               ("Whey protein", "1-2 doses", "Recuperacao de grande massa muscular.")],
    "gluteos": [("Creatina monoidratada", "3-5g ao dia", "Suporte a progressao de carga."),
                ("Whey protein", "1-2 doses", "Hipertrofia de gluteos.")],
    "core": [("Whey protein", "1-2 doses", "Se a proteina estiver baixa.")],
    "mobilidade": [("Colageno hidrolisado", "10g ao dia", "Articulacoes e tecido conjuntivo."),
                   ("Omga 3", "1-2g ao dia", "Efeito anti-inflamatorio.")],
    "postura": [("Magnesio", "200-400mg a noite", "Relaxamento muscular; consulte se usar medicamentos."),
                ("Omga 3", "1-2g ao dia", "Saude de articulacoes e musculos.")],
    "funcional": [("Whey protein", "1-2 doses", "Recuperacao geral."),
                  ("Creatina monoidratada", "3-5g ao dia", "Versatilidade de desempenho.")],
}

SUPPLEMENTS_LIMIT = {
    "hernia_discal": [("Colageno hidrolisado", "10-15g ao dia com vitamina C", "Suporte a disco e tecido conjuntivo; nao substitui tratamento."),
                      ("Vitamina D3", "1000-2000 UI ao dia", "Saude ossea e muscular."),
                      ("Omga 3", "1-2g ao dia", "Efeito anti-inflamatorio.")],
    "bico_papagaio": [("Colageno hidrolisado", "10-15g ao dia com vitamina C", "Suporte a tecido conjuntivo da coluna."),
                      ("Vitamina D3", "1000-2000 UI ao dia", "Saude ossea."),
                      ("Omga 3", "1-2g ao dia", "Anti-inflamatorio.")],
    "hernia_abdominal": [("Colageno hidrolisado", "10-15g ao dia", "Suporte ao tecido conjuntivo."),
                         ("Vitamina D3", "1000-2000 UI", "Saude geral e muscular.")],
    "joelho": [("Colageno hidrolisado", "10-15g ao dia com vitamina C", "Cartilagem e tendoes."),
               ("Omga 3", "1-2g ao dia", "Anti-inflamatorio articular."),
               ("Vitamina D3", "1000-2000 UI", "Saude ossea.")],
    "coluna": [("Colageno hidrolisado", "10-15g ao dia", "Tecido conjuntivo da coluna."),
               ("Magnesio", "200-400mg a noite", "Relaxamento muscular.")],
    "ombro": [("Colageno hidrolisado", "10-15g ao dia", "Tendoes do manguitor rotador."),
              ("Omga 3", "1-2g ao dia", "Anti-inflamatorio.")],
    "punho": [("Colageno hidrolisado", "10-15g ao dia", "Tendoes e ligamentos."),
              ("Omga 3", "1-2g ao dia", "Anti-inflamatorio.")],
    "cardiaco": [("Omga 3", "1-2g ao dia", "Saude cardiovascular; somente com avaliacao medica."),
                 ("Coenzima Q10", "100-200mg ao dia", "Frequente em usuarios de estatinas; avalie com medico.")],
    "pressao": [("Magnesio", "200-400mg ao dia", "Pode ajudar na pressao; avalie com medico."),
                ("Omga 3", "1-2g ao dia", "Saude cardiovascular.")],
    "diabetes": [("Vitamina D3", "1000-2000 UI", "Metabolismo e imunidade."),
                 ("Cromo", "200-400 mcg ao dia", "Apoio ao metabolismo da glicose; avalie com medico."),
                 ("Omga 3", "1-2g ao dia", "Saude cardiovascular.")],
    "gravidez": [("Acido folico", "400-600 mcg ao dia", "Essencial na gestacao; apenas com orientacao medica."),
                 ("Ferro", "Conforme exame", "Somente se houver anemia e orientacao do pre-natal."),
                 ("DHA/Omga 3", "200-300mg ao dia", "Desenvolvimento fetal; somente com orientacao medica.")],
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
