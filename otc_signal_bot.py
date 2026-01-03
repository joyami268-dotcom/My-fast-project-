import ta

def otc_signal_bot(data):
    """
    data = pandas DataFrame
    columns: open, high, low, close
    timeframe: 1m / 5m
    """

    close = data['close']

    rsi = ta.momentum.RSIIndicator(close, window=14).rsi().iloc[-1]
    ema_fast = ta.trend.EMAIndicator(close, window=9).ema_indicator().iloc[-1]
    ema_slow = ta.trend.EMAIndicator(close, window=21).ema_indicator().iloc[-1]
    macd = ta.trend.MACD(close).macd_diff().iloc[-1]

    if ema_fast > ema_slow and rsi < 55 and macd >= 0:
        return "CALL 🔼 (OTC)"

    if ema_fast < ema_slow and rsi > 45 and macd <= 0:
        return "PUT 🔽 (OTC)"

    if ema_fast > ema_slow:
        return "CALL 🔼 (trend OTC)"
    else:
        return "PUT 🔽 (trend OTC)"
