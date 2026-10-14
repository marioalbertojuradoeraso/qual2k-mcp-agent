"""Extrae la curva de Oxígeno Disuelto (x_km, DO) de la sección
'Water Quality Summary' de un archivo .out de QUAL2K y la guarda en CSV.

El ancho de la columna 'Reach Label' es variable (a veces vacía), así que
los campos numéricos no están siempre en la misma posición. Se localizan los
4 campos consecutivos (x_km, cond, ISS, DO) por su patrón de valores:
    x_km en [0,15]  |  cond en [100,600]  |  ISS en [0,20]  |  DO en [0,20]
y se toma la primera coincidencia válida de cada fila.
"""
import csv
import sys
from pathlib import Path

CARPETA = Path(r"C:\Users\majur\QUAL2K")


def _es_numero(tok: str) -> bool:
    try:
        float(tok)
        return True
    except ValueError:
        return False


def extraer_curva_do(ruta_out: Path):
    lineas = ruta_out.read_text(encoding="utf-8", errors="ignore").splitlines()
    inicio = None
    for i, linea in enumerate(lineas):
        if "Water Quality Summary" in linea and "Min" not in linea and "Max" not in linea:
            inicio = i
            break
    if inicio is None:
        raise RuntimeError("No se encontró '** Water Quality Summary **'")

    datos = []
    for linea in lineas[inicio + 1:]:
        if linea.strip().startswith("**"):  # inicio de la siguiente sección
            break
        toks = linea.split()
        # buscar 4 numéricos consecutivos con el patrón (x, cond, iss, do)
        for j in range(len(toks) - 3):
            if not all(_es_numero(t) for t in toks[j:j + 4]):
                continue
            x_km, cond, iss, do = (float(t) for t in toks[j:j + 4])
            if (0.0 <= x_km <= 15.0 and 100.0 <= cond <= 600.0
                    and 0.0 <= iss <= 20.0 and 0.0 <= do <= 20.0):
                etiqueta = " ".join(toks[1:j]).strip()
                datos.append((x_km, do, etiqueta))
                break
    return datos


def main():
    archivo = sys.argv[1] if len(sys.argv) > 1 else "HO04Q2KpHSOD.out"
    salida = sys.argv[2] if len(sys.argv) > 2 else "curva_do_base.csv"
    ruta = CARPETA / archivo
    datos = extraer_curva_do(ruta)
    with (CARPETA / salida).open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["x_km", "do_mgl", "etiqueta"])
        for x, do, et in datos:
            w.writerow([f"{x:.6f}", f"{do:.6f}", et])
    do_vals = [d for _, d, _ in datos]
    print(f"Archivo: {archivo}")
    print(f"Puntos extraídos: {len(datos)}")
    if do_vals:
        i_min = do_vals.index(min(do_vals))
        print(f"DO min = {min(do_vals):.3f} mg/L en x = {datos[i_min][0]:.3f} km")
        print(f"DO max = {max(do_vals):.3f} mg/L")
    print(f"Guardado en: {salida}")


if __name__ == "__main__":
    main()
