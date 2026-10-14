"""Remediación combinada del WWTP vía MCP (cadena de dos crear_escenario):

Paso 1: HO04Q2KpHSOD.q2k -> Escenario_Temp.q2k
        CBOD lento y rápido del WWTP: 13.35 -> 6.675 mg/L  (-50 %)
Paso 2: Escenario_Temp.q2k -> Escenario_Remediacion.q2k
        Amoníaco del WWTP: 5000 -> 2500 ugN/L               (-50 %)
Paso 3: correr_simulacion con Escenario_Remediacion.q2k
"""
import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

CARPETA = Path(r"C:\Users\majur\QUAL2K")
PYTHON = str(CARPETA / "mcp_env" / "Scripts" / "python.exe")

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


async def main() -> None:
    server_params = StdioServerParameters(
        command=PYTHON, args=["servidor_mcp.py"], cwd=str(CARPETA),
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("[OK] Conectado al servidor MCP (Servidor_QUAL2K)")

            # --- Paso 1: reducir CBOD del WWTP (-50 %) ---
            r1 = await session.call_tool(
                "crear_escenario",
                {"archivo_base": "HO04Q2KpHSOD.q2k", "nuevo_nombre": "Escenario_Temp.q2k",
                 "buscar": "13.35", "reemplazar": "6.675"},
            )
            t1 = "\n".join(getattr(b, "text", "") for b in r1.content)
            print("[1/3] CBOD WWTP 13.35 -> 6.675 mg/L (-50 %):", t1.strip(),
                  "| isError:", r1.isError)

            # --- Paso 2: reducir amoníaco del WWTP (-50 %) ---
            r2 = await session.call_tool(
                "crear_escenario",
                {"archivo_base": "Escenario_Temp.q2k", "nuevo_nombre": "Escenario_Remediacion.q2k",
                 "buscar": "5000,0,0", "reemplazar": "2500,0,0"},
            )
            t2 = "\n".join(getattr(b, "text", "") for b in r2.content)
            print("[2/3] NH4 WWTP 5000 -> 2500 ugN/L (-50 %):", t2.strip(),
                  "| isError:", r2.isError)

            # Verificación en disco
            ruta = CARPETA / "Escenario_Remediacion.q2k"
            cont = ruta.read_text(encoding="utf-8", errors="ignore")
            print("     Verificación: '6.675' presente:", "6.675" in cont,
                  "| '2500,0,0' presente:", "2500,0,0" in cont,
                  "| quedan '13.35':", "13.35" in cont,
                  "| quedan '5000,0,0':", "5000,0,0" in cont)

            # --- Paso 3: simular ---
            r3 = await session.call_tool(
                "correr_simulacion", {"archivo_entrada": "Escenario_Remediacion.q2k"},
            )
            t3 = "\n".join(getattr(b, "text", "") for b in r3.content)
            print("[3/3] Simulación:", t3.strip(), "| isError:", r3.isError)
            err = CARPETA / "Escenario_Remediacion.err"
            if err.exists():
                e = err.read_text(encoding="utf-8", errors="ignore").strip()
                print("     .err:", repr(e[:200]) if e else "(vacío)")

    print("[OK] Remediación combinada completada.")


if __name__ == "__main__":
    asyncio.run(main())
