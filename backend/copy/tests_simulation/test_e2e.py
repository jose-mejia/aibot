import asyncio
import aiohttp
import json
import subprocess
import time
import sys
import argparse

# Configuration
API_URL = "http://127.0.0.1:8000"

async def test_flow():
    print("[TEST] Waiting for API Server to be ready...")
    async with aiohttp.ClientSession() as session:
        # Wait for boot
        for i in range(10):
            try:
                async with session.get(f"{API_URL}/docs") as resp:
                    if resp.status == 200:
                        print("[TEST] API Server is Up!")
                        break
            except:
                time.sleep(1)
        else:
             print("[TEST] API Server failed to start.")
             return

        # 1. Register Master (Assuming empty DB or Seed logic works)
        # Using the new /users/public endpoint
        print("[TEST] Registering Master...")
        TOKEN_MASTER = None
        try:
             async with session.post(f"{API_URL}/users/public", json={
                 "username": "master_test", 
                 "password": "password123", 
                 "role": "MASTER",
                 "allowed_mt5_id": "999999" 
             }) as resp:
                 if resp.status == 200:
                     data = await resp.json()
                     TOKEN_MASTER = data['access_token']
                     print(f"[TEST] Master Registered. Token: {TOKEN_MASTER[:10]}...")
                 elif resp.status == 400:
                     # Already exists, try login
                     print("[TEST] Master exists, logging in...")
                     async with session.post(f"{API_URL}/token", data={"username": "master_test", "password": "password123"}) as lresp:
                         if lresp.status == 200:
                             d = await lresp.json()
                             TOKEN_MASTER = d['access_token']
                         else:
                             print(f"[TEST] Failed to login Master: {await lresp.text()}")
                             return
                 else:
                     print(f"[TEST] Failed to register Master: {await resp.text()}")
                     # If we can't create master because DB works and we are not first, we need Admin.
                     # For this isolated test, assume clean DB or seed allowed.
        except Exception as e:
             print(f"[TEST] Exception Master Reg: {e}")
             return

        if not TOKEN_MASTER:
            print("[TEST] Could not obtain Master Token. Aborting.")
            return

        # 2. Register Client
        print("[TEST] Registering Client...")
        TOKEN_CLIENT = None
        # ... logic similar to master ...
        async with session.post(f"{API_URL}/users/public", json={
             "username": "client_test", 
             "password": "password123", 
             "role": "FOLLOWER",
             "allowed_mt5_id": "888888" 
         }) as resp:
             if resp.status == 200:
                 data = await resp.json()
                 TOKEN_CLIENT = data['access_token']
                 print(f"[TEST] Client Registered. Token: {TOKEN_CLIENT[:10]}...")
             elif resp.status == 400:
                 async with session.post(f"{API_URL}/token", data={"username": "client_test", "password": "password123"}) as lresp:
                        if lresp.status == 200:
                             d = await lresp.json()
                             TOKEN_CLIENT = d['access_token']


        if not TOKEN_CLIENT:
             print("[TEST] No Client Token.")
             return

        # 3. Simulate Signal Flow
        # Connect Client WebSocket
        import websockets
        ws_url = f"ws://127.0.0.1:8000/ws?token={TOKEN_CLIENT}"
        print(f"[TEST] Connecting Client WS: {ws_url}")
        
        async with websockets.connect(ws_url) as ws:
             print("[TEST] Client Connected to WS.")
             
             # Wait for Snapshot
             msg = await ws.recv()
             print(f"[TEST] Client Received Initial: {msg}")
             
             # Master Sends Signal
             print("[TEST] Master sending signal...")
             signal_payload = {
                 "master_ticket": 12345,
                 "symbol": "EURUSD",
                 "type": "BUY",
                 "volume": 0.1,
                 "price": 1.1000,
                 "sl": 1.0900,
                 "tp": 1.1100
             }
             
             async with session.post(
                 f"{API_URL}/signal/broadcast", 
                 json=signal_payload, 
                 headers={"Authorization": f"Bearer {TOKEN_MASTER}"}
             ) as sresp:
                 print(f"[TEST] Master Send Status: {sresp.status}")
                 if sresp.status != 200:
                     print(await sresp.text())
            
             # Client Should Receive
             print("[TEST] Client waiting for signal...")
             msg = await asyncio.wait_for(ws.recv(), timeout=5.0)
             print(f"[TEST] Client Received: {msg}")
             
             data = json.loads(msg)
             if data.get('event') == 'OPEN' and data['data']['ticket'] == 12345:
                 print("[SUCCESS] Signal Flow Verified!")
             else:
                 print("[FAILURE] Received wrong data.")

async def main():
    # We assume the Server (Rust) is ALREADY RUNNING on localhost:8000
    # User should run `cargo run` in api_server before this.
    try:
        await test_flow()
    except Exception as e:
        print(f"[TEST] Failure: {e}")
        
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
