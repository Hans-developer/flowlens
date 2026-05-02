========================================================================
🔍 FLOWLENS v2.1 - Herramienta de Auditoría y Trazabilidad Visual
========================================================================

DESCRIPCIÓN:
FlowLens es un motor de rastreo para Python diseñado para auditar la 
ejecución lógica de algoritmos. Transforma la ejecución de código en 
un reporte HTML interactivo que permite visualizar el flujo de 
procesos, tiempos de respuesta y la naturaleza de cada operación.

Ideal para desarrolladores independientes e investigadores que 
buscan una forma profesional de mostrar cómo funcionan sus sistemas.

AUTOR: Hans Saldias (Analista Programador)
ESTADO: Propuesta para la comunidad de CPython

------------------------------------------------------------------------
✨ CARACTERÍSTICAS PRINCIPALES
------------------------------------------------------------------------

*   ORDEN CRONOLÓGICO: Muestra exactamente dónde comienza (INICIO) y 
    termina (FIN) cada proceso.
*   DETECCIÓN DE INTENCIÓN: Clasifica automáticamente si la función es 
    un "TRABAJO INTERNO / CÁLCULO" o si es para "MOSTRAR DATOS".
*   MÉTRICAS DE RENDIMIENTO: Registra el tiempo exacto de ejecución 
    en milisegundos (ms) para cada bloque.
*   TRAZABILIDAD DE DATOS: Captura los argumentos de entrada y los 
    valores de retorno en cada paso.

------------------------------------------------------------------------
🚀 CÓMO UTILIZAR FLOWLENS
------------------------------------------------------------------------

1. REQUISITOS:
   No requiere dependencias externas. Solo necesitas tener el archivo 
   `flowlens.py` en tu carpeta de proyecto.

2. IMPLEMENTACIÓN RÁPIDA:
   Importa el objeto `lens` y usa el decorador `@lens.track_stats` 
   en las funciones que deseas auditar.

   Ejemplo:
   
   from flowlens import lens

   @lens.track_stats
   def mi_algoritmo(valor):
       # Esto será detectado como cálculo interno
       return valor * 2

   @lens.track_stats
   def mostrar_datos(resultado):
       # Esto será detectado como salida de datos
       print(resultado)

   # Iniciar captura
   lens.start()
   
   # Ejecutar lógica
   res = mi_algoritmo(50)
   mostrar_datos(res)
   
   # Detener y generar reporte
   lens.stop()

3. RESULTADO:
   Se generará un archivo llamado `flowlens_report.html` que se 
   abrirá automáticamente en tu navegador predeterminado.

------------------------------------------------------------------------
📂 ARCHIVOS DEL PROYECTO
------------------------------------------------------------------------

*   flowlens.py       -> El núcleo del motor de auditoría.
*   demo_test.py      -> Script de prueba con 15 procesos integrados.
*   README.txt        -> Instrucciones de uso.

------------------------------------------------------------------------
"La claridad en el código es la base de una auditoría segura."
========================================================================
