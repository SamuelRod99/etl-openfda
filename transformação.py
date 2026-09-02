import logging
import pandas as pd


logger = logging.getLogger(__name__)


def organizar_dados(todos_dados):

    dados_report = []
    dados_patient = []
    dados_reaction = []
    dados_drug = []

    for relatorio in todos_dados:

         # REPORT
        primarysource = relatorio.get("primarysource", {})
        sender = relatorio.get("sender", {})

        dados_pre_report = {
            "safetyreportid": relatorio.get("safetyreportid"),#como validar?
            "transmissiondateformat": relatorio.get("transmissiondateformat"),
            "transmissiondate": relatorio.get("transmissiondate"), #Y
            "serious": relatorio.get("serious"),#Y
            "seriousnessdeath": relatorio.get("seriousnessdeath"),#Y
            "receivedateformat": relatorio.get("receivedateformat"),
            "receivedate": relatorio.get("receivedate"),#Y
            "receiptdateformat": relatorio.get("receiptdateformat"),
            "receiptdate": relatorio.get("receiptdate"),#Y
            "fulfillexpeditecriteria": relatorio.get("fulfillexpeditecriteria"),#Y
            "companynumb": relatorio.get("companynumb"),#?
            "reportercountry": primarysource.get("reportercountry"),#Y
            "qualification": primarysource.get("qualification"),#Y
            "senderorganization": sender.get("senderorganization"),#Y
            "receiver": relatorio.get("receiver")#Y
        }
        dados_report.append(dados_pre_report)

        # PATIENT
        patient = relatorio.get("patient", {})
        patientdeath = patient.get("patientdeath", {})

        dados_pre_patient = {
            "safetyreportid": relatorio.get("safetyreportid"),
            "patientonsetage": patient.get("patientonsetage"),#Y
            "patientonsetageunit": patient.get("patientonsetageunit"),
            "patientsex": patient.get("patientsex"),
            "patientdeathdateformat": patientdeath.get("patientdeathdateformat"),
            "patientdeathdate": patientdeath.get("patientdeathdate")#Y
        }
        dados_patient.append(dados_pre_patient)

        # REACTION
        for reaction in patient.get("reaction", []):

            dados_pre_reaction = {
                "safetyreportid": relatorio.get("safetyreportid"),
                "reactionmeddrapt": reaction.get("reactionmeddrapt")#Y
            }
            dados_reaction.append(dados_pre_reaction)

        # DRUG
        for drug in patient.get("drug", []):

            dados_pre_drug = {
                "safetyreportid": relatorio.get("safetyreportid"),
                "drugcharacterization": drug.get("drugcharacterization"),
                "medicinalproduct": drug.get("medicinalproduct"),#Y
                "drugauthorizationnumb": drug.get("drugauthorizationnumb"),
                "drugadministrationroute": drug.get("drugadministrationroute"),
                "drugindication": drug.get("drugindication")#Y
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

    #remover duplicadas
    df_report.drop_duplicates(inplace=True)
    df_patient.drop_duplicates(inplace=True)
    df_reaction.drop_duplicates(inplace=True)
    df_drug.drop_duplicates(inplace=True)

    #normalização de datas
    df_report['transmissiondate'] = pd.to_datetime(df_report['transmissiondate'], format='%Y%m%d')
    df_report['receivedate'] = pd.to_datetime(df_report['receivedate'], format='%Y%m%d')
    df_report['receiptdate'] = pd.to_datetime(df_report['receiptdate'], format='%Y%m%d')
    df_patient['patientdeathdate'] = pd.to_datetime(df_report['patientdeathdate'], format='%Y%m%d')

    #normalização de inteiros
    patientonsetageunit
    df_patient['patientonsetage'] = df_patient['patientonsetage'].astype(int)

    #conversão de código: consultar documentação
    traducao_seriedade = {1: 'Grave', 2: 'Não Grave'} #tradução dos campos serius
    df_report['serious'] = df_report['serious'].replace(traducao_seriedade)
    df_report['seriousnessdeath'] = df_report['seriousnessdeath'].replace(1:'Óbito')
    df_report['seriousnessdeath'] = df_report['seriousnessdeath'].fillna('Não Fatal')

    traducao_velocidade_processamento_relatorio = {1: 'sim', 2: 'Não'}
    df_report['fulfillexpeditecriteria'] = df_report['fulfillexpeditecriteria'].replace(traducao_velocidade_processamento_relatorio)

    traducao_qualificação = {1: 'Médico', 2: 'Farmacêutico', 3: 'Outro profissional de saúde',4: 'Advogado', 5: 'Consumidor ou profissional que não atua na área da saúde'}
    df_report['qualification'] = df_report['qualification'].replace(traducao_qualificação)

    

    #padronização de texto
    df_report['reportercountry'] = df_report['reportercountry'].str.upper().str.strip()
    df_report['senderorganization'] = df_report['senderorganization'].str.strip()
    df_report['receiver'] = df_report['receiver'].str.strip()
    df_reaction['reactionmeddrapt'] = df_report['reactionmeddrapt'].str.strip()
    df_drug['medicinalproduct'] = df_report['medicinalproduct'].str.upper().str.strip()
    df_drug['drugindication'] = df_report['drugindication'].str.upper().str.strip()



    return (
        df_report,
        df_patient,
        df_reaction,
        df_drug
    )
