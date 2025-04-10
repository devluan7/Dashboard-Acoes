import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import date
#Pegando a data atual
data_atual = date.today()


@st.cache_data #Faz com que as informaçoes da função abaixo fiquem armazenadas em cache
def carregar_dados(empresas):
    texto_tickers = " ".join(empresas)
    dados_acao = yf.Tickers(texto_tickers)
    cotacoes_acao = dados_acao.history(period = "1d", start = "2010-01-01", end = data_atual)
    cotacoes_acao = cotacoes_acao["Close"]   
    return cotacoes_acao

@st.cache_data #Faz com que as informaçoes da função abaixo fiquem armazenadas em cache
def carregar_tickers_acoes():
    base_tickers = pd.read_csv("IBOV.csv", sep = ";")
    tickers = list(base_tickers["Código"])
    tickers = [item + ".SA" for item in tickers]
    return tickers
acoes = carregar_tickers_acoes()
dados = carregar_dados(acoes)

#Interface
st.write("""
## Evolução do preço das ações ao longo dos anos:
""")


#Preparando os dados que vão ser exibidos (filtros)
st.sidebar.header("Filtros")
#Filtro de ações
lista_acoes =  st.sidebar.multiselect("Filtrar ações", dados.columns)
if lista_acoes:
    dados = dados[lista_acoes]
    if len(lista_acoes) == 1:
       acao_unica = lista_acoes[0]
       dados = dados.rename(columns={acao_unica: "Close"})

#Filtro de Datas
data_inicial = dados.index.min().to_pydatetime()
data_final = dados.index.max().to_pydatetime()
intervalo_datas = st.sidebar.slider("Esolha o período", min_value=data_inicial, max_value=data_final, value=(data_inicial, data_final))
dados = dados.loc[intervalo_datas[0]:intervalo_datas[1]]


#Criar o Gráfico
st.line_chart(dados)

#Filtro Performance de ativos
texto_perfomance_ativos = ""

if len(lista_acoes) == 0:
    lista_acoes = dados.columns
elif len(lista_acoes) == 1:
    dados = dados.rename(columns={"Close": acao_unica})

carteira = [1000 for acao in lista_acoes]
total_inicial_carteira = sum(carteira)

for i, acao in enumerate(lista_acoes):
    #Mudar a cor no markdown = :Cor[texto]
    if pd.isna(dados[acao].iloc[-1]) or pd.isna(dados[acao].iloc[0]):
        texto_perfomance_ativos += f"  \n{acao}: :gray[Dados insuficientes no período]"
        continue
    performance_ativo = dados[acao].iloc[-1] / dados[acao].iloc[0] - 1
    performance_ativo = float(performance_ativo)

    carteira[i] *= (1 + performance_ativo)
   
    if performance_ativo > 0:
        texto_perfomance_ativos = texto_perfomance_ativos + f"  \n{acao}: :green[{performance_ativo:.2%}]"
    elif performance_ativo < 0:
         texto_perfomance_ativos = texto_perfomance_ativos + f"  \n{acao}: :red[{performance_ativo:.2%}]"
    else:
         texto_perfomance_ativos = texto_perfomance_ativos + f"  \n{acao}: :blue[{performance_ativo:.2%}]"

total_final_carteira = sum(carteira)
performance_carteira = total_final_carteira / total_inicial_carteira - 1

if performance_carteira > 0:
        texto_performance_carteira = f"Performance da carteira com todos os ativos: :green[{performance_carteira:.2%}]"
elif performance_carteira < 0:
     texto_performance_carteira = f"Performance da carteira com todos os ativos: :red[{performance_carteira:.2%}]"
else:
     texto_performance_carteira = f"Performance da carteira com todos os ativos: :blue[{performance_carteira:.2%}]"


st.write(f"""

### Perfomance em cada ativo no período selecionado:
{texto_perfomance_ativos}

{texto_performance_carteira}
""")

