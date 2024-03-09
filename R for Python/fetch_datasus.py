import datetime
import requests

def fetch_datasus(year_start, month_start, year_end, month_end, uf="all", information_system="", vars=None, stop_on_error=False, timeout=240):
    # Verifica se o sistema de informação de saúde é válido
    available_information_system = ["SIH-RD", "SIH-RJ", "SIH-SP", "SIH-ER", "SIM-DO", "SIM-DOFET", "SIM-DOEXT", "SIM-DOINF", "SIM-DOMAT", "SINASC",
                                    "CNES-LT", "CNES-ST", "CNES-DC", "CNES-EQ", "CNES-SR", "CNES-HB", "CNES-PF", "CNES-EP", "CNES-RC", "CNES-IN", "CNES-EE", "CNES-EF", "CNES-GM",
                                    "SIA-AB", "SIA-ABO", "SIA-ACF", "SIA-AD", "SIA-AN", "SIA-AM", "SIA-AQ", "SIA-AR", "SIA-ATD", "SIA-PA", "SIA-PS", "SIA-SAD",
                                    "SINAN-DENGUE", "SINAN-CHIKUNGUNYA", "SINAN-ZIKA", "SINAN-MALARIA"]
    if information_system not in available_information_system:
        raise ValueError("Health information system unknown.")
    
    # Cria datas para verificação
    if information_system.startswith("SIH") or information_system.startswith("CNES") or information_system.startswith("SIA"):
        date_start = datetime.date(year_start, month_start, 1)
        date_end = datetime.date(year_end, month_end, 1)
    elif information_system.startswith("SIM") or information_system == "SINASC" or information_system.startswith("SINAN"):
        date_start = datetime.date(year_start, 1, 1)
        date_end = datetime.date(year_end, 1, 1)

    # Verifica datas
    if date_start > date_end:
        raise ValueError("Start date must be greater than end date.")

    # Cria sequência de datas
    if information_system.startswith("SIH") or information_system.startswith("CNES") or information_system.startswith("SIA"):
        dates = [datetime.date(year, month, 1).strftime("%y%m") for year in range(year_start, year_end+1) for month in range(1, 13)]
    elif information_system.startswith("SIM") or information_system == "SINASC" or information_system.startswith("SINAN"):
        dates = [str(year) for year in range(year_start, year_end+1)]

    # Verifica UF
    ufs = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
    if uf != "all" and uf not in ufs:
        raise ValueError("UF unknown.")
    
    lista_uf = ufs if uf == "all" else [uf]

    # Restante da lógica

    files_list = []

    if information_system == "SIM-DOFET" or information_system == "SIM-DOEXT" or information_system == "SIM-DOINF":
        # Datas disponíveis
        geral_url = "ftp://ftp.datasus.gov.br/dissemin/publicos/SIM/CID10/DOFET/"
        prelim_url = "ftp://ftp.datasus.gov.br/dissemin/publicos/SIM/PRELIM/DOFET/"

        tmp = requests.get(geral_url).text.split('\n')
        tmp = [x for x in tmp if "DOFET" in x or "DOEXT" in x or "DOINF" in x]
        tmp = list(set([x[5:7] for x in tmp]))
        avail_geral = sorted([int("19" + x) if x.startswith("9") else int("20" + x) for x in tmp])

        tmp = requests.get(prelim_url).text.split('\n')
        tmp = [x for x in tmp if "DOFET" in x or "DOEXT" in x or "DOINF" in x]
        tmp = list(set([x[5:7] for x in tmp]))
        avail_prelim = sorted([int("19" + x) if x.startswith("9") else int("20" + x) for x in tmp])

        # Check if required dates are available
        if not all(date in avail_geral + avail_prelim for date in dates):
            print("As seguintes datas não estão disponíveis no DataSUS: {}".format(", ".join([str(date) for date in dates if date not in avail_geral + avail_prelim])))
        valid_dates = [date for date in dates if date in avail_geral + avail_prelim]

        # Message about preliminary data
        if any(date in avail_prelim for date in valid_dates):
            print("As seguintes datas são preliminares: {}".format(", ".join([str(date) for date in valid_dates if date in avail_prelim])))

        # Lista de arquivos
        if uf != "Any":
            print("Os dados não estão disponíveis por UF. Fazendo download de todos os dados disponíveis.")

        if information_system == "SIM-DOFET":
            files_list_1 = [geral_url + "DOFET" + str(date)[2:4] + ".dbc" for date in valid_dates if date in avail_geral]
            files_list_2 = [prelim_url + "DOFET" + str(date)[2:4] + ".dbc" for date in valid_dates if date in avail_prelim]
        elif information_system == "
