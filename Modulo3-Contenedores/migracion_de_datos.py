import sqlite3
import pandas as pd
from sqlalchemy import create_engine


sqlite_file = "dbformula1/Formula1_4tables.sqlite"
postgres_url = "postgresql://test:test@localhost:5432/tempdb"


sqlite_conn = sqlite3.connect(sqlite_file)
pg_engine = create_engine(postgres_url)


tables = pd.read_sql_query(
    "SELECT name FROM sqlite_master WHERE type='table';", sqlite_conn
)["name"].tolist()

print(tables)


for table in tables:
    try:
        print(f"Migrando tabla: {table}")
        df = pd.read_sql_query(f"SELECT * FROM {table};", sqlite_conn)

        if table == "races":
            # Reemplaza caracteres nulos (\x00) en columnas de tipo string
            df = df.applymap(lambda x: x.replace("\x00", "") if isinstance(x, str) else x)

        df.to_sql(table, pg_engine, if_exists="replace", index=False)
        print(f"{table} migrada correctamente.\n")
    except Exception as e:
        print(f" Error al migrar {table}: {e}\n")


sqlite_conn.close()
