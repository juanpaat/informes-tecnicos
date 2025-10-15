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
1. **Pegar datos** de Excel/Google Sheets directamente
2. **Editar campos** en tiempo real con interfaz visual
3. **Generar gráficos** automáticamente (4 tipos de visualizaciones)
4. **Descargar informe** en formato Word profesional

### **📊 Visualizaciones Automáticas**
- **Gráfico de barras**: Presencia de plagas por tipo
- **Matriz de riesgo**: Evaluación visual de riesgos internos vs externos  
- **Gráfico de dona**: Distribución de riesgos externos
- **Gráfico de dona**: Distribución de riesgos internos

### **🌟 Ventajas de la Interfaz Web**

| Característica | Descripción |
|---|---|
| **📱 Accesible** | Funciona en cualquier navegador, celular o computadora |
| **� Sin instalación** | No requiere software adicional |
| **✏️ Edición visual** | Modifica cualquier campo antes de generar |
| **📊 Vista previa** | Ve todos los datos organizados por categorías |
| **⚡ Rápido** | Genera informes en segundos |
| **☁️ En la nube** | Acceso desde cualquier lugar |

## 🎯 **Cómo Usar el Sistema**

### **Paso 1: Acceder a la Aplicación**
- **En línea**: Accede directamente desde el navegador (enlace proporcionado)
- **Local**: Ejecuta `streamlit run app.py` en tu computadora

### **Paso 2: Cargar Datos**
1. **Copia** una fila completa de tu hoja de cálculo (Excel/Google Sheets)
2. **Pega** los datos en el área de texto de la aplicación
3. **Haz clic** en "� Cargar Datos"

### **Paso 3: Revisar y Editar**
- La aplicación muestra automáticamente todos los campos organizados
- **Edita** cualquier campo que necesites modificar
- **Revisa** la información de plagas y riesgos

### **Paso 4: Generar Informe**
1. **Haz clic** en "📄 Generar Informe Técnico"
2. **Espera** mientras se crean los gráficos (segundos)
3. **Descarga** automáticamente el archivo Word

## �📁 Estructura del proyecto

```
informes-tecnicos/
├── app.py                           # 🌐 Aplicación web Streamlit (PRINCIPAL)
├── main.py                          # 💻 Versión línea de comandos (alternativa)
├── config.py                        # ⚙️ Configuración y cálculos automáticos
├── utils.py                         # 🔧 Funciones de generación y gráficos
├── requirements.txt                 # 📦 Dependencias de Python
├── INFORME TÉCNICO FINAL.docx       # 📋 Plantilla Word (REQUERIDA)
├── logo2021.png                     # 🎨 Logo de la empresa
└── README.md                        # 📖 Esta guía
```

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

**🎯 El sistema está diseñado para ser intuitivo y confiable. La mayoría de problemas se resuelven verificando que los datos estén completos y el formato sea correcto.**
