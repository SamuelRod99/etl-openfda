import logging

from extração import extrair_dados
from transformação import (organizar_dados, criar_dataframes, transformar_dados)
from load import load
from Validacao import (validar_dados, valid_quanti_dados)


# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

def main():

    # URL da API
    url = "https://api.fda.gov/drug/event.json"

    # -------------------------
    # EXTRAÇÃO
    # -------------------------
    todos_dados = extrair_dados(
        url=url,
        limit=3,
        max_paginas=1
    )

    # -------------------------
    # ORGANIZAÇÃO
    # -------------------------
    
    (
        dados_report,
        dados_patient,
        dados_reaction,
        dados_drug
    ) = organizar_dados(todos_dados)

    logger.info("Extração finalizada")
    # -------------------------
    # CRIAÇÃO DOS DATAFRAMES
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
    logger.info("Criação de dataframes finalizada")
    # -------------------------
    # TRANSFORMAÇÃO
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
    logger.info("Tratamento de dados finalizado")
    #-------------------------
    # Validação
    # -------------------------
    validar_dados(df_report, df_patient, df_reaction, df_drug)
    valid_quanti_dados(dados_report, df_report)
    #-------------------------
    # LOAD
    #-------------------------
    load(df_report, df_patient, df_reaction, df_drug)
    
    #-------------------------
    # RESULTADO
    # -------------------------
    logger.info("carregamento finalizado")

    logger.info("ETL executado com sucesso!")

    print("\nREPORT:")
    df_report.info()

    print("\nPATIENT:")
    df_patient.info()

    print("\nREACTION:")
    df_reaction.info()

    print("\nDRUG:")
    df_drug.info()


if __name__ == "__main__":
    main()