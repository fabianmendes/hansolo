# Try out for create the functions to
# curate the Margin Cross assets!

def cleanChain(cross):

    '''
    Curate Margin (Cross) assets!
    :param cross: client.get_margin_account()
    :return:
    '''

    margin_d = cross
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