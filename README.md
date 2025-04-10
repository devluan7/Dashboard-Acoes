# 📈 Dashboard de Ações com Streamlit
### Este projeto é um dashboard interativo para análise de ações da bolsa brasileira, feito com Python e Streamlit.

Funcionalidades: 
- Filtragem por período de tempo para análise histórica dos preços.
- Filtro de múltiplas ações para comparar desempenho individual ou em grupo.
- Gráfico interativo da evolução dos preços com base nos filtros selecionados.
- Simulação de carteira de investimentos com cálculo de performance final.
- Performance individual por ativo, com cores dinâmicas:
- Carregamento inteligente com cache usando @st.cache_data, acelerando a execução do app.
- Atualização automática da data final, sempre pegando o dia atual utilizando datetime.
