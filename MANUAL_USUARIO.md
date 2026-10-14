# Manual de Usuario: Consultor Experto QUAL2K con IA (vía MCP)

**Creador y Desarrollador Principal:** Ing. Mario Alberto Jurado Eraso  
**Repositorio Oficial:** [https://github.com/marioalbertojuradoeraso/qual2k-mcp-agent](https://github.com/marioalbertojuradoeraso/qual2k-mcp-agent)

## Introducción
Este proyecto transforma la manera en que interactuamos con el modelo de calidad del agua QUAL2K. A través del protocolo MCP, una Inteligencia Artificial controla el motor de cálculo de Fortran. Ya no dependes de las macros de Excel; ahora puedes simular, calibrar y graficar escenarios conversando en lenguaje natural.

---

## Prerrequisitos Críticos: El Motor y la Plantilla Base
El agente de IA modifica datos, pero necesita el motor matemático original y un archivo base para empezar.

**Paso A: Obtener el motor de Fortran**
1. Ve a la página oficial: [www.qual2k.com](http://www.qual2k.com) y descarga el archivo `.zip` del modelo.
2. Descomprímelo en una carpeta de tu PC (por ejemplo: `C:\QUAL2K_Temp`).
3. Busca el archivo `q2kfortran3b2.exe`. Cópialo y pégalo en la carpeta de este proyecto MCP.

**Paso B: Generar la plantilla base (.q2k) — ¡Cuidado con la Celda B10!**
1. Abre el archivo Excel de QUAL2K que acabas de descargar.
2. Ve a la hoja principal (pestaña **QUAL2K**).
3. **PASO CRÍTICO:** Busca la celda **B10** (*"Path to directory..."*). Modifica esa celda pegando la ruta exacta de tu carpeta (ej. `C:\QUAL2K_Temp`). Si esta ruta es incorrecta, el Excel arrojará un error.
4. Haz clic en el botón **"Run Fortran"** en el Excel. Esto generará automáticamente un archivo de texto con extensión `.q2k` (ej. `Escenario.q2k`).
5. Copia ese archivo `.q2k` y pégalo en la carpeta de este proyecto MCP.

---

## Instalación y Configuración

1. Clona este repositorio o descárgalo como ZIP y ábrelo en tu terminal.
2. Crea y activa un entorno virtual:
   * Windows: `python -m venv mcp_env` y luego `.\mcp_env\Scripts\activate`
3. Instala las dependencias: `pip install -r requirements.txt`
4. Inicia el servidor MCP local o conéctalo a tu IA favorita (OpenCode, Claude Desktop, etc.).

## Activar al "Consultor Experto"
Abre el archivo `habilidad_consultor_qual2k.md`, copia su contenido y envíaselo a tu agente de IA. La IA te dirá que ha asumido el rol de Consultor y comenzará a guiarte paso a paso.
