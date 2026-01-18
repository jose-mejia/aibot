import MetaTrader5 as mt5
import os

# Caminho hardcoded conforme solicitado
MT5_PATH = r"C:\Program Files\IC Markets Global01\terminal64.exe"
EXPECTED_ID = 7409735

print(f"--- DIAGNOSTIC SCRIPT: RAW MT5 CONNECTION ---")
print(f"Checking if file exists at path: {MT5_PATH}")

if os.path.exists(MT5_PATH):
    print("File EXISTS on disk.")
else:
    print("WARNING: File NOT FOUND on disk check. mt5.initialize might fail with -10004.")

print(f"Target Path: {MT5_PATH}")
print(f"Target ID: {EXPECTED_ID}")

print("\n--- ACTION: mt5.initialize(path=MT5_PATH) ---")
try:
    if not mt5.initialize(path=MT5_PATH):
        error = mt5.last_error()
        print(f"❌ FAILED to Initialize.")
        print(f"Error Code: {error}")
        print(f"Decoded: {error}")
    else:
        print("✅ SUCCESS: mt5.initialize() returned True.")
        
        info = mt5.account_info()
        if info:
            print(f"CONNECTED LOGIN: {info.login}")
            print(f"SERVER: {info.server}")
            print(f"BALANCE: {info.balance}")
            
            if info.login == EXPECTED_ID:
                print("✅ MATCH: Identity Confirmed.")
            else:
                print(f"❌ MISMATCH: Connected to WRONG account! Expected {EXPECTED_ID}.")
        else:
            print("⚠️ WARNING: Connected but account_info is None (Terminal starting up?)")

        mt5.shutdown()

except Exception as e:
    print(f"CRITICAL EXCEPTION: {e}")

print("--- END DIAGNOSTIC ---")
