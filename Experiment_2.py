import sqlite3

conn = sqlite3.connect('TradingJournal.db')
connection_cursor = conn.cursor()
connection_cursor.execute("""
                                           DELETE FROM 'Intraday_Ledger';
                               """)
a= connection_cursor.fetchall()
print(a)
conn.commit()