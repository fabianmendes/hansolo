import binance as bi, requests as req
from os import environ as env
from binance.client import Client
import numpy as np
import pandas as pd

tbnbkey = env.get("API_KEY")
tbnbsec = env.get("API_SECRET")
         # TODO create a changing token method.
client = Client(tbnbkey, tbnbsec)

ttaapio = env.get("TAAPIO")

bount_booklet = {}  # to work about.
# dictionary of classes, each obj = pair.

class Bounty(object):

    def __init__(self, a, client):

        self.c = client
         # TODO create a changing token method.
        self.tto = a

        quests = {}  # object : "ATOM"
                     # (Quest) (asset)
            #Quest será como hago con las
        #listas: en la posicion será el obj
        #y en este caso, el key es el objeto.


    class Quest:

        def __init__(self,
                     rawdata,  #dictionary.
                     # ↑ portafoliom_iso[i]

                     asset = "ATOM",
                     vs = "USDT",  # quotea!
                     margin = False,
                     iso = False):
            if margin:
                m = "margin"
                isol = "cross"
                if iso:
                    isol = "iso"
            else:
                m = ""
                isol = ""

            #TODO: Curate all this next
            #  because is for Margin only!
            self.pair = rawdata["symbol"]
            self.undertaker = rawdata["baseAsset"]
                # ↑ base_asset_asset
            asset = self.undertaker["asset"]  # asset (ATOM)
            self.vs = rawdata["quoteAsset"]
                # ↑ qote_asset_asset
            vs = self.vs['asset']  # vs (USDT)

            self.pairslash= asset + "/" + vs
            self.name = self.pair + "_" + m + "_" + isol

            self.main = rawdata
            self.marginratio = self.main["marginRatio"]

            self.un_free = self.undertaker["free"]
            self.vs_free = self.vs["free"]

            self.un_borr = self.undertaker["borrowed"]
            self.vs_borr = self.vs["borrowed"]

            self.un_lckd = self.undertaker["locked"]
            self.vs_lckd = self.vs["locked"]

            

hunter = Bounty(client, ttaapio)
lista = []
'''
lista.append(hunter.Quest(margin=True, iso = True))

print(lista[0].pair)
print(hunter.c)
'''
print(client.get_asset_balance("USDT"))
#   hunter.c.get_asset_balance("USDT")
print(client.get_account())
margin_d=client.get_margin_account()
m_assets = margin_d["userAssets"]  # CROSS
portafoliom = []  # raw list of assets account info.
portafoliom_assets = [] # names
portafoliom_free =[]
portafoliom_borrowed = []
portafoliom_locked = []
portafoliom_dollars= []
portafoliom_convert= []
my_precision = '{:.{}f}'.format
for i in range(len(m_assets)):
    if (float(m_assets[i]['free']) or
	    float(m_assets[i]['borrowed']) or
	    float(m_assets[i]['locked'])) != 0:
        portafoliom.append(m_assets[i])
        portafoliom_assets.append(
			m_assets[i]["asset"])  # names.

# \/ it needs: TODO mt/func to return portafolio.
#   portafolio's names (symbols, es decir, asset)
#   Acceso a la data de "free" "locked" "borrowed"
#   y la suma de ello la tendremos con TotalAssets.
for i in range(len(portafoliom_assets)):
    portafoliom_free.append(
		portafoliom[i]["free"])
    portafoliom_borrowed.append(
    	portafoliom[i]["borrowed"])
    portafoliom_locked.append(
	    portafoliom[i]["locked"])
    #---
    print(portafoliom_assets)
    print(portafoliom_assets[i])
    print(portafoliom[i])
    lista.append(hunter.
                 Quest(portafoliom[i],
                       margin=True, iso=True))
    print(lista[-1].pair)
    #print(hunter.c)
    #_____________________
    # TODO esta parte no hara falta para el method.
    # Pero si hara falta el par, que es 'symbol'
    yeah = portafoliom_assets[i] + "USDT"
    if float(portafoliom[i]["borrowed"]) != 0:
        if portafoliom_assets[i] != ("USDT" or "BUSD"):
            portafoliom_convert.append(my_precision(
                    float(portafoliom_borrowed[-1])/
                    float(client.get_symbol_ticker(
                            symbol=yeah)["price"]), 4))
        else:
            portafoliom_convert.append(portafoliom_borrowed[-1])
    else:
        portafoliom_convert.append(None)
 #   ''' # price and value (division)
    sum = float(portafoliom_free[i]) + float(portafoliom_borrowed[i])
    if portafoliom_assets[i] == ("USDT" or "BUSD"):
        portafoliom_dollars.append("("+str(
                            my_precision(
                                sum, 3)+")"))
    if portafoliom_assets[i] == 'BNB':
        portafoliom_dollars.append("("+str(my_precision(
            sum*float(client.get_symbol_ticker(
                symbol="BNBBUSD")["price"]), 4))+")")
    elif portafoliom_assets[i] !=  ("USDT" or "BUSD"):
        portafoliom_dollars.append("("+str(my_precision(
            sum*float(client.get_symbol_ticker(symbol=
                                yeah)["price"]), 4))+")")
 #           '''
#for i in range(len(portafoliom)):
margin_array = np.array([#portafoliom_assets,
                    portafoliom_dollars,
					portafoliom_free,
					portafoliom_borrowed,
                    portafoliom_convert,
					portafoliom_locked])

margin_pan = pd.DataFrame(margin_array,
                columns=portafoliom_assets,
                index=['aprox.$', 'free',
                        'borrow', 'aprox.$',
                        'locked'])
#print(float(portafoliom_free[3])*float(client.get_symbol_ticker(symbol="BNBBUSD")["price"]))
print("\nMargin. (Cross), portafolio:")
print(margin_pan)
'''
print(portafoliom_assets)
print(margin_array_iso)
'''

 