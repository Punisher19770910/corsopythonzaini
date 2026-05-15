import ordini #import file ordini.py e importi tutto ciò che è in esso contenuto
#from ordini import ordine_dict #importo solo ordine_dict da ordini.py

def main():
    print("Hello, World!")


def fun2():
    print("secondo print")



resi = [
    {"codice_reso": "R001", "quantita_resa": 2},
    {"codice_reso": "R002", "quantita_resa": 1},
]

print(ordini.ordine_dict["totale"])
tval = 0


#ordine["resi"] = sorted(resi, key=lambda t: t["quantita_resa"], reverse=True)

if __name__ == "__main__":
    main()
    fun2()
    print("Calcolo tot ordine")
    ordini.ordine_dict["totale"] = ordini.rtot(tval)
    print(ordini.ordine_dict["totale"])

print("finito!")
