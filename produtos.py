import streamlit as st
import pandas as pd
from datetime import datetime as dt
from components import arquivos
import plotly.express as px


def dashboard():
    st.set_page_config(page_title="Produtos", page_icon=" ", layout="wide")
    
    #with open('style.css') as f:
        #st.markdown(f"<style>{f.read()} </style>", unsafe_allow_html=True)

    st.sidebar.subheader('Filtros')

    produto1 = st.sidebar.text_input('Produto1:', key='txt-produto1')
    produto2 = st.sidebar.text_input('Produto2:', key='txt-produto2')
    start_date = st.sidebar.date_input('Data inicial:', dt(2024, 1, 1))
    end_date = st.sidebar.date_input('Data final:', dt.today())

    # Convertendo os inputs de data para datetime
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Lógica para filtrar por 'produto1'
    filtro_prod1 = arquivos.arquivos_vendas[
        (arquivos.arquivos_vendas['_CodigoReferenciaProduto'] == produto1) &
        (arquivos.arquivos_vendas['Creation Date'] >= start_date) &
        (arquivos.arquivos_vendas['Creation Date'] <= end_date)
    ]

    # Lógica para filtrar por 'produto2'
    filtro_prod2 = arquivos.arquivos_vendas[
        (arquivos.arquivos_vendas['_CodigoReferenciaProduto'] == produto2) &
        (arquivos.arquivos_vendas['Creation Date'] >= start_date) &
        (arquivos.arquivos_vendas['Creation Date'] <= end_date)
    ]

    filtro_prod2_P = filtro_prod2[(filtro_prod2['Reference Code'] == 'P')]
    filtro_prod2_M = filtro_prod2[(filtro_prod2['Reference Code'] == 'M')]
    filtro_prod2_G = filtro_prod2[(filtro_prod2['Reference Code'] == 'G')]
    filtro_prod2_GG = filtro_prod2[(filtro_prod2['Reference Code'] == 'GG')]
    filtro_prod2_XG = filtro_prod2[(filtro_prod2['Reference Code'] == 'XG')]

    orders_produto2_P = filtro_prod2_P['Order'].unique()
    orders_produto2_M = filtro_prod2_M.groupby('Reference Code')['Order'].unique().explode().unique()
    orders_produto2_G = filtro_prod2_G['Order'].unique()
    orders_produto2_GG = filtro_prod2_GG['Order'].unique()
    orders_produto2_XG = filtro_prod2_XG['Order'].unique()

    filtro_prod1['P'] = filtro_prod1['Order'].isin(orders_produto2_P).astype(int)
    filtro_prod1['M'] = filtro_prod1['Order'].isin(orders_produto2_M).astype(int)
    filtro_prod1['G'] = filtro_prod1['Order'].isin(orders_produto2_G).astype(int)
    filtro_prod1['GG'] = filtro_prod1['Order'].isin(orders_produto2_GG).astype(int)
    filtro_prod1['XG'] = filtro_prod1['Order'].isin(orders_produto2_XG).astype(int)
    filtro_prod1['Total AnB'] = filtro_prod1[['P', 'M', 'G', 'GG', 'XG']].sum(axis=1).astype(int)

    # Lógica para filtrar a tabela
    grouped_data_tamanhos = filtro_prod1.groupby(['Reference Code', 'ID_SKU', ]).agg(
        {'Order': 'count', 'P': 'sum', 'M': 'sum', 'G': 'sum', 'GG': 'sum', 'XG': 'sum', 'Total AnB': 'sum'}).reset_index()

    # Adiciona coluna de porcentagem em relação a 'Total AnB'
    grouped_data_tamanhos['P%'] = ((grouped_data_tamanhos['P'] / grouped_data_tamanhos['Total AnB'] * 100).fillna(0).round(2).astype(str) + '%')
    grouped_data_tamanhos['M%'] = ((grouped_data_tamanhos['M'] / grouped_data_tamanhos['Total AnB'] * 100).fillna(0).round(2).astype(str) + '%')
    grouped_data_tamanhos['G%'] = ((grouped_data_tamanhos['G'] / grouped_data_tamanhos['Total AnB'] * 100).fillna(0).round(2).astype(str) + '%')
    grouped_data_tamanhos['GG%'] = ((grouped_data_tamanhos['GG'] / grouped_data_tamanhos['Total AnB'] * 100).fillna(0).round(2).astype(str) + '%')
    grouped_data_tamanhos['XG%'] = ((grouped_data_tamanhos['XG'] / grouped_data_tamanhos['Total AnB'] * 100).fillna(0).round(2).astype(str) + '%')


    # Define a ordem dos Reference Codes como categóricos
    ordered_reference_codes = ['P', 'M', 'G', 'GG', 'XG']
    grouped_data_tamanhos['Reference Code'] = pd.Categorical(grouped_data_tamanhos['Reference Code'], ordered_reference_codes)

    # Ordena o DataFrame com base na coluna 'Reference Code'
    grouped_data_tamanhos = grouped_data_tamanhos.sort_values(by='Reference Code')

    # Adiciona linha de total para a tabela-tamanhos
    data_for_table_tamanhos = grouped_data_tamanhos.to_dict('records')

    # Adiciona linha de total para a tabela-tamanhos
    total_tamanhos_prod1 = grouped_data_tamanhos['Order'].sum()
    total_tamanhos_prod2_P = grouped_data_tamanhos['P'].sum()
    total_tamanhos_prod2_M = grouped_data_tamanhos['M'].sum()
    total_tamanhos_prod2_G = grouped_data_tamanhos['G'].sum()
    total_tamanhos_prod2_GG = grouped_data_tamanhos['GG'].sum()
    total_tamanhos_prod2_XG = grouped_data_tamanhos['XG'].sum()
    total_tamanhos_AnB = grouped_data_tamanhos['Total AnB'].sum()

    data_for_table_tamanhos.append({'Reference Code': 'Total', 'Order': total_tamanhos_prod1, 'P': total_tamanhos_prod2_P,
                                    'M': total_tamanhos_prod2_M, 'G': total_tamanhos_prod2_G,
                                    'GG': total_tamanhos_prod2_GG, 'XG': total_tamanhos_prod2_XG,
                                    'Total AnB': total_tamanhos_AnB,
                                    'P%': (total_tamanhos_prod2_P / total_tamanhos_AnB * 100).round(2).astype(str) + '%',
                                    'M%': (total_tamanhos_prod2_M / total_tamanhos_AnB * 100).round(2).astype(str) + '%',
                                    'G%': (total_tamanhos_prod2_G / total_tamanhos_AnB * 100).round(2).astype(str) + '%',
                                    'GG%': (total_tamanhos_prod2_GG / total_tamanhos_AnB * 100).round(2).astype(str) + '%',
                                    'XG%': (total_tamanhos_prod2_XG / total_tamanhos_AnB * 100).round(2).astype(str) + '%',
                                    'Total': total_tamanhos_prod1})

    columns = ["Reference Code", "Order", "P", "P%", 'M', 'M%', 'G', 'G%', 'GG', 'GG%', 'XG', 'XG%', 'Total AnB']

    # Criando o DataFrame
    tabela_anb = pd.DataFrame(data_for_table_tamanhos)

    # Reordenando as colunas
    tabela_anb = tabela_anb[columns]
    # Renomeie as colunas nos DataFrames tabela_anb e data_for_table_prod2_df
    tabela_anb.rename(columns={"Reference Code": "Tamanho"}, inplace=True)

    # Aplicando o estilo ao DataFrame
    column_config = {}
    for column in tabela_anb.columns:
        if column != "Tamanho":
            column_config[column] = st.column_config.Column(column, width="small")

    # Apresenta as tabelas lado a lado com tamanhos personalizados
    col1, col2 = st.columns([4, 1]) # 80% e 20% respectivamente

    # Mostra a tabela_anb na primeira coluna
    col1.dataframe(tabela_anb, column_config=column_config, height=260, hide_index=True)

    #==================================================TABELA DE COMPRADOS EM CONJUNTO==================================================#

    # Verifica se o produto1 está definido antes de mostrar a segunda tabela
    if produto1:

        orders_produto1 = filtro_prod1['Order'].unique()
        filtro_order_prod1 = arquivos.arquivos_vendas[arquivos.arquivos_vendas['Order'].isin(orders_produto1)]
        filtro_prod2 = filtro_order_prod1[filtro_order_prod1['_CodigoReferenciaProduto'] != produto1]
        grouped_data_tamanhos = filtro_prod2.groupby(['_CodigoReferenciaProduto']).agg({'Order': 'count'}).reset_index()
        grouped_data_tamanhos = grouped_data_tamanhos.sort_values(by='Order', ascending=False)
        grouped_data_tamanhos.rename(columns={"_CodigoReferenciaProduto": "Produto"}, inplace=True)
        data_for_table_prod2 = grouped_data_tamanhos.to_dict('records')
        
        # Adiciona linha de total para a tabela-tamanhos
        total_tamanhos_prod1 = grouped_data_tamanhos['Order'].sum()
        total_row = {'Produto': 'Total', 'Order': total_tamanhos_prod1}
        data_for_table_prod2.insert(0, total_row)
        
        # Código necessário pois que data_for_table_prod2 é uma lista
        data_for_table_prod2_df = pd.DataFrame(data_for_table_prod2)
        
        col2.dataframe(data_for_table_prod2_df, hide_index=True, height=248, width=210)



    #================================================GRÁFICO DE LINHAS ESTOQUE================================================#
    filtro_prod_estoque = arquivos.arquivos_estoques[
    (arquivos.arquivos_estoques['_CodigoReferenciaProduto'] == produto1) &
    (arquivos.arquivos_estoques['Data Backup'] >= start_date) &
    (arquivos.arquivos_estoques['Data Backup'] <= end_date)
    ]

    # Agrupa os dados por data, código de referência e IDSKU, somando as quantidades de estoque
    dados_estoque = filtro_prod_estoque.groupby(['Data Backup', '_CodigoReferenciaProduto', 'Tamanho'])['Estoque'].sum().reset_index()

    # Criação do gráfico de linha com Plotly Express
    figura = px.line(dados_estoque, x='Data Backup', y='Estoque', color='Tamanho',
                    title='Estoque ao longo do período para cada tamanho',
                    labels={'Estoque': 'Quantidade de Estoque', 'Data Backup': 'Data'})

    rótulos_y = None
    for i in range(len(dados_estoque)):
        if rótulos_y is None or dados_estoque['Estoque'][i] != rótulos_y:
            text = f"<b>{dados_estoque['Estoque'][i]}</b>"
            
        figura.add_annotation(x=dados_estoque['Data Backup'][i], y=dados_estoque['Estoque'][i],
                        text=text, showarrow=False, xshift=0, yshift=7)
        rótulos_y = dados_estoque['Estoque'][i]

    # Exibir o gráfico
    st.plotly_chart(figura, use_container_width=True)


    #================================================GRÁFICO DE MAPA================================================#

    dfmap = filtro_prod1.groupby(['lat', 'lon']).size().reset_index(name='count')

    df = pd.DataFrame({
        "col1": dfmap['lat'],
        "col2": dfmap['lon'],
        "col3": dfmap['count'] * 1000,
    })

    st.map(df,
        latitude='col1',
        longitude='col2',
        size='col3')