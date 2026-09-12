import os
import xmlrpc.client
from dotenv import load_dotenv

load_dotenv("secrets.env")

url = os.environ["ODOO_URL"]
db = os.environ["ODOO_DB"]
username = os.environ["ODOO_USERNAME"]
password = os.environ["ODOO_API_KEY"]

common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")


def get_stock(nom_produit=None, limit=10):
    domaine = [
        ["location_id.complete_name", "=", "WH/Stock"]
    ]

    if nom_produit:
        domaine.append(
            ["product_id.name", "like", nom_produit]
        )

    return models.execute_kw(
        db,
        uid,
        password,
        "stock.quant",
        "search_read",
        [domaine],
        {
            "fields": [
                "product_id",
                "quantity",
                "location_id"
            ],
            "limit": limit
        }
    )


def get_sales(limit=10):
    return models.execute_kw(db, uid, password,
        "sale.order", "search_read",
        [[]],
        {"fields": ["name", "partner_id", "amount_total", "state"], "limit": limit})


def get_invoices(limit=10):
    return models.execute_kw(db, uid, password,
        "account.move", "search_read",
        [[["move_type", "=", "out_invoice"]]],
        {"fields": ["name", "partner_id", "amount_total", "state"], "limit": limit})


if __name__ == "__main__":
    print("STOCK :")
    for l in get_stock(limit=5):
        print(f"- {l['product_id'][1]} : {l['quantity']}")

    print("\nVENTES :")
    for v in get_sales(limit=5):
        nom_client = v['partner_id'][1] if v['partner_id'] else "N/A"
        print(f"- {v['name']} | {nom_client} | {v['amount_total']} | {v['state']}")

    print("\nFACTURES :")
    for f in get_invoices(limit=5):
        nom_client = f['partner_id'][1] if f['partner_id'] else "N/A"
        print(f"- {f['name']} | {nom_client} | {f['amount_total']} | {f['state']}")
