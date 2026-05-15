def main():
   print("Hello, World!")

def fun2():
   print("secondo print")

ordine = { "nome" : "pippo", "num_ordine" : 12345, "data_ord" : "31/12/2026", "totale" : 1234.87, "tot_qty" : 200, "righe" : [{"numr" : 1, "qta" : 5, "prezzou" : 30}, {"numr" : 2, "qta" : 10, "prezzou" : 10}]}
resi = [
   {"codice_reso": "R001", "quantita_resa": 2},
   {"codice_reso": "R002", "quantita_resa": 1}
]

print(ordine ["totale"] )
tval = 0  

def rtot(tval):
  for i in range (len(ordine ["righe"])):
    tval = tval + (ordine ["righe"] [i] ["qta"] * ordine ["righe"] [i] ["prezzou"])
  print (tval)
  return tval

if __name__ == "__main__":
   main()
   fun2()
   print("Calcolo tot ordine" )
   ordine ["totale"] = rtot(tval)
   print(ordine ["totale"] )

print("finito!")
