import psycopg2

try:
    conn = psycopg2.connect(
        host="10.2.53.15",
        port=5432,
        #database="smev_adapter_single",
        database="uad_int",
        user="gegorov",
        password="87zerkaLo22"
    )

    cur = conn.cursor()
    cur.execute("""
        SELECT table_name
        FROM information_schema.tables
    """)

    tables = cur.fetchall()
    print(tables)

    cur.close()
    conn.close()

except psycopg2.Error as e:
    print("Error: ", e)
