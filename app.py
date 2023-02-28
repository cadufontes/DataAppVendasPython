import pandas as pd
import plotly.express as px
import streamlit as st

#lendo as bases de dados
pd.set_option('display.float_format', lambda x: '%.2f' % x)
df_vendas = pd.read_excel('Vendas.xlsx')
df_produtos = pd.read_excel('Produtos.xlsx')

#joins #inner, full, left, join
df = pd.merge(df_vendas, df_produtos, how='left', on='ID Produto')

df['Custo'] = df['Custo Unitário'] * df['Quantidade']
df['Lucro'] = df['Valor Venda'] - df['Custo']
df['mes_ano'] = df['Data Venda'].dt.to_period('M').astype(str)
df['trimestre_ano'] = df['Data Venda'].dt.to_period('Q').astype(str)

total_custo = (round(df['Custo'].sum(),2)).astype('str')
total_custo = total_custo.replace('.',',')
total_custo = 'R$' + total_custo[:2] + '.' + total_custo[2:5] + '.' + total_custo[5:]

total_lucro = (round(df['Lucro'].sum(), 2)).astype('str')
total_lucro = total_lucro.replace('.',',')
total_lucro = 'R$ ' + total_lucro[:2] + '.' + total_lucro[2:5] + '.' + total_lucro[5:]

#para os gráficos
produtos_vendidos_marca = df.groupby("Marca")["Quantidade"].sum().reset_index()
lucro_categoria = df.groupby("Categoria")["Lucro"].sum().reset_index()
lucro_mes_categoria = df.groupby(["mes_ano", "Categoria"])["Lucro"].sum().reset_index()

st.markdown(
    """
    <style>
    [data-testid="stMetricLabel"] {
        color: #fff;
    }
    [data-testid="stMetricValue"] {
        font-size: 26px;
        color: #fff;
    }
    [data-testid="metric-container"] {
        background-color: #333;
        border-radius: 15px;
        padding: 5px 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def main():
    st.title('Análise de Vendas')
    st.image('vendas.png')

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Custo Total", value=total_custo)
    with col2:
        st.metric(label="Lucro Total", value=total_lucro)
    with col3:
        st.metric(label="Total de Clientes", value=df['ID Cliente'].nunique())

    col1, col2 = st.columns(2)

    fig = px.bar(produtos_vendidos_marca, x='Quantidade', y='Marca', orientation='h', text='Quantidade', 
            width=380, height=400, title='Total de Produtos Vendidos por Marca')
    col1.plotly_chart(fig)

    fig1 = px.pie(lucro_categoria, values='Lucro', names='Categoria', width=380, height=400, 
                 title='Total de Lucro por Categoria')
    col2.plotly_chart(fig1)

    fig2 = px.line(lucro_mes_categoria, x='mes_ano', y='Lucro', width=900, height=400, 
                 title='Lucro X Mês X Categoria', markers=True, color="Categoria", 
                 labels={"mes_ano":"Mês", "Lucro":"Lucro no Mês"})
    st.plotly_chart(fig2)

if __name__ == '__main__':
    main()
