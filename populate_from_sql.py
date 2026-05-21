from pathlib import Path
from sqlalchemy import create_engine, text


def populate_from_sql(sql_file: str = "dati_popolamento.sql") -> None:
    engine = create_engine("sqlite:///Ordini.db", echo=False, future=True)
    sql_path = Path(sql_file)
    if not sql_path.exists():
        print(f"File SQL '{sql_file}' non trovato.")
        return

    sql = sql_path.read_text()

    with engine.connect() as conn:
        with conn.begin():
            for stmt in (s.strip() for s in sql.split(";") if s.strip()):
                conn.execute(text(stmt))

    print(f"Eseguiti gli INSERT da '{sql_file}' su Ordini.db.")


if __name__ == "__main__":
    populate_from_sql()
