import mercadopago

ACCESS_TOKEN = "APP_USR-5755291131578047-062109-31405c772e3e2b75c93005a2a051b331-3486812115"

def verificar_pago(idReserva):
    sdk = mercadopago.SDK(ACCESS_TOKEN)
    resultado = sdk.payment().search({"external_reference": str(idReserva)})
    pagos = resultado["response"].get("results", [])

    if not pagos:
        return None, None, None

    pago = pagos[0]
    
    return pago.get("status"), pago.get("transaction_amount"), str(pago.get("id"))