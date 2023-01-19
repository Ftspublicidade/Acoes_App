import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go

@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('utf-8')

def main():
    st.title("Analisando Ações - Fernanda Santos")
    st.image("imagem.png")
    simbolos_empresa = {'Ibovespa': '^BVSP', 
                        'Via Varejo': 'VIIA3.SA', 
                        'Apple': 'AAPL', 
                        'Petrobras': 'PBR'}

    option = st.selectbox("Qual Empresa deseja analisar?",
                        (simbolos_empresa.keys()))

    df = yf.Ticker(simbolos_empresa[option]).history(start="2018-01-01").reset_index()
    
    st.text("Visualizando os últimos registros do dataset")
    slider = st.slider("Valores", 0, 100)
    st.dataframe(df.tail(slider))

    # Gráficos

    st.header("Gráfico fechamento das ações")
    fig = px.line(df, x="Date", y="Close", title="Fechamento das ações", 
    template="seaborn")
    st.plotly_chart(fig, use_container_width=True)

    dividendos = df.groupby(df["Date"].dt.year)["Dividends"].sum().reset_index()
    fig = px.line(dividendos, x= "Date", y="Dividends", 
    title="Dividendos Anuais", template="seaborn")
    st.plotly_chart(fig)

    st.subheader("Gráfico de Candlestick, onde podemos analisar a oscilação entre a abertura e o fechamento, e se a ação fechou maior ou menor que o preço de abertura, para isso só analisar pela cor, os vermelhos fecharam com o preço menor do que o de abertura e os verdes fecharam com o preço maior do que o de abertura.")
    df_grafico = df.nlargest(7, "Date")
    fig = go.Figure(data=[go.Candlestick(x=df_grafico['Date'],
                open=df_grafico['Open'],
                high=df_grafico['High'],
                low=df_grafico['Low'],
                close=df_grafico['Close'])])
    
    fig.update_layout(
    title='Candlestick últimos 7 dias')
    st.write(fig)

    csv = convert_df(df)

    st.download_button(
    label="Download dos dados em CSV",
    data=csv,
    file_name='acoes.csv',
    mime='text/csv',
)



    
    
        




if __name__ == '__main__':
    main()

