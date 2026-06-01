import streamlit as st
import pandas as pd
import plotly.express as px

dados = pd.read_excel("Vendas_Base_de_Dados.xlsx")

dados["Faturamento"] = dados["Quantidade"] * dados["Valor Unitário"]

st.title("Dashboard de Vendas")

st.write("Tabela de vendas do mês:")
st.dataframe(dados)

st.sidebar.title("Filtros")

lojas = sorted(dados["Loja"].unique())
loja_escolhida = st.sidebar.selectbox("Escolha a loja:", lojas)

produtos = ["Todos"] + sorted(dados[dados["Loja"] == loja_escolhida]["Produto"].unique())
produto_escolhido = st.sidebar.selectbox("Escolha o produto:", produtos)

dados_filtrados = dados[dados["Loja"] == loja_escolhida]

if produto_escolhido != "Todos":
    dados_filtrados = dados_filtrados[dados_filtrados["Produto"] == produto_escolhido]

st.write(f"Dados da loja {loja_escolhida}:")
st.dataframe(dados_filtrados)

faturamento_total = dados_filtrados["Faturamento"].sum()
quantidade_total = dados_filtrados["Quantidade"].sum()
numero_vendas = len(dados_filtrados)

st.subheader("Resumo da seleção")

col1, col2, col3 = st.columns(3)

col1.metric("Faturamento total", f"R$ {faturamento_total:,.2f}")
col2.metric("Quantidade vendida", int(quantidade_total))
col3.metric("Número de vendas", numero_vendas)

dados_faturamento_loja = (
    dados.groupby("Loja")["Faturamento"]
    .sum()
    .reset_index()
    .sort_values(by="Faturamento", ascending=False)
)

grafico = px.bar(
    dados_faturamento_loja,
    x="Loja",
    y="Faturamento",
    title="Faturamento por Loja"
)

st.plotly_chart(grafico)

dados_pizza = (
    dados[dados["Loja"] == loja_escolhida]
    .groupby("Produto")["Faturamento"]
    .sum()
    .reset_index()
    .sort_values(by="Faturamento", ascending=False)
)

if produto_escolhido != "Todos":
    dados_pizza = dados_pizza[dados_pizza["Produto"] == produto_escolhido]

grafico_pizza = px.pie(
    dados_pizza,
    names="Produto",
    values="Faturamento",
    title=f"Participação dos produtos no faturamento da loja {loja_escolhida}"
)

st.plotly_chart(grafico_pizza)

if produto_escolhido == "Todos":
    st.info(
        f"Na loja {loja_escolhida}, o faturamento total considerando todos os produtos foi de R$ {faturamento_total:,.2f}."
    )
else:
    st.info(
        f"Na loja {loja_escolhida}, o produto '{produto_escolhido}' teve um faturamento total de R$ {faturamento_total:,.2f}."
    )