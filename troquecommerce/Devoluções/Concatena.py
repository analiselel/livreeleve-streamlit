import pandas as pd
from glob import glob

# Obter uma lista de todos os arquivos xlsx na pasta atual
arquivos_xlsx = glob('*.xlsx')

# Lista para armazenar os DataFrames das planilhas
df_list = []

# Loop através de cada arquivo xlsx
for arquivo in arquivos_xlsx:
    # Ler o arquivo Excel
    df = pd.read_excel(arquivo)
    
    # Converter a coluna 'Data' para o formato de data
    df['Data'] = pd.to_datetime(df['Data']).dt.date
    
    # Adicionar DataFrame à lista
    df_list.append(df)

# Concatenar os DataFrames da lista
df_concat = pd.concat(df_list)

# Salvar o DataFrame concatenado em um novo arquivo Excel
arquivo_concatenado = 'troquecommerce.xlsx'
df_concat.to_excel(arquivo_concatenado, index=False)

print("As planilhas foram concatenadas com sucesso em", arquivo_concatenado)
