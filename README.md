# Financial analist

Esse é um projeto desenvolvido para auxiliar analistas de mercado financeiro, nele se encontram algumas conclusões técnicas baseadas em índices, análise e volume do operações de ativos.
O projeto conta com algumas formas de extrair dados para garantir que os dados estejam sempre atualizados com os últimos valores de fechamento de mercado.

## Requerimentos

Lembre-se de instalar as dependências em seu ambiente usando o comando `pip install -r requirements.txt`

## Classes e funções

`DataExtractor`: Essa é a função que que irá realizar a extração dos dados macro econômicos ou alguma stock. Para isso você pode chamar as funções desta classe:
- stock( ticker ) : retorna um dataframe de preço e um de volume de operações de uma ação específica
- valor_dolar_mundo( ) : retorna um dataframe como os valores de variação do dólar em relação às demais moedas do mundo
- valor_dolar_brasil( ) : retorna um dataframe como os valores do dólar em relação ao Real brasileiro
- taxa_juros_brasil( ) : retorna um dataframe como os valores da taxa selic mensal
- taxa_juros_americana( ) : retorna um dataframe como os valores da taxa de juros americana
- inflacao_brasil( ) : retorna um dataframe como os valores da inflação acumulada de 12 meses
- inflacao_americana( ) : retorna um dataframe como os valores da inflação americana acumulada de 12 meses
- indice_ouro( ) : retorna um dataframe de preço e um de volume de operações do índice de ouro
- indice_de_medo( ) : retorna um dataframe como os valores do índice que indica o medo do mercado internacional

`MovingAverageAnalisys`: Essa é a função que que irá realizar a classificação de tendência de curto e longo prazo e a indicação da agressividade dessas tendências:
Essa classe pode ter seus valores de janela de médias móveis de curto e longo prazo alterados utilizando os argumentos short_window e long_window. Segue exemplo de inicialização da classe:

FinancialAnalist.MovingAverageAnalisys(df_dif_inflacao, short_window=3, long_window=12) - houve a alteração das janelas para 3 e 12 períodos.
- classify_trend( ) : indica a tendência e a agressividade do indicador indicado na inicialização da classe

`Indicators` : Pode ser utilizado para te retornar a análise de tendência ou volume de um ativo em variáveis tipo string:
- dolar_mundial( df_dolar_mundial ) : retorna as tendências de curto e longo prazo do dolar em escala mundial
- dolar_vs_real( df_dolar_real ) : retorna as tendências de curto e longo prazo do dólar em escala nacional
- dolar_vs_real_dif( df_dolar_mundial, df_dolar_real ) : retorna as tendências de curto e longo da comparação entre a valorização do dolár nas escalas mundial e nacional
- juros_eua_br( df_juros_eua, df_juros_br ) : retorna as tendências de curto e longo da comparação entre a as taxas de juros americana e brasileira
- inflacao_eua_br( df_inflacao_eua, df_inflacao_br ) : retorna as tendências de curto e longo da comparação entre a as inflações americana e brasileira
- medo( df_medo ) : retorna a tendência do medo em relação à media histórica
- ouro( df_ouro_preco, df_ouro_volume ) : retorna a tendência de curto prazo e se o índice de negociação está alto ou baixo
- stock( df_stock_preco, df_stock_volume ) : retorna as tendências de curto e longo prazo e se o índice de negociação está alto ou baixo.
