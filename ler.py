# teste para tranformar + exceção

import csv
from dbfread import DBF

# Caminho para o arquivo .dbc
caminho_arquivo_dbc = 'PAPB2101.dbc'

# Use a função DBF para ler o arquivo .dbc
tabela_dbf = DBF(caminho_arquivo_dbc, encoding='latin1')

# Caminho para o arquivo CSV de saída
caminho_arquivo_csv = 'PARN2101.csv'

# Escrever os dados da tabela em um arquivo CSV
with open(caminho_arquivo_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    # Escreva os cabeçalhos das colunas
    writer.writerow(tabela_dbf.field_names)
    # Escreva os dados das linhas
    for registro in tabela_dbf:
        # Inicialize uma lista para armazenar os valores convertidos
        valores_convertidos = []
        # Itere sobre os valores do registro
        for valor in registro.values():
            # Inclua tratamento de exceção para conversão de dados
            try:
                # Tente decodificar o valor para utf-8
                valor_decodificado = valor.decode('utf-8')
                # Tente converter o valor decodificado para float
                valor_convertido = float(valor_decodificado)
            except (UnicodeDecodeError, ValueError):
                # Se a decodificação ou a conversão falharem, adicione None à lista de valores convertidos
                valor_convertido = None
            valores_convertidos.append(valor_convertido)
        # Escreva a lista de valores convertidos no arquivo CSV
        writer.writerow(valores_convertidos)
