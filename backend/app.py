"""
Multi-Asset Signal Robot — Backend API
"""

import os
import time
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

TWELVEDATA_API_KEY = os.environ.get("TWELVEDATA_API_KEY", "")

app = FastAPI(title="Multi-Asset Signal Robot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SYMBOLS = {
    "GOLD": {"type": "twelvedata", "td_symbol": "XAU/USD", "label": "XAU/USD"},
    "SILVER": {"type": "twelvedata", "td_symbol": "XAG/USD", "label": "XAG/USD"},
    "BTC": {"type": "cryptocompare", "cc_symbol": "BTC", "label": "BTC/USDT"},
    "SOL": {"type": "cryptocompare", "cc_symbol": "SOL", "label": "SOL/USDT"},
}

_cache = {}
CACHE_SECONDS = 25


def ema(values, period):
    k = 2 / (period + 1)
    ema_vals = [values[0]]
    for v in values[1:]:
        ema_vals.append(v * k + ema_vals[-1] * (1 - k))
    return ema_vals


def rsi(values, period=14):
    if len(values) < period + 1:
        return [50.0] * len(values)
    gains, losses = [0.0], [0.0]
    for i in range(1, len(values)):
        change = values[i] - values[i - 1]
        gains.append(max(change, 0.0))
        losses.append(max(-change, 0.0))
    avg_gain = sum(gains[1:period + 1]) / period
    avg_loss = sum(losses[1:period + 1]) / period
    rsis = [50.0] * (period + 1)
    for i in range(period + 1, len(values)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        rs = avg_gain / avg_loss if avg_loss != 0 else 100
        rsis.append(100 - (100 / (1 + rs)))
    while len(rsis) < len(values):
        rsis.append(rsis[-1])
    return rsis


def fetch_binance_closes(symbol, interval="5m", limit=100):
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    closes = [float(c[4]) for c in data]
    last_price = closes[-1]
    return closes, last_price


def fetch_cryptocompare_closes(symbol, limit=100):
    url = "https://min-api.cryptocompare.com/data/v2/histominute"
    params = {"fsym": symbol, "tsym": "USD", "limit": limit, "aggregate": 5}
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    if data.get("Response") != "Success":
        raise RuntimeError(data.get("Message", "CryptoCompare error"))
    candles = data["Data"]["Data"]
    closes = [float(c["close"]) for c in candles if c["close"] > 0]
    last_price = closes[-1]
    return closes, last_price


def fetch_twelvedata_closes(td_symbol, interval="5min", outputsize=100):
    if not TWELVEDATA_API_KEY:
        raise RuntimeError("TWELVEDATA_API_KEY not set")
    url = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": td_symbol,
        "interval": interval,
        "outputsize": outputsize,
        "apikey": TWELVEDATA_API_KEY,
        "order": "ASC",
    }
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    if "values" not in data:
        raise RuntimeError(data.get("message", "TwelveData error"))
    closes = [float(v["close"]) for v in data["values"]]
    last_price = closes[-1]
    return closes, last_price


def compute_signal(closes):
    if len(closes) < 25:
        return "WAIT", 0.0, 0.0

    ema9 = ema(closes, 9)
    ema21 = ema(closes, 21)
    rsi14 = rsi(closes, 14)

    prev_diff = ema9[-2] - ema21[-2]
    curr_diff = ema9[-1] - ema21[-1]
    curr_rsi = rsi14[-1]

    crossed_up = prev_diff <= 0 and curr_diff > 0
    crossed_down = prev_diff >= 0 and curr_diff < 0
    trending_up = curr_diff > 0
    trending_down = curr_diff < 0

    signal = "WAIT"
    if (crossed_up or trending_up) and 40 <= curr_rsi <= 70:
        signal = "BUY"
    elif (crossed_down or trending_down) and 30 <= curr_rsi <= 60:
        signal = "SELL"

    return signal, curr_rsi, curr_diff


def get_symbol_data(key, cfg):
    now = time.time()
    cached = _cache.get(key)
    if cached and now - cached["ts"] < CACHE_SECONDS:
        return cached["data"]

    try:
        if cfg["type"] == "binance":
            closes, price = fetch_binance_closes(cfg["binance_symbol"])
        elif cfg["type"] == "cryptocompare":
            closes, price = fetch_cryptocompare_closes(cfg["cc_symbol"])
        else:
            closes, price = fetch_twelvedata_closes(cfg["td_symbol"])

        signal, curr_rsi, diff = compute_signal(closes)
        result = {
            "symbol": key,
            "label": cfg["label"],
            "price": round(price, 4),
            "signal": signal,
            "rsi": round(curr_rsi, 1),
            "status": "LIVE",
            "updated": int(now),
        }
    except Exception as e:
        result = {
            "symbol": key,
            "label": cfg["label"],
            "price": None,
            "signal": "ERROR",
            "rsi": None,
            "status": f"OFFLINE ({e})",
            "updated": int(now),
        }

    _cache[key] = {"ts": now, "data": result}
    return result


@app.get("/api/signals")
def get_signals():
    results = {key: get_symbol_data(key, cfg) for key, cfg in SYMBOLS.items()}
    return {"generated_at": int(time.time()), "data": results}


@app.get("/api/signals/{symbol}")
def get_signal_one(symbol: str):
    symbol = symbol.upper()
    if symbol not in SYMBOLS:
        return {"error": f"Unknown symbol '{symbol}'. Valid: {list(SYMBOLS.keys())}"}
    return get_symbol_data(symbol, SYMBOLS[symbol])


@app.get("/")
def root():
    return {"status": "ok", "message": "Multi-Asset Signal Robot API running"}
