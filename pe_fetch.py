import requests
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

# ====== 填你自己的 ======
SENDER_EMAIL = "你的gmail@gmail.com"
RECEIVER_EMAIL = "你的gmail@gmail.com"
GMAIL_APP_PASSWORD = "你的应用密码"
API_KEY = "你的AlphaVantageKey"
# =======================

SYMBOL = "QQQ"

def fetch_pe():
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={SYMBOL}&apikey={API_KEY}"
    data = requests.get(url).json()

    pe = data.get("PERatio")
    if not pe:
        return None, None, None, None

    pe = float(pe)

    # 分位判断（简化版）
    if pe > 30:
        level = "高估（约70%+）"
        advice = "少投"
    elif pe > 25:
        level = "偏高"
        advice = "正常或少投"
    elif pe < 20:
        level = "低估"
        advice = "多投"
    else:
        level = "正常"
        advice = "定投"

    return pe, level, advice, datetime.now().strftime("%Y-%m-%d")

def send_email(content):
    msg = MIMEText(content, "plain", "utf-8")
    msg["Subject"] = "纳指100估值日报"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, GMAIL_APP_PASSWORD)
        server.send_message(msg)

def main():
    pe, level, advice, date = fetch_pe()

    if pe is None:
        content = "❌ 获取数据失败"
    else:
        content = f"""
📊 纳指100估值日报（QQQ）

日期：{date}
PE：{pe}

估值：{level}
建议：{advice}

说明：
使用QQQ代替纳指100
"""

    send_email(content)

if __name__ == "__main__":
    main()
