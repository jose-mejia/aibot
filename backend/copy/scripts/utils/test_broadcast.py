import requests
import json
import time
import random
import hmac
import hashlib

API_URL = "http://127.0.0.1:8000"
USERNAME = "master"
PASSWORD = "master123"

def login():
    print(f"🔑 Logando como {USERNAME}...")
    resp = requests.post(f"{API_URL}/token", data={"username": USERNAME, "password": PASSWORD})
    if resp.status_code == 200:
        token = resp.json()['token']
        print(f"✅ Login com sucesso! Token: {token[:10]}...")
        return token
    else:
        print(f"❌ Falha no login: {resp.text}")
        return None

def get_headers(token, payload):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    timestamp = str(int(time.time() * 1000))
    headers["X-Timestamp"] = timestamp
    
    # Payload string for signature must be minified json
    payload_str = json.dumps(payload, sort_keys=True, separators=(',', ':'))
    canonical = f"{timestamp}.{payload_str}"
    
    signature = hmac.new(
        token.encode('utf-8'), 
        canonical.encode('utf-8'), 
        hashlib.sha256
    ).hexdigest()
    
    headers["X-Signature"] = signature
    return headers

def send_signal(token):
    ticket = random.randint(100000, 999999)
    signal = {
        "master_ticket": ticket,
        "symbol": "BTCUSD",
        "type": "BUY",
        "volume": 0.01,
        "price": 50000.0,
        "sl": 49000.0,
        "tp": 52000.0,
        "time_msc": int(time.time() * 1000)
    }
    
    print(f"📡 Enviando sinal FAKE de COMPRA: Ticket {ticket}...")
    headers = get_headers(token, signal)
    
    try:
        # Usando json=signal o requests já faz o dump, mas precisamos garantir que o formato bata com a assinatura
        # Por isso vamos passar data=string
        payload_str = json.dumps(signal, sort_keys=True, separators=(',', ':'))
        
        resp = requests.post(
            f"{API_URL}/signal/broadcast", 
            data=payload_str, 
            headers=headers
        )
        
        if resp.status_code == 200:
            print("✅ Sinal enviado com sucesso! (Status 200)")
            print("Response:", resp.json())
        else:
            print(f"❌ Erro ao enviar sinal: {resp.status_code} - {resp.text}")
            
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")

if __name__ == "__main__":
    token = login()
    if token:
        time.sleep(1)
        send_signal(token)
