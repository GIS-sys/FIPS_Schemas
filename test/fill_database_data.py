import psycopg2
import csv
import os
import subprocess
import sys
from psycopg2 import sql

import util


def create_database(db_config: dict):
    output = subprocess.run(["createdb", "-h", db_config["host"], "-p", str(db_config["port"]),
                    "-U", db_config["user"], db_config["dbname"]],
                    env={"PGPASSWORD": db_config["password"]}, check=False, capture_output=True)
    error = output.stderr.decode()
    if not error:
        return
    if "already exists" in error:
        print(f"Database {db_config['dbname']} already exists")
        return
    raise Exception(str(output))


def iterate_saved_tables(output_dir: str) -> list[tuple[str, str]]:
    for filename in os.listdir(output_dir):
        if not filename.endswith(".csv"):
            continue
        table = filename[:-4]
        path = os.path.join(output_dir, filename)
        yield table, path


def create_table(cur, table: str, path: str):
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)
    quoted_cols = [sql.Identifier(h) for h in headers]
    create_stmt = sql.SQL("CREATE TABLE {} ({})").format(
        sql.Identifier(table),
        sql.SQL(", ").join(sql.SQL("{} TEXT").format(col) for col in quoted_cols)
    )
    cur.execute(create_stmt)


def fill_table(cur, table: str, path: str):
    with open(path, "r", encoding="utf-8") as f:
        cur.copy_expert(
            sql.SQL("COPY {} FROM STDIN WITH CSV HEADER").format(sql.Identifier(table)),
            f
        )


def main():
    DB_CONFIG = util.load_config(config_path=util.CONFIG_PATH_TEST)
    create_database(DB_CONFIG)

    with psycopg2.connect(**DB_CONFIG) as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            for table, path in iterate_saved_tables(output_dir=util.OUTPUT_DIR):
                create_table(cur=cur, table=table, path=path)
                fill_table(cur=cur, table=table, path=path)
                print(f"Imported {table}")


if __name__ == "__main__":
    main()

