# -*- coding: utf-8 -*-
# Base de exercicios do FitNews
# Campos: nome, grupo, equipamento, nivel, contraindicado_para (codigos separados por virgula)
# Codigos de limitacao:
# hernia_discal, bico_papagaio, hernia_abdominal, coluna, joelho, ombro, punho,
# quadril, tornozelo, cervical, cardiaco, pressao, gravidez

EXERCISES = [
    # ---------------- PEITO ----------------
    ("Supino reto com halteres", "peito", "halteres", "iniciante", ""),
    ("Supino reto com barra", "peito", "barra", "intermediario", ""),
    ("Supino inclinado com halteres", "peito", "halteres", "intermediario", "ombro"),
    ("Supino declinado com halteres", "peito", "halteres", "intermediario", "ombro,cervical"),
    ("Supino no Smith", "peito", "maquina", "iniciante", ""),
    ("Flexao de braco", "peito", "peso_corporal", "iniciante", "punho,ombro"),
    ("Flexao diamante", "peito", "peso_corporal", "intermediario", "punho,ombro"),
    ("Flexao declinada ( pesos elevados )", "peito", "peso_corporal", "intermediario", "punho,ombro,cervical"),
    ("Crucifixo com halteres", "peito", "halteres", "iniciante", "ombro"),
    ("Crucifixo no cabo", "peito", "cabo", "iniciante", ""),
    ("Paralelas ( dips )", "peito", "peso_corporal", "avancado", "ombro,punho"),
    ("Supino com halteres no banco reto", "peito", "halteres", "iniciante", ""),

    # ---------------- COSTAS ----------------
    ("Puxada frontal ( pulldown )", "costas", "maquina", "iniciante", ""),
    ("Puxada frontal pegada inversa", "costas", "maquina", "intermediario", "punho"),
    ("Barra fixa", "costas", "peso_corporal", "avancado", ""),
    ("Remada sentada no cabo", "costas", "cabo", "iniciante", ""),
    ("Remada em pe com cabo", "costas", "cabo", "iniciante", ""),
    ("Remada com halteres em apoio", "costas", "halteres", "iniciante", "hernia_discal,bico_papagaio,coluna"),
    ("Remada curvada com barra", "costas", "barra", "intermediario", "hernia_discal,bico_papagaio,coluna"),
    ("Levantamento terra", "costas", "barra", "avancado", "hernia_discal,bico_papagaio,coluna"),
    ("Terra romeno", "costas", "barra", "avancado", "hernia_discal,bico_papagaio,coluna"),
    ("Bom dia ( good morning )", "costas", "barra", "avancado", "hernia_discal,bico_papagaio,coluna"),
    ("Hiperextensao no banco 45 graus", "costas", "peso_corporal", "intermediario", "hernia_discal,bico_papagaio,coluna"),
    ("Extensao lombar isometrica ( prancha dorsal )", "costas", "peso_corporal", "iniciante", "hernia_abdominal"),
    ("Remada no Smith curvado", "costas", "maquina", "intermediario", "hernia_discal,bico_papagaio,coluna"),

    # ---------------- OMBROS ----------------
    ("Desenvolvimento com halteres sentado", "ombros", "halteres", "intermediario", "ombro"),
    ("Desenvolvimento com barra", "ombros", "barra", "intermediario", "ombro,coluna"),
    ("Supino militar", "ombros", "barra", "avancado", "ombro"),
    ("Elevacao lateral com halteres", "ombros", "halteres", "iniciante", "ombro"),
    ("Elevacao frontal com halteres", "ombros", "halteres", "iniciante", "ombro"),
    ("Face pull no cabo", "ombros", "cabo", "iniciante", ""),
    ("Encolhimento com halteres ( trapezio )", "ombros", "halteres", "iniciante", "cervical"),
    ("Elevacao frontal na polia", "ombros", "cabo", "iniciante", "ombro"),
    ("Puxada para o queixo", "ombros", "barra", "intermediario", "ombro"),

    # ---------------- BICEPS ----------------
    ("Rosca direta em pe com halteres", "biceps", "halteres", "iniciante", ""),
    ("Rosca com barra reta", "biceps", "barra", "iniciante", "punho"),
    ("Rosca martelo", "biceps", "halteres", "iniciante", ""),
    ("Rosca scott", "biceps", "maquina", "intermediario", ""),
    ("Rosca concentrada", "biceps", "halteres", "iniciante", ""),
    ("Rosca no cabo", "biceps", "cabo", "iniciante", ""),
    ("Rosca inclinada com halteres", "biceps", "halteres", "intermediario", ""),

    # ---------------- TRICEPS ----------------
    ("Triceps na polia ( corda )", "triceps", "cabo", "iniciante", ""),
    ("Triceps coice com halteres", "triceps", "halteres", "iniciante", ""),
    ("Triceps testa com barra", "triceps", "barra", "intermediario", "ombro,punho"),
    ("Triceps frances com halteres", "triceps", "halteres", "intermediario", "ombro"),
    ("Extensao de triceps no cabo", "triceps", "cabo", "iniciante", ""),
    ("Mergulho inverso no banco", "triceps", "peso_corporal", "intermediario", "punho"),

    # ---------------- QUADRICEPS ----------------
    ("Agachamento livre com barra", "quadriceps", "barra", "intermediario", "hernia_discal,bico_papagaio,coluna,joelho,quadril"),
    ("Agachamento no Smith", "quadriceps", "maquina", "iniciante", "joelho"),
    ("Agachamento goblet ( halteres )", "quadriceps", "halteres", "iniciante", ""),
    ("Agachamento sumo", "quadriceps", "halteres", "intermediario", "hernia_discal,bico_papagaio,coluna,joelho,quadril"),
    ("Leg press 45 graus", "quadriceps", "maquina", "iniciante", ""),
    ("Cadeira extensora", "quadriceps", "maquina", "iniciante", ""),
    ("Agachamento com salto", "quadriceps", "peso_corporal", "avancado", "joelho,coluna,hernia_discal,bico_papagaio,cardiaco,pressao"),
    ("Passada ( afundo ) com halteres", "quadriceps", "halteres", "intermediario", "joelho,hernia_discal,bico_papagaio,coluna"),
    ("Agachamento bulgaro", "quadriceps", "halteres", "avancado", "joelho,coluna,hernia_discal,bico_papagaio"),
    ("Cadeira adutora", "quadriceps", "maquina", "iniciante", ""),
    ("Cadeira abdutora", "quadriceps", "maquina", "iniciante", ""),

    # ---------------- POSTERIOR ----------------
    ("Cadeira flexora", "posterior", "maquina", "iniciante", ""),
    ("Mesa flexora", "posterior", "maquina", "iniciante", ""),
    ("Stiff com halteres", "posterior", "halteres", "intermediario", "hernia_discal,bico_papagaio,coluna"),
    ("Pull through no cabo", "posterior", "cabo", "iniciante", ""),
    ("Nordic curl", "posterior", "peso_corporal", "avancado", "joelho"),
    ("Levantamento terra peso morto", "posterior", "barra", "avancado", "hernia_discal,bico_papagaio,coluna"),

    # ---------------- GLUTEOS ----------------
    ("Hip thrust com barra", "gluteo", "barra", "intermediario", ""),
    ("Ponte de gluteo", "gluteo", "peso_corporal", "iniciante", ""),
    ("Abducao de quadril no cabo", "gluteo", "cabo", "iniciante", ""),
    ("Chute de gluteo em quatro apoios", "gluteo", "peso_corporal", "iniciante", ""),
    ("Donkey kick ( patada em quadrupedia )", "gluteo", "peso_corporal", "iniciante", ""),
    ("Elevacao lateral de quadril deitado", "gluteo", "peso_corporal", "iniciante", ""),
    ("Hip thrust no Smith", "gluteo", "maquina", "iniciante", ""),

    # ---------------- PANTURRILHA ----------------
    ("Elevacao de panturrilha em pe", "panturrilha", "maquina", "iniciante", ""),
    ("Elevacao de panturrilha sentado", "panturrilha", "maquina", "iniciante", ""),
    ("Elevacao de panturrilha no leg press", "panturrilha", "maquina", "iniciante", ""),
    ("Elevacao de panturrilha em pe com halteres", "panturrilha", "halteres", "iniciante", "tornozelo"),

    # ---------------- CORE ----------------
    ("Prancha isometrica", "core", "peso_corporal", "iniciante", "hernia_abdominal"),
    ("Prancha lateral", "core", "peso_corporal", "intermediario", "hernia_abdominal,ombro"),
    ("Abdominal tradicional ( crunch )", "core", "peso_corporal", "iniciante", "hernia_discal,bico_papagaio,hernia_abdominal,coluna"),
    ("Abdominal remador", "core", "peso_corporal", "intermediario", "hernia_discal,bico_papagaio,hernia_abdominal,coluna"),
    ("Elevacao de pernas deitado", "core", "peso_corporal", "intermediario", "hernia_discal,bico_papagaio,hernia_abdominal,coluna"),
    ("Abdominal bicicleta", "core", "peso_corporal", "iniciante", "hernia_discal,bico_papagaio,hernia_abdominal,coluna"),
    ("Abdominal em V ( jackknife )", "core", "peso_corporal", "avancado", "hernia_discal,bico_papagaio,hernia_abdominal,coluna"),
    ("Mountain climber", "core", "peso_corporal", "intermediario", "hernia_discal,bico_papagaio,hernia_abdominal,coluna,ombro"),
    ("Russian twist", "core", "peso_corporal", "intermediario", "hernia_discal,bico_papagaio,hernia_abdominal,coluna"),
    ("Rotacao com cabo ( woodchop )", "core", "cabo", "intermediario", "hernia_discal,bico_papagaio,coluna"),
    ("Toque de calcanhar deitado", "core", "peso_corporal", "iniciante", "hernia_discal,bico_papagaio,hernia_abdominal,coluna"),
    ("Pallof press no cabo", "core", "cabo", "intermediario", ""),
    ("Dead bug ( inseto morto )", "core", "peso_corporal", "iniciante", ""),
    ("Bird dog ( cachorro passaro )", "core", "peso_corporal", "iniciante", ""),
    ("Respiracao diafragmatica em decubito", "core", "peso_corporal", "iniciante", ""),
    ("Abdominal na maquina", "core", "maquina", "iniciante", "hernia_discal,bico_papagaio,hernia_abdominal,coluna"),
    ("Prancha com toque de ombro", "core", "peso_corporal", "intermediario", "hernia_abdominal,ombro"),

    # ---------------- CARDIO ----------------
    ("Caminhada rapida na esteira", "cardio", "cardio", "iniciante", ""),
    ("Corrida na esteira", "cardio", "cardio", "intermediario", "joelho,tornozelo,gravidez"),
    ("Bicicleta ergometrica", "cardio", "cardio", "iniciante", ""),
    ("Eliptico", "cardio", "cardio", "iniciante", "joelho"),
    ("Remo ergometrico", "cardio", "cardio", "intermediario", "hernia_discal,bico_papagaio,coluna"),
    ("Corda navalha", "cardio", "cardio", "intermediario", "ombro,punho,cardiaco,pressao,hernia_discal,bico_papagaio"),
    ("Polichinelo", "cardio", "cardio", "iniciante", "joelho,tornozelo,gravidez"),
    ("Marcha em lugar", "cardio", "cardio", "iniciante", ""),
    ("Burpee", "cardio", "cardio", "avancado", "hernia_discal,bico_papagaio,hernia_abdominal,joelho,coluna,cardiaco,pressao,ombro,punho"),
    ("Treino intervalado de alta intensidade ( HIIT )", "cardio", "cardio", "avancado", "joelho,cardiaco,pressao,gravidez,coluna,hernia_discal,bico_papagaio"),

    # ---------------- MOBILIDADE ----------------
    ("Rotacao de quadril em pe", "mobilidade", "peso_corporal", "iniciante", ""),
    ("Gato camelo ( cat cow )", "mobilidade", "peso_corporal", "iniciante", ""),
    ("Circulos de ombro", "mobilidade", "peso_corporal", "iniciante", ""),
    ("Postura da crianca ( child pose )", "mobilidade", "peso_corporal", "iniciante", ""),
    ("Alongamento de quadriceps em pe", "mobilidade", "peso_corporal", "iniciante", "joelho,quadril"),
    ("Alongamento de peitoral na porta", "mobilidade", "peso_corporal", "iniciante", "ombro"),
    ("Alongamento de isquiotibiais em pe", "mobilidade", "peso_corporal", "iniciante", "hernia_discal,bico_papagaio,coluna"),
    ("Flexao de tronco em pe ( toque de pes )", "mobilidade", "peso_corporal", "iniciante", "hernia_discal,bico_papagaio,coluna"),
    ("Torcao de coluna sentada", "mobilidade", "peso_corporal", "iniciante", "hernia_discal,bico_papagaio,coluna"),
    ("Rotação de tronco em pé", "mobilidade", "peso_corporal", "iniciante", "hernia_discal,bico_papagaio,coluna"),
    ("Mobilidade de tornozelo ( paredao )", "mobilidade", "peso_corporal", "iniciante", ""),
    ("Alongamento de gluteo sentado", "mobilidade", "peso_corporal", "iniciante", "quadril"),
]
