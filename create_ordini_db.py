from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, ForeignKey


def create_database() -> None:
    engine = create_engine("sqlite:///Ordini.db", echo=False, future=True)
    metadata = MetaData()

    Table(
        "Ordini_testata",
        metadata,
        Column("num_ordine", Integer, primary_key=True),
        Column("data_ordine", String(10), nullable=False),
        Column("cod_cliente", String(20), nullable=False),
        Column("tot_prezzo", Float, nullable=False),
        Column("tot_qty", Integer, nullable=False),
    )

    Table(
        "Ordini_righe",
        metadata,
        Column("num_ordine", Integer, ForeignKey("Ordini_testata.num_ordine"), nullable=False),
        Column("cod_articolo", String(20), nullable=False),
        Column("qty", Integer, nullable=False),
        Column("prezzo_unitario", Float, nullable=False),
    )

    metadata.create_all(engine)
    print("Database 'Ordini.db' creato con le tabelle Ordini_testata e Ordini_righe.")


if __name__ == "__main__":
    create_database()
