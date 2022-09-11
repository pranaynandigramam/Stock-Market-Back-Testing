def dataExtractor(stock: str, start_day: int, start_month: int, start_year: int):
    import datetime as dt
    from pandas_datareader import data as pdr
    import yfinance as yf

    yf.pdr_override()

    start = dt.datetime(start_year, start_month, start_day)
    now = dt.datetime.now()

    data = round(pdr.get_data_yahoo(stock, start, now), 2)
    data.drop('Adj Close', axis=1, inplace=True)

    return data


def indicatorCalculator(data, indicator: str = 'RSI', lookBack: int = 14, slow_lookBank: int = 12, fast_lookBank: int = 26):
    from talib import RSI, ADX, PLUS_DI, MINUS_DI, MACD

    open_ = data['Open']
    high = data['High']
    low = data['Low']
    close = data['Close']
    volume = data['Volume']

    indicator_value = None

    if indicator == 'RSI':
        indicator_value = RSI(close, lookBack)
    elif indicator == 'ADX':
        indicator_value = ADX(high, low, close, lookBack)
    elif indicator == 'PLUS_DI':
        indicator_value = PLUS_DI(high, low, close, lookBack)
    elif indicator == 'MINUS_DI':
        indicator_value = MINUS_DI(high, low, close, lookBack)
    elif indicator == 'MACD':
        indicator_value = MACD(close, fast_lookBank, slow_lookBank, lookBack)

    return indicator_value


def conditionApplier(indicator_values, prices, buy_condition=20, sell_condition=80):
    pos = 0
    bp = []
    sp = []

    for i, j in zip(indicator_values, prices):
        if i <= buy_condition and pos == 0:
            bp.append(j)
            pos = 1
        elif i >= sell_condition and pos == 1:
            sp.append(j)
            pos = 0

    return bp, sp


def buySellPrices(buy_prices, sell_prices):
    zipping = zip(buy_prices, sell_prices)

    return zipping


def profitAndLoss(combinedList: list):
        profitTrades = []
        lossTrades = []
        allTrades = []

        for i in combinedList:
            differance = i[1] - i[0]
            if differance > 0:
                profitTrades.append(differance)
                allTrades.append(differance)
            elif differance < 0:
                lossTrades.append(differance)
                allTrades.append(differance)

        return profitTrades, lossTrades, allTrades


def multipleParameters(profitTrades, lossTrades, allTrades):
        from statistics import mean

        totalTrades = len(profitTrades) + len(lossTrades)
        wins = len(profitTrades)
        losses = len(lossTrades)
        maxGain = round(max(profitTrades), 2)
        maxLoss = round(min(lossTrades), 2)
        avgGain = round(mean(profitTrades), 2)
        avgLoss = round(mean(lossTrades), 2)
        winningStreak = winLossStreak(allTrades, True)
        loosingStreak = winLossStreak(allTrades, False)
        totalProfit = round(sum(allTrades), 2)

        return totalTrades, wins, losses, maxGain, maxLoss, avgGain, avgLoss, winningStreak, loosingStreak, totalProfit


def max_runs_of_ones(bits):
        from itertools import groupby

        maxvalue = 0

        for bit, group in groupby(bits):
            if bit:
                maxvalue = max(maxvalue, sum(group))

        return maxvalue


def winLossStreak(someList: list, winLoss: bool = True):
        from numpy import array

        converter = array(someList)
        value = 0
        if winLoss:
            value = max_runs_of_ones(converter > 0)
        elif not winLoss:
            value = max_runs_of_ones(converter < 0)

        return value













