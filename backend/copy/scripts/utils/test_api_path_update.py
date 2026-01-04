import requests
import sqlite3
import os
import json

API_URL = "http://127.0.0.1:8000"
DB_PATH = os.path.join("api_server", "aibot.db")

def test_update_path():
    print("🧪 TEST: Updating MT5 Path via API (Self-Update)...")

    # 1. Login as Client
    session = requests.Session()
    login_payload = {"username": "client", "password": "123123"}
    
    try:
        res = session.post(f"{API_URL}/token", data=login_payload)
        if res.status_code != 200:
            print(f"❌ Login Failed: {res.text}")
            return
        
        token = res.json().get("access_token")
        print("✅ Login Successful")
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Send Update Request (PATCH /users/me or PUT /users/me depending on implementation, here it is PATCH logic usually but endpoint is POST/PUT often. 
        # Check handler: pub async fn update_me (...) -> Response
        # Route in api_server/src/main.rs needed check? Usually mapped to PATCH or PUT. 
        # Assuming PATCH /users/me based on logs seen earlier: "DEBUG request{method=PATCH uri=/users/me"
        
        new_path = r"C:\Test\MT5\terminal64.exe"
        update_payload = {"mt5_path": new_path}
        
        # Using PATCH as per logs
        res = session.patch(f"{API_URL}/users/me", json=update_payload, headers=headers)
        
        if res.status_code != 200:
            print(f"❌ Update Failed. Status: {res.status_code}, Body: {res.text}")
        else:
            print(f"✅ API Response: 200 OK. Body: {res.text}")

        # 3. Verify in DB
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT mt5_path FROM users WHERE username='client'")
        row = cursor.fetchone()
        conn.close()
        
        if row and row[0] == new_path:
            print(f"✅ SUCCESS: Database has updated path: {row[0]}")
        else:
            actual = row[0] if row else "None"
            print(f"❌ FAILURE: Database has: {actual} (Expected: {new_path})")
            print("   -> The API fix didn't work or the server wasn't restarted/recompiled.")

    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_update_path()
