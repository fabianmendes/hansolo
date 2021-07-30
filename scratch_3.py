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

    def __init__(self, client, a):

        self.c = client
        # TODO create a changing token method.
        self.tto = a

        quests_dict = {}  # object : "ATOM"?
        # (Quest) (asset)
        # Quest será como hago con las
        # listas: en la posicion será el obj
        # y en este caso, el key es el objeto.
        quests = [
# Bounty().quests.append(Bounty.Quest(raw))
                   ]  # ↑ IMPORTANT.
        # Bounty.list[i] <object Quest class>
        self.portafolio = {"spot": [],  #list.
                       "margin_c": [],  #list.
                       "margin_i": {}}  # idk.

        self.getAssets(self.c, #spot=True,
                       margin_c=True,
                       )
        self.getAssets(self.c, spot=True,
                       #margin_c=True,
                       )


    def convertUs(self, amounts, names):
        '''

        :param amounts: necessary <list>
        :param names: necesary <list linked>
        :return: lista_convert<list $aprox.>
        '''

        lista_convert = []  # portafoliom_dollars = []
        my_precision = '{:.{}f}'.format

        for i in range(len(amounts)):
            lista_ass = names[i]

            yeah = lista_ass + "USDT"
            if lista_ass != ("USDT" or "BUSD"):
                lista_convert.append(my_precision(
                    float(amounts[i]) *
                    float(client.get_symbol_ticker(
                        symbol=yeah)["price"]), 4))
            elif "USD" in lista_ass:
            #else:
                lista_convert.append(
                    my_precision(float(amounts[i]), 4))
        aux = []
        for i in range(len(lista_convert)):
            if float(lista_convert[i])*1000 == 0:
                aux.append(None)
            else:
                aux.append("("+str(lista_convert[i])+")")
        return  aux

    def getAssets(self, cli, spot=False,
                  margin_c=False, margin_i=False):
        if  spot:
            spot = cli.get_account()  # raw dict.
            # TODO this doesn't work ↑
            spot_dlist = spot["balances"]  # '' list.
            portafolios = []  # assets' dictionary list
            portafolios_assets = []  # just names.

            portafolios_free = []
            portafolios_lckd = []

            for i in range(len(spot_dlist)):
                if (float(spot_dlist[i]['free']) or
                float(spot_dlist[i]['locked'])) != 0:
                    portafolios.append(spot_dlist[i])
                    portafolios_assets.append(
                        spot_dlist[i]["asset"])
                    portafolios_free.append(
                        spot_dlist[i]["free"])
                    portafolios_lckd.append(
                        spot_dlist[i]["locked"])
            '''
            # [[assets], [free], [$], [lck], [$Total]]
            lista_portafolio_spot = []
            lista_portafoliom_crs = []
            # ---
            lista_protafoliom_iso = []
            # ↑ [base, quot, x, [], [], ] per pos.
            '''
            self.spot = portafolios # raw dict. List!
            self.portafolio["spot"] = [
                                    portafolios_assets,
                                    portafolios_free,

                                    portafolios_lckd,]
                # Done list. Let's add Total and $ aprox.
            self.portafolio["spot"].append(  # ←(total)
                                    self.sumAssets(
                                        portafolios_free,
                                        portafolios_lckd))

            # Done. We have self.portafolio["spot"] !!

            self.data_spot = self.dataWallet(
                                self.portafolio["spot"])

        if  margin_c:
            margin_d = cli.get_margin_account()
            m_assets = margin_d["userAssets"]  # CROSS

            portafoliom = []  # raw list of assets account info.
            portafoliom_assets = []  # names
            portafoliom_free = []
            portafoliom_borrowed = []
            portafoliom_locked = []
            '''
            portafoliom_dollars = []  # free $aprox.
            portafoliom_convert = []  # borrow $apx.
            '''
            for i in range(len(m_assets)):
                if (float(m_assets[i]['free']) or
                    float(m_assets[i]['borrowed']) or
                    float(m_assets[i]['locked'])) != 0:
                    portafoliom.append(m_assets[i]) #raw info.
                    portafoliom_assets.append(
                            m_assets[i]["asset"])  # names.


                    portafoliom_free.append(
                            m_assets[i]["free"])
                    portafoliom_borrowed.append(
                            m_assets[i]["borrowed"])
                    portafoliom_locked.append(
                            m_assets[i]["locked"])

            self.margin_c = portafoliom  # raw dict List!
            self.portafolio["margin_c"] = [
                        portafoliom_assets,  # names
                        self.convertUs(portafoliom_free,
                                       portafoliom_assets),
                        portafoliom_free,
                        portafoliom_borrowed,
                        self.convertUs(portafoliom_borrowed,
                                       portafoliom_assets),
                        portafoliom_locked,

                        self.convertUs(
                            self.sumAssets(
                                    self.sumAssets(portafoliom_free,
                                                portafoliom_borrowed),
                                    portafoliom_locked),
                            portafoliom_assets),
                         ]
            self.data_cross = self.dataWallet(
                                self.portafolio["margin_c"])

        # print(portafolios)

    def sumAssets(self, uno, dos):
        aux = []
        for i in range(len(uno)):
            a = float(uno[i])
            b = float(dos[i])
            aux.append(a + b)

        return aux  # a list.


    def dataWallet(self, lista,
                    #cual="All",
                    ):
        if len(lista) == 4:
            cloumna = lista[0]
            lista_aux = lista[1:]
            top_array = np.array(lista_aux)
            self.ta = np.array(self.portafolio["spot"][0]
                    )
            index = [
                    'free', 'locked',
                    'Total:',]
            pan = pd.DataFrame(top_array,
                               columns=lista[0],
                               index=index)
            return pan
        #else:
        if len(lista) == 7:
            margin_ar = np.array(lista[1:])

            index = [
                'aprox.$', 'free', 'borrow',
                'aprox.$', 'locked', #'Total:',
                'Total:$']
            pan = pd.DataFrame(margin_ar,
                        columns=lista[0],
                        index= index)
            return pan
        #if len(lista) ==
        #else:
            # error! Message.


    #class Talent:


    class Quest:

        def __init__(self,
                     rawdata,  #dictionary.
                     # ↑ portafoliom_iso[i]

                     asset="ATOM",
                     vs="USDT",  # quotea!
                     margin=False,
                     iso=False):
            if margin:
                self.m = "margin"
                self.isol = "cross"
                if iso:
                    self.isol = "iso"
            else:
                self.m = ""
                self.isol = ""


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
            self.name = self.pair + "_" + self.m\
                        + "_" + self.isol

            self.main = rawdata
            self.marginratio = self.main["marginRatio"]

            self.un_free = self.undertaker["free"]
            self.vs_free = self.vs["free"]

            self.un_borr = self.undertaker["borrowed"]
            self.vs_borr = self.vs["borrowed"]

            self.un_lckd = self.undertaker["locked"]
            self.vs_lckd = self.vs["locked"]

    def printPanda(self, cual="All"):

        if cual == "spot":
            print("\nSpot, portafolio:")
            print(#self.data_spot
                #self.top_array
                  pd.DataFrame(self.portafolio["spot"]).T
                  )

        if cual == "margin_c":
            print("\nMargin. (Cross), portafolio:")
            print(self.data_cross)

        if cual == "margin_i":
            print("\nMargin.ISOlated, portafolio:")
            #print(self.data_misol)

        elif cual == "All":
            self.printPanda(cual="spot")
            self.printPanda(cual="margin_c")
            #self.printPanda(cual="margin_i")


    def cleanChain(self, cross):

        '''
        Curate Margin (Cross) assets!
        :param cross: client.get_margin_account()
        :return:
        '''

        margin_d = cross  # (dictionary)
        m_assets = margin_d["userAssets"]

        portafoliom = []  # raw list of assets account info.
        portafoliom_assets = []  # names.

        portafoliom_free = []
        portafoliom_borrowed = []
        portafoliom_locked = []

        portafoliom_dollars = []
        portafoliom_convert = []
        my_precision = '{:.{}f}'.format

        for i in range(len(m_assets)):
            if (float(m_assets[i]['free']) or
                float(m_assets[i]['borrowed']) or
                float(m_assets[i]['locked'])) != 0:
                portafoliom.append(m_assets[i])
                portafoliom_assets.append(
                    m_assets[i]["asset"])  # names.

            yeah = portafoliom_assets[i] + "USDT"
            if float(portafoliom[i]["borrowed"]) != 0:
                if portafoliom_assets[i] != ("USDT" or "BUSD"):
                    portafoliom_convert.append(my_precision(
                        float(portafoliom_borrowed[-1]) /
                        float(client.get_symbol_ticker(
                            symbol=yeah)["price"]), 4))
                else:
                    portafoliom_convert.append(portafoliom_borrowed[-1])
            else:
                portafoliom_convert.append(None)
                #   ''' # price and value (division)
            sum = float(portafoliom_free[i]) + float(portafoliom_borrowed[i])
            if portafoliom_assets[i] == ("USDT" or "BUSD"):
                portafoliom_dollars.append("(" + str(
                    my_precision(
                        sum, 3) + ")"))
            if portafoliom_assets[i] == 'BNB':
                portafoliom_dollars.append("(" + str(my_precision(
                    sum * float(client.get_symbol_ticker(
                        symbol="BNBBUSD")["price"]), 4)) + ")")
            elif portafoliom_assets[i] != ("USDT" or "BUSD"):
                portafoliom_dollars.append("(" + str(my_precision(
                    sum * float(client.get_symbol_ticker(symbol=
                                                         yeah)["price"]), 4)) + ")")
        # TODO. Save the lists, and reorganize'em
        # to be able to print as panda.

hunter = Bounty(client, ttaapio)
lista = []
'''
lista.append(hunter.Quest(margin=True, iso = True))

print(lista[0].pair)
print(hunter.c)

print(client.get_asset_balance("USDT"))
# /\  It's Spot !
#   hunter.c.get_asset_balance("USDT")
print(client.get_account())
margin_d = client.get_margin_account()
'''
#print(hunter.c)
hunter.printPanda(#cual="margin_c"
                  )
print(hunter.ta)