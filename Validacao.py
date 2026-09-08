import logging

logger = logging.getLogger(__name__)

def validar_dados(df_report, df_patient, df_reaction, df_drug):

    if df_report.empty:
        raise ValueError("df_report está vazio")

    if df_patient.empty:
        raise ValueError("df_patient está vazio")

    if df_reaction.empty:
        raise ValueError("df_reaction está vazio")

    if df_drug.empty:
        raise ValueError("df_drug está vazio")


    #validadando integridade dos dados
    ids_report = set(df_report["safetyreportid"])
    ids_reaction = set(df_reaction["safetyreportid"])
    ids_patient = set(df_patient["safetyreportid"])
    ids_drugs = set(df_drug["safetyreportid"])

    ids_invalidos_reaction = ids_reaction - ids_report
    ids_invalidos_patient = ids_patient - ids_report
    ids_invalidos_drugs = ids_drugs - ids_report

    if ids_invalidos_reaction:
        raise ValueError("Existem reactions sem report correspondente.")
    if ids_invalidos_patient:
        raise ValueError("Existem patient sem report correspondente.")
    if ids_invalidos_drugs:
            raise ValueError("Existem drug sem report correspondente.")


    #informando quantidade de registros de dados
    logger.info(f"Registros transformados: {len(df_report)}")

    return True

#validação de quantidade de dados
def valid_quanti_dados (dados_report, df_report):
     if len(df_report) < len(dados_report) * 0.5:
        raise ValueError("Mais de 50% dos registros foram perdidos.")