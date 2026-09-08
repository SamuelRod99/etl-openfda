import logging
import pandas as pd
import numpy as np
from datetime import date


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
    df_patient.loc[df_patient["patientonsetage"] > 120, "patientonsetage"] = np.nan 

    #conversão de código: consultar documentação
    traducao_seriedade = {'1': 'Grave', '2': 'Não Grave'} #tradução dos campos serius
    df_report['serious'] = df_report['serious'].replace(traducao_seriedade)
    df_report['seriousnessdeath'] = df_report['seriousnessdeath'].replace('1','Óbito')

    traducao_velocidade_processamento_relatorio = {'1': 'sim', '2': 'Não'}
    df_report['fulfillexpeditecriteria'] = df_report['fulfillexpeditecriteria'].replace(traducao_velocidade_processamento_relatorio)

    traducao_qualificação = {'1': 'Médico', '2': 'Farmacêutico', '3': 'Outro profissional de saúde','4': 'Advogado', '5': 'Consumidor ou profissional que não atua na área da saúde'}
    df_report['qualification'] = df_report['qualification'].replace(traducao_qualificação)

    traducao_age_unit = {'800': 'Década', '801': 'Ano', '802': 'Mês', '803': 'Semana', '804': 'Dia', '805': 'Hora'}
    df_patient['patientonsetageunit'] = df_patient['patientonsetageunit'].replace(traducao_age_unit) #--------------tratar caso venha um código desconhcido------------

    traducao_sex = {'0': 'Unknown', '1': 'Male', '2': 'Female'}
    df_patient['patientsex'] = df_patient['patientsex'].replace(traducao_sex)

    traducao_drug_characterization = {'1': 'Suspeito', '2': 'concomitante', '3': 'Interagente'}
    df_drug['drugcharacterization'] = df_drug['drugcharacterization'].replace(traducao_drug_characterization)

    vias_administracao = {1: "Auricular", 2: "Bucal", 3: "Cutânea", 4: "Dental", 5: "Endocervical", 6: "Endossinusal", 7: "Endotraqueal", 8: "Epidural", 9: "Extra-amniótica", 10: "Hemodiálise", 11: "Intracavernosa", 12: "Intra-amniótica", 13: "Intra-arterial", 14: "Intra-articular", 15: "Intrauterina", 16: "Intracardíaca", 17: "Intracavernosa", 18: "Intracerebral", 19: "Intracervical", 20: "Intracisternal", 21: "Intracorneal", 22: "Intracoronária", 23: "Intradérmica", 24: "Intradiscal (intraespinal)", 25: "Intra-hepática", 26: "Intralesional", 27: "Intralinftática", 28: "Intramedular (medula óssea)", 29: "Intrameníngea", 30: "Intramuscular", 31: "Intraocular", 32: "Intrapericárdica", 33: "Intraperitoneal", 34: "Intrapleural", 35: "Intra-sinovial", 36: "Intratumoral", 37: "Intratecal", 38: "Intratorácica", 39: "Intratraqueal", 40: "Intravenosa em bolus", 41: "Gotejamento intravenoso", 42: "Intravenosa (não especificada)", 43: "Intravesical", 44: "Iontoforese", 45: "Nasal", 46: "Técnica de curativo oclusivo", 47: "Oftálmica", 48: "Oral", 49: "Orofaríngea", 50: "Outra", 51: "Parenteral", 52: "Periarticular", 53: "Perineural", 54: "Retal", 55: "Respiratória (inalação)", 56: "Retrobulbar", 57: "Subconjuntival", 58: "Subcutânea", 59: "Subdérmica", 60: "Sublingual", 61: "Tópica", 62: "Transdérmica", 63: "Transmamária", 64: "Transplacentária", 65: "Desconhecida", 66: "Uretral", 67: "Vaginal"}
    df_drug["drugadministrationroute"] = (pd.to_numeric(df_drug["drugadministrationroute"], errors="coerce").replace(vias_administracao))


    #padronização de texto
    df_report['reportercountry'] = df_report['reportercountry'].str.upper().str.strip()
    df_report['senderorganization'] = df_report['senderorganization'].str.strip()
    df_report['receiverorganization'] = df_report['receiverorganization'].str.strip()
    df_reaction['reactionmeddrapt'] = df_reaction['reactionmeddrapt'].str.strip()
    df_drug['medicinalproduct'] = df_drug['medicinalproduct'].str.upper().str.strip()
    df_drug['drugindication'] = df_drug['drugindication'].str.upper().str.strip()





    return (
        df_report,
        df_patient,
        df_reaction,
        df_drug
    )

