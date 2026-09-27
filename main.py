from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from html import escape

app = FastAPI()


# TESTOVACIE PONUKY
# Neskôr ich nahradíme skutočnými dátami z Ricardo.

offers = [
    {
        "name": "Sony WH-1000XM5",
        "buy": 95,
        "sell": 155,
        "shipping": 8,
        "fee": 0.10,
    },
    {
        "name": "Apple AirPods Pro 2",
        "buy": 79,
        "sell": 129,
        "shipping": 6,
        "fee": 0.10,
    },
    {
        "name": "Nintendo Switch OLED",
        "buy": 150,
        "sell": 220,
        "shipping": 8,
        "fee": 0.10,
    },
    {
        "name": "Apple Watch Series 9",
        "buy": 180,
        "sell": 260,
        "shipping": 8,
        "fee": 0.10,
    },
    {
        "name": "iPhone 15 Pro 256GB",
        "buy": 420,
        "sell": 560,
        "shipping": 10,
        "fee": 0.10,
    },
    {
        "name": "Samsung Galaxy S24",
        "buy": 280,
        "sell": 390,
        "shipping": 10,
        "fee": 0.10,
    },
    {
        "name": "GoPro HERO 12",
        "buy": 190,
        "sell": 280,
        "shipping": 8,
        "fee": 0.10,
    },
    {
        "name": "Dyson V15 Detect",
        "buy": 280,
        "sell": 430,
        "shipping": 15,
        "fee": 0.10,
    },
]


def calculate_profit(offer):
    profit = offer["sell"] - offer["buy"]

    return round(profit, 2)
@app.get("/", response_class=HTMLResponse)
def home(search: str = "", max_price: float = 0):

    results = []

    for offer in offers:

        matches_search = (
            not search
            or search.lower() in offer["name"].lower()
        )

        matches_price = (
            max_price <= 0
            or offer["buy"] <= max_price
        )

        if matches_search and matches_price:
            offer_copy = offer.copy()

            offer_copy["profit"] = calculate_profit(offer)

            offer_copy["margin"] = round(
                offer_copy["profit"]
                / offer["buy"]
                * 100,
                1
            )

            results.append(offer_copy)

    results.sort(
        key=lambda x: x["profit"],
        reverse=True
    )

    cards = ""

    for offer in results:

        if offer["profit"] >= 40:
            status = "🔥 Veľmi zaujímavé"
        elif offer["profit"] >= 25:
            status = "🟢 Zaujímavé"
        elif offer["profit"] >= 10:
            status = "🟡 Slabší deal"
        else:
            status = "🔴 Nezaujímavé"

        cards += f"""
        <div class="deal">

            <div class="deal-header">
                <h3>{escape(offer["name"])}</h3>
                <span>{status}</span>
            </div>

            <div class="numbers">

                <div>
                    <small>Nákup</small>
                    <strong>{offer["buy"]} CHF</strong>
                </div>

                <div>
                    <small>Predaj</small>
                    <strong>{offer["sell"]} CHF</strong>
                </div>

                <div>
                    <small>Zisk</small>
                    <strong class="profit">
                        {offer["profit"]} CHF
                    </strong>
                </div>

                <div>
                    <small>Marža</small>
                    <strong>
                        {offer["margin"]} %
                    </strong>
                </div>

            </div>


        </div>
        """

    if not results:
        cards = """
        <div class="empty">
            😕 Nenašli sme žiadne ponuky.
        </div>
        """

    return f"""
    <!DOCTYPE html>

    <html lang="sk">

    <head>

        <meta charset="UTF-8">

        <meta
            name="viewport"
            content="width=device-width, initial-scale=1.0"
        >

        <title>Ricardo Deal Finder</title>

        <style>

            * {{
                box-sizing: border-box;
            }}

            body {{
                font-family: Arial, sans-serif;
                background: #f4f5f7;
                margin: 0;
                padding: 40px 20px;
                color: #222;
            }}

            .container {{
                max-width: 1000px;
                margin: auto;
            }}

            h1 {{
                margin-bottom: 5px;
            }}

            .subtitle {{
                color: #666;
                margin-bottom: 30px;
            }}

            .search-box {{
                background: white;
                padding: 25px;
                border-radius: 15px;
                box-shadow: 0 3px 15px rgba(0,0,0,0.08);
                margin-bottom: 25px;
            }}

            input {{
                padding: 13px;
                border: 1px solid #ccc;
                border-radius: 8px;
                margin-right: 8px;
                font-size: 15px;
            }}

            button {{
                padding: 13px 22px;
                border: none;
                border-radius: 8px;
                background: #111;
                color: white;
                font-weight: bold;
                cursor: pointer;
            }}

            button:hover {{
                background: #333;
            }}

            .deal {{
                background: white;
                padding: 22px;
                border-radius: 15px;
                margin-bottom: 15px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.06);
            }}

            .deal-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 20px;
            }}

            .deal-header span {{
                font-weight: bold;
            }}

            .numbers {{
                display: grid;
                grid-template-columns:
                    repeat(4, 1fr);
                gap: 15px;
                margin-top: 20px;
            }}

            .numbers div {{
                background: #f5f5f5;
                padding: 15px;
                border-radius: 10px;
            }}

            small {{
                display: block;
                color: #777;
                margin-bottom: 5px;
            }}

            strong {{
                font-size: 20px;
            }}

            .profit {{
                color: #16823b;
            }}

            .empty {{
                background: white;
                padding: 30px;
                border-radius: 15px;
                text-align: center;
            }}

            .test {{
                background: #fff3cd;
                padding: 12px;
                border-radius: 8px;
                margin-top: 15px;
                color: #664d03;
            }}

            @media (max-width: 700px) {{
                .numbers {{
                    grid-template-columns: 1fr 1fr;
                }}

                input {{
                    width: 100%;
                    margin-bottom: 10px;
                }}

                button {{
                    width: 100%;
                }}
            }}

        </style>

    </head>

    <body>

        <div class="container">

            <h1>🔎 Ricardo Deal Finder</h1>

            <p class="subtitle">
                Hľadanie potenciálne výhodných ponúk
            </p>

            <div class="search-box">

                <form method="get">

                    <input
                        type="text"
                        name="search"
                        placeholder="Napr. iPhone"
                        value="{escape(search)}"
                    >

                    <input
                        type="number"
                        name="max_price"
                        placeholder="Max. cena CHF"
                        value="{max_price if max_price > 0 else ''}"
                    >

                    <button type="submit">
                        Hľadať
                    </button>

                </form>

                <div class="test">
                    ⚠️ Toto sú zatiaľ testovacie ponuky.
                    Ricardo pripojíme neskôr.
                </div>

            </div>

            {cards}

        </div>

    </body>

    </html>
    """