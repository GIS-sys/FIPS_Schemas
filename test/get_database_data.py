import psycopg2
import csv
import os
import shutil
from psycopg2 import sql

import util


def create_folder_structure(output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    for f in os.listdir(output_dir):
        if f.endswith(".csv"):
            os.unlink(os.path.join(output_dir, f))


def fetch_tables(cur) -> list[str]:
    cur.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
          AND table_type = 'BASE TABLE'
        ORDER BY table_name
    """)
    return [row[0] for row in cur.fetchall()]


def fetch_columns(cur, table: str) -> list[str]:
    cur.execute("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = %s
        ORDER BY ordinal_position
    """, (table,))
    return [row[0] for row in cur.fetchall()]


def fetch_rows(cur, table: str, limit: int) -> list[list]:
    quoted = sql.Identifier(table)
    cur.execute(sql.SQL("SELECT * FROM {} LIMIT %s").format(quoted), [limit])
    return cur.fetchall()


def save(table: str, columns: list[str], rows: list[list], output_dir: str):
    path = os.path.join(output_dir, f"{table}.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(rows)


def archive(output_dir: str):
    shutil.make_archive(output_dir, "zip", output_dir)


def main():
    DB_CONFIG = util.load_config(config_path=util.CONFIG_PATH_PROD)
    create_folder_structure(output_dir=util.OUTPUT_DIR)

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            tables = fetch_tables(cur=cur)
            print(tables)
            for table in tables:
                columns = fetch_columns(cur=cur, table=table)
                rows = fetch_rows(cur=cur, table=table, limit=util.LIMIT_ROWS)
                save(table=table, columns=columns, rows=rows, output_dir=util.OUTPUT_DIR)
                print(f"Exported {len(rows)} rows from {table}")
    archive(output_dir=util.OUTPUT_DIR)


if __name__ == "__main__":
    main()

