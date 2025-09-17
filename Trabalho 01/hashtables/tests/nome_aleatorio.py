# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 17:21:09 2025

@author: uende
"""

import random
from faker import Faker

# --- CONFIGURAÇÃO INICIAL ---
# 1. Definimos a lista de localidades (idiomas) que serão utilizadas, conforme solicitado.
#    'pt_BR' -> Português (Brasil)
#    'en_US' -> Inglês (Estados Unidos)
#    'es_ES' -> Espanhol (Espanha)
#    'fr_FR' -> Francês (França)
#    'de_DE' -> Alemão (Alemanha)

locales = ['pt_BR', 'en_US', 'es_ES', 'fr_FR', 'de_DE']
SEED_VALUE = 42
random.seed(SEED_VALUE)
Faker.seed(SEED_VALUE)

# 2. Para otimizar, criamos uma única instância da classe Faker para cada idioma.
#    Isso evita ter que recarregar os dicionários de nomes a cada chamada.
faker_instances = {locale: Faker(locale) for locale in locales}

def gerar_nome_aleatorio():
    """
    Gera um nome aleatório de três partes, combinando nomes e sobrenomes
    de diferentes idiomas (português, inglês, espanhol, francês e alemão).

    Regras seguidas:
    1) O nome terá 3 partes: nome, segundo nome e sobrenome.
    2) Cada parte é formada por uma combinação de vogais e consoantes (ao usar nomes reais).
    3) Cada parte inicia com letra maiúscula, formando um pseudônimo.
    4) Utiliza dicionários de nomes e sobrenomes da biblioteca Faker.

    Retorna:
        str: Uma string contendo o nome completo gerado.
    """
    
    # --- SELEÇÃO DOS IDIOMAS PARA CADA PARTE DO NOME ---
    # Escolhemos aleatoriamente um idioma para cada uma das três partes do nome.
    # Isso permite combinações como "João (pt) William (en) Schneider (de)".
    locale_nome = random.choice(locales)
    locale_segundo_nome = random.choice(locales)
    locale_sobrenome = random.choice(locales)

    # --- GERAÇÃO DE CADA PARTE DO NOME ---
    # Usamos a instância do Faker correspondente ao idioma sorteado.
    # A biblioteca já garante que os nomes comecem com letra maiúscula.
    
    # 1ª Parte: Nome
    primeiro_nome = faker_instances[locale_nome].first_name()
    
    # 2ª Parte: Segundo Nome (usamos a mesma função de gerar nome próprio)
    segundo_nome = faker_instances[locale_segundo_nome].first_name()

    # 3ª Parte: Sobrenome
    sobrenome = faker_instances[locale_sobrenome].last_name()
    
    # --- COMBINAÇÃO E RETORNO ---
    # Juntamos as três partes para formar o nome completo.
    nome_completo = f"{primeiro_nome} {segundo_nome} {sobrenome}"
    
    return nome_completo

def gerar_nomes_aleatorios(n, seed=42):
    random.seed(seed)
    Faker.seed(seed)

    nomes = []
    for i in range(n):
        nomes.append(gerar_nome_aleatorio())
    
    return nomes
    

# --- EXECUÇÃO DO ALGORITMO ---
# Bloco principal que será executado quando o script for iniciado.
if __name__ == "__main__":
    print("Gerando 20 nomes aleatórios multilíngues:")
    print("-" * 40)
    
    # Gera e imprime 10 exemplos de nomes.
    for i in range(20):
        nome_gerado = gerar_nome_aleatorio()
        print(f"{i+1}: {nome_gerado}")
    
    print("-" * 40)