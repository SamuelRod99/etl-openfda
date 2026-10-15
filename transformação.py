import logging
import pandas as pd
import numpy as np
from mapeamentos import (
    TRADUCAO_SERIEDADE,
    TRADUCAO_OBITO,
    TRADUCAO_CRITERIO_EXPEDIDO,
    TRADUCAO_QUALIFICACAO,
    TRADUCAO_UNIDADE_IDADE,
    TRADUCAO_SEXO,
    TRADUCAO_CARACTERIZACAO_MEDICAMENTO,
    TRADUCAO_VIA_ADIMISTRACAO
)


logger = logging.getLogger(__name__)


def organizar_dados(todos_dados):

    dados_report = []
    dados_patient = []
    dados_reaction = []
    dados_drug = []

    for relatorio in todos_dados:

        # REPORT
        primarysource = relatorio.get("primarysource") or {}
        sender = relatorio.get("sender") or {}
        receiver = relatorio.get("receiver") or {}

        dados_pre_report = {
            "safetyreportid": relatorio.get("safetyreportid"),
            "transmissiondate": relatorio.get("transmissiondate"),
            "serious": relatorio.get("serious"),
            "seriousnessdeath": relatorio.get("seriousnessdeath"),
            "receivedate": relatorio.get("receivedate"),
            "receiptdate": relatorio.get("receiptdate"),
            "fulfillexpeditecriteria": relatorio.get("fulfillexpeditecriteria"),
            "companynumb": relatorio.get("companynumb"),
            "reportercountry": primarysource.get("reportercountry"),
            "qualification": primarysource.get("qualification"),
            "senderorganization": sender.get("senderorganization"),
            "receiverorganization": receiver.get("receiverorganization")
        }

        dados_report.append(dados_pre_report)

        # PATIENT
        patient = relatorio.get("patient", {})
        patientdeath = patient.get("patientdeath", {})

        dados_pre_patient = {
            "safetyreportid": relatorio.get("safetyreportid"),
            "patientonsetage": patient.get("patientonsetage"),
            "patientonsetageunit": patient.get("patientonsetageunit"),
            "patientsex": patient.get("patientsex"),
            "patientdeathdate": patientdeath.get("patientdeathdate")
        }
        dados_patient.append(dados_pre_patient)

        # REACTION
        for reaction in patient.get("reaction", []):

            dados_pre_reaction = {
                "safetyreportid": relatorio.get("safetyreportid"),
                "reactionmeddrapt": reaction.get("reactionmeddrapt")
            }
            dados_reaction.append(dados_pre_reaction)

        # DRUG
        for drug in patient.get("drug", []):

            dados_pre_drug = {
                "safetyreportid": relatorio.get("safetyreportid"),
                "drugcharacterization": drug.get("drugcharacterization"),
                "medicinalproduct": drug.get("medicinalproduct"),
                "drugauthorizationnumb": drug.get("drugauthorizationnumb"),
                "drugadministrationroute": drug.get("drugadministrationroute"),
                "drugindication": drug.get("drugindication")
            }
            dados_drug.append(dados_pre_drug)

    return (
        dados_report,
        dados_patient,
        dados_reaction,
        dados_drug
    )


def criar_dataframes( dados_report, dados_patient, dados_reaction, dados_drug):
    df_report = pd.DataFrame(dados_report)
    df_patient = pd.DataFrame(dados_patient)
    df_reaction = pd.DataFrame(dados_reaction)
    df_drug = pd.DataFrame(dados_drug)

    return (
        df_report,
        df_patient,
        df_reaction,
        df_drug
    )

def transformar_dados(df_report, df_patient, df_reaction, df_drug):
    
    #remover duplicadas e nulos
    df_report.drop_duplicates(inplace=True)
    df_patient.drop_duplicates(inplace=True)
    df_reaction.drop_duplicates(inplace=True)
    df_drug.drop_duplicates(inplace=True)

    df_report = df_report.dropna(subset=["safetyreportid"])
    df_patient = df_patient.dropna(subset=["safetyreportid"])
    df_reaction = df_reaction.dropna(subset=["safetyreportid"])
    df_drug = df_drug.dropna(subset=["safetyreportid"])

    #normalização de datas          #pela documntação da api todas as datas são setadas no mesmo formato
    df_report['transmissiondate'] = pd.to_datetime(df_report['transmissiondate'], format='%Y%m%d', errors='coerce')
    df_report['receivedate'] = pd.to_datetime(df_report['receivedate'], format='%Y%m%d', errors='coerce')
    df_report.loc[df_report["receivedate"] > pd.Timestamp.today(), "receivedate"] = np.nan #valores de data acima da data atual serão entendidos como valores informados de forma errado, portanto transformados em nulos
    df_report['receiptdate'] = pd.to_datetime(df_report['receiptdate'], format='%Y%m%d', errors='coerce')
    df_patient['patientdeathdate'] = pd.to_datetime(df_patient['patientdeathdate'], format='%Y%m%d', errors='coerce')

    #normalização de inteiros
    df_patient['patientonsetage'] = pd.to_numeric(df_patient['patientonsetage'], errors="coerce")
    df_patient.loc[df_patient["patientonsetage"] < 0, "patientonsetage"] = np.nan #valores de idade abaixo de zero serão entendidos como valores informados de forma errado, portanto transformados em nulos
    

    #conversão de código: consultar documentação
    df_report['serious'] = df_report['serious'].replace(TRADUCAO_SERIEDADE)
    
    df_report['seriousnessdeath'] = df_report['seriousnessdeath'].replace(TRADUCAO_OBITO)

    df_report['fulfillexpeditecriteria'] = df_report['fulfillexpeditecriteria'].replace(TRADUCAO_CRITERIO_EXPEDIDO)

    df_report['qualification'] = df_report['qualification'].replace(TRADUCAO_QUALIFICACAO)

    df_patient['patientonsetageunit'] = df_patient['patientonsetageunit'].replace(TRADUCAO_UNIDADE_IDADE) 

    df_patient['patientsex'] = df_patient['patientsex'].replace(TRADUCAO_SEXO)

    df_drug['drugcharacterization'] = df_drug['drugcharacterization'].replace(TRADUCAO_CARACTERIZACAO_MEDICAMENTO)

    df_drug["drugadministrationroute"] = (pd.to_numeric(df_drug["drugadministrationroute"], errors="coerce").replace(TRADUCAO_VIA_ADIMISTRACAO))


    #padronização de texto
    df_report['reportercountry'] = df_report['reportercountry'].str.upper().str.strip()
    df_report['senderorganization'] = df_report['senderorganization'].str.strip()
    df_report['receiverorganization'] = df_report['receiverorganization'].str.strip()
    df_reaction['reactionmeddrapt'] = df_reaction['reactionmeddrapt'].str.strip()
    df_drug['medicinalproduct'] = df_drug['medicinalproduct'].str.upper().str.strip()
    df_drug['drugindication'] = df_drug['drugindication'].str.upper().str.strip()

    return (df_report, df_patient, df_reaction, df_drug)

