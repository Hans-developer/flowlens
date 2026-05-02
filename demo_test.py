from flowlens import lens
import time

# --- CAPA DE VALIDACIÓN (TRABAJO INTERNO) ---
@lens.track_stats
def validar_usuario(id_u):
    return {"status": "ok", "nivel": "premium"}

@lens.track_stats
def verificar_stock(sku):
    return True

@lens.track_stats
def comprobar_limite_credito(id_u, monto):
    return monto < 5000

# --- CAPA DE CÁLCULOS (TRABAJO INTERNO) ---
@lens.track_stats
def calcular_subtotal(items):
    return sum(item['p'] for item in items)

@lens.track_stats
def aplicar_descuento_lealtad(total):
    return total * 0.90

@lens.track_stats
def calcular_iva(neto):
    return neto * 0.19

@lens.track_stats
def estimar_costo_envio(region):
    return 15.50

@lens.track_stats
def sumar_total_final(neto, iva, envio):
    return neto + iva + envio

# --- CAPA DE SALIDA (MOSTRAR DATOS) ---
@lens.track_stats
def generar_etiqueta_impresion(datos):
    return f"ETIQUETA_PDF_{datos['id']}"

@lens.track_stats
def mostrar_confirmacion_pantalla(msj):
    print(f"PANTALLA: {msj}")
    return "Renderizado exitoso"

@lens.track_stats
def mostrar_alerta_seguridad(tipo):
    print(f"ALERTA: {tipo}")
    return "Alerta enviada"

# --- PROCESOS DE ORQUESTACIÓN ---
@lens.track_stats
def autorizar_pago(id_u, total):
    if comprobar_limite_credito(id_u, total):
        return "PAGO_APROBADO"
    return "RECHAZADO"

@lens.track_stats
def preparar_logistica(region, orden_id):
    costo = estimar_costo_envio(region)
    return generar_etiqueta_impresion({"id": orden_id, "costo": costo})

@lens.track_stats
def procesar_orden_completa(usuario_id, productos, zona):
    # 1. Validación
    usr = validar_usuario(usuario_id)
    verificar_stock("SKU-99")
    
    # 2. Cálculos
    sub = calcular_subtotal(productos)
    neto = aplicar_descuento_lealtad(sub)
    impuesto = calcular_iva(neto)
    
    # 3. Pago
    pago = autorizar_pago(usuario_id, neto)
    
    # 4. Logística y Salida
    log = preparar_logistica(zona, "ORD-123")
    mostrar_confirmacion_pantalla(f"Orden {pago} con éxito.")
    
    return "ORDEN_FINALIZADA"

# --- EJECUCIÓN DEL TEST ---
if __name__ == "__main__":
    carrito = [{'n': 'Laptop', 'p': 1000}, {'n': 'Mouse', 'p': 50}]
    
    lens.start()
    # Este proceso disparará la cadena de 15 llamadas
    procesar_orden_completa("HANS_SALDIAS", carrito, "RM_CHILE")
    lens.stop()