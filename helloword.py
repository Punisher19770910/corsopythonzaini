import ordini #import file ordini.py e importi tutto ciò che è in esso contenuto
#from ordini import ordine_dict #importo solo ordine_dict da ordini.pàyà

import statistics as stats
import os
import matplotlib.pyplot as plt

import pandas as pd

import sqlalchemy as sa

def create_flights_engine(db_path: str = "flights.db") -> sa.engine.Engine:
    """Crea e restituisce l'engine SQLAlchemy per il DB SQLite flights.db."""
    database_url = f"sqlite:///{db_path}"
    engine = sa.create_engine(database_url, echo=False, future=True)
    return engine


def query_airlines(engine: sa.engine.Engine):
    """Esegue una query sulla tabella airlines e restituisce tutte le righe."""
    metadata = sa.MetaData()
    airlines = sa.Table("airlines", metadata, autoload_with=engine)
    stmt = sa.select(airlines)
    with engine.connect() as conn:
        result = conn.execute(stmt)
        return result.mappings().all()

#sql alchemy è un modulo per interagire con database in modo più semplice e pythonico, permette di scrivere query SQL usando il linguaggio Python e gestisce la connessione al database in modo efficiente.
def query_airlines_pandas(engine: sa.engine.Engine) -> pd.DataFrame:
    """Esegue una query SQL usando pandas.read_sql sulla tabella airlines."""
    query = "SELECT * FROM airlines"
    return pd.read_sql(query, engine)


def main():
    print("Hello, World!")

#sudo apt update -> aggiorno la lista dei pacchetti disponibili
#sudo apt install python3-pip -> installo pip per gestire i pacchetti python
#python3 -m pip install --user --upgrade pip -> aggiorno pip
#pip list -> mostra i pacchetti installati
#pip install pandas -> installo modulo pandas per la gestione dei dati
#sudo apt install python3-venv -> installo modulo per creare ambienti virtuali
#python3 -m venv myenv -> creo ambiente virtuale
#source myenv/bin/activate -> attivo l'ambiente virtuale
# pip install pandas -> installo pandas nell'ambiente virtuale (default ulktima versione)

def fun2():
    print("secondo print")



resi = [
    {"codice_reso": "R001", "quantita_resa": 2},
    {"codice_reso": "R002", "quantita_resa": 1},
]

print(ordini.ordine_dict["totale"])
tval = 0


#ordine["resi"] = sorted(resi, key=lambda t: t["quantita_resa"], reverse=Tr


if __name__ == "__main__":
    main()
    fun2()
    print("Calcolo tot ordine")
    ordini.ordine_dict["totale"] = ordini.rtot(tval)
    print(ordini.ordine_dict["totale"])
    engine = create_flights_engine()
    airlines_rows = query_airlines(engine)
    print("Airlines rows:", airlines_rows)
    airlines_df = query_airlines_pandas(engine)
    print("Airlines DataFrame:\n", airlines_df)

df = pd.read_csv("dati.csv") #leggo un file csv con pandas, df è un dataframe, una struttura dati simile a una tabella
print(df) #stampo il dataframe

print("DF_FILTRATO")
df_filtrato = df[df["nome_prodotto"] == "Zaino"] #filtro il dataframe per mostrare solo le righe in cui colonna1 è uguale a "Zaino"
print(df_filtrato)

ax = df_filtrato.plot(kind="bar", x="nome_prodotto", y="quantità") #creo un grafico a barre con i dati filtrati, x è la colonna nome_prodotto e y è la colonna quantità
fig = ax.get_figure()
fig.savefig("plot_csv.jpeg", dpi=300, bbox_inches="tight")
plt.close(fig)



print("finito!")
