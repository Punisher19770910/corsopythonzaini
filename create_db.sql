drop table if exists Ordini_righe;
DROP TABLE IF EXISTS Ordini_testata;
CREATE TABLE IF NOT EXISTS Ordini_testata (
  num_ordine INTEGER PRIMARY KEY,
  data_ordine TEXT NOT NULL,
  cod_cliente TEXT NOT NULL,
  tot_prezzo REAL NOT NULL,
  tot_qty INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS Ordini_righe (
  num_ordine INTEGER NOT NULL,
  cod_articolo TEXT NOT NULL,
  qty INTEGER NOT NULL,
  prezzo_unitario REAL NOT NULL,
  FOREIGN KEY (num_ordine) REFERENCES Ordini_testata(num_ordine)
);
