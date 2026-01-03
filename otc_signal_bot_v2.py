import ta

def otc_1m_signal(data):
    """
    data: pandas DataFrame
    required columns: ['open', 'high', 'low', 'close']
    timeframe: 1 minute (OTC)
    works best on:
    EUR/JPY OTC, USD/JPY OTC, GBP/USD OTC, AUD/USD OTC
    """

    close = data['close']
    high = data['high']
    low = data['low']

    # Indicators
    rsi = ta.momentum.RSIIndicator(close, window=14).rsi().iloc[-1]
    ema_fast = ta.trend.EMAIndicator(close, window=9).ema_indicator().iloc[-1]
    ema_slow = ta.trend.EMAIndicator(close, window=21).ema_indicator().iloc[-1]
    macd = ta.trend.MACD(close).macd_diff().iloc[-1]

    # Last candle wick analysis (OTC fake move filter)
    last_high = high.iloc[-1]
    last_low = low.iloc[-1]
    last_close = close.iloc[-1]

    upper_wick = last_high - last_close
    lower_wick = last_close - last_low

    # 🔼 CALL CONDITION (1M OTC)
    if (
        ema_fast > ema_slow and          # trend up
        rsi <= 55 and                    # not overbought
        macd >= 0 and                    # momentum up
        lower_wick > upper_wick          # rejection from down
    ):
        return "CALL 🔼 (1M OTC)"

    # 🔽 PUT CONDITION (1M OTC)
    if (
        ema_fast < ema_slow and          # trend down
        rsi >= 45 and                    # not oversold
        macd <= 0 and                    # momentum down
        upper_wick > lower_wick          # rejection from up
    ):
        return "PUT 🔽 (1M OTC)"

    # FORCE TREND ENTRY (NO NO-TRADE)
    if ema_fast > ema_slow:
        return "CALL 🔼 (trend 1M OTC)"
    else:
        return "PUT 🔽 (trend 1M OTC)"
