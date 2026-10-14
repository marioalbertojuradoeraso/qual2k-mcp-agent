"""Cliente MCP en cadena: crear_escenario -> (verificar) -> correr_simulacion."""
import asyncio
from pathlib import Path

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
            init = await session.initialize()
            print("Conectado al servidor:", init.serverInfo.name, init.serverInfo.version)

            tools = await session.list_tools()
            print("Herramientas disponibles:")
            for t in tools.tools:
                print(" -", t.name, "-", (t.description or "").strip())

            # --- Tarea 1: crear escenario ---
            print("\n--- Llamando a crear_escenario ---")
            r1 = await session.call_tool(
                "crear_escenario",
                {
                    "archivo_base": "HO04Q2KpHSOD.q2k",
                    "nuevo_nombre": "Escenario_Prueba.q2k",
                    "buscar": "HO04",
                    "reemplazar": "TEST",
                },
            )
            texto1 = "\n".join(getattr(b, "text", "") for b in r1.content)
            print(texto1)
            print("isError:", r1.isError)

            # Confirmar que el archivo se creó antes de continuar
            ruta_nueva = Path(CARPETA) / "Escenario_Prueba.q2k"
            if r1.isError or not ruta_nueva.exists():
                print("\nLa herramienta NO confirmó la creación del archivo. Se detiene la cadena.")
                return

            contenido = ruta_nueva.read_text(encoding="utf-8", errors="ignore")
            print("Verificacion en disco: archivo existe | contiene 'TEST':",
                  "TEST" in contenido, "| contiene 'HO04':", "HO04" in contenido)

            # --- Tarea 2: correr simulacion con el nuevo archivo ---
            print("\n--- Llamando a correr_simulacion ---")
            r2 = await session.call_tool(
                "correr_simulacion",
                {"archivo_entrada": "Escenario_Prueba.q2k"},
            )
            texto2 = "\n".join(getattr(b, "text", "") for b in r2.content)
            print(texto2[:4000])
            print("isError:", r2.isError)


if __name__ == "__main__":
    asyncio.run(main())
