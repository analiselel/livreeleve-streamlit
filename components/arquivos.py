from glob import glob
import pandas as pd
import os

# Obter o caminho absoluto para a pasta de vendas
pasta_vendas = os.path.abspath('vendas')
pasta_vendas = sorted(glob(r'vendas/*.xlsx'))
arquivos_vendas = pd.concat((pd.read_excel(cont, usecols=['Creation Date', 'Order', 'ID_SKU', 'SKU Name', '_CodigoReferenciaProduto', 'Quantity_SKU', 'Reference Code', 'SKU Selling Price', 'lat', 'lon']) for cont in pasta_vendas), ignore_index=True)
# Converter a coluna "Creation Date" para o formato brasileiro
arquivos_vendas['Creation Date'] = pd.to_datetime(arquivos_vendas['Creation Date']).dt.tz_localize(None)
arquivos_vendas['ID_SKU'] = arquivos_vendas['ID_SKU'].astype(str)   #Converte os dados da coluna ID_SKU em texto
arquivos_vendas['Reference Code'] = arquivos_vendas['Reference Code'].str.split('_').str[-1]  # Atualiza a coluna 'Reference Code' para conter somente o último valor após o caractere "_"


# Obter o caminho absoluto para a pasta de estoques
pasta_estoques = os.path.abspath('googlesheets')
pasta_estoques = sorted(glob(r'googlesheets/movimentacao_estoque.xlsx'))
arquivos_estoques = pd.concat((pd.read_excel(cont, usecols=['IDSKU', 'Estoque', 'Data Backup', '_CodigoReferenciaProduto', 'Tamanho']) for cont in pasta_estoques), ignore_index=True)

arquivos_estoques['Data Backup'] = pd.to_datetime(arquivos_estoques['Data Backup']).dt.tz_localize(None)
arquivos_estoques['IDSKU'] = arquivos_estoques['IDSKU'].astype(str)