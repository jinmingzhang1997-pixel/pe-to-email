import requests
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

# ====== 填你自己的 ======
SENDER_EMAIL = "jinmingzhang1997@gmail.com"
RECEIVER_EMAIL = "jinmingzhang1997@gmail.com"
GMAIL_APP_PASSWORD = "xoddgfuthhvwbdan"
API_KEY = "TOJRJ2NRZ6CWOKFV"
# =======================

SYMBOL = "QQQ"

def get_prices():
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{SYMBOL}?range=1y&interval=1d"
    data = requests.get(url).json()

    result = data["chart"]["result"][0]
    prices = result["indicators"]["quote"][0]["close"]

    prices = [p for p in prices if p is not None]
    return prices

def calc_percentile(prices):
    current = prices[-1]
    return round((np.array(prices) < current).mean() * 100, 2)

def get_advice(pct):
    if pct > 75:
        return "高位：少投"
    elif pct < 30:
        return "低位：多投"
    return "正常：定投"

def main():
    prices = get_prices()
    pct = calc_percentile(prices)
    advice = get_advice(pct)

    content = f"""
纳指100（QQQ）定投信号

日期：{datetime.now().strftime('%Y-%m-%d')}

价格分位：{pct}%

建议：{advice}
"""

    print(content)

if __name__ == "__main__":
    main()
