from datetime import date, timedelta

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, insert, inspect

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

if __name__ == "__main__":
    engine = create_engine("sqlite:///Ordini.db", echo=False, future=True)  
    describe_table(engine, "Ordini_testata")