import csv
import json
import logging
from pathlib import Path

import requests

API_URL = "https://jsonplaceholder.typicode.com/users"
OUTPUT_DIR = Path("datos")

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def consultar_api():
    try:
        respuesta = requests.get(API_URL, timeout=15)
        respuesta.raise_for_status()
        usuarios = respuesta.json()

        if not isinstance(usuarios, list):
            raise ValueError("La respuesta no es una lista.")

        return usuarios

    except requests.exceptions.HTTPError as error:
        logging.error("Error HTTP: %s", error)
    except requests.exceptions.RequestException as error:
        logging.error("Error de conexión: %s", error)
    except ValueError as error:
        logging.error("Error en los datos recibidos: %s", error)

    return None


def guardar_archivos(usuarios):
    OUTPUT_DIR.mkdir(exist_ok=True)

    archivo_json = OUTPUT_DIR / "inventario.json"
    archivo_csv = OUTPUT_DIR / "inventario.csv"

    archivo_json.write_text(
        json.dumps(usuarios, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    columnas = ["id", "name", "username", "email", "website"]
    with archivo_csv.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=columnas)
        escritor.writeheader()
        for usuario in usuarios:
            escritor.writerow({
                columna: usuario.get(columna, "")
                for columna in columnas
            })

    logging.info("Se procesaron %s registros.", len(usuarios))
    logging.info("Archivos creados: %s y %s", archivo_json, archivo_csv)


def main():
    usuarios = consultar_api()
    if usuarios is not None:
        guardar_archivos(usuarios)


if __name__ == "__main__":
    main()
