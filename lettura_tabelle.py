import argparse
import json
from datetime import date

from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.exc import IntegrityError


def list_table_rows(engine, table_name: str) -> None:
    metadata = MetaData()
    metadata.reflect(bind=engine, only=[table_name])
    table = metadata.tables.get(table_name)
    if table is None:
        print(f"Tabella '{table_name}' non trovata nel database.")
        return

    with engine.connect() as conn:
        stmt = text(f'SELECT * FROM "{table_name}"')
        result = conn.execute(stmt)
        rows = result.mappings().all()

    print(f"\nValori in '{table_name}' ({len(rows)} righe):")
    print('-' * 60)
    for r in rows:
        print(dict(r))


def get_order_details(order_number: int) -> dict | None:
    engine = create_db_engine()
    metadata = MetaData()
    metadata.reflect(bind=engine, only=["Ordini_testata", "Ordini_righe"])
    testata = metadata.tables.get("Ordini_testata")
    righe = metadata.tables.get("Ordini_righe")

    if testata is None or righe is None:
        print("Una o entrambe le tabelle non sono state trovate nel database.")
        return

    with engine.connect() as conn:
        header = conn.execute(
            text("SELECT * FROM Ordini_testata WHERE num_ordine = :order_number"),
            {"order_number": order_number},
        ).mappings().first()

        if header is None:
            print(f"Ordine {order_number} non trovato.")
            return None

        detail_rows = conn.execute(
            text("SELECT * FROM Ordini_righe WHERE num_ordine = :order_number"),
            {"order_number": order_number},
        ).mappings().all()

    order_data = {
        "testata": dict(header),
        "righe": [dict(r) for r in detail_rows],
    }
    json_output = json.dumps(order_data, ensure_ascii=False, indent=2)
    print(json_output)
    #return json_output
    return order_data


def get_orders_by_article_code(article_code: str) -> list[dict]:
    engine = create_db_engine()
    metadata = MetaData()
    metadata.reflect(bind=engine, only=["Ordini_testata", "Ordini_righe"])
    testata = metadata.tables.get("Ordini_testata")
    righe = metadata.tables.get("Ordini_righe")

    if testata is None or righe is None:
        print("Le tabelle Ordini_testata o Ordini_righe non sono state trovate nel database.")
        return []

    with engine.connect() as conn:
        result = conn.execute(
            text(
                "SELECT t.*, r.* "
                "FROM Ordini_testata t "
                "JOIN Ordini_righe r ON t.num_ordine = r.num_ordine "
                "WHERE r.cod_articolo = :article_code "
                "ORDER BY t.num_ordine, r.cod_articolo"
            ),
            {"article_code": article_code},
        ).mappings().all()

    if not result:
        print(f"Nessun ordine trovato per il codice articolo '{article_code}'.")
        return []

    orders: list[dict] = []
    current_order_number = None
    current_order = None

    for row in result:
        order_number = row["num_ordine"]
        if order_number != current_order_number:
            if current_order is not None:
                orders.append(current_order)

            current_order_number = order_number
            current_order = {
                "testata": {
                    key: row[key]
                    for key in row.keys()
                    if key in testata.columns.keys()
                },
                "righe": [],
            }

        detail_row = {
            key: row[key]
            for key in row.keys()
            if key in righe.columns.keys()
        }
        current_order["righe"].append(detail_row)

    if current_order is not None:
        orders.append(current_order)

    print(json.dumps(orders, ensure_ascii=False, indent=2))
    return orders


def get_available_order_numbers() -> list[int]:
    engine = create_db_engine()
    metadata = MetaData()
    metadata.reflect(bind=engine, only=["Ordini_testata"])
    testata = metadata.tables.get("Ordini_testata")
    if testata is None:
        return []

    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT num_ordine FROM Ordini_testata ORDER BY num_ordine")
        )
        return [row[0] for row in result.fetchall()]


def ask_int(prompt: str, default: int | None = None) -> int | None:
    while True:
        raw = input(prompt).strip()
        if raw == "" and default is not None:
            return default
        try:
            return int(raw)
        except ValueError:
            print("Valore non valido. Inserisci un intero.")


def ask_float(prompt: str, default: float | None = None) -> float | None:
    while True:
        raw = input(prompt).strip()
        if raw == "" and default is not None:
            return default
        try:
            return float(raw)
        except ValueError:
            print("Valore non valido. Inserisci un numero.")


def add_order_interactive() -> None:
    print("\nAggiungi un nuovo ordine:")
    num_ordine = ask_int("Numero ordine: ")
    if num_ordine is None:
        print("Numero ordine non valido. Annullato.")
        return

    data_ordine = input("Data ordine (YYYY-MM-DD, vuoto = oggi): ").strip() or date.today().isoformat()
    cod_cliente = input("Codice cliente: ").strip() or "CL000"
    tot_qty = ask_int("Totale quantità: ") or 0
    tot_prezzo = ask_float("Totale prezzo: ") or 0.0

    righe = []
    numero_righe = ask_int("Quante righe vuoi inserire? ") or 0
    for idx in range(1, numero_righe + 1):
        print(f"\nRiga {idx}:")
        cod_articolo = input("  Codice articolo: ").strip() or f"ART{idx:03d}"
        qty = ask_int("  Quantità: ") or 0
        prezzo_unitario = ask_float("  Prezzo unitario: ") or 0.0
        righe.append({
            "cod_articolo": cod_articolo,
            "qty": qty,
            "prezzo_unitario": prezzo_unitario,
        })

    order_data = {
        "testata": {
            "num_ordine": num_ordine,
            "data_ordine": data_ordine,
            "cod_cliente": cod_cliente,
            "tot_prezzo": tot_prezzo,
            "tot_qty": tot_qty,
        },
        "righe": righe,
    }

    insert_order_from_dict(order_data)
 
def insert_order_from_dict(order_data: dict) -> int:
    engine = create_db_engine()
    required_keys = {"testata", "righe"}
    if not required_keys.issubset(order_data):
        raise ValueError("Il dizionario deve contenere le chiavi 'testata' e 'righe'.")

    header_data = order_data["testata"]
    line_items = order_data["righe"]
    if "num_ordine" not in header_data:
        raise ValueError("Il dizionario 'testata' deve contenere 'num_ordine'.")

    order_number = header_data["num_ordine"]
    prepared_rows = []
    for item in line_items:
        row = dict(item)
        if "num_ordine" not in row:
            row["num_ordine"] = order_number
        prepared_rows.append(row)

    metadata = MetaData()
    metadata.reflect(bind=engine, only=["Ordini_testata", "Ordini_righe"])
    testata = metadata.tables.get("Ordini_testata")
    righe = metadata.tables.get("Ordini_righe")

    if testata is None or righe is None:
        raise RuntimeError("Le tabelle Ordini_testata o Ordini_righe non esistono nel database.")

    with engine.begin() as conn:
        try:
            conn.execute(
                text(
                    "INSERT INTO Ordini_testata "
                    "(num_ordine, data_ordine, cod_cliente, tot_prezzo, tot_qty) "
                    "VALUES (:num_ordine, :data_ordine, :cod_cliente, :tot_prezzo, :tot_qty)"
                ),
                header_data,
            )
            line_insert = text(
                "INSERT INTO Ordini_righe "
                "(num_ordine, cod_articolo, qty, prezzo_unitario) "
                "VALUES (:num_ordine, :cod_articolo, :qty, :prezzo_unitario)"
            )
            conn.execute(line_insert, prepared_rows)
            print(f"Ordine {order_number} inserito con {len(prepared_rows)} righe.")
        except IntegrityError as exc:
            raise RuntimeError(f"Errore di integrità durante l'inserimento: {exc}") from exc
    return order_number


def insert_order(order_data: dict, db_path: str = "Ordini.db") -> None:
    """Insert a single order into the database.

    Accepts order dicts with keys either `testata` or `header` and a `righe` list.
    """
    if not isinstance(order_data, dict):
        raise ValueError("order_data deve essere un dizionario")

    if "testata" not in order_data:
        raise ValueError("Il dizionario deve contenere la chiave 'testata'.")

    od = order_data
    engine = create_db_engine(db_path)
    try:
        insert_order_from_dict(engine, od)
    except Exception as exc:
        print(f"Errore durante l'inserimento ordine {od.get('testata', {}).get('num_ordine')}: {exc}")
        raise


def insert_orders(orders: list[dict], db_path: str = "Ordini.db") -> None:
    """Insert multiple orders (list of dicts) into the database using a single engine.

    Each item may use `header` or `testata` as the header key.
    """
    if not isinstance(orders, (list, tuple)):
        raise ValueError("orders deve essere una lista di dizionari")

    engine = create_db_engine(db_path)
    for order_data in orders:
        if not isinstance(order_data, dict):
            raise ValueError("Ogni elemento di orders deve essere un dizionario")
        if "testata" not in order_data:
            raise ValueError("Ogni dizionario deve contenere la chiave 'testata'.")
        try:
            insert_order_from_dict(engine, order_data)
        except Exception as exc:
            print(f"Errore inserimento ordine {order_data.get('testata', {}).get('num_ordine')}: {exc}")
            raise

def create_db_engine(db_path: str = "Ordini.db"):
    return create_engine(f"sqlite:///{db_path}", echo=False, future=True)

def main() -> None:
    parser = argparse.ArgumentParser(description="Stampa dati ordini da Ordini.db")
    parser.add_argument("--order", "-o", type=int, help="Numero dell'ordine da estrarre")
    args = parser.parse_args()

    engine = create_db_engine()

    if args.order is not None:
        get_order_details(args.order)
        return

    action = input("Vuoi aggiungere un ordine (A) o leggere un ordine specifico (L)? [L]: ").strip().lower()
    if action == "a":
        add_order_interactive()
        return

    available_orders = get_available_order_numbers()
    if available_orders:
        print("Ordini disponibili:", ", ".join(str(n) for n in available_orders))
        selected = input("Inserisci il numero dell'ordine da visualizzare (premi invio per mostrare tutte le tabelle): ")
        if selected.strip():
            try:
                order_number = int(selected.strip())
                get_order_details(order_number)
                return
            except ValueError:
                print("Valore non valido. Inserisci un numero d'ordine intero.")
    else:
        print("Nessun ordine disponibile in Ordini_testata.")

    list_table_rows(engine, "Ordini_testata")
    list_table_rows(engine, "Ordini_righe")


if __name__ == "__main__":
    main()
