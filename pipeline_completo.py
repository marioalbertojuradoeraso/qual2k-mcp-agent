"""Cadena completa de tareas vía MCP (servidor LOCAL servidor_mcp.py):

1. Conectar al servidor MCP e inicializar sesión.
2. crear_escenario  : clona HO04Q2KpHSOD.q2k reduciendo la carga de CBOD
                      de 1.34 a 0.67 mg/L (-50%) -> Escenario_Remediacion.q2k
3. correr_simulacion: ejecuta el motor Fortran con el nuevo escenario.
4. buscar_en_resultados: extrae la sección 'Water Quality Summary' del .out.

Al final verifica en disco que el .out nuevo exista.
"""
import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Evita UnicodeEncodeError en consolas Windows (cp1252)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

CARPETA = Path(r"C:\Users\majur\QUAL2K")
PYTHON = str(CARPETA / "mcp_env" / "Scripts" / "python.exe")

BASE = "HO04Q2KpHSOD.q2k"
NUEVO = "Escenario_Remediacion.q2k"
BUSCAR = "1.34"      # concentración de CBOD (mg/L) en la BC
REEMPLAZAR = "0.67"  # reducción del 50 % de la carga orgánica


async def main() -> None:
    server_params = StdioServerParameters(
        command=PYTHON,
        args=["servidor_mcp.py"],
        cwd=str(CARPETA),
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # --- 1) Conexión e inicialización ---
            init = await session.initialize()
            print("[OK] Conectado al servidor MCP:", init.serverInfo.name,
                  "v" + str(init.serverInfo.version))

            tools = await session.list_tools()
            print("Herramientas disponibles:")
            for t in tools.tools:
                print("   •", t.name, "—", (t.description or "").strip())

            # --- 2) Crear escenario modificado (remediación: CBOD -50 %) ---
            print("\n--- Tarea 1: crear_escenario ---")
            print(f"    base={BASE}  nuevo={NUEVO}")
            print(f"    cambiar {BUSCAR!r} -> {REEMPLAZAR!r} (CBOD -50 %)")
            r1 = await session.call_tool(
                "crear_escenario",
                {"archivo_base": BASE, "nuevo_nombre": NUEVO,
                 "buscar": BUSCAR, "reemplazar": REEMPLAZAR},
            )
            txt1 = "\n".join(getattr(b, "text", "") for b in r1.content)
            print("   ", txt1, "| isError:", r1.isError)

            ruta_nueva = CARPETA / NUEVO
            if r1.isError or not ruta_nueva.exists():
                print("   [FAIL] No se creó el escenario. Se detiene la cadena.")
                return
            contenido = ruta_nueva.read_text(encoding="utf-8", errors="ignore")
            print("    Verificación en disco: existe ✓ | contiene '0.67':",
                  "0.67" in contenido, "| quedan '1.34':", "1.34" in contenido)

            # --- 3) Correr la simulación con el nuevo escenario ---
            print("\n--- Tarea 2: correr_simulacion ---")
            print("    motor q2kfortran3b2.exe con", NUEVO)
            r2 = await session.call_tool(
                "correr_simulacion", {"archivo_entrada": NUEVO},
            )
            txt2 = "\n".join(getattr(b, "text", "") for b in r2.content)
            print("   ", txt2.strip(), "| isError:", r2.isError)

            ruta_out = CARPETA / "Escenario_Remediacion.out"
            ruta_err = CARPETA / "Escenario_Remediacion.err"
            print("    .out existe:", ruta_out.exists(),
                  "| .err existe:", ruta_err.exists())
            if ruta_err.exists():
                err = ruta_err.read_text(encoding="utf-8", errors="ignore").strip()
                print("    contenido .err:", repr(err[:300]) if err else "(vacío)")

            # --- 4) Extraer la sección de resultados (curva de OD) ---
            print("\n--- Tarea 3: buscar_en_resultados ---")
            r3 = await session.call_tool(
                "buscar_en_resultados",
                {"archivo_salida": "Escenario_Remediacion.out",
                 "termino_busqueda": "Water Quality Summary"},
            )
            txt3 = "\n".join(getattr(b, "text", "") for b in r3.content)
            print(txt3[:2600])
            print("    isError:", r3.isError)

    print("\n[OK] Cadena MCP completada.")


if __name__ == "__main__":
    asyncio.run(main())
