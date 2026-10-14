# Manual de Usuario: Consultor Experto QUAL2K con IA (vía MCP)

**Creador y Desarrollador Principal:** Ing. Mario Alberto Jurado Eraso  
**Repositorio Oficial:** [https://github.com/marioalbertojuradoeraso/qual2k-mcp-agent](https://github.com/marioalbertojuradoeraso/qual2k-mcp-agent)

## Introducción
Este proyecto transforma la manera en que interactuamos con el modelo de calidad del agua QUAL2K. A través del protocolo MCP, una Inteligencia Artificial controla el motor de cálculo de Fortran. Ya no dependes de las macros de Excel; ahora puedes simular, calibrar y graficar escenarios conversando en lenguaje natural.

---

## Prerrequisitos Críticos: La Plantilla Base (.q2k)
El motor de Fortran (`q2kfortran3b2.exe`) ya viene incluido en este repositorio, por lo que está listo para usarse. Sin embargo, el agente de IA necesita un archivo base `.q2k` de tu río para empezar a trabajar.

**Paso Único: Generar la plantilla base (.q2k) — ¡Cuidado con la Celda B10!**
1. Ve a la página oficial: [www.qual2k.com](http://www.qual2k.com) y descarga el archivo `.zip` del modelo completo.
2. Descomprímelo en cualquier carpeta temporal y abre el archivo Excel de QUAL2K.
3. Ve a la hoja principal (pestaña **QUAL2K**).
4. **PASO CRÍTICO:** Busca la celda **B10** (*"Path to directory..."*). Modifica esa celda pegando la ruta exacta de tu carpeta temporal. Si esta ruta es incorrecta, el Excel arrojará un error.
5. Haz clic en el botón **"Run Fortran"** en el Excel. Esto generará automáticamente un archivo de texto con extensión `.q2k` (ej. `Escenario.q2k`).
6. Copia ese archivo `.q2k` y pégalo en la carpeta de este proyecto MCP. A partir de aquí, la IA toma el control.

---

## Instalación y Configuración

1. Clona este repositorio o descárgalo como ZIP y ábrelo en tu terminal.
2. Crea y activa un entorno virtual:
   * Windows: `python -m venv mcp_env` y luego `.\mcp_env\Scripts\activate`
3. Instala las dependencias: `pip install -r requirements.txt`
4. Inicia el servidor MCP local o conéctalo a tu IA favorita (OpenCode, Claude Desktop, etc.).

## Activar al "Consultor Experto"
Abre el archivo `habilidad_consultor_qual2k.md`, copia su contenido y envíaselo a tu agente de IA. La IA te dirá que ha asumido el rol de Consultor y comenzará a guiarte paso a paso.
