import pandas as pd

# Carregar a planilha
planilha = pd.read_excel(r"C:\Users\User\Desktop\Teste Api Produtos\dados.xlsx")

# Função para criar a URL
def criar_url(sku):
    return f"https://lojalivreeleve.vtexcommercestable.com.br/api/logistics/pvt/inventory/skus/{sku}"

# Aplicar a função à coluna "IDSKU" e criar a coluna "URL API"
planilha['URL API'] = planilha['IDSKU'].apply(criar_url)

# Salvar a planilha atualizada em um novo arquivo
planilha.to_excel(r"C:\Users\User\Desktop\Teste Api Produtos\dados_atualizados.xlsx", index=False)
