import logging

from extração import extrair_dados
from transformação import transformar_dados


# ---------------------------------
# CONFIGURAÇÃO DO LOGGING
# ---------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ---------------------------------
# CONFIGURAÇÕES
# ---------------------------------

URL = "https://api.fda.gov/drug/event.json"

LIMIT = 1

MAX_PAGINAS = 1


# ---------------------------------
# PIPELINE
# ---------------------------------

def main():

    # ETAPA 1 — EXTRAÇÃO

    todos_dados = extrair_dados(
        url=URL,
        limit=LIMIT,
        max_paginas=MAX_PAGINAS
    )

    # ETAPA 2 — TRANSFORMAÇÃO

    dados_transformados = transformar_dados(todos_dados)
    #criar dataframes
    dataframes = criar_dataframes( dados_report, dados_patient, dados_reaction, dados_drug)

    # Visualização temporária
    print(dados_transformados["report"])
    print( df_report)


if __name__ == "__main__":
    main()