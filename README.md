# Sistema de Generación de Informes Técnicos

## ¿Qué hace este sistema?

Este sistema automatiza la creación de informes técnicos para servicios de control de plagas. Toma datos de una hoja de cálculo (Excel/Google Sheets) y los convierte en un documento de Word profesional con gráficos incluidos.

## 🌐 **Aplicación Web - Listo para la Nube**

### **Uso en Línea (Streamlit Cloud)**
La aplicación está desplegada y lista para usar en la nube:
- **Acceso directo desde cualquier navegador**
- **Sin instalación requerida**
- **Interfaz intuitiva y profesional**
- **Descarga directa de informes**

### **Uso Local**
```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar aplicación web
streamlit run app.py

# 3. Usar desde el navegador
# - Se abre automáticamente en http://localhost:8501
# - Pegar datos de Excel/Google Sheets
# - Revisar y editar campos
# - Generar y descargar informe
```

### 💻 **Método Tradicional (Línea de Comandos)**

#### 1. Preparación inicial
```bash
# Asegúrate de estar en el directorio del proyecto
cd /ruta/a/informes-tecnicos

# Instala las dependencias (solo la primera vez)
pip install -r requirements.txt
```

#### 2. Configurar tus datos
1. **Abre el archivo `config.py`**
2. **Busca la línea que dice `SPREADSHEET_LINE =`**
3. **Reemplaza todo el texto entre las comillas con los datos de tu hoja de cálculo**

```python
# Ejemplo: copia una fila completa de Excel/Google Sheets y pégala aquí
SPREADSHEET_LINE = "11/10/2025 19:28:13	3692	U.R. CAMINO VERDE DEL BOSQUE..."
```

#### 3. Ejecutar el sistema
```bash
python main.py
```

**¡Eso es todo!** El sistema creará automáticamente tu informe con el nombre:
`Informe_[NOMBRE_CLIENTE]_[FECHA].docx`

---

## ✨ **Características Principales**

### **🔄 Proceso Automático Completo**
1. **Pegar datos** de Excel/Google Sheets directamente (60 campos automáticos)
2. **Editar campos** en tiempo real con interfaz visual organizada por categorías
3. **Aplicar formato consistente** automáticamente con fuente Roboto Mono
4. **Generar gráficos** automáticamente (4 tipos de visualizaciones profesionales)
5. **Descargar informe** en formato Word profesional con un clic

### **📊 Visualizaciones Automáticas**
- **Gráfico de barras**: Presencia de plagas por tipo
- **Matriz de riesgo**: Evaluación visual de riesgos internos vs externos  
- **Gráfico de dona**: Distribución de riesgos externos
- **Gráfico de dona**: Distribución de riesgos internos

### **🤖 Corrección Automática de Texto con IA (NUEVO)**
- **Integración LangChain + OpenAI**: Corrección inteligente de español latinoamericano
- **Campos corregidos automáticamente**: observaciones, recomendaciones específicas, antecedentes
- **Preservación del contenido**: Mantiene significado, tono y registro originales
- **Configuración opcional**: Funciona sin API key (devuelve texto original)

### **🌟 Ventajas de la Interfaz Web**

| Característica | Descripción |
|---|---|
| **📱 Accesible** | Funciona en cualquier navegador, celular o computadora |
| **🚀 Sin instalación** | No requiere software adicional |
| **✏️ Edición visual** | Modifica cualquier campo antes de generar |
| **📊 Vista previa** | Ve todos los datos organizados por categorías |
| **🔤 Fuente consistente** | Aplica automáticamente Roboto Mono para uniformidad |
| **🤖 Corrección IA** | LangChain + OpenAI corrigen automáticamente textos en español |
| **⚡ Rápido** | Genera informes en segundos |
| **☁️ En la nube** | Acceso desde cualquier lugar |

## 🎯 **Cómo Usar el Sistema**

### **Paso 1: Acceder a la Aplicación**
- **En línea**: Accede directamente desde el navegador (enlace proporcionado)
- **Local**: Ejecuta `streamlit run app.py` en tu computadora

### **Paso 2: Cargar Datos**
1. **Copia** una fila completa de tu hoja de cálculo (Excel/Google Sheets)
2. **Pega** los datos en el área de texto de la aplicación
3. **Haz clic** en "📥 Cargar Datos"

### **Paso 3: Revisar y Editar**
- La aplicación muestra automáticamente todos los campos organizados por categorías:
  - 🏢 **Información del Cliente**: Cliente, sede, dirección, municipio, teléfono, sector
  - 📅 **Información del Servicio**: Fecha, horas, tipo de control, método, áreas
  - 👥 **Personal**: Técnico encargado, técnicos, acompañante, cargo
  - 🔬 **Tratamiento y Observaciones**: Plaguicidas, observaciones, recomendaciones
  - 🐛 **Presencia de Plagas**: 9 tipos con selectores visuales (🟢 Sin evidencia → 🔴 Mucha evidencia)
  - 🌍 **Riesgos Externos**: 11 factores con opciones cualitativas y cuantitativas
  - 🏢 **Riesgos Internos**: 12 factores con evaluación detallada
- **Edita** cualquier campo con interfaz intuitiva (texto, áreas de texto, selectores)
- **Datos adicionales** disponibles en sección expandible

### **Paso 4: Generar Informe**
1. **Haz clic** en "📄 Generar Informe Técnico"
2. **Espera** mientras se procesan los datos y se crean los gráficos
3. **Descarga** automáticamente el archivo Word con un clic

## �📁 Estructura del proyecto

```
informes-tecnicos/
├── app.py                           # 🌐 Aplicación web Streamlit (PRINCIPAL)
├── main.py                          # 💻 Versión línea de comandos (alternativa)
├── config.py                        # ⚙️ Configuración y cálculos automáticos
├── utils.py                         # 🔧 Funciones de generación, gráficos y corrección IA
├── requirements.txt                 # 📦 Dependencias de Python (incluye LangChain)
├── .env                             # 🔑 Variables de entorno (OPENAI_API_KEY)
├── .env.example                     # 📋 Ejemplo de configuración de variables
├── INFORME TÉCNICO FINAL.docx       # 📋 Plantilla Word (REQUERIDA)
├── logo2021.png                     # 🎨 Logo de la empresa
└── README.md                        # 📖 Esta guía
```

### **🤖 Corrección Automática de Texto con IA**

El sistema integra **LangChain + OpenAI** para corregir automáticamente textos en español latinoamericano, mejorando la calidad profesional de los informes.

#### **📝 Campos Corregidos Automáticamente**
- **`obs_generales`**: Observaciones generales del servicio
- **`reco_especificas_1`**: Primera recomendación específica  
- **`reco_especificas_2`**: Segunda recomendación específica
- **`reco_especificas_3`**: Tercera recomendación específica
- **`antecedentes`**: Información de antecedentes del cliente

#### **🔧 Configuración de OpenAI API**

**Para habilitar las correcciones automáticas:**

1. **Obtener API Key de OpenAI**:
   - Visita [platform.openai.com](https://platform.openai.com)
   - Crea una cuenta o inicia sesión
   - Ve a "API Keys" y genera una nueva clave
   - Copia la clave (comienza con `sk-...`)

2. **Configurar según el entorno**:

   **🥇 Opción 1: Streamlit Cloud (Recomendado para producción)**
   ```toml
   # En la configuración de Streamlit Cloud, agregar en "Secrets":
   OPENAI_API_KEY = "tu_clave_aqui"
   ```

   **🥈 Opción 2: Testing Local (.env)**
   ```bash
   # Crear archivo .env en el directorio del proyecto
   echo "OPENAI_API_KEY=tu_clave_aqui" > .env
   ```

   **🥉 Opción 3: Variable de Entorno del Sistema**
   ```bash
   # Linux/Mac
   export OPENAI_API_KEY="tu_clave_aqui"
   
   # Windows
   set OPENAI_API_KEY=tu_clave_aqui
   ```

#### **🔄 Jerarquía de Configuración (NUEVO)**

El sistema busca la API key en este orden de prioridad:

1. **🏆 Streamlit Secrets** (`.streamlit/secrets.toml` o configuración cloud)
2. **🔧 Archivo .env** (para desarrollo local)
3. **💻 Variable de entorno del sistema**
4. **⚠️ Sin API key** (funciona sin correcciones automáticas)

#### **⚙️ Funcionamiento**

**Con API Key configurada**:
- ✅ **Corrección automática** aplicada a todos los campos especificados
- ✅ **Mejora ortografía, gramática y puntuación** 
- ✅ **Preserva significado y tono original**
- ✅ **Optimizado para español latinoamericano**

**Sin API Key**:
- ⚠️ **Advertencia en consola** pero el sistema funciona normalmente
- ✅ **Textos originales** se mantienen sin cambios
- ✅ **Generación de informes** continúa sin interrupciones

#### **🎯 Prompt de Corrección Especializado**

El sistema utiliza un prompt específicamente diseñado para corrección de español:

```
Eres un experto lingüista y corrector de estilo especializado en español latinoamericano.
Tu función es reescribir textos en español para mejorar su ortografía, gramática, puntuación y coherencia,
manteniendo el significado original, el tono natural y el registro adecuado.
No resumas, no traduzcas, no cambies el contenido factual.
Simplemente corrige y mejora la redacción cuando sea necesario.
Si el texto ya está bien escrito, devuélvelo sin cambios.
```

#### **💡 Características de la Corrección IA**

| Aspecto | Descripción |
|---|---|
| **Modelo usado** | GPT-3.5-turbo (balance calidad/costo) |
| **Temperatura** | 0.1 (precisión máxima) |
| **Límite tokens** | 1000 por campo |
| **Idioma objetivo** | Español latinoamericano |
| **Preservación** | Contenido factual y tono original |
| **Fallback** | Funciona sin API key (devuelve original) |

## 🧠 **Inteligencia del Sistema**

### **Procesamiento Automático de Datos**
El sistema reconoce y procesa automáticamente **60 campos** de información:

**📋 Información Básica**
- Cliente, dirección, municipio, teléfono
- Fecha, horas de servicio, técnicos
- Tipo de control, métodos aplicados

**� Evaluación de Plagas**
- 9 tipos de plagas evaluadas
- Niveles de infestación automáticos
- Conversión de emojis a puntajes numéricos

**⚠️ Análisis de Riesgos**
- **11 factores externos**: Vecindario, basuras, construcciones, etc.
- **12 factores internos**: Limpieza, capacitación, sellamiento, etc.
- **Cálculo automático** con pesos configurables
- **Matriz visual** de riesgos combinados

### **Generación Inteligente de Gráficos**
1. **Detecta automáticamente** los niveles de riesgo
2. **Calcula distribuciones** proporcionales
3. **Genera colores** apropiados según el riesgo
4. **Crea leyendas** descriptivas
5. **Optimiza tamaños** para el documento final

### **Motor de Plantillas**
- **Busca automáticamente** todos los marcadores `{{campo}}`
- **Reemplaza texto** en párrafos y tablas
- **Inserta imágenes** en posiciones exactas
- **Mantiene formato** original del documento
- **Limpia archivos temporales** automáticamente

## 📊 **Gráficos que Genera Automáticamente**

El sistema crea **4 visualizaciones profesionales** que se insertan automáticamente en el informe:

### **1. 📊 Gráfico de Presencia de Plagas**
- **Qué muestra**: Nivel de infestación de 9 tipos de plagas
- **Formato**: Gráfico de barras con escala visual
- **Escala**: 0 (Sin evidencia) → 4 (Mucha evidencia)
- **Plagas incluidas**: Cucarachas, hormigas, moscas, mosquitos, zancudos, ratones, ratas, larvas

### **2. 🎯 Matriz de Evaluación de Riesgos**
- **Qué muestra**: Posición exacta del riesgo total combinado
- **Formato**: Matriz 3×3 con código de colores
- **Ejes**: Riesgo Interno (X) vs Riesgo Externo (Y)
- **Colores**: 🔴 Alto → 🟠 Medio → 🟢 Bajo
- **Zonas numeradas**: I-IX para fácil referencia

### **3. 🌍 Gráfico de Dona - Riesgos Externos**
- **Qué muestra**: Distribución proporcional de 11 factores externos
- **Incluye**: Limpieza vecindario, manejo basuras, construcciones cercanas, locales de comida
- **Formato**: Gráfico de dona con porcentajes automáticos
- **Inteligente**: Solo muestra factores con riesgo > 0

### **4. 🏢 Gráfico de Dona - Riesgos Internos**
- **Qué muestra**: Distribución proporcional de 12 factores internos
- **Incluye**: Limpieza establecimiento, capacitación, sellamiento, ventilación, grietas
- **Formato**: Gráfico de dona con porcentajes automáticos
- **Inteligente**: Solo muestra factores con riesgo > 0

## 🔄 **Sistema de Marcadores Inteligente**

### **Funcionamiento Automático**
El sistema busca y reemplaza automáticamente **todos los marcadores** en la plantilla Word:

**Formato de marcadores:**
```
{{ nombre_del_campo }}
```

**Ejemplos de reemplazo automático:**
```
{{ cliente }}           → "U.R. CAMINO VERDE DEL BOSQUE"
{{ direccion }}         → "Cl. 39SUR # 27 - 55"  
{{ fecha }}             → "11/10/2025"
{{ tecnico_encargado }} → "Jose Garizado"
{{ obs_generales }}     → "En el momento de realizar el control..."
{{ plaguicidas }}       → "Black Jack gel, I con 10 me"
```

**Marcadores especiales para gráficos:**
```
{{ img_1 }}                    → Gráfico de presencia de plagas
{{ img_2 }}                    → Matriz de evaluación de riesgos
{{ riesgos_externos_plot }}    → Gráfico dona riesgos externos
{{ riesgos_internos_plot }}    → Gráfico dona riesgos internos
```

## ⚠️ **Problemas Comunes y Soluciones**

### **❌ "No se pueden cargar los datos"**
**Causa**: Datos incompletos o formato incorrecto
**Solución**: 
- Asegúrate de copiar **toda la fila** desde Excel/Google Sheets
- Incluye **todas las columnas** (debe tener 60 campos)
- Usa **Ctrl+C** para copiar y **Ctrl+V** para pegar
- Haz clic en "📥 Cargar Datos" después de pegar

### **❌ "Template file not found"**  
**Causa**: Falta el archivo de plantilla
**Solución**: 
- Verifica que existe `INFORME TÉCNICO FINAL.docx` 
- El archivo debe estar en la misma carpeta que `app.py`
- No cambies el nombre del archivo de plantilla

### **❌ "Error al generar gráficos"**
**Causa**: Problemas con los valores de riesgo
**Solución**:
- Revisa que los campos de riesgo tengan valores válidos
- Formatos correctos: 🟢 Excelente, 🟡 Buena, 🟠 Regular, 🔴 Mala
- Para cantidades: 🟢 Nada, 🟡 Pocas, 🟠 Bastantes, 🔴 Muchas

### **❌ "La descarga no funciona"**
**Causa**: Bloqueo del navegador o problema temporal
**Solución**:
- Actualiza la página y vuelve a generar
- Verifica que tu navegador permita descargas
- Intenta con otro navegador si persiste el problema

### **❌ "Faltan marcadores en el informe"**
**Causa**: Marcadores mal escritos en la plantilla
**Solución**:
- Verifica el formato exacto: `{{ campo }}` (con espacios)
- No uses `{{campo}}` (sin espacios)
- Revisa mayúsculas y minúsculas

### **❌ "LangChain: OPENAI_API_KEY no configurada"**
**Causa**: API key de OpenAI no está configurada en ninguna fuente
**Solución**:
- Obtén tu API key en [platform.openai.com](https://platform.openai.com/api-keys)
- **Streamlit Cloud**: Agrega `OPENAI_API_KEY` en la configuración de Secrets
- **Local Testing**: Crea archivo `.env` con `OPENAI_API_KEY=tu_clave_aqui`
- **Sistema**: Configura como variable de entorno del sistema
- **Funcionalidad**: El sistema funciona sin API key (usa textos originales)
- **Jerarquía**: El sistema busca en Streamlit Secrets → .env → variables de entorno

### **❌ "Error al corregir texto con LangChain"**
**Causa**: Problema de conectividad o límites de API de OpenAI
**Solución**:
- Verifica tu saldo de créditos en OpenAI
- Revisa tu conexión a internet
- Espera unos minutos si hay límites de velocidad
- **Funcionalidad**: El sistema continúa con textos originales automáticamente

### **❌ "Import langchain could not be resolved"**
**Causa**: Dependencias de LangChain no instaladas
**Solución**:
- Ejecuta: `pip install -r requirements.txt`
- Verifica que incluya: `langchain>=0.1.0` y `langchain-openai>=0.1.0`
- Reinicia el servidor Streamlit después de instalar
**Causa**: Advertencia normal - la fuente Roboto Mono no está instalada en el servidor
**Solución**:
- **No es un error crítico** - el sistema funciona correctamente
- Se usa automáticamente una fuente monoespaciada alternativa
- Los documentos mantienen consistencia de formato
- En Streamlit Cloud esto es comportamiento esperado y normal

## 🛠️ **Personalización y Configuración**

### **⚙️ Ajustar Cálculos de Riesgo**
Puedes modificar la importancia de cada factor editando los pesos en `config.py`:

**Riesgos Externos** (`PESOS_RIESGO_EXTERNO`):
```python
'limpieza_vecindario': 0.13,      # 13% del riesgo total
'manejo_basuras_vecindario': 0.13, # 13% del riesgo total  
'locales_comida': 0.14,           # 14% del riesgo total
# ... otros factores
```

**Riesgos Internos** (`PESOS_RIESGO_INTERNO`):
```python
'limpieza_establecimiento': 0.17,  # 17% del riesgo total
'areas_manipulacion_comida': 0.11, # 11% del riesgo total
'sellamiento_puertas': 0.10,       # 10% del riesgo total
# ... otros factores
```

### **📐 Cambiar Tamaños de Gráficos**
En `app.py`, líneas de `add_image_to_placeholder()`:

**Gráficos pequeños** (presencia y matriz):
```python
width=7.2, height=4.55  # Cambiar según necesidades
```

**Gráficos grandes** (donas):
```python  
width=12.0, height=7.60  # Cambiar según necesidades
```

### **🏷️ Agregar Nuevos Marcadores**
1. **En `config.py`**, agregar en `get_data_dict()`:
```python
'mi_nuevo_campo': self.mi_nuevo_valor,
```

2. **En la plantilla Word**, usar: `{{ mi_nuevo_campo }}`

### **🎨 Personalizar Colores de Gráficos**
En `utils.py`, modificar las secciones de colores:
- **Matriz**: Variable `colors` en `create_risk_matrix_plot()`
- **Donas**: `plt.cm.Reds` y `plt.cm.Blues` en las funciones de dona

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

## 🚀 **Estado del Sistema - Listo para Producción**

### **✅ Completamente Funcional**
- ✅ **Interfaz web profesional** con Streamlit
- ✅ **Procesamiento automático** de 60 campos de datos  
- ✅ **4 gráficos profesionales** generados automáticamente
- ✅ **Corrección IA automática** con LangChain + OpenAI (español latinoamericano)
- ✅ **Cálculo inteligente** de riesgos con pesos configurables
- ✅ **Reemplazo completo** de marcadores en plantilla Word
- ✅ **Descarga directa** sin archivos residuales en servidor
- ✅ **Limpieza automática** de archivos temporales
- ✅ **Optimizado para la nube** (Streamlit Cloud ready)

### **⚡ Rendimiento Optimizado**
| Característica | Especificación |
|---|---|
| **Tiempo de generación** | 2-5 segundos completos |
| **Tamaño del informe** | 500KB - 1MB (con gráficos) |
| **Calidad de imágenes** | 300 DPI (resolución profesional) |
| **Campos procesados** | 60 campos automáticamente |
| **Tipos de gráficos** | 4 visualizaciones diferentes |
| **Compatibilidad** | Cualquier navegador moderno |

### **☁️ Despliegue en la Nube**
- **Listo para Streamlit Cloud** sin configuración adicional
- **Sin dependencias complejas** - funciona out-of-the-box
- **Gestión automática de memoria** y archivos temporales
- **Escalable** para múltiples usuarios simultáneos
- **Acceso desde cualquier dispositivo** con internet

### **🔤 Consistencia de Fuentes (NUEVO)**
- **Preservación de formato**: Mantiene el formato original de la plantilla durante el reemplazo de datos
- **Aplicación automática**: Aplica fuente Roboto Mono consistente a todo el documento para evitar mezcla de tipos
- **Preservación de tamaños**: Mantiene los tamaños de fuente originales de la plantilla (títulos, cuerpo, etc.)
- **Formato profesional**: Todos los documentos usan Roboto Mono con tamaños originales para apariencia uniforme
- **Fallback inteligente**: Si Roboto Mono no está disponible, usa fuente monoespaciada del sistema
- **Solución técnica**: Corrige el problema común de inconsistencia de fuentes en documentos generados automáticamente

### **🔒 Seguridad y Privacidad**
- **Sin almacenamiento permanente** de datos sensibles
- **Limpieza automática** después de cada uso
- **Procesamiento local temporal** - datos no persisten
- **Sin logs** de información confidencial

## 📞 **Soporte y Ayuda**

### **🆘 Primer Nivel de Soporte**
1. **Verifica tu conexión** a internet
2. **Refresca la página** y vuelve a intentar
3. **Copia toda la fila** desde Excel/Google Sheets
4. **Revisa el formato** de los datos pegados

### **🔧 Soporte Técnico**
Si persisten los problemas:
- Revisa que todos los **archivos estén presentes** en el repositorio
- Confirma que la **plantilla Word existe** y es accesible
- Verifica que los **datos tengan 60 columnas** completas
- Prueba con **diferentes navegadores** si hay problemas de descarga

### **💬 Contacto**
Para soporte avanzado o personalizaciones:
- Reporta problemas específicos con **capturas de pantalla**
- Incluye **ejemplos de los datos** que causan errores
- Especifica **navegador y sistema operativo** usado

---

## 📈 **Estado Actual del Sistema**

### **✅ Completamente Funcional - Versión 1.4**
- **Fecha de última actualización**: Octubre 2025
- **Interfaz Streamlit**: Totalmente operativa con categorización visual de datos
- **Corrección IA**: LangChain + OpenAI con jerarquía inteligente de configuración
- **API Key Hierarchy**: Streamlit Secrets → .env → variables de entorno → sin API key
- **Fuente consistente**: Roboto Mono aplicada automáticamente (con fallback inteligente)
- **4 gráficos automáticos**: Presencia de plagas, matriz de riesgo, donas de riesgos
- **60 campos procesados**: Extracción y edición completa de datos
- **Descarga directa**: Archivos Word generados instantáneamente

### **🔧 Notas Técnicas Importantes**
- **Advertencias de fuente**: "Font family 'Roboto Mono' not found" es normal en servidores cloud
- **Deprecaciones Streamlit**: Advertencias sobre `use_container_width` no afectan funcionalidad
- **Compatibilidad**: Funciona perfectamente en local y Streamlit Cloud
- **Rendimiento**: Generación de informes en 2-5 segundos típicamente

### **📁 Archivos del Proyecto**
```
informes-tecnicos/
├── app.py                    # 35.2 KB - Aplicación Streamlit principal
├── main.py                   # 5.9 KB - Versión línea de comandos  
├── config.py                 # 22.7 KB - Configuración y parseo de datos
├── utils.py                  # 45.1 KB - Funciones de generación, gráficos y corrección IA
├── requirements.txt          # 118 B - Dependencias Python (incluye LangChain)
├── .env                      # Variable - Archivo de configuración OpenAI API Key
├── .env.example              # 120 B - Ejemplo de configuración de variables
├── INFORME TÉCNICO FINAL.docx # 2.6 MB - Plantilla Word requerida
├── logo2021.png             # 433 KB - Logo corporativo
└── README.md                # 19.8 KB - Esta documentación
```

---

**🎯 El sistema está diseñado para ser intuitivo y confiable. La mayoría de problemas se resuelven verificando que los datos estén completos y el formato sea correcto.**
