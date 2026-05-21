from fastapi import FastAPI
import lettura_tabelle as ordini

app = FastAPI()


@app.get("/ordini/{num_ordine}")
async def get_ordine(num_ordine: int):
    ordine = ordini.get_order_details(num_ordine)
    return ordine

@app.get("/ordini")
async def get_ordini():
    ordini_disponibili = ordini.get_available_order_numbers()
    return {"ordini": ordini_disponibili}

@app.get("/ordini/articolo/{article_code}")
async def get_ordini_by_article_code(article_code: str):
    ordini_prelevati = ordini.get_orders_by_article_code(article_code)
    return ordini_prelevati