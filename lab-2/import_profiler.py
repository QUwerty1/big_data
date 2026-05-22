import pyodbc
import csv
import os

csv_path = os.path.expanduser('profiler_before.csv')

conn = pyodbc.connect(
    'DRIVER={ODBC Driver 18 for SQL Server};'
    'SERVER=127.0.0.1,1433;'
    'DATABASE=tempdb;'
    'UID=sa;'
    'PWD=gRdpW6eEFqNG;'
    'TrustServerCertificate=Yes'
)
cursor = conn.cursor()

with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # заголовок
    inserted = 0
    for row in reader:
        if len(row) != 15:
            continue
        cursor.execute("""
            INSERT INTO tempdb.dbo.ProfilerResults
            (EventClass, TextData, ApplicationName, NTUserName, LoginName,
             ClientProcessID, SPID, StartTime, CPU, Reads, Writes, Duration,
             DatabaseID, DatabaseName, HostName)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, row)
        inserted += 1

conn.commit()
print(f"Импортировано строк: {inserted}")
conn.close()