# -*- coding: utf-8 -*-
"""Assistente de dúvidas por IA do FitNews.

Provedor padrao: Google Gemini (tier gratuito) — troque com IA_PROVIDER.
A chave NUNCA vai para o repositorio: configure por variavel de ambiente
(IA_API_KEY, IA_PROVIDER, IA_MODEL) ou no arquivo local ia_secreto.py
(mesmas variaveis, ignorado pelo git).

Provedores suportados:
  gemini     https://ai.google.dev          (gratis, padrao)
  openrouter https://openrouter.ai          (modelos :free)
  groq       https://api.groq.com           (tier gratuito)
"""
import json
import os
import urllib.error
import urllib.request

TIMEOUT = 30

MODELOS_PADRAO = {
    "gemini": "gemini-2.0-flash",
    "openrouter": "meta-llama/llama-3.3-70b-instruct:free",
    "groq": "llama-3.3-70b-versatile",
}

ENDPOINTS = {
    "openrouter": "https://openrouter.ai/api/v1/chat/completions",
    "groq": "https://api.groq.com/openai/v1/chat/completions",
}


class IAErro(Exception):
    """Falha ao consultar o provedor (mensagem ja amigavel, sem segredos)."""


def _config():
    provedor = os.environ.get("IA_PROVIDER", "gemini").strip().lower()
    chave = os.environ.get("IA_API_KEY", "").strip()
    modelo = os.environ.get("IA_MODEL", "").strip()
    if not chave:
        try:
            import ia_secreto  # arquivo local, fora do git
            provedor = str(getattr(ia_secreto, "IA_PROVIDER", provedor)).strip().lower()
            chave = str(getattr(ia_secreto, "IA_API_KEY", "")).strip()
            modelo = modelo or str(getattr(ia_secreto, "IA_MODEL", "")).strip()
        except Exception:
            pass
    if provedor not in MODELOS_PADRAO:
        provedor = "gemini"
    if not modelo:
        modelo = MODELOS_PADRAO[provedor]
    return provedor, chave, modelo


def configurado():
    """True quando ha chave disponivel para consultar a IA."""
    _, chave, _ = _config()
    return bool(chave)


def _post_json(url, payload, headers):
    corpo = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url, data=corpo, method="POST",
        headers={"Content-Type": "application/json", "Accept": "application/json",
                 **headers})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        # a chave vai no cabecalho (nao na URL): seguro para log/erro
        raise IAErro("o provedor recusou a chamada (HTTP %s)" % exc.code) from None
    except IAErro:
        raise
    except Exception as exc:
        raise IAErro("falha de rede com o provedor (%s)"
                     % exc.__class__.__name__) from None


def perguntar(sistema, contexto, pergunta):
    """Devolve a resposta da IA. Levanta IAErro em qualquer falha."""
    provedor, chave, modelo = _config()
    if not chave:
        raise IAErro("IA nao configurada (falta IA_API_KEY)")

    entrada = contexto.strip() + "\n\nPergunta do aluno: " + pergunta.strip()

    if provedor == "gemini":
        url = ("https://generativelanguage.googleapis.com/v1beta/models/"
               + modelo + ":generateContent")
        dados = _post_json(url, {
            "system_instruction": {"parts": [{"text": sistema}]},
            "contents": [{"role": "user", "parts": [{"text": entrada}]}],
            "generationConfig": {"maxOutputTokens": 800, "temperature": 0.4},
        }, {"x-goog-api-key": chave})
        try:
            partes = dados["candidates"][0]["content"]["parts"]
            texto = "".join(p.get("text", "") for p in partes).strip()
        except (KeyError, IndexError, TypeError):
            texto = ""
        if not texto:
            raise IAErro("resposta vazia ou inesperada do Gemini")
        return texto

    url = ENDPOINTS.get(provedor)
    if not url:
        raise IAErro("provedor desconhecido")
    dados = _post_json(url, {
        "model": modelo,
        "messages": [{"role": "system", "content": sistema},
                     {"role": "user", "content": entrada}],
        "max_tokens": 800,
        "temperature": 0.4,
    }, {"Authorization": "Bearer " + chave})
    try:
        texto = dados["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError):
        texto = ""
    if not texto:
        raise IAErro("resposta vazia ou inesperada do provedor")
    return texto
