import numpy as np
import pandas as pd
import yfinance as yf
import datetime

import pandas_datareader as pdr
from bcb import currency
from bcb import sgs
from scipy.stats import linregress

class FinancialAnalist:

    def __init__(self) -> None:
        pass

    class DataExtractor:

        def __init__(self) -> None:
            pass

        def stocks(self, ticker):
            self.total_data = yf.download(ticker)

            df_preco = self.total_data['Close']

            df_volume = self.total_data['Volume']

            return df_preco, df_volume
        
        def valor_dolar_mundo(self):

            df_dxy = yf.download("DX-Y.NYB", start="2002-01-01")['Close']

            return df_dxy
        
        def valor_dolar_brasil(self):

            df_usdbrl = currency.get("USD", 
                    start='2002-01-01',
                    end=datetime.date.today())
            
            return df_usdbrl
        
        def taxa_juros_brasil(self):

            df_taxa_juros = sgs.get({'selic': 432}, start='2002-02-01')
            df_taxa_juros = df_taxa_juros.resample('ME').last()

            return df_taxa_juros
        
        def taxa_juros_americana(self):

            df_taxa_juros_americana = pdr.fred.FredReader("FEDFUNDS", 
                                                        start='2002-01-01', 
                                                        end = datetime.date.today()).read()
            
            df_taxa_juros_americana = df_taxa_juros_americana.resample('ME').last()

            return df_taxa_juros_americana
            
        
        def inflacao_brasil(self):

            df = sgs.get({'IPCA': 433}, start='2002-02-01')

            df.index = df.index.to_period('M')

            dfr = df.rolling(12)

            i12 = dfr.apply(lambda x: (1 + x/100).prod() - 1).dropna() * 100

            i12.index= i12.index = pd.to_datetime(i12.index.to_timestamp())

            return i12
        
        def inflacao_americana(self):

            df_inflacao = pdr.fred.FredReader("CPIAUCSL", start='2002-01-01', end = datetime.date.today()).read()
            df_inflacao['CPI_Pct_Change_Annual'] = df_inflacao['CPIAUCSL'].pct_change(periods=12) * 100

            df_inflacao_acumulada = df_inflacao['CPI_Pct_Change_Annual'].dropna()

            return df_inflacao_acumulada
        
        
        def indice_ouro(self):

            df_ouro = yf.download("GOLD")

            df_ouro_price = df_ouro['Close']
            df_ouro_volume = df_ouro['Volume']

            return df_ouro_price, df_ouro_volume
        
        def indice_de_medo(self):

            df_medo = pdr.fred.FredReader("VIXCLS", start='2001-01-01', end = datetime.date.today()).read()
            df_medo = df_medo.dropna()

            return df_medo
        




    class MovingAverageAnalisys:
        
        def __init__(self, history_data, short_window = 9, long_window = 40):
            """
            Inicializa a classe com os dados históricos.
            
            :param dados_historicos: Lista de preços históricos da ação.
            """
            self.history_data = history_data
            self.short_window = short_window
            self.long_window = long_window
        


        def classify_trend(self):
                
            self.df_short = pd.DataFrame(self.history_data.rolling(window=self.short_window, closed='left').mean()).dropna().tail(30).iloc[:, -1]
    
            self.df_long = pd.DataFrame(self.history_data.rolling(window=self.long_window, closed='left').mean()).dropna().tail(30).iloc[:, -1]
            
            # Fazer a regressão linear
            x_short = np.arange(len(self.df_short))
            y_short = self.df_short.to_numpy().flatten()
            slope_short, intercept, r_value, p_value, std_err_short = linregress(x_short, y_short)

            x_long = np.arange(len(self.df_long))
            y_long = self.df_long.to_numpy().flatten()
            slope_long, intercept, r_value, p_value, std_err_long = linregress(x_long, y_long)

            # Definição de limiares
            diferenca_short = abs(slope_short) - abs(std_err_short)
            diferenca_long = abs(slope_long) - abs(std_err_long)

            limiar = 0.5
            
            if slope_short > 0:
                if diferenca_short > limiar :
                    short_trend = 'tendência de alta agressiva no curto prazo'
                else:
                    short_trend = 'tendência de alta suave no curto prazo'
            else:
                if diferenca_short > limiar:
                    short_trend = 'tendência de baixa agressiva no curto prazo'
                else:
                    short_trend = 'tendência de baixa suave no curto prazo'
                

            if slope_long > 0:
                if diferenca_long > limiar:
                    long_trend = 'tendência de alta agressiva no longo prazo'
                else:
                    long_trend = 'tendência de alta suave no longo prazo'
            else:
                if diferenca_long > limiar:
                    long_trend = 'tendência de baixa agressiva no longo prazo'
                else:
                    long_trend = 'tendência de baixa suave no longo prazo'


            return short_trend, long_trend




    class Indicators:
        def __init__(self) -> None:
            pass

        
        def dolar_mundial(self,dolar_mundo):
            dolar_analist = FinancialAnalist.MovingAverageAnalisys(dolar_mundo)

            dolar_short_trend, dolar_long_trend = dolar_analist.classify_trend()

            return dolar_short_trend, dolar_long_trend

        def dolar_vs_real(self,dolar_real):
            dolar_vs_real_analist = FinancialAnalist.MovingAverageAnalisys(dolar_real)

            dolar_vs_real_short_trend, dolar_vs_real_long_trend = dolar_vs_real_analist.classify_trend()

            return dolar_vs_real_short_trend, dolar_vs_real_long_trend 

        def dolar_vs_real_dif(self, dolar_mundo, dolar_brasil):
            
            df_dolar_mundo_pct = dolar_mundo.pct_change() * 100
            df_dolar_mundo_pct= df_dolar_mundo_pct.tail(2000).cumsum() #apenas os 2000 últimos valores em porcentagem acumulativa

            df_dolar_brasil_pct = dolar_brasil.pct_change() * 100
            df_dolar_brasil_pct= df_dolar_brasil_pct.tail(2000).cumsum()

            df_dif = df_dolar_brasil_pct['USD'] - df_dolar_mundo_pct
            df_dif = df_dif.dropna()
        
            dolar_vs_real_dif_analist = FinancialAnalist.MovingAverageAnalisys(df_dif)
            dolar_dif_short_trend, dolar_dif_long_trend = dolar_vs_real_dif_analist.classify_trend()

            return dolar_dif_short_trend, dolar_dif_long_trend

        def juros_eua_br(self, juros_eua, juros_brasil):
            
            df_juros_eua_pct = juros_eua
            

            df_juros_brasil_pct = juros_brasil

            df_dif_juros = df_juros_brasil_pct['selic'] - df_juros_eua_pct['FEDFUNDS']
            df_dif_juros = df_dif_juros.dropna()
        
            juros_dif_analist = FinancialAnalist.MovingAverageAnalisys(df_dif_juros, short_window=3, long_window=12)
            juros_dif_short_trend, juros_dif_long_trend = juros_dif_analist.classify_trend()

            return juros_dif_short_trend, juros_dif_long_trend
        
        def inflacao_eua_br(self, inflacao_eua, inflacao_brasil):
            
            df_inflacao_eua_pct = inflacao_eua
            
            df_inflacao_brasil_pct = inflacao_brasil

            df_dif_inflacao = df_inflacao_brasil_pct['IPCA'] - df_inflacao_eua_pct['CPI_Pct_Change_Annual']
            df_dif_inflacao = df_dif_inflacao.dropna()
        
            inflacao_dif_analist = FinancialAnalist.MovingAverageAnalisys(df_dif_inflacao, short_window=3, long_window=12)
            inflacao_dif_short_trend, inflacao_dif_long_trend = inflacao_dif_analist.classify_trend()

            return inflacao_dif_short_trend, inflacao_dif_long_trend

        def medo(self, medo):

            df_medo = medo
            media_medo = df_medo.mean()

            dif_medo = df_medo - media_medo

            medo_analist = FinancialAnalist.MovingAverageAnalisys(dif_medo, short_window=21)

            medo_short_trend, medo_short_trend = medo_analist.classify_trend()

            return medo_short_trend
        
        def ouro(self, ouro_price, ouro_volume):

            df_ouro_price = ouro_price
            df_ouro_volume = ouro_volume

            ouro_analist = FinancialAnalist.MovingAverageAnalisys(df_ouro_price)
            ouro_short_trend, ouro_long_trend = ouro_analist.classify_trend()

            vol_semana = df_ouro_volume.tail(7)

            media_ouro_vol = df_ouro_volume.mean()

            media_ultima_semana = vol_semana.mean() 

            if media_ultima_semana > media_ouro_vol:

                procura_ouro = "Índice de Negociação alto"

            else:

                procura_ouro = "Índice de Negociação baixo"

            return ouro_short_trend, procura_ouro


        def stock(self, stock_price, stock_volume):

            df_stock_price = stock_price
            df_stock_volume = stock_volume

            stock_analist = FinancialAnalist.MovingAverageAnalisys(df_stock_price)
            stock_short_trend, stock_long_trend = stock_analist.classify_trend()

            self.vol_semana = df_stock_volume.tail(7)

            self.media_stock_vol = df_stock_volume.mean()

            self.media_ultima_semana = self.vol_semana.mean() 

            if self.media_ultima_semana > self.media_stock_vol:

                procura_stock = "Índice de Negociação alto"

            else:

                procura_stock = "Índice de Negociação baixo"

            return stock_short_trend, stock_long_trend, procura_stock

          