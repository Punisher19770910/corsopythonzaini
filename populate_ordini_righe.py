import random

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, insert


def main() -> None:
    engine = create_engine("sqlite:///Ordini.db", echo=False, future=True)
    metadata = MetaData()

    ordini_righe = Table(
        "Ordini_righe",
        metadata,
        Column("num_ordine", Integer, nullable=False),
        Column("cod_articolo", String(20), nullable=False),
        Column("qty", Integer, nullable=False),
        Column("prezzo_unitario", Float, nullable=False),
    )

    articoli = ["ART001", "ART002", "ART003", "ART004", "ART005", "ART006"]

    rows = []
    for num_ordine in range(1001, 1011):
        line_count = random.randint(2, 6)
        for line in range(line_count):
            rows.append(
                {
                    "num_ordine": num_ordine,
                    "cod_articolo": random.choice(articoli),
                    "qty": random.randint(1, 20),
                    "prezzo_unitario": round(random.uniform(5.0, 150.0), 2),
                }
            )

    with engine.begin() as connection:
        connection.execute(insert(ordini_righe), rows)

    print(f"Inseriti {len(rows)} record in Ordini_righe.")


if __name__ == "__main__":
    main()
