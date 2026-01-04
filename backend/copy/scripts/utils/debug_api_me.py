import requests

API_URL = "http://127.0.0.1:8000"
USERNAME = "master"
PASSWORD = "master123"

def check_me():
    print(f"🔑 Logando como {USERNAME}...")
    try:
        resp = requests.post(f"{API_URL}/token", data={"username": USERNAME, "password": PASSWORD})
        if resp.status_code == 200:
            token = resp.json()['token']
            print(f"✅ Login OK. Token: {token[:10]}...")
            
            headers = {"Authorization": f"Bearer {token}"}
            me_resp = requests.get(f"{API_URL}/users/me", headers=headers)
            print(f"🔍 Resposta de /users/me: {me_resp.json()}")
            
            mt5_id = me_resp.json().get('allowed_mt5_id')
            role = me_resp.json().get('role')
            print(f"👉 ID ESPERADO PELA API: {mt5_id}")
            print(f"👉 ROLE: {role}")
        else:
            print(f"❌ Login falhou: {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")

if __name__ == "__main__":
    check_me()
