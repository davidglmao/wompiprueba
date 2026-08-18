import argparse
import json
import os

import pandas as pd


def procesar_transacciones(nm_archivo_entrada):
    nm_transacciones_aprobadas = []

    with open(nm_archivo_entrada, "r", encoding="utf-8") as nm_archivo:
        for nm_linea in nm_archivo:
            nm_transaccion = json.loads(nm_linea)

            if nm_transaccion["status"] == "APPROVED":
                nm_transacciones_aprobadas.append({
                    "fecha": nm_transaccion["created_at"],
                    "bin": nm_transaccion["payment_method_type"]["extra"]["bin"],
                    "monto": nm_transaccion["amount_in_cents"]
                })

    nm_df_aprobadas = pd.DataFrame(nm_transacciones_aprobadas)

    nm_df_aprobadas["fecha"] = pd.to_datetime(nm_df_aprobadas["fecha"])
    nm_df_aprobadas["dia"] = nm_df_aprobadas["fecha"].dt.day
    nm_df_aprobadas["mes"] = nm_df_aprobadas["fecha"].dt.month
    nm_df_aprobadas["anio"] = nm_df_aprobadas["fecha"].dt.year

    nm_resumen = (
        nm_df_aprobadas
        .groupby(
            ["dia", "mes", "anio", "bin"],
            as_index=False
        )
        .agg(
            cantidad_transacciones=("monto", "count"),
            monto_total_aprobado=("monto", "sum")
        )
    )

    return nm_resumen


if __name__ == "__main__":
    nm_parser = argparse.ArgumentParser(
        description="Genera un resumen de transacciones aprobadas."
    )

    nm_parser.add_argument(
        "--input",
        required=True,
        help="Ruta del archivo JSONL de entrada."
    )

    nm_parser.add_argument(
        "--output",
        required=True,
        help="Ruta del archivo Parquet de salida."
    )

    nm_args = nm_parser.parse_args()

    nm_resultado = procesar_transacciones(nm_args.input)

    nm_directorio_salida = os.path.dirname(nm_args.output)

    if nm_directorio_salida:
        os.makedirs(nm_directorio_salida, exist_ok=True)

    nm_resultado.to_parquet(
        nm_args.output,
        index=False
    )
