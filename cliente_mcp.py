"""Cliente MCP: se conecta al servidor QUAL2K y corre la simulacion."""
import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

CARPETA = r"C:\Users\majur\QUAL2K"
PYTHON = CARPETA + r"\mcp_env\Scripts\python.exe"


async def main() -> None:
    server_params = StdioServerParameters(
        command=PYTHON,
        args=["servidor_mcp.py"],
        cwd=CARPETA,
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 1) Inicializar la conexion
            init = await session.initialize()
            print("Conectado al servidor:", init.serverInfo.name, init.serverInfo.version)

            # 2) Listar herramientas disponibles
            tools = await session.list_tools()
            print("Herramientas disponibles:")
            for t in tools.tools:
                print(" -", t.name, "-", (t.description or "").strip())

            # 3) Llamar a correr_simulacion con el archivo .q2k
            resultado = await session.call_tool(
                "correr_simulacion",
                {"archivo_entrada": "HO04Q2KpHSOD.q2k"},
            )
            print("\n--- Resultado de correr_simulacion ---")
            for bloque in resultado.content:
                texto = getattr(bloque, "text", "")
                if texto:
                    print(texto)
            print("isError:", resultado.isError)


if __name__ == "__main__":
    asyncio.run(main())
