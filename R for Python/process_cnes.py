import pandas as pd
import numpy as np
from functools import reduce

def process_cnes(data, information_system=["CNES-ST", "CNES-PF"], nomes=True, municipality_data=True):
    
    # Check information system
    available_information_system = ["CNES-ST", "CNES-PF"]
    if information_system not in available_information_system:
        raise ValueError("Health information system unknown.")

    # Convert DataFrame to pandas DataFrame
    data = pd.DataFrame(data)

    # Convert columns to numeric
    cols_to_numeric = ["CPF_CNPJ", "CNPJ_MAN", "CLIENTEL", "TP_UNID", "TURNO_AT", "NIV_HIER", "TP_PREST", "ORGEXPED", 
                       "PF_PJ", "NIV_DEP", "COD_IR", "ESFERA_A", "RETENCAO", "ATIVIDAD", "NATUREZA", "NAT_JUR", "CLASAVAL", 
                       "TERCEIRO"]
    data[cols_to_numeric] = data[cols_to_numeric].apply(pd.to_numeric, errors='coerce')

    # Convert columns to character
    cols_to_character = ["REGSAUDE", "TPGESTAO"]
    data[cols_to_character] = data[cols_to_character].astype(str)

    # Convert columns to Sim ou Nao
    cols_to_sim_nao = ["AV_ACRED", "AV_PNASS", "GESPRG1E", "GESPRG1M", "GESPRG2E", "GESPRG2M", "GESPRG4E", "GESPRG4M", 
                       "NIVATE_A", "GESPRG3E", "GESPRG3E", "GESPRG3M", "GESPRG5E", "GESPRG5M", "GESPRG6E", "GESPRG6M", 
                       "NIVATE_H", "GESPRG3E", "URGEMERG", "ATENDAMB", "CENTROBS", "CENTRNEO", "ATENDHOS", "SERAP01P", 
                       "SERAP01T", "SERAP02P", "SERAP02T", "SERAP03P", "SERAP03T", "SERAP04P", "SERAP04T", "SERAP05P", 
                       "SERAP05T", "SERAP06P", "SERAP06T", "SERAP07P", "SERAP07T", "SERAP08P", "SERAP08T", "SERAP09P", 
                       "SERAP09T", "SERAP10P", "SERAP10T", "SERAP11P", "SERAP11T", "SERAPOIO", "RES_BIOL", "RES_QUIM", 
                       "RES_RADI", "RES_COMU", "COLETRES", "COMISS01", "COMISS02", "COMISS03", "COMISS04", "COMISS05", 
                       "COMISS06", "COMISS07", "COMISS08", "COMISS09", "COMISS10", "COMISS11", "COMISS12", "COMISSAO", 
                       "AP01CV01", "AP01CV02", "AP01CV05", "AP01CV06", "AP01CV03", "AP01CV04", "AP02CV01", "AP02CV02", 
                       "AP02CV05", "AP02CV06", "AP02CV03", "AP02CV04", "AP03CV01", "AP03CV02", "AP03CV05", "AP03CV06", 
                       "AP03CV03", "AP03CV04", "AP04CV01", "AP04CV02", "AP04CV05", "AP04CV06", "AP04CV03", "AP04CV04", 
                       "AP05CV01", "AP05CV02", "AP05CV05", "AP05CV06", "AP05CV03", "AP05CV04", "AP06CV01", "AP06CV02", 
                       "AP06CV05", "AP06CV06", "AP06CV03", "AP06CV04", "AP07CV01", "AP07CV02", "AP07CV05", "AP07CV06", 
                       "AP07CV03", "AP07CV04", "ATEND_PR", "VINC_SUS"]
    data[cols_to_sim_nao] = np.where(data[cols_to_sim_nao] == 1, 'Sim', 'Nao')

    # ATIVIDAD
    atividade_dict = {1: "Unidade Universitária", 2: "Unidade Escola Superior Isolada", 3: "Unidade Auxiliar de Ensino", 
                      4: "Unidade de Pesquisa", 5: "Unidade de Prestação de Serviço de Saúde", 
                      6: "Unidade de Prestação de Serviço Social", 7: "Unidade de Gestão", 8: "Unidade de Ensino", 
                      9: "Unidade de Práticas Integrativas e Complementares em Saúde (PICS)", 
                      10: "Unidade de Atenção Básica em Saúde da Família (UBASF)", 
                      11: "Unidade de Pronto Atendimento (UPA)", 12: "Unidade de Atendimento Especializado", 
                      13: "Unidade de Referência", 14: "Unidade Móvel Terrestre", 15: "Unidade Móvel Fluvial", 
                      16: "Unidade Móvel Marítima", 17: "Unidade de Pronto Atendimento (UPA)", 
                      18: "Unidade de Pronto Atendimento (UPA)", 19: "Unidade de Pronto Atendimento (UPA)"}
    data['ATIVIDAD'] = data['ATIVIDAD'].map(atividade_dict)

    # CLIENTEL
    clientel_dict = {1: "Indiferenciada", 2: "Atendimento Especializado", 3: "Própria", 4: "Mista", 5: "Atendimento Especializado"}
    data['CLIENTEL'] = data['CLIENTEL'].map(clientel_dict)

    # TURNO_AT
    turno_at_dict = {1: "Matutino", 2: "Vespertino", 3: "Noturno", 4: "Integral", 5: "Outro"}
    data['TURNO_AT'] = data['TURNO_AT'].map(turno_at_dict)

    # NATUREZA
    natureza_dict = {1: "Pública", 2: "Privada", 3: "Filantrópica", 4: "Sociedade civil", 5: "Outra"}
    data['NATUREZA'] = data['NATUREZA'].map(natureza_dict)

    # Add fantasy names and company name
    if nomes:
        data["NOME_FANT"] = "fantasy name"
        data["NOME_EMPR"] = "company name"

    # Add municipality details
    if municipality_data:
        data["MUNIC_RESI"] = "Municipality details"

    return data
