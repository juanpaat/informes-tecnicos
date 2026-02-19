<div align="center">
  <img src="logo2021.png" alt="Serviplagas" width="200"/>
</div>

# Sistema de Generación de Informes Técnicos

Genera informes técnicos de control de plagas en formato Word a partir de una fila copiada directamente de la hoja de cálculo.

---

## Requisitos

- Python 3.9 o superior
- El archivo `INFORME TÉCNICO FINAL.docx` en la raíz del proyecto
- Una clave de API de OpenAI (opcional — si no se configura, el informe se genera con los textos originales del técnico)

---

## Instalación

```bash
pip install -r requirements.txt
```

---

## Cómo ejecutar

```bash
streamlit run app.py
```

Se abre en `http://localhost:8501`.

---

## Flujo de uso

1. Copia una fila completa de la hoja de cálculo (59 o 60 columnas, separadas por tabulaciones).
2. Pégala en el área de texto y haz clic en **"Cargar Datos"**.
3. Revisa y edita los campos si es necesario.
4. Haz clic en **"Generar Informe Técnico"**.
5. Descarga el archivo `.docx`.

---

## Configurar la clave de OpenAI

El sistema la busca en este orden:

1. **Streamlit Secrets** (para despliegue en la nube): agrega en la configuración de Secrets de la app:
   ```
   OPENAI_API_KEY = "sk-..."
   ```
2. **Archivo `.env`** (para uso local): crea el archivo en la raíz del proyecto:
   ```
   OPENAI_API_KEY=sk-...
   ```
3. **Variable de entorno del sistema**:
   ```bash
   export OPENAI_API_KEY="sk-..."   # macOS / Linux
   set OPENAI_API_KEY=sk-...        # Windows
   ```

---

## Estructura del proyecto

```
informes-tecnicos/
├── app.py                        # Aplicación web (Streamlit) — interfaz principal
├── main.py                       # Alternativa por línea de comandos
├── config.py                     # Parseo de datos, pesos de riesgo y prompts de IA
├── utils.py                      # Gráficos, plantilla y llamadas a la API
├── requirements.txt              # Dependencias
├── .env                          # Clave de OpenAI (no se sube al repositorio)
├── INFORME TÉCNICO FINAL.docx    # Plantilla Word
└── logo2021.png                  # Logo de la empresa
```

---

## Cómo editar

### Ajustar el peso de los factores de riesgo
Edita los diccionarios `PESOS_RIESGO_EXTERNO` y `PESOS_RIESGO_INTERNO` en `config.py`. Los pesos de cada grupo deben sumar `1.0`.

### Cambiar los textos o instrucciones de la IA
Los prompts están en `config.py`:
- `LANGCHAIN_PROMPT_TEMPLATE` — controla cómo se mejoran las observaciones generales.
- `RECOMMENDATIONS_PROMPT_TEMPLATE` — controla cómo se generan las recomendaciones.

### Modificar la plantilla Word
Abre `INFORME TÉCNICO FINAL.docx` y edita el diseño libremente. Los marcadores `{{nombre}}` se reemplazan automáticamente al generar el informe. No elimines ni cambies el nombre de un marcador si no actualizas también el código.

### Marcadores disponibles

| Categoría | Marcadores |
|---|---|
| Cliente y servicio | `{{cliente}}`, `{{sede}}`, `{{direccion}}`, `{{municipio}}`, `{{telefono}}`, `{{sector}}`, `{{fidelidad}}`, `{{fecha}}`, `{{hora}}`, `{{h_inicio}}`, `{{h_salida}}` |
| Personal | `{{tecnico_encargado}}`, `{{tecnicos}}`, `{{acompanante}}`, `{{cargo}}` |
| Control | `{{tipo_de_control}}`, `{{metodo_control}}`, `{{areas_controladas}}`, `{{plaguicidas}}`, `{{periodicidad}}` |
| Textos principales | `{{obs_generales}}`, `{{reco_general}}`, `{{reco_especificas_1}}`, `{{reco_especificas_2}}`, `{{reco_especificas_3}}`, `{{antecedentes}}` |
| Plagas | `{{cucarachas}}`, `{{hormigas}}`, `{{moscas}}`, `{{mosquitos}}`, `{{zancudo}}`, `{{raton_casero}}`, `{{rata_noruega}}`, `{{raton_tejado}}`, `{{larvas_mosquitos}}` |
| Gráficos | `{{img_1}}`, `{{img_2}}`, `{{riesgos_externos_plot}}`, `{{riesgos_internos_plot}}` |

---

## Problemas comunes

| Síntoma | Causa probable | Solución |
|---|---|---|
| "No se pueden cargar los datos" | La fila no tiene 59 o 60 campos | Copia la fila completa desde la hoja de cálculo |
| "Template file not found" | Falta la plantilla Word | Verifica que `INFORME TÉCNICO FINAL.docx` esté en la raíz |
| Recomendaciones u observaciones sin mejorar | Clave de OpenAI no configurada o inválida | Configura la clave según la sección anterior |
| Marcadores sin reemplazar en el documento | El marcador en la plantilla no coincide exactamente | Verifica que use el formato `{{nombre_del_campo}}` sin espacios ni tildes adicionales |
