from mcp.server.fastmcp import FastMCP
import subprocess
from pathlib import Path

mcp = FastMCP("Servidor_QUAL2K")

@mcp.tool()
def correr_simulacion(archivo_entrada: str) -> str:
    """Ejecuta el motor QUAL2K con el archivo .q2k especificado en la carpeta actual."""
    carpeta_actual = Path(__file__).parent.absolute()
    motor = carpeta_actual / "q2kfortran3b2.exe"
    if not motor.exists(): return f"Error: No encontré el motor en {motor}"
    try:
        subprocess.run([str(motor), archivo_entrada], cwd=str(carpeta_actual), capture_output=True, text=True, check=True)
        return "¡Éxito! Simulación terminada."
    except subprocess.CalledProcessError as error:
        return f"Error al correr el motor:\n{error.stderr}"

@mcp.tool()
def crear_escenario(archivo_base: str, nuevo_nombre: str, buscar: str, reemplazar: str) -> str:
    """Crea una copia del archivo .q2k cambiando un texto o número específico."""
    carpeta_actual = Path(__file__).parent.absolute()
    ruta_base, ruta_nueva = carpeta_actual / archivo_base, carpeta_actual / nuevo_nombre
    if not ruta_base.exists(): return f"Error: No se encontró {archivo_base}"
    try:
        nuevo_contenido = ruta_base.read_text(encoding="utf-8", errors="ignore").replace(buscar, reemplazar)
        ruta_nueva.write_text(nuevo_contenido, encoding="utf-8")
        return f"Escenario creado exitosamente como {nuevo_nombre}."
    except Exception as e:
        return f"Error al crear escenario: {str(e)}"

@mcp.tool()
def buscar_en_resultados(archivo_salida: str, termino_busqueda: str) -> str:
    """Busca una palabra clave en el archivo .out (ej. 'Dissolved Oxygen') y extrae esa sección de resultados."""
    carpeta_actual = Path(__file__).parent.absolute()
    ruta_archivo = carpeta_actual / archivo_salida
    if not ruta_archivo.exists(): return f"Error: No se encontró {archivo_salida}"
    try:
        lineas = ruta_archivo.read_text(encoding="utf-8", errors="ignore").splitlines()
        resultado = []
        capturando = False
        for linea in lineas:
            if termino_busqueda.lower() in linea.lower():
                capturando = True
                resultado.append(f"--- SECCIÓN ENCONTRADA: {termino_busqueda} ---")
            
            # Si encontramos el término, capturamos las siguientes 25 líneas (suficiente para una tabla de QUAL2K)
            if capturando:
                resultado.append(linea)
                if len(resultado) > 25: break
        
        return "\n".join(resultado) if resultado else f"No encontré '{termino_busqueda}' en los resultados."
    except Exception as e:
        return f"Error al leer resultados: {str(e)}"

if __name__ == "__main__":
    mcp.run()