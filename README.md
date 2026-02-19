<div align="center">
  <img src="logo2021.png" alt="Serviplagas" width="200"/>
</div>

# Sistema de Generación de Informes Técnicos — Serviplagas

Automatiza la creación de informes técnicos de control de plagas. Toma los datos de una fila de la hoja de cálculo (Google Sheets / Excel), los procesa y genera un documento Word profesional con gráficos y texto mejorado por IA.

---

## Estructura del proyecto

```
informes-tecnicos/
├── app.py                        # Aplicación web (Streamlit) — interfaz principal
├── main.py                       # Alternativa por línea de comandos
├── config.py                     # Parseo de datos, pesos de riesgo y prompts de IA
├── utils.py                      # Generación de gráficos, reemplazo de plantilla y llamadas a IA
├── requirements.txt              # Dependencias de Python
├── .env                          # Clave de API de OpenAI (no se sube al repositorio)
├── INFORME TÉCNICO FINAL.docx    # Plantilla Word requerida
└── logo2021.png                  # Logo de la empresa
```

---

## Requisitos

- Python 3.9 o superior
- Una clave de API de OpenAI (necesaria para la mejora automática de texto)
- El archivo de plantilla `INFORME TÉCNICO FINAL.docx` en la raíz del proyecto

---

## Instalación

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar la clave de OpenAI (ver sección más abajo)
```

---

## Cómo usar

### Opción A — Aplicación web (recomendada)

```bash
streamlit run app.py
```

Se abre automáticamente en `http://localhost:8501`.

**Pasos:**
1. Copia una fila completa de la hoja de cálculo (debe tener 59 o 60 campos separados por tabulaciones).
2. Pégala en el área de texto y haz clic en **"Cargar Datos"**.
3. Revisa y edita los campos que necesites (cliente, observaciones, condiciones de riesgo, etc.).
4. Haz clic en **"Generar Informe Técnico"**.
5. Descarga el archivo `.docx` generado.

### Opción B — Línea de comandos

1. Abre `config.py` y reemplaza el valor de `SPREADSHEET_LINE` con tu fila de datos.
2. Ejecuta:

```bash
python main.py
```

El informe se guarda como `Informe_[CLIENTE]_[FECHA].docx` en la misma carpeta.

---

## Configuración de la clave de OpenAI

El sistema busca la clave en este orden:

1. **Streamlit Secrets** (para despliegue en Streamlit Cloud): agrega `OPENAI_API_KEY = "sk-..."` en la configuración de Secrets de la app.
2. **Archivo `.env`** (para uso local): crea un archivo `.env` en la raíz del proyecto con:
   ```
   OPENAI_API_KEY=sk-...
   ```
3. **Variable de entorno del sistema**:
   ```bash
   export OPENAI_API_KEY="sk-..."   # macOS / Linux
   set OPENAI_API_KEY=sk-...        # Windows
   ```

Si no se configura ninguna clave, el sistema funciona igual pero usa los textos originales del técnico sin mejora de IA.

---

## Qué hace la IA

Cuando la clave de OpenAI está configurada, el sistema realiza **dos llamadas al modelo** al momento de generar el informe:

### 1. Mejora de observaciones generales (`obs_generales`)
Reescribe y mejora el texto de observaciones del técnico integrando de forma coherente:
- Las condiciones higiénicas y locativas externas e internas
- Las plagas encontradas en la visita
- El sector y tipo de control

**Modelo:** `gpt-5-mini` | **Temperatura:** 0.1 | **Tokens máx.:** 1 500

### 2. Generación de recomendaciones
Genera 4 recomendaciones complementarias entre sí a partir del contexto completo de la visita:

| Campo | Descripción |
|---|---|
| `reco_general` | Cuidado del tratamiento aplicado (conservar plaguicidas, evitar mojar superficies, continuidad del programa) |
| `reco_especificas_1` | Sugerencia sobre un aspecto higiénico o locativo (ej. sellamiento, accesos) |
| `reco_especificas_2` | Sugerencia sobre un aspecto diferente (ej. almacenamiento, manejo de residuos) |
| `reco_especificas_3` | Sugerencia sobre un tercer aspecto (ej. ventilación, drenajes, iluminación) |

Las recomendaciones usan un tono sugerente y cortés ("se sugiere", "se recomienda"). No incluyen plazos, urgencias ni acciones propias del servicio de control de plagas.

**Modelo:** `gpt-5-mini` | **Temperatura:** 0.2 | **Tokens máx.:** 2 000

Si alguna llamada falla (error de API, clave inválida, etc.), el sistema mantiene el texto original del técnico sin interrumpir la generación del informe.

---

## Gráficos generados automáticamente

El informe incluye 4 visualizaciones creadas con matplotlib:

| Gráfico | Descripción |
|---|---|
| `{{img_1}}` | Barras de presencia de plagas (9 tipos) |
| `{{img_2}}` | Matriz de riesgo interno vs. externo (3×3) |
| `{{riesgos_externos_plot}}` | Dona de distribución de riesgos externos (11 factores) |
| `{{riesgos_internos_plot}}` | Dona de distribución de riesgos internos (12 factores) |

---

## Marcadores disponibles en la plantilla Word

Los marcadores tienen el formato `{{nombre}}` y se reemplazan automáticamente.

**Información del servicio:**
`{{cliente}}`, `{{sede}}`, `{{direccion}}`, `{{municipio}}`, `{{telefono}}`, `{{sector}}`, `{{fidelidad}}`, `{{fecha}}`, `{{hora}}`, `{{h_inicio}}`, `{{h_salida}}`

**Personal:**
`{{tecnico_encargado}}`, `{{tecnicos}}`, `{{acompanante}}`, `{{cargo}}`

**Detalles del control:**
`{{tipo_de_control}}`, `{{metodo_control}}`, `{{areas_controladas}}`, `{{plaguicidas}}`, `{{periodicidad}}`

**Textos principales:**
`{{obs_generales}}`, `{{reco_general}}`, `{{reco_especificas_1}}`, `{{reco_especificas_2}}`, `{{reco_especificas_3}}`, `{{antecedentes}}`

**Presencia de plagas:**
`{{cucarachas}}`, `{{hormigas}}`, `{{moscas}}`, `{{mosquitos}}`, `{{zancudo}}`, `{{raton_casero}}`, `{{rata_noruega}}`, `{{raton_tejado}}`, `{{larvas_mosquitos}}`

---

## Cálculo de riesgos

Los riesgos se calculan a partir de las calificaciones de la hoja de cálculo (emojis como `🟢 Buena`, `🟠 Regular`, `🔴 Mala`) aplicando pesos configurables definidos en `config.py`.

**Factores externos (11):** condiciones del vecindario, limpieza, basuras, infraestructura, iluminación, animales, construcciones, zonas verdes, cuerpos de agua, desagües, locales de comida.

**Factores internos (12):** condiciones generales, limpieza, almacenamiento, iluminación, capacitación del personal, sellamiento de puertas, ventilación, grietas, entrada/salida de material, acumulación de objetos, áreas de manipulación de comida, presencia de animales.

Para ajustar la importancia de cada factor, edita los diccionarios `PESOS_RIESGO_EXTERNO` y `PESOS_RIESGO_INTERNO` en `config.py`. Los pesos de cada grupo deben sumar 1.0.

---

## Problemas comunes

| Error | Causa probable | Solución |
|---|---|---|
| "No se pueden cargar los datos" | La fila no tiene 59 o 60 campos | Copia la fila completa desde la hoja de cálculo incluyendo todas las columnas |
| "Template file not found" | Falta la plantilla Word | Verifica que `INFORME TÉCNICO FINAL.docx` esté en la raíz del proyecto |
| "OPENAI_API_KEY no configurada" | Clave de API no encontrada | Configura la clave en `.env`, en variables de entorno o en Streamlit Secrets |
| "No se pudieron generar recomendaciones" | Error en la llamada a OpenAI | Revisa saldo, conexión y validez de la clave. El informe se genera igual con los textos originales |
| "Font family 'Roboto Mono' not found" | Fuente no instalada en el servidor | No es un error crítico; el documento se genera correctamente con una fuente alternativa |
| El informe tiene marcadores sin reemplazar | El marcador en la plantilla no coincide con la clave | Verifica que el marcador en el `.docx` use exactamente `{{nombre_del_campo}}` |
