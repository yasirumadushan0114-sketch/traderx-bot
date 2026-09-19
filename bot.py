import time, requests

TOKEN = "8754338829:AAHTLOl2Xt6ybUs61z0JSkCJKV8B0XD9hyg"
CHAT_ID = "5507036264"
COINS = ["BTCUSDT","ETHUSDT","SOLUSDT","BNBUSDT","NOTUSDT","DOGEUSDT","PEPEUSDT","WIFUSDT","BONKUSDT","FLOKIUSDT","SHIBUSDT","1000SATSUSDT","ORDIUSDT","ENAUSDT","WUSDT","TONUSDT","AVAXUSDT","ADAUSDT","XRPUSDT","TRXUSDT","LINKUSDT","DOTUSDT","MATICUSDT","NEARUSDT","APTUSDT","ARBUSDT","OPUSDT","INJUSDT","SEIUSDT","TIAUSDT"]

def ema(data, period):
    k=2/(period+1); e=data[0]
    for p in data[1:]: e=p*k+e*(1-k)
    return e

def send(msg):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id":CHAT_ID,"text":msg})

send("✅ TraderX Scanner Started! 30 Coins Check වෙනවා")

while True:
    for coin in COINS:
        try:
            r=requests.get(f"https://api.binance.com/api/v3/klines?symbol={coin}&interval=15m&limit=210",timeout=10).json()
            closes=[float(k[4]) for k in r]; highs=[float(k[2]) for k in r]; lows=[float(k[3]) for k in r]
            price=closes[-1]; e50=ema(closes,50); e200=ema(closes,200)
            lastHigh=None
            for i in range(5,len(r)-5):
                if all(highs[j]<=highs[i] for j in range(i-5,i+6)): lastHigh=highs[i]
            if lastHigh and price>lastHigh and e50>e200:
                send(f"🚀 BUY LABEL\nCoin: {coin}\nPrice: {price}\n15m")
        except: pass
        time.sleep(0.5)
    time.sleep(60)
