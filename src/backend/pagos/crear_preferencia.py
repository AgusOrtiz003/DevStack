import mercadopago

ACCESS_TOKEN = "APP_USR-5755291131578047-062109-31405c772e3e2b75c93005a2a051b331-3486812115"

def crear_preferencia_mp(idReserva, descripcion, monto) -> str:
    sdk = mercadopago.SDK(ACCESS_TOKEN)

    preference_data = {
        "items": [
            {
                "title": descripcion,
                "quantity": 1,
                "unit_price": monto,
                "currency_id": "ARS",
            }
        ],
        "external_reference": str(idReserva),
    }

    result = sdk.preference().create(preference_data)
    preference = result["response"]
    return preference.get("init_point")