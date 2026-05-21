from pathlib import Path
from sqlalchemy import create_engine, text


def create_database_from_sql(sql_file: str = "create_db.sql") -> None:
    engine = create_engine("sqlite:///Ordini.db", echo=False, future=True)
    sql_path = Path(sql_file)
    if not sql_path.exists():
        print(f"File SQL '{sql_file}' non trovato.")
        return

    sql = sql_path.read_text()

    with engine.connect() as conn:
        with conn.begin():
            # Split statements on semicolon and execute non-empty ones
            for stmt in (s.strip() for s in sql.split(";") if s.strip()):
                conn.execute(text(stmt))

    print(f"Database 'Ordini.db' creato eseguendo '{sql_file}'.")


if __name__ == "__main__":
    create_database_from_sql()
