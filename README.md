# Wompi - Data Engineering Test

## Objetivo

Procesar el archivo de transacciones en formato JSONL y generar una vista agregada con información de las transacciones aprobadas en formato Parquet.

La vista final contiene:

* Día de la transacción
* Mes
* Año
* BIN (Bank Identification Number)
* Cantidad de transacciones aprobadas
* Monto total aprobado

## Estructura del ejercicio

```text
wompiPrueba/
├── output/
│   └── transaction_summary.parquet
├── src/
│   └── gts.py
├── README.md
└── requirements.txt
```

## Procesamiento

El script `src/gts.py` realiza las siguientes operaciones:

1. Lee el archivo de entrada en formato JSONL.
2. Filtra únicamente las transacciones con estado `APPROVED`.
3. Extrae la fecha de creación (`created_at`), el BIN y el monto de la transacción (`amount_in_cents`).
4. Convierte la fecha de creación a formato de fecha.
5. Obtiene el día, mes y año de la transacción.
6. Agrupa las transacciones por día, mes, año y BIN.
7. Calcula la cantidad de transacciones aprobadas por grupo.
8. Calcula el monto total aprobado por grupo.
9. Genera el resultado en formato Parquet.

## Ejecución

El script recibe como parámetros la ruta del archivo de entrada y la ruta del archivo de salida.

```bash
python src/gts.py --input transactions_50k.jsonl --output output/transaction_summary.parquet
```

Ejemplo utilizando el archivo de prueba:

```bash
python src/gts.py \
    --input transactions_50k.jsonl \
    --output output/transaction_summary.parquet
```

## Dependencias

Las dependencias necesarias se encuentran en `requirements.txt`.

Para instalarlas:

```bash
pip install -r requirements.txt
```

Las principales dependencias utilizadas son:

* `pandas`: procesamiento y agregación de datos.
* `pyarrow`: generación del archivo de salida en formato Parquet.

## Resultado

El archivo generado se encuentra en:

```text
output/transaction_summary.parquet
```

Sobre el archivo de prueba se obtuvieron los siguientes resultados durante la validación:

* 50.000 transacciones procesadas.
* 42.427 transacciones con estado `APPROVED`.
* 150 BIN distintos.
* Período de transacciones desde el 1 de abril de 2024 hasta el 28 de septiembre de 2024.
* 21.529 registros en la vista agregada final.

## Validaciones

Durante el desarrollo se realizaron las siguientes validaciones:

* Se verificó que el archivo contiene 50.000 registros.
* Se verificó la distribución de estados de las transacciones.
* Se verificó que existen 42.427 transacciones `APPROVED`.
* Se verificó que no existen registros sin BIN.
* Se verificó que no existen registros sin fecha.
* Se verificó que `amount_in_cents` es un valor entero.
* Se verificó que la cantidad de transacciones agrupadas corresponde a las 42.427 transacciones aprobadas.
* Se verificó que el monto total después de la agregación coincide con el monto total de las transacciones aprobadas.

## Supuestos

* Se consideran únicamente las transacciones cuyo estado es `APPROVED`.
* El monto se mantiene en centavos (`amount_in_cents`) durante el procesamiento para conservar la representación original del archivo de entrada y evitar conversiones innecesarias.
* La fecha utilizada para la agregación corresponde al campo `created_at`.
* El BIN utilizado corresponde al campo `payment_method_type.extra.bin`.
* La granularidad de la vista final es día, mes, año y BIN.

## Idempotencia

El proceso es idempotente respecto al archivo de entrada y los parámetros utilizados.

Cada ejecución genera nuevamente el resultado a partir de los datos de entrada y sobrescribe el archivo de salida. Por lo tanto, ejecutar el script varias veces con el mismo archivo de entrada produce el mismo resultado.

## Entorno de ejecución

El desarrollo y las pruebas del procesamiento se realizaron utilizando Google Colab.

El código ejecutado en Colab corresponde al mismo script `src/gts.py` almacenado en este repositorio.

## Autor

Prueba técnica - Ingeniero de Datos
