import sqlite3
conn = sqlite3.connect('api_server/aibot.db')
c = conn.cursor()
rows = c.execute('SELECT ticket, symbol, type, volume, status FROM signals ORDER BY ticket DESC LIMIT 10').fetchall()
print("\n=== ÚLTIMOS SINAIS NO BANCO ===")
if rows:
    for r in rows:
        print(f"Ticket: {r[0]}, Symbol: {r[1]}, Type: {r[2]}, Volume: {r[3]}, Status: {r[4]}")
else:
    print("Nenhum sinal encontrado")
conn.close()
