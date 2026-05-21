-- Inserimenti esempio per Ordini_testata
INSERT INTO Ordini_testata (num_ordine, data_ordine, cod_cliente, tot_prezzo, tot_qty) VALUES (1001, '2025-01-15', 'CL001', 450.75, 12);
INSERT INTO Ordini_testata (num_ordine, data_ordine, cod_cliente, tot_prezzo, tot_qty) VALUES (1002, '2025-02-03', 'CL002', 1200.00, 30);
INSERT INTO Ordini_testata (num_ordine, data_ordine, cod_cliente, tot_prezzo, tot_qty) VALUES (1003, '2025-03-21', 'CL003', 89.50, 3);
INSERT INTO Ordini_testata (num_ordine, data_ordine, cod_cliente, tot_prezzo, tot_qty) VALUES (1004, '2025-04-05', 'CL004', 760.20, 18);
INSERT INTO Ordini_testata (num_ordine, data_ordine, cod_cliente, tot_prezzo, tot_qty) VALUES (1005, '2025-05-11', 'CL005', 320.00, 7);

-- Inserimenti esempio per Ordini_righe
INSERT INTO Ordini_righe (num_ordine, cod_articolo, qty, prezzo_unitario) VALUES (1001, 'ART001', 2, 25.50);
INSERT INTO Ordini_righe (num_ordine, cod_articolo, qty, prezzo_unitario) VALUES (1001, 'ART003', 10, 30.00);
INSERT INTO Ordini_righe (num_ordine, cod_articolo, qty, prezzo_unitario) VALUES (1002, 'ART002', 20, 40.00);
INSERT INTO Ordini_righe (num_ordine, cod_articolo, qty, prezzo_unitario) VALUES (1002, 'ART004', 10, 20.00);
INSERT INTO Ordini_righe (num_ordine, cod_articolo, qty, prezzo_unitario) VALUES (1003, 'ART005', 3, 29.83);
INSERT INTO Ordini_righe (num_ordine, cod_articolo, qty, prezzo_unitario) VALUES (1004, 'ART006', 5, 50.00);
INSERT INTO Ordini_righe (num_ordine, cod_articolo, qty, prezzo_unitario) VALUES (1004, 'ART001', 13, 15.40);
INSERT INTO Ordini_righe (num_ordine, cod_articolo, qty, prezzo_unitario) VALUES (1005, 'ART002', 7, 45.71);
