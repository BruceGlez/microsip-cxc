from conexion_firebird import conectar_firebird
from resumen_clientes import generar_resumen_por_cliente_base
from resumen_simplificado import generar_resumen_simplificado
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from pathlib import Path

def consultar():
    global df_resultado
    try:
        conn = conectar_firebird()
        query = """
        SELECT 
            C.CLIENTE_ID,
            C.NOMBRE AS CLIENTE,
            C.MONEDA_ID,
            SUM(S.CARGOS_CXC + S.CARGOS_XACR - S.CREDITOS_CXC - S.CREDITOS_XACR) AS SALDO_CXC,
            (SELECT 
                SUM(D.IMPORTE_NETO + D.TOTAL_IMPUESTOS)
             FROM DOCTOS_VE D
             WHERE 
                D.CLIENTE_ID = C.CLIENTE_ID
                AND D.TIPO_DOCTO = 'R'
                AND D.ESTATUS = 'P'
                AND D.MONEDA_ID = C.MONEDA_ID
            ) AS REMISIONES_PENDIENTES
        FROM SALDOS_CC S
        JOIN CLIENTES C ON S.CLIENTE_ID = C.CLIENTE_ID
        GROUP BY C.CLIENTE_ID, C.NOMBRE, C.MONEDA_ID
        HAVING SUM(S.CARGOS_CXC + S.CARGOS_XACR - S.CREDITOS_CXC - S.CREDITOS_XACR) <> 0
            OR (SELECT 
                    SUM(D.IMPORTE_NETO + D.TOTAL_IMPUESTOS)
                FROM DOCTOS_VE D
                WHERE 
                    D.CLIENTE_ID = C.CLIENTE_ID
                    AND D.TIPO_DOCTO = 'R'
                    AND D.ESTATUS = 'P'
                    AND D.MONEDA_ID = C.MONEDA_ID
            ) IS NOT NULL
        """

        cursor = conn.cursor()
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()

        for item in tree.get_children():
            tree.delete(item)

        for row in rows:
            tree.insert("", "end", values=row)

        df_resultado = pd.DataFrame(rows, columns=columns)

        cursor.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error:\\n{str(e)}")

def exportar():
    if df_resultado.empty:
        messagebox.showinfo("Sin datos", "Primero realiza una consulta.")
        return
    hoy = date.today().isoformat()
    ruta = Path("reportes")
    ruta.mkdir(exist_ok=True)
    archivo = ruta / f"reporte_credito_clientes_{hoy}.xlsx"
    df_resultado.to_excel(archivo, index=False, float_format="%.2f")
    messagebox.showinfo("Exportado", f"Archivo guardado como:\\n{archivo}")

def exportar_resumen():
    if df_resultado.empty:
        messagebox.showinfo("Sin datos", "Primero realiza una consulta.")
        return
    try:
        df_resumen = generar_resumen_por_cliente_base(df_resultado)
        columnas_numericas = ['REMISIONES_PESOS', 'CXC_PESOS', 'REMISIONES_DOLARES', 'CXC_DOLARES']
        df_resumen[columnas_numericas] = df_resumen[columnas_numericas].apply(pd.to_numeric, errors='coerce')
        hoy = date.today().isoformat()
        ruta = Path("reportes")
        ruta.mkdir(exist_ok=True)
        archivo = ruta / f"resumen_credito_unificado_{hoy}.xlsx"
        df_resumen.to_excel(archivo, index=False, float_format="%.2f")
        messagebox.showinfo("Resumen exportado", f"Archivo guardado como:\\n{archivo}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al exportar resumen:\\n{str(e)}")

def exportar_resumen_simplificado():
    if df_resultado.empty:
        messagebox.showinfo("Sin datos", "Primero realiza una consulta.")
        return
    try:
        df_simplificado = generar_resumen_simplificado(df_resultado)
        df_simplificado[['TOTAL_PESOS', 'TOTAL_DOLARES']] = df_simplificado[['TOTAL_PESOS', 'TOTAL_DOLARES']].apply(pd.to_numeric, errors='coerce')
        hoy = date.today().isoformat()
        ruta = Path("reportes")
        ruta.mkdir(exist_ok=True)
        archivo = ruta / f"resumen_simplificado_{hoy}.xlsx"
        df_simplificado.to_excel(archivo, index=False, float_format="%.2f")
        messagebox.showinfo("Resumen simplificado exportado", f"Archivo guardado como:\\n{archivo}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al exportar resumen simplificado:\\n{str(e)}")

root = tk.Tk()
root.title("Monitoreo de crédito - Microsip")
root.geometry("1050x500")

frame_top = tk.Frame(root)
frame_top.pack(pady=10)

btn_consultar = tk.Button(frame_top, text="Consultar saldos", command=consultar)
btn_consultar.pack(side="left", padx=5)

btn_exportar = tk.Button(frame_top, text="Exportar a Excel", command=exportar)
btn_exportar.pack(side="left", padx=5)

btn_exportar_resumen = tk.Button(frame_top, text="Exportar resumen agrupado", command=exportar_resumen)
btn_exportar_resumen.pack(side="left", padx=5)

btn_exportar_resumen_simplificado = tk.Button(frame_top, text="Exportar resumen simplificado", command=exportar_resumen_simplificado)
btn_exportar_resumen_simplificado.pack(side="left", padx=5)

cols = ["CLIENTE_ID", "CLIENTE", "MONEDA_ID", "SALDO_CXC", "REMISIONES_PENDIENTES"]
tree = ttk.Treeview(root, columns=cols, show="headings", height=20)

for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.pack(expand=True, fill="both", padx=10, pady=10)

df_resultado = pd.DataFrame()

root.mainloop()