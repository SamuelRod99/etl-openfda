import logging
import pandas as pd


logger = logging.getLogger(__name__)

def load (df_report, df_patient, df_reaction, df_drug):

    df_report.to_csv('dados_report.csv', index=False)
    df_patient.to_csv('dados_paciente.csv', index=False)
    df_reaction.to_csv('dados_reações.csv', index=False)
    df_drug.to_csv('dados_drogas.csv', index=False)