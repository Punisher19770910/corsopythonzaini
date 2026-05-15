def rtot(tval):
    for i in range(len(ordine_dict["righe"])):
        tval = tval + (ordine_dict["righe"][i]["qta"] * ordine_dict["righe"][i]["prezzou"])
    print(tval)
    return tval

ordine_dict = {
    "nome": "pippo",
    "num_ordine": 12345,
    "data_ord": "31/12/2026",
    "totale": 1234.87,
    "tot_qty": 200,
    "righe": [
        {"numr": 1, "qta": 5, "prezzou": 30},
        {"numr": 2, "qta": 10, "prezzou": 10},
    ],
}