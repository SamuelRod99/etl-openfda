import logging
from pathlib import Path


logger = logging.getLogger(__name__)

def load (df_report, df_patient, df_reaction, df_drug):
    pasta_saida = Path("dados")
    pasta_saida.mkdir(parents = True, exist_ok=True)

    arquivos = {
        "dados_report.csv": df_report,
        "dados_patient.csv": df_patient,
        "dados_reaction.csv": df_reaction,
        "dados_drug.csv": df_drug,
    }

    for nome, df in arquivos.items():
        caminho = pasta_saida/nome
        df.to_csv(caminho, index=False, encoding="utf-8")

        logger.info("Arquivo %s salvo: %d registros", caminho, len(df))
