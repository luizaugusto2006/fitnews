# FITNEWS — Academia de Musculação (site completo)

Site de academia com **gerador automático de plano de treino**, bloqueio de exercícios
perigosos por limitação, aquecimento/alongamento, alimentação por idade e suplementos
sugeridos.

**Em produção:** https://fitnews.pythonanywhere.com

## O que o site faz

1. **Criar plano de treino** — nome, sexo, data de nascimento (idade), peso, altura (IMC
   automático), nível de treino, nível de atividade, dias/semana, horário, local
   (academia/casa), **limitações** (hérnia de disco, bico de papagaio, hérnia abdominal,
   coluna, joelho, ombro, punho, quadril, tornozelo, cardíaco, pressão, diabetes, asma,
   gestante, cirurgia recente) e **focos múltiplos** (braços, peito, costas, ombros,
   pernas, glúteos, core, fortalecimento, perda de peso, resistência, hipertrofia,
   definição, mobilidade, postura, funcional).
2. **Banco de exercícios com contraindicações** — cada exercício tem a lista de
   limitações para as quais ele é proibido. Se você marcar hérnia de disco/bico de
   papagaio, exercícios de carga axial, flexão e rotação da coluna são **excluídos**
   (agachamento livre, terra, remada curvada, bom dia, abdominais clássicos, burpees...)
   e o plano é montado só com opções seguras.
3. **Plano gerado automaticamente** — dias A/B/C..., séries, repetições, descanso e
   ordem, variando por objetivo (perda de peso = 3x15-20/30s; hipertrofia = 4x8-12/60-90s;
   força = 4x6-8/90-120s...).
4. **Editar o foco** — ao trocar objetivos ou limitações, o plano é recalculado
   mantendo o que não mudou e substituindo apenas o que mudou.
5. **Aquecimento + alongamento pré e pós** — geral, ativação específica por dia e
   alongamentos pós-treino por grupo muscular (também filtrados pelas limitações).
6. **Alimentação por idade** — faixas <20, 20-29, 30-39, 40-49, 50-59, 60+ com calorias
   (Mifflin-St Jeor quando há peso/altura), proteína/carboidrato/gordura, 5 refeições e
   ajuste ao objetivo (déficit/superávit).
7. **Suplementos** — combinando base por idade + extras do foco + extras da limitação,
   com dosagem indicativa e avisos.
8. **Meus planos** (`/planos`) — lista **apenas os planos da sua conta** (exige login).
9. **Painel admin** — CRUD simples da base de exercícios (adicionar/editar/excluir,
   marcar contraindicações) e dos planos gerados.
10. **Área do Personal Trainer** (`/personal`):
    - Cadastro (nome, e-mail, senha) e login com sessão própria;
    - Gera um **código de vínculo** `FIT-XXXXXX` (com botão "Copiar");
    - **Meus clientes** com **busca por nome** — clique no nome e abra o plano/séries;
    - **Filtros por foco e por limitação** (ex.: só alunos com hérnia);
    - **Novo plano para cliente** (já nasce vinculado);
    - O aluno também pode informar o código no formulário do plano (vínculo automático);
    - **Planos aguardando vínculo** — o personal assume planos criados sem código;
    - **Anotações do personal** por plano (salvas e visíveis na página do plano);
    - Desvincular plano; estatísticas de clientes/planos.
11. **Compartilhar o plano**: botão **WhatsApp**, **QR Code gerado localmente**
    (sem serviço externo) e **copiar link**.
12. **Timer de descanso**: botão ⏱ ao lado do descanso (pega o tempo do texto,
    ex.: `60s`, `90-120s`, `1 min`), com barra flutuante, +15s, pular e alerta sonoro.
13. **Trocar exercício**: botão "↻ trocar" em cada exercício abre alternativas do
    **mesmo grupo já filtradas pelas limitações** (validadas no servidor).
14. **Anotar cargas**: campo ao lado de cada exercício + "Salvar cargas" por dia
    (persiste no plano e aparece no resumo impresso).
15. **Resumo 1 página** (`/plano/<token>/resumo`): ficha enxuta para imprimir/salvar PDF.
16. **Política de Privacidade (LGPD)** em `/privacidade` + aceite obrigatório no formulário.
17. **Backup CSV** no admin: `Baixar planos` e `Baixar exercícios` (UTF-8 com BOM, abre no Excel).
18. **Padrão celular (mobile-first):** menu hambúrguer, tabelas de treino em cartões,
    abas com rolagem horizontal, botões grandes (alvo de toque ≥44px), inputs em 16px
    (sem zoom automático no iOS), meta tags de app (theme-color, standalone) e
    layout de uma coluna abaixo de 768px.
19. **Contas de usuário e link secreto**: cada plano nasce com um **link secreto**
    `/plano/<token>` (sem IDs sequenciais — quem não tem o link não abre). O criador
    pode **salvar o plano em uma conta** (`/conta`: e-mail + senha) para encontrá-lo
    depois em Meus planos; sem conta, basta guardar o link. Recuperação de senha por
    **código `REC-XXXXXX`** exibido no cadastro (o site não envia e-mails). O código
    do personal (`FIT-XXXXXX`) continua **opcional**.

## Rodar localmente

```bash
pip install -r requirements.txt
python app.py
# http://127.0.0.1:5000
```

O banco `fitnews.db` (SQLite) é criado e populado automaticamente na primeira execução.

Teste automatizado (smoke test):

```bash
python test_site.py
```

## Acesso admin

- URL: `/admin` — usuário e senha definidos em `app.py` (`ADMIN_USER` e
  `ADMIN_PASSWORD`), podendo ser sobrescritos pelas variáveis de ambiente de
  mesmo nome (e defina uma `SECRET_KEY` forte em produção).

## Área do Personal

- URL: `/personal` — cadastro livre (e-mail + senha de 6+ caracteres).
- Após o cadastro, a página mostra o **código FIT-XXXXXX** do personal.
- O aluno informa esse código no formulário "Criar plano" (campo opcional)
  ou o personal usa "Novo plano para cliente" / "Vincular" no painel.
- Busca por nome em "Meus clientes"; clique no nome para ver séries e
  anotações; botão "Ver séries" abre o plano completo.

## Publicar no PythonAnywhere

1. Faça o **push** deste repositório para o GitHub
   (`https://github.com/luizaugusto2006/fitnews.git`).
2. No PythonAnywhere: **Dashboard → Files → Clone a Git repository** →
   cole a URL do repositório (ou suba os arquivos pelo gerenciador de arquivos).
3. **Bash console** no diretório do projeto:
   ```bash
   mkvirtualenv fitnews --python=3.11
   pip install -r requirements.txt
   ```
4. **Web → Add a new web app → Manual configuration** (não usar Django/Flask automático).
5. No arquivo **WSGI configuration file**, troque o conteúdo por:
   ```python
   import sys
   sys.path.insert(0, '/home/SEU_USUARIO/fitnews')

   from fitnews_wsgi import app  # noqa
   ```
   Crie o arquivo `fitnews_wsgi.py` na raiz do projeto:
   ```python
   import os, sys
   sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
   from app import app
   ```
   (Alternativa: aponte o WSGI direto para o `wsgi.py` da raiz, ajustando o caminho.)
6. **Virtualenv:** escolha o ambiente `fitnews` criado no passo 3.
7. **Reload** e acesse `https://SEU_USUARIO.pythonanywhere.com`
   (mapeie o domínio `fitnews.pythonanywhere.com` em **Domains**, se já estiver
   liberado para a sua conta).
8. Segurança: defina `ADMIN_PASSWORD` e `SECRET_KEY` em
   **Web → Environment variables** (ou no arquivo `.env` carregado pelo seu WSGI).

## Estrutura

```
fitnews/
├── app.py               # rotas Flask (público + admin)
├── gerador.py           # gerador do plano (treino, alongamento, nutrição, suplementos)
├── database.py          # esquema SQLite + seed
├── data_exercises.py    # base de exercícios + contraindicações
├── data_content.py      # alongamentos, dietas por idade, suplementos
├── wsgi.py              # entrada WSGI
├── test_site.py         # smoke test
├── requirements.txt
├── templates/           # páginas HTML
└── static/              # css e js
```

## Aviso legal

Conteúdo educativo gerado automaticamente. **Não substitui** avaliação médica,
nutricional ou acompanhamento de um educador físico.
