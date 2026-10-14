# QUAL2K MCP Server

> **An AI bridge between the QUAL2K Fortran river-water-quality engine and Large Language Models.**
> *Un puente de IA entre el motor Fortran de calidad del agua QUAL2K y los Modelos de Lenguaje.*

![QUAL2K](https://img.shields.io/badge/QUAL2K-v3.00b8-blue) ![MCP](https://img.shields.io/badge/MCP-1.30.0-green) ![Python](https://img.shields.io/badge/Python-3.12-blue) ![R](https://img.shields.io/badge/R-4.x-lightgrey)

---

## English

### What is this?

[QUAL2K](https://www.epa.gov/) is the EPA's steady-state river water-quality model (Fortran engine `q2kfortran3b2.exe`). Traditionally it is driven from an Excel workbook (`Q2KMaster…xlsm`). This project exposes the whole simulation workflow as **MCP (Model Context Protocol) tools**, so an AI agent (Claude, OpenCode, …) can run complete water-quality studies **without touching Excel**:

| MCP tool | What it does |
|---|---|
| `crear_escenario` | Safely clones a `.q2k` scenario file replacing a parameter (e.g. a pollutant load). |
| `correr_simulacion` | Runs the QUAL2K Fortran engine in the background with the given `.q2k` file. |
| `buscar_en_resultados` | Searches the (heavy) `.out` result file for a keyword and extracts that section (e.g. `Water Quality Summary`). |

Downstream helpers (plain Python + R/ggplot2) extract the Dissolved Oxygen profile and render publication-grade longitudinal plots.

### Installation (first time only)

```bash
# 1. Clone the repository
git clone https://github.com/marioalbertojuradoeraso/qual2k-mcp-agent.git
cd qual2k-mcp-agent

# 2. Create and activate a virtual environment
python -m venv mcp_env
mcp_env\Scripts\activate        # Windows
# source mcp_env/bin/activate   # Linux / macOS

# 3. Install dependencies (pinned: the server uses the MCP v1 API)
pip install -r requirements.txt

# 4. Make sure R is installed if you want the scientific plots
#    (scripts use ggplot2)
```

> **Version note:** `requirements.txt` pins `mcp==1.30.0` because `servidor_mcp.py` uses the MCP v1 API (`mcp.server.fastmcp.FastMCP`). Version 2.x renamed that API and breaks the server.

### How to ask the AI to use it

Point your MCP client (Claude / OpenCode) at `servidor_mcp.py`, then prompt something like:

> *"Connect to the local MCP server in `servidor_mcp.py`. Clone the base scenario, cut the WWTP's CBOD and ammonia loads by 50 %, run the model, extract the Dissolved Oxygen curve from the Water Quality Summary, and use R to generate a scientific plot."*

The agent will chain the three tools, verify every step on disk (scenario created → `.err` empty → section extracted), and deliver the plot plus a quantitative summary (e.g. sag recovery from 3.69 to 4.03 mg/L, clearing the 4.0 mg/L hypoxia threshold).

### Project layout

```
├── servidor_mcp.py              # MCP server: the 3 QUAL2K tools
├── pipeline_completo.py         # Full chain client (scenario → run → extract)
├── remediacion_completa.py      # Combined WWTP remediation chain (CBOD + NH4)
├── modificar_y_correr.py        # Generic helper: clone-with-replace + run
├── cliente_mcp.py               # Minimal connection + simulation client
├── consulta_resultados.py       # Results-section query client
├── cadena_tareas.py             # Chained create → verify → run client
├── extraer_do.py                # DO-curve extractor (.out → CSV)
├── perfil_oxigeno_comparativo.R # Publication-grade DO profile (ggplot2)
├── HO04Q2KpHSOD.q2k            # Base scenario (Boulder Creek, 8/21/1987)
├── Escenario_Remediacion.q2k   # Remediation scenario (WWTP −50 % CBOD/NH4)
├── q2kfortran3b2.exe            # QUAL2K Fortran engine
├── Q2KMasterv3b2r1_Master.xlsm  # Original Excel interface (reference)
└── requirements.txt             # Pinned dependencies (mcp==1.30.0)
```

Results (`.out`), engine logs (`.err`, `.log`), the virtual environment and caches are excluded via `.gitignore` — every user regenerates them by running the model.

---

## Español

### ¿Qué es esto?

[QUAL2K](https://www.epa.gov/) es el modelo de calidad del agua en ríos de la EPA (motor Fortran `q2kfortran3b2.exe`). Tradicionalmente se opera desde un libro de Excel (`Q2KMaster…xlsm`). Este proyecto expone todo el flujo de simulación como **herramientas MCP (Model Context Protocol)**, para que un agente de IA (Claude, OpenCode, …) ejecute estudios completos de calidad del agua **sin tocar Excel**:

| Herramienta MCP | Qué hace |
|---|---|
| `crear_escenario` | Clona de forma segura un escenario `.q2k` reemplazando un parámetro (ej. una carga contaminante). |
| `correr_simulacion` | Ejecuta el motor Fortran de QUAL2K en segundo plano con el `.q2k` indicado. |
| `buscar_en_resultados` | Busca una palabra clave en el archivo pesado de resultados `.out` y extrae esa sección (ej. `Water Quality Summary`). |

Scripts de apoyo (Python + R/ggplot2) extraen el perfil de Oxígeno Disuelto y generan gráficos longitudinales de calidad científica.

### Instalación (solo la primera vez)

```bash
# 1. Clonar el repositorio
git clone https://github.com/marioalbertojuradoeraso/qual2k-mcp-agent.git
cd qual2k-mcp-agent

# 2. Crear y activar el entorno virtual
python -m venv mcp_env
mcp_env\Scripts\activate        # Windows
# source mcp_env/bin/activate   # Linux / macOS

# 3. Instalar dependencias (fijadas: el servidor usa la API v1 de MCP)
pip install -r requirements.txt

# 4. Tener R instalado si se quieren los gráficos científicos
#    (los scripts usan ggplot2)
```

> **Nota de versión:** `requirements.txt` fija `mcp==1.30.0` porque `servidor_mcp.py` usa la API v1 de MCP (`mcp.server.fastmcp.FastMCP`). La versión 2.x renombró esa API y rompe el servidor.

### Cómo pedirle a la IA que lo use

Apunta tu cliente MCP (Claude / OpenCode) a `servidor_mcp.py` y luego pide algo como:

> *"Conéctate al servidor MCP local en `servidor_mcp.py`. Clona el escenario base, reduce 50 % la carga de CBOD y amoníaco del WWTP, corre el modelo, extrae la curva de Oxígeno Disuelto del Water Quality Summary y usa R para generar un gráfico científico."*

El agente encadenará las tres herramientas, verificará cada paso en disco (escenario creado → `.err` vacío → sección extraída) y entregará el gráfico más un resumen cuantitativo (ej. recuperación del sag de 3.69 a 4.03 mg/L, superando el umbral de hipoxia de 4.0 mg/L).

### Estructura del proyecto

```
├── servidor_mcp.py              # Servidor MCP: las 3 herramientas QUAL2K
├── pipeline_completo.py         # Cliente de cadena completa (escenario → corrida → extracción)
├── remediacion_completa.py      # Cadena de remediación combinada del WWTP (CBOD + NH4)
├── modificar_y_correr.py        # Utilidad genérica: clonar-con-reemplazo + correr
├── cliente_mcp.py               # Cliente mínimo de conexión + simulación
├── consulta_resultados.py       # Cliente de consulta de secciones de resultados
├── cadena_tareas.py             # Cliente encadenado crear → verificar → correr
├── extraer_do.py                # Extractor de curva de OD (.out → CSV)
├── perfil_oxigeno_comparativo.R # Perfil de OD de calidad científica (ggplot2)
├── HO04Q2KpHSOD.q2k            # Escenario base (Boulder Creek, 21/8/1987)
├── Escenario_Remediacion.q2k   # Escenario de remediación (WWTP −50 % CBOD/NH4)
├── q2kfortran3b2.exe            # Motor Fortran de QUAL2K
├── Q2KMasterv3b2r1_Master.xlsm  # Interfaz Excel original (referencia)
└── requirements.txt             # Dependencias fijadas (mcp==1.30.0)
```

Los resultados (`.out`), bitácoras del motor (`.err`, `.log`), el entorno virtual y las cachés están excluidos vía `.gitignore` — cada usuario los regenera corriendo el modelo.
