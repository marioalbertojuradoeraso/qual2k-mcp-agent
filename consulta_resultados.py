"""Cliente MCP: llama a buscar_en_resultados y guarda la respuesta exacta en UTF-8."""
import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

CARPETA = r"C:\Users\majur\QUAL2K"
PYTHON = CARPETA + r"\mcp_env\Scripts\python.exe"

ARCHIVO = sys.argv[1] if len(sys.argv) > 1 else "Escenario_Prueba.out"
TERMINO = sys.argv[2] if len(sys.argv) > 2 else "(mgO2/L)"
SALIDA = Path(CARPETA) / "resultado_busqueda.txt"


async def main() -> None:
    server_params = StdioServerParameters(
        command=PYTHON,
        args=["servidor_mcp.py"],
        cwd=CARPETA,
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            init = await session.initialize()
            print("Conectado al servidor:", init.serverInfo.name, init.serverInfo.version)

            r = await session.call_tool(
                "buscar_en_resultados",
                {"archivo_salida": ARCHIVO, "termino_busqueda": TERMINO},
            )
            texto = "\n".join(getattr(b, "text", "") for b in r.content)
            print("isError:", r.isError)

            SALIDA.write_text(
                f"Herramienta: buscar_en_resultados\n"
                f"Parametros: archivo_salida={ARCHIVO!r}, termino_busqueda={TERMINO!r}\n"
                f"isError: {r.isError}\n"
                f"--- Respuesta exacta ---\n{texto}\n",
                encoding="utf-8",
            )
            print("Respuesta guardada en:", SALIDA)


if __name__ == "__main__":
    asyncio.run(main())
