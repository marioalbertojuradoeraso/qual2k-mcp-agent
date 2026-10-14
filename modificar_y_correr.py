"""Helper: conecta al servidor MCP, crea un escenario (replace) y corre la simulación.
Uso: python modificar_y_correr.py <base.q2k> <nuevo.q2k> <buscar> <reemplazar>
"""
import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

CARPETA = Path(r"C:\Users\majur\QUAL2K")
PYTHON = str(CARPETA / "mcp_env" / "Scripts" / "python.exe")


async def main(base: str, nuevo: str, buscar: str, reemplazar: str) -> None:
    server_params = StdioServerParameters(
        command=PYTHON, args=["servidor_mcp.py"], cwd=str(CARPETA),
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            r1 = await session.call_tool(
                "crear_escenario",
                {"archivo_base": base, "nuevo_nombre": nuevo,
                 "buscar": buscar, "reemplazar": reemplazar},
            )
            txt1 = "\n".join(getattr(b, "text", "") for b in r1.content)
            print(f"[crear_escenario] {base} -> {nuevo}  ({buscar!r} -> {reemplazar!r})")
            print("   ", txt1, "| isError:", r1.isError)
            if r1.isError or not (CARPETA / nuevo).exists():
                print("   [FAIL] no se creó el escenario.")
                return

            r2 = await session.call_tool(
                "correr_simulacion", {"archivo_entrada": nuevo},
            )
            txt2 = "\n".join(getattr(b, "text", "") for b in r2.content)
            print(f"[correr_simulacion] motor con {nuevo}")
            print("   ", txt2.strip(), "| isError:", r2.isError)
            err = CARPETA / (Path(nuevo).stem + ".err")
            if err.exists():
                e = err.read_text(encoding="utf-8", errors="ignore").strip()
                print("    .err:", repr(e[:200]) if e else "(vacío)")


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Uso: python modificar_y_correr.py <base> <nuevo> <buscar> <reemplazar>")
        raise SystemExit(1)
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    asyncio.run(main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
