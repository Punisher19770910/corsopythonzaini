from datetime import date, timedelta
import random

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, insert, inspect
from sqlalchemy.exc import IntegrityError


def generate_random_date(start_year: int = 2024) -> str:
    start = date(start_year, 1, 1)
    end = date(start_year, 12, 31)
    random_days = random.randrange((end - start).days + 1)
    return (start + timedelta(days=random_days)).isoformat()


def describe_table(engine, table_name: str) -> None:
    inspector = inspect(engine)
    columns = inspector.get_columns(table_name)
    pk = inspector.get_pk_constraint(table_name).get("constrained_columns", [])
    fks = inspector.get_foreign_keys(table_name)

    print(f"Struttura della tabella '{table_name}':")
    print("-" * 50)
    for column in columns:
        print(
            f"{column['name']:20} {column['type']:20} "
            f"nullable={column['nullable']} default={column.get('default')}")

    if pk:
        print(f"Primary key: {pk}")
    if fks:
        for fk in fks:
            print(f"Foreign key: {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
    print("-" * 50)
    print()


def main() -> None:
    engine = create_engine("sqlite:///Ordini.db", echo=False, future=True)
    metadata = MetaData()

    ordini_testata = Table(
        "Ordini_testata",
        metadata,
        Column("num_ordine", Integer, primary_key=True),
        Column("data_ordine", String(10), nullable=False),
        Column("cod_cliente", String(20), nullable=False),
        Column("tot_prezzo", Float, nullable=False),
        Column("tot_qty", Integer, nullable=False),
    )

    clienti = ["CL001", "CL002", "CL003", "CL004", "CL005"]

    rows = []
    for idx in range(1, 11):
        num_ordine = 1000 + idx
        tot_qty = random.randint(5, 80)
        tot_prezzo = round(random.uniform(100.0, 2500.0), 2)

        rows.append(
            {
                "num_ordine": num_ordine,
                "data_ordine": generate_random_date(2025),
                "cod_cliente": random.choice(clienti),
                "tot_prezzo": tot_prezzo,
                "tot_qty": tot_qty,
            }
        )

    with engine.begin() as connection:
        try:
            # Use SQLite "OR IGNORE" to skip rows with duplicate primary keys
            connection.execute(insert(ordini_testata).prefix_with("OR IGNORE"), rows)
            print("Inserimento eseguito (i record duplicati sono stati ignorati).")
        except IntegrityError as e:
            print("Errore di integrità durante l'inserimento:", e)
        except Exception as e:
            print("Errore durante l'inserimento:", e)

    print(f"Tentati inserimenti: {len(rows)} in Ordini_testata.")
    #describe_table(engine, "Ordini_testata")


if __name__ == "__main__":
    main()
