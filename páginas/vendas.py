import streamlit as st

# Função para a página de "Vendas"
def dashboard_vendas():
    st.markdown("**Dados de Vendas**")
    
#====================================================================================================#
import streamlit as st
import pandas as pd
from datetime import datetime as dt
from components import arquivos
import os

pasta_devolucoes = os.path.abspath('troquecommerce')
arquivos_devolucoes = os.path.join(pasta_devolucoes, 'troquecommerce.xlsx')
devolucoes = pd.read_excel(arquivos_devolucoes, usecols=['Data', '_CodigoReferenciaProduto', 'Total de Reversas', 'Trocas',	'Devoluções', 'Valor das Trocas', 
                                                         'Valor das Devoluções',	'Tamanho - Ficou Grande',	'Tamanho - Ficou Pequeno',	
                                                         'Não gostei do produto',	'Transparência', 'Não vestiu bem',	'Defeito - Problemas na costura',
                                                         'Marketplace',	'Produto errado - Comprei um produto e recebi outro',	
                                                         'Defeito - Problemas no tecido ou na estampa',	'Arrependimento'])

# Função para a página de "Vendas"
def dashboard_devolucoes():
    st.markdown("**Dados de Devoluções**")
    
    produto1 = st.sidebar.text_input('Produto:', key='txt-produto1')
    start_date = st.sidebar.date_input('Data inicial:', dt(2024, 1, 1))
    end_date = st.sidebar.date_input('Data final:', dt.today())

    # Convertendo os inputs de data para datetime
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
   # Lógica para filtrar por 'produto1'
    filtro_prod1 = devolucoes[
        (devolucoes['_CodigoReferenciaProduto'] == produto1) &
        (devolucoes['Data'] >= start_date) &
        (devolucoes['Data'] <= end_date)
    ]
    
    st.write(filtro_prod1)