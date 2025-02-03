import psycopg2

conn = psycopg2.connect(host = "localhost", port = 5432, dbname = "vehicle", user = "postgres", password = "password")
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS motors (
    maker CHAR,
    model CHAR,
    variant CHAR,
    transmission CHAR,
    engine CHAR,
    year INTEGER,
    mileage INTEGER
);
    """)

cur.execute("""CREATE TABLE IF NOT EXISTS trucks (
    maker CHAR,
    model CHAR,
    variant CHAR,
    transmission CHAR,
    engine CHAR,
    year INTEGER,
    mileage INTEGER
);
    """)

conn.commit()

cur.close()
conn.close()