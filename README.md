# 📊 Sistema de Generación de Informes Técnicos

## 🎯 ¿Qué hace este sistema?

Este sistema automatiza la creación de informes técnicos para servicios de control de plagas. Toma datos de una hoja de cálculo (Excel/Google Sheets) y los convierte en un documento de Word profesional con gráficos incluidos.

### Características principales:
- ✅ Reemplaza automáticamente todos los datos del servicio en la plantilla
- ✅ Genera 4 gráficos profesionales (presencia de plagas, matriz de riesgo, y gráficos de dona)
- ✅ Calcula automáticamente los puntajes de riesgo interno y externo
- ✅ Limpia y formatea el texto automáticamente
- ✅ Crea archivos con nombres únicos por cliente y fecha

## 🚀 Cómo usar el sistema

### 1. Preparación inicial
```bash
# Asegúrate de estar en el directorio del proyecto
cd /ruta/a/informes-tecnicos

# Instala las dependencias (solo la primera vez)
pip install -r requirements.txt
```

### 2. Configurar tus datos
1. **Abre el archivo `config.py`**
2. **Busca la línea que dice `SPREADSHEET_LINE =`**
3. **Reemplaza todo el texto entre las comillas con los datos de tu hoja de cálculo**

```python
# Ejemplo: copia una fila completa de Excel/Google Sheets y pégala aquí
SPREADSHEET_LINE = "11/10/2025 19:28:13	3692	U.R. CAMINO VERDE DEL BOSQUE..."
```

### 3. Ejecutar el sistema
```bash
python main.py
```

**¡Eso es todo!** El sistema creará automáticamente tu informe con el nombre:
`Informe_[NOMBRE_CLIENTE]_[FECHA].docx`

## 📁 Estructura del proyecto

```
informes-tecnicos/
├── main.py                          # Archivo principal - ejecuta todo el proceso
├── config.py                        # Configuración - aquí pones tus datos
├── utils.py                         # Funciones internas del sistema
├── requirements.txt                 # Lista de programas necesarios
├── INFORME TÉCNICO FINAL.docx       # Plantilla (DEBE existir)
└── README.md                        # Esta guía
```

## 🔧 Archivos explicados en detalle

### **config.py** - El cerebro del sistema
**¿Qué hace?**
- Toma la línea de hoja de cálculo que pegaste
- La divide en 60 campos individuales (cliente, dirección, fecha, etc.)
- Calcula automáticamente los puntajes de riesgo
- Convierte las calificaciones con emojis (🔴 Mala, 🟢 Excelente) a números

**Datos que procesa:**
- Información básica: cliente, dirección, técnico, fecha, hora
- Presencia de plagas: cucarachas, hormigas, moscas, ratones, etc.
- Evaluación de riesgos externos: limpieza del vecindario, cercanía a basuras, etc.
- Evaluación de riesgos internos: limpieza del establecimiento, capacitación, etc.
- Observaciones y recomendaciones del técnico

### **main.py** - El coordinador
**¿Qué hace?**
1. Carga la configuración desde `config.py`
2. Abre la plantilla de Word
3. Genera los 4 gráficos automáticamente
4. Reemplaza todos los {{marcadores}} con datos reales
5. Guarda el informe final

**Proceso paso a paso:**
1. **Validación**: Verifica que existe la plantilla
2. **Generación de gráficos**: Crea las 4 visualizaciones
3. **Inserción de imágenes**: Coloca los gráficos en el documento
4. **Reemplazo de texto**: Sustituye todos los {{marcadores}}
5. **Guardado**: Crea el archivo final

### **utils.py** - Las herramientas
**¿Qué contiene?**
- **ReportGenerator**: Clase principal que maneja el documento de Word
- **Funciones de gráficos**: Crean las visualizaciones profesionales
- **Herramientas de texto**: Limpian y formatean el texto automáticamente
- **Cálculos de riesgo**: Convierten calificaciones a puntajes numéricos

## 📊 Gráficos que genera automáticamente

### 1. **{{img_1}}** - Gráfico de Presencia de Plagas
- **Tipo**: Gráfico de barras
- **Tamaño**: 7.2cm × 4.55cm
- **Muestra**: Nivel de infestación de 9 tipos de plagas
- **Escala**: 0-4 (0=Sin evidencia, 4=Mucha evidencia)

### 2. **{{img_2}}** - Matriz de Evaluación de Riesgos
- **Tipo**: Matriz 3×3 con colores
- **Tamaño**: 7.2cm × 4.55cm
- **Muestra**: Posición del riesgo total (interno vs externo)
- **Colores**: Rojo=Alto riesgo, Naranja=Medio, Verde=Bajo

### 3. **{{riesgos_externos_plot}}** - Gráfico de Dona de Riesgos Externos
- **Tipo**: Gráfico de dona con líneas de conexión
- **Tamaño**: 12cm × 7.60cm
- **Muestra**: Distribución de 11 factores de riesgo externos
- **Incluye**: Limpieza del vecindario, manejo de basuras, cercanía a restaurantes, etc.

### 4. **{{riesgos_internos_plot}}** - Gráfico de Dona de Riesgos Internos
- **Tipo**: Gráfico de dona con líneas de conexión
- **Tamaño**: 12cm × 7.60cm
- **Muestra**: Distribución de 12 factores de riesgo internos
- **Incluye**: Limpieza del establecimiento, capacitación, sellamiento, etc.

## � Cómo funciona el reemplazo de marcadores

### Formato correcto de marcadores:
```
{{ nombre_del_campo }}
```

### Ejemplos de marcadores que se reemplazan automáticamente:
```
{{ cliente }}           → "U.R. CAMINO VERDE DEL BOSQUE"
{{ direccion }}         → "Cl. 39SUR # 27 - 55"
{{ fecha }}             → "11/10/2025"
{{ tecnico_encargado }} → "Jose Garizado"
{{ obs_generales }}     → "En el momento de realizar el control..."
{{ reco_general }}      → "Conservar plaguicidas aplicados..."
```

## 🔍 Solución de problemas comunes

### ❌ Error: "Template file not found"
**Problema**: No encuentra la plantilla
**Solución**: Asegúrate de que existe el archivo `INFORME TÉCNICO FINAL.docx` en la carpeta

### ❌ Error: "Expected 60 values, got X values"
**Problema**: Los datos de la hoja de cálculo no tienen 60 columnas
**Soluciones**:
1. Verifica que copiaste la fila completa (todas las columnas)
2. Revisa el `DELIMITER` en `config.py`:
   - `'\t'` para Excel/Google Sheets (tabulaciones)
   - `','` para archivos CSV (comas)

### ❌ Los gráficos no aparecen
**Problema**: Las imágenes no se insertan
**Verificaciones**:
1. Revisa que los marcadores estén escritos correctamente:
   - `{{img_1}}` (presencia de plagas)
   - `{{img_2}}` (matriz de riesgo)
   - `{{riesgos_externos_plot}}` (dona externa)
   - `{{riesgos_internos_plot}}` (dona interna)

### ❌ Algunos marcadores no se reemplazan
**Problema**: Quedan {{marcadores}} sin reemplazar en el documento final
**Soluciones**:
1. Verifica que el marcador en la plantilla coincida exactamente con el nombre en `config.py`
2. Revisa que no haya espacios extra: `{{ cliente }}` (correcto) vs `{{  cliente  }}` (incorrecto)
3. Considera mayúsculas y minúsculas

## 🛠️ Personalización avanzada

### Agregar nuevos marcadores:
1. **En `config.py`**, agrega el nuevo campo en `get_data_dict()`:
```python
def get_data_dict(self) -> Dict[str, Any]:
    return {
        'mi_nuevo_campo': self.algun_valor,
        # ... otros campos existentes
    }
```

2. **En la plantilla de Word**, agrega: `{{ mi_nuevo_campo }}`

### Cambiar el tamaño de las imágenes:
1. **Para img_1 e img_2** (presencia y matriz): Modifica en `main.py`:
```python
generator.add_image_to_placeholder(
    placeholder="{{img_1}}",
    image_path=viz1,
    width=7.2,    # Cambiar aquí
    height=4.55   # Y aquí
)
```

2. **Para gráficos de dona**: Modifica en `main.py`:
```python
generator.add_image_to_placeholder(
    placeholder="{{riesgos_externos_plot}}",
    image_path=viz3,
    width=12.0,   # Cambiar aquí
    height=7.60   # Y aquí
)
```

### Modificar los cálculos de riesgo:
En `config.py`, ajusta los pesos en las secciones:
- `PESOS_RIESGO_EXTERNO`: Para factores externos
- `PESOS_RIESGO_INTERNO`: Para factores internos

## 📋 Lista completa de marcadores disponibles

**Información básica del servicio:**
- `{{ cliente }}`, `{{ direccion }}`, `{{ municipio }}`
- `{{ fecha }}`, `{{ hora }}`, `{{ h_inicio }}`, `{{ h_salida }}`
- `{{ tecnico_encargado }}`, `{{ tecnicos }}`, `{{ acompanante }}`, `{{ cargo }}`

**Detalles del servicio:**
- `{{ tipo_de_control }}`, `{{ metodo_control }}`, `{{ areas_controladas }}`
- `{{ plaguicidas }}`, `{{ periodicidad }}`

**Observaciones y recomendaciones:**
- `{{ obs_generales }}`, `{{ reco_general }}`
- `{{ reco_especificas_1 }}`, `{{ reco_especificas_2 }}`, `{{ reco_especificas_3 }}`
- `{{ antecedentes }}`

**Datos de contacto:**
- `{{ telefono }}`, `{{ sector }}`, `{{ fidelidad }}`

**Presencia de plagas (texto):**
- `{{ cucarachas }}`, `{{ hormigas }}`, `{{ moscas }}`, `{{ mosquitos }}`
- `{{ zancudo }}`, `{{ raton_casero }}`, `{{ rata_noruega }}`, `{{ raton_tejado }}`
- `{{ larvas_mosquitos }}`

**Gráficos (imágenes):**
- `{{ img_1 }}` - Gráfico de presencia de plagas
- `{{ img_2 }}` - Matriz de evaluación de riesgos  
- `{{ riesgos_externos_plot }}` - Gráfico de dona de riesgos externos
- `{{ riesgos_internos_plot }}` - Gráfico de dona de riesgos internos

## ✅ Estado actual del sistema

**✅ COMPLETAMENTE FUNCIONAL**
- Procesa automáticamente 60 campos de datos
- Genera 4 gráficos profesionales de alta calidad
- Reemplaza todos los marcadores correctamente
- Calcula riesgos automáticamente con pesos configurables
- Limpia y formatea texto automáticamente
- Maneja archivos temporales de manera eficiente

**Rendimiento típico:**
- Tiempo de generación: 1-3 segundos
- Tamaño del documento final: ~500KB-1MB
- Calidad de imágenes: 300 DPI (profesional)

## 📞 Soporte

Si encuentras problemas:
1. Verifica que todos los archivos estén en el directorio correcto
2. Revisa que la plantilla `INFORME TÉCNICO FINAL.docx` existe
3. Confirma que los datos de la hoja de cálculo están completos (60 columnas)
4. Ejecuta `python main.py` y revisa los mensajes en la consola

¡El sistema está diseñado para ser simple y confiable! La mayoría de problemas se resuelven verificando que los archivos estén en su lugar y que los datos estén completos.
