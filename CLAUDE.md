# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the project

```bash
# Web app (primary interface)
streamlit run app.py

# CLI (uses hardcoded SPREADSHEET_LINE in config.py)
python main.py
```

## Dependencies

```bash
pip install -r requirements.txt
```

The project uses a local virtualenv at `.venv_informes-tecnicos/`. Activate with:
```bash
source .venv_informes-tecnicos/bin/activate
```

## API key

The LLM requires an OpenAI key. Lookup order in `get_openai_api_key()` (`utils.py`):
1. `st.secrets["OPENAI_API_KEY"]` (Streamlit Cloud deployment)
2. `.env` file via `python-dotenv`
3. System environment variable

Current model: `gpt-4.1-mini` (used in both LLM call sites). Do not change to `gpt-5-mini` — that model silently returns empty content.

## Architecture

Four files do all the work:

**`config.py`** — Data layer. `ReportConfig` parses a 60-field tab-delimited spreadsheet row into named attributes, computes weighted risk scores, and exposes `get_data_dict()` for template substitution. Also holds both LLM prompt templates (`LANGCHAIN_PROMPT_TEMPLATE`, `RECOMMENDATIONS_PROMPT_TEMPLATE`).

**`utils.py`** — Engine. `ReportGenerator` loads the `.docx` template, replaces `{{placeholder}}` markers (handling Word's run-splitting quirk), and inserts chart images. Standalone functions generate the four matplotlib charts. `apply_text_corrections()` orchestrates the two LLM calls and returns the enriched data dict — it must be called **before** `replace_placeholders()`, not inside it.

**`app.py`** — Streamlit UI. Parses the pasted spreadsheet row, renders editable fields, recalculates risk scores from edits, then calls `apply_text_corrections()` explicitly (with UI progress feedback) before `replace_placeholders()`.

**`main.py`** — CLI wrapper. Same flow: parse → charts → `apply_text_corrections()` → `replace_placeholders()` → save.

## LLM flow (critical)

`apply_text_corrections(data_dict)` makes two sequential calls:
1. **obs_generales** — rewrites the technician's general observations using `LANGCHAIN_PROMPT_TEMPLATE`. Returns original if text ≤ 3 chars.
2. **recommendations** — calls `generate_recommendations()` which uses `RECOMMENDATIONS_PROMPT_TEMPLATE` and expects a JSON response with keys `reco_generales`, `reco_especificas_1/2/3`. Returns `{}` on any failure; the caller falls back to original technician text.

Both calls use a `SystemMessage` + `HumanMessage` pair. On any exception, the function returns the original `data_dict` unchanged — failures are silent in the terminal but surface as `st.warning` in the Streamlit UI.

## Data dict keys

The dict passed through the pipeline uses these key names for the LLM context builders:
- Pest fields: `cucarachas`, `hormigas`, `moscas`, `mosquitos`, `zancudo`, `raton_casero`, `rata_noruega`, `raton_tejado`, `larvas_mosquitos`
- External risk fields: `genera_vecindario`, `limpieza_vecindario`, `manejo_basuras_vecindario`, `infraes_vecindario`, `ilumina_vecindario`, `animal_cercanias`, `construccion_cerca`, `zonas_verdes_cerca`, `cuerpos_de_agua_cerca`, `desagues_cerca`, `locales_comida`
- Internal risk fields: `general_establecimiento`, `limpieza_establecimiento`, `almacenamiento_establecimiento`, `iluminacion_establecimiento`, `capacitacion_personal`, `sellamiento_puertas`, `ventilacion_establecimiento`, `grietas_instalaciones`, `entrada_salida_material`, `acumulacion_objetos`, `areas_manipulacion_comida`, `presencia_animales`

Risk fields store **text values** (e.g. `"🟡 Buena"`) in the data dict — not numeric scores. `app.py` adds them to `parsed_data` from `config.*_text` attributes. `config.get_data_dict()` does NOT include them; they are added separately in `app.py`'s `parse_data()`.

## Prompt rules (do not violate)

- Never use `"reinfestación"` — only `"infestación"` (report covers one visit, not a time series)
- Always write `"roedores (plaga menor)"` — never without parentheses
- Recommendations must be suggestive (`"se sugiere"`, `"se recomienda"`), no deadlines, no urgency, no service actions (monitoring, product application, station installation)
- LLM must not invent data not present in the prompt
