import requests
import re
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# ================== 配置区（这里不用改） ==================
# 下面三个会从GitHub Secrets读取，不用填在这里
SENDER_EMAIL = ""
RECEIVER_EMAIL = ""
GMAIL_APP_PASSWORD = ""
# ===========================================

URL = "https://www.gurufocus.com/economic_indicators/6778/nasdaq-100-pe-ratio"

def fetch_pe():
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(URL, headers=headers, timeout=15)
    resp.raise_for_status()
    
    match = re.search(r"was (\d+\.\d+) as of (\d{4}-\d{2}-\d{2})", resp.text)
    if not match:
        return None, None, None
    
    pe = float(match.group(1))
    date_str = match.group(2)
    median = 24.46   # 历史中位数
    
    if pe > 33:
        level = "明显高估（约70%+历史分位）"
        advice = "建议【高位少投或维持基准定投】"
    elif pe > 27:
        level = "偏高位"
        advice = "建议【正常或少投】"
    elif pe < 24:
        level = "低估"
        advice = "建议【低位多投】"
    else:
        level = "正常区间"
        advice = "建议【正常定投】"
    
    return pe, date_str, median, level, advice

def send_email(subject, body):
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(SENDER_EMAIL, GMAIL_APP_PASSWORD)
    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
    server.quit()

if __name__ == "__main__":
    pe, date_str, median, level, advice = fetch_pe()
    
    if pe is None:
        body = "❌ 抓取数据失败，请检查。"
        subject = "纳指100 PE日报 - 抓取失败"
    else:
        body = f"""纳斯达克100（NDX）PE历史分位日报

日期：{date_str}
当前 Trailing PE：{pe:.2f}
历史中位数（50%分位）：{median}

当前估值水平：{level}
操作建议：{advice}

说明：PE越高，分位越高。高位建议少投，低位建议多投。
当前参考（2026-04-14）：PE 36.45，属于明显高估。
"""
        subject = f"纳指100 PE日报 {date_str} - {level}"
    
    send_email(subject, body)
    print("邮件已发送！")
