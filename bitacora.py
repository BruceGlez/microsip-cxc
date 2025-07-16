import pandas as pd
from pathlib import Path
from datetime import date
from resumen_simplificado import generar_resumen_simplificado

def guardar_bitacora(df_raw):
    hoy = date.today().isoformat()
    df_simplificado = generar_resumen_simplificado(df_raw)
    df_simplificado['FECHA'] = hoy

    ruta = Path("bitacora")
    ruta.mkdir(exist_ok=True)
    archivo = ruta / "bitacora_clientes.xlsx"

    if archivo.exists():
        df_existente = pd.read_excel(archivo)
        df_total = pd.concat([df_existente, df_simplificado], ignore_index=True)
    else:
        df_total = df_simplificado

    df_total.to_excel(archivo, index=False, float_format="%.2f")