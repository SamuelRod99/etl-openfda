import logging

from extração import extrair_dados
from transformação import organizar_dados
from transformação import criar_dataframes
from transformação import transformar_dados


# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():

    # URL da API
    url = "https://api.fda.gov/drug/event.json"

    # -------------------------
    # 1. EXTRAÇÃO
    # -------------------------

    todos_dados = extrair_dados(
        url=url,
        limit=3,
        max_paginas=1
    )

    # -------------------------
    # 2. ORGANIZAÇÃO
    # -------------------------

    (
        dados_report,
        dados_patient,
        dados_reaction,
        dados_drug
    ) = organizar_dados(todos_dados)

    # -------------------------
    # 3. CRIAÇÃO DOS DATAFRAMES
    # -------------------------

    (
        df_report,
        df_patient,
        df_reaction,
        df_drug
    ) = criar_dataframes(
        dados_report,
        dados_patient,
        dados_reaction,
        dados_drug
    )

    # -------------------------
    # 4. TRANSFORMAÇÃO
    # -------------------------

    (
        df_report,
        df_patient,
        df_reaction,
        df_drug
    ) = transformar_dados(
        df_report,
        df_patient,
        df_reaction,
        df_drug
    )

    # -------------------------
    # 5. RESULTADO
    # -------------------------

    print("\nETL executado com sucesso!")

    print("\nREPORT:")
    print(df_report.head())

    print("\nPATIENT:")
    print(df_patient.head())

    print("\nREACTION:")
    print(df_reaction.head())

    print("\nDRUG:")
    print(df_drug.head())


if __name__ == "__main__":
    main()