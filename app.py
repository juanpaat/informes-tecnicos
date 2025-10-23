"""
Aplicación Streamlit para Generación de Informes Técnicos
Sistema automatizado para crear informes de control de plagas desde datos de hoja de cálculo
"""

import streamlit as st
import tempfile
import os
from typing import Dict, Any, List, Tuple
import logging

# Importar las clases y funciones existentes
from config import ReportConfig, PESOS_RIESGO_EXTERNO, PESOS_RIESGO_INTERNO
from utils import (
    ReportGenerator, parse_spreadsheet_line, map_rating_to_score, 
    calculate_risk_score, sentence_case_after_period, remove_double_spaces,
    validate_file_path
)

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Informes Técnicos",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado para diseño profesional
st.markdown("""
<style>
    /* Tema principal */
    .main-header {
        background: linear-gradient(90deg, #1f4e79 0%, #2980b9 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    /* Contenedores de sección */
    .section-container {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #2980b9;
        margin: 1rem 0;
    }
    
    /* Tarjetas de datos */
    .data-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
        border-left: 3px solid #3498db;
    }
    
    /* Etiquetas de variables */
    .variable-label {
        font-weight: bold;
        color: #2c3e50;
        font-size: 0.9rem;
        margin-bottom: 0.2rem;
    }
    
    /* Valores de variables */
    .variable-value {
        color: #34495e;
        font-size: 1rem;
        padding: 0.2rem 0;
    }
    
    /* Botones personalizados */
    .stButton > button {
        background: linear-gradient(90deg, #2980b9 0%, #3498db 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    /* Área de texto mejorada */
    .stTextArea textarea {
        border-radius: 8px;
        border: 2px solid #bdc3c7;
        font-family: 'Courier New', monospace;
    }
    
    /* Indicadores de estado */
    .success-indicator {
        color: #27ae60;
        font-weight: bold;
    }
    
    .warning-indicator {
        color: #f39c12;
        font-weight: bold;
    }
    
    .error-indicator {
        color: #e74c3c;
        font-weight: bold;
    }
    
    /* Espaciado mejorado */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Inicializar variables de sesión"""
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False
    if 'parsed_data' not in st.session_state:
        st.session_state.parsed_data = {}
    if 'config_instance' not in st.session_state:
        st.session_state.config_instance = None
    if 'report_generated' not in st.session_state:
        st.session_state.report_generated = False
    if 'report_count' not in st.session_state:
        st.session_state.report_count = 0

def validate_spreadsheet_data(data_text: str) -> Tuple[bool, str, List[str]]:
    """
    Validar datos de hoja de cálculo pegados
    
    Returns:
        Tuple[bool, str, List[str]]: (válido, mensaje_error, valores_parseados)
    """
    try:
        if not data_text.strip():
            return False, "Por favor ingrese los datos de la hoja de cálculo", []
        
        # Detectar delimitador automáticamente
        delimiter = '\t' if '\t' in data_text else ','
        values = parse_spreadsheet_line(data_text.strip(), delimiter)
        
        # Si solo faltan 1 campo (59 en lugar de 60), agregar valor por defecto al final
        if len(values) == 59:
            values.append("Sin información")
            return True, "Datos válidos (campo faltante completado automáticamente)", values
        
        if len(values) < 59:
            return False, f"Se esperan 60 campos, pero solo se encontraron {len(values)}. Verifique que copió toda la fila.", values
        
        return True, "Datos válidos", values
        
    except Exception as e:
        return False, f"Error al procesar los datos: {str(e)}", []

def create_config_from_data(data_text: str) -> ReportConfig:
    """
    Crear instancia de ReportConfig con datos personalizados
    """
    # Crear una clase temporal que hereda de ReportConfig
    class StreamlitReportConfig(ReportConfig):
        def __init__(self, spreadsheet_line: str):
            # Temporalmente reemplazar la línea de datos
            original_line = ReportConfig.SPREADSHEET_LINE
            ReportConfig.SPREADSHEET_LINE = spreadsheet_line
            
            try:
                super().__init__()
            finally:
                # Restaurar la línea original
                ReportConfig.SPREADSHEET_LINE = original_line
    
    return StreamlitReportConfig(data_text.strip())

def parse_data() -> None:
    """Función para parsear y validar los datos ingresados"""
    data_input = st.session_state.get('spreadsheet_input', '').strip()
    
    if not data_input:
        st.error("Por favor ingrese los datos de la hoja de cálculo")
        return
    
    with st.spinner("Validando y procesando datos..."):
        is_valid, error_msg, values = validate_spreadsheet_data(data_input)
        
        if not is_valid:
            st.error(f"❌ **Error de validación:** {error_msg}")
            st.session_state.data_loaded = False
            return
        
        try:
            # Crear instancia de configuración con los datos proporcionados
            config = create_config_from_data(data_input)
            
            # Validar configuración
            if not config.validate():
                st.error("❌ **Error:** No se encontró el archivo de plantilla 'INFORME TÉCNICO FINAL.docx'")
                st.session_state.data_loaded = False
                return
            
            # Guardar en session state
            st.session_state.config_instance = config
            parsed_data = config.get_data_dict()
            
            # Agregar los datos de riesgo que no están en get_data_dict()
            risk_data = {
                # Riesgos externos (valores originales de la hoja de cálculo)
                "genera_vecindario": getattr(config, 'genera_vecindario_text', '🟢 Nada'),
                "limpieza_vecindario": getattr(config, 'limpieza_vecindario_text', '🟢 Nada'),
                "manejo_basuras_vecindario": getattr(config, 'manejo_basuras_vecindario_text', '🟢 Nada'),
                "infraes_vecindario": getattr(config, 'infraes_vecindario_text', '🟢 Nada'),
                "ilumina_vecindario": getattr(config, 'ilumina_vecindario_text', '🟢 Nada'),
                "animal_cercanias": getattr(config, 'animal_cercanias_text', '🟢 Nada'),
                "construccion_cerca": getattr(config, 'construccion_cerca_text', '🟢 Nada'),
                "zonas_verdes_cerca": getattr(config, 'zonas_verdes_cerca_text', '🟢 Nada'),
                "cuerpos_de_agua_cerca": getattr(config, 'cuerpos_de_agua_cerca_text', '🟢 Nada'),
                "desagues_cerca": getattr(config, 'desagues_cerca_text', '🟢 Nada'),
                "locales_comida": getattr(config, 'locales_comida_text', '🟢 Nada'),
                # Riesgos internos (valores originales de la hoja de cálculo)
                "general_establecimiento": getattr(config, 'general_establecimiento_text', '🟢 Nada'),
                "limpieza_establecimiento": getattr(config, 'limpieza_establecimiento_text', '🟢 Nada'),
                "almacenamiento_establecimiento": getattr(config, 'almacenamiento_establecimiento_text', '🟢 Nada'),
                "iluminacion_establecimiento": getattr(config, 'iluminacion_establecimiento_text', '🟢 Nada'),
                "capacitacion_personal": getattr(config, 'capacitacion_personal_text', '🟢 Nada'),
                "sellamiento_puertas": getattr(config, 'sellamiento_puertas_text', '🟢 Nada'),
                "ventilacion_establecimiento": getattr(config, 'ventilacion_establecimiento_text', '🟢 Nada'),
                "grietas_instalaciones": getattr(config, 'grietas_instalaciones_text', '🟢 Nada'),
                "entrada_salida_material": getattr(config, 'entrada_salida_material_text', '🟢 Nada'),
                "acumulacion_objetos": getattr(config, 'acumulacion_objetos_text', '🟢 Nada'),
                "areas_manipulacion_comida": getattr(config, 'areas_manipulacion_comida_text', '🟢 Nada'),
                "presencia_animales": getattr(config, 'presencia_animales_text', '🟢 Nada')
            }
            
            # Combinar los datos
            parsed_data.update(risk_data)
            st.session_state.parsed_data = parsed_data
            st.session_state.data_loaded = True
            st.session_state.report_generated = False
            
            st.success("✅ **Datos cargados exitosamente!** Revise la información extraída a continuación.")
            
        except Exception as e:
            st.error(f"❌ **Error al procesar los datos:** {str(e)}")
            st.session_state.data_loaded = False

def display_variables() -> None:
    """Mostrar las variables extraídas en un formato organizado y editable"""
    if not st.session_state.data_loaded or not st.session_state.parsed_data:
        return
    
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.subheader("📋 Datos Extraídos")
    st.markdown("*Los datos se han extraído automáticamente. Puede editarlos si es necesario.*")
    
    # Organizar datos en categorías
    data_categories = {
        "🏢 Información del Cliente": {
            "cliente": "Cliente",
            "sede": "Sede",
            "direccion": "Dirección", 
            "municipio": "Municipio",
            "telefono": "Teléfono",
            "sector": "Sector"
        },
        "📅 Información del Servicio": {
            "fecha": "Fecha",
            "hora": "Hora Programada",
            "h_inicio": "Hora Inicio",
            "h_salida": "Hora Salida",
            "tipo_de_control": "Tipo de Control",
            "metodo_control": "Método de Control",
            "areas_controladas": "Áreas Controladas"
        },
        "👥 Personal": {
            "tecnico_encargado": "Técnico Encargado",
            "tecnicos": "Técnicos",
            "acompanante": "Acompañante",
            "cargo": "Cargo"
        },
        "🔬 Tratamiento y Observaciones": {
            "plaguicidas": "Plaguicidas Utilizados",
            "obs_generales": "Observaciones Generales",
            "reco_general": "Recomendaciones Generales",
            "periodicidad": "Periodicidad"
        }
    }
    
    # Crear columnas para layout responsive
    cols = st.columns(2)
    
    col_idx = 0
    for category, fields in data_categories.items():
        with cols[col_idx % 2]:
            st.markdown(f"### {category}")
            
            for field_key, field_label in fields.items():
                if field_key in st.session_state.parsed_data:
                    current_value = st.session_state.parsed_data[field_key]
                    
                    # Campo de texto editable
                    if field_key in ["obs_generales", "reco_general", "direccion"]:
                        # Campos de texto largo
                        new_value = st.text_area(
                            field_label,
                            value=str(current_value),
                            key=f"edit_{field_key}",
                            height=160
                        )
                    else:
                        # Campos de texto corto
                        new_value = st.text_input(
                            field_label,
                            value=str(current_value),
                            key=f"edit_{field_key}"
                        )
                    
                    # Actualizar si cambió
                    st.session_state.parsed_data[field_key] = new_value
        
        col_idx += 1
    
    # Mostrar datos de presencia de plagas en sección separada
    st.markdown("### 🐛 Presencia de Plagas")
    
    pest_fields = {
        "cucarachas": "Cucarachas",
        "hormigas": "Hormigas", 
        "moscas": "Moscas",
        "mosquitos": "Mosquitos",
        "zancudo": "Zancudos",
        "raton_casero": "Ratón Casero",
        "rata_noruega": "Rata Noruega",
        "raton_tejado": "Ratón de Tejado",
        "larvas_mosquitos": "Larvas de Mosquitos"
    }
    
    pest_options = ["🟢 Sin evidencia", "🟡 Poca evidencia", "🟠 Considerable evidencia", "🔴 Mucha evidencia"]
    
    pest_cols = st.columns(3)
    for idx, (field_key, field_label) in enumerate(pest_fields.items()):
        with pest_cols[idx % 3]:
            if field_key in st.session_state.parsed_data:
                current_value = st.session_state.parsed_data[field_key]
                new_value = st.selectbox(
                    field_label,
                    options=pest_options,
                    index=pest_options.index(current_value) if current_value in pest_options else 0,
                    key=f"edit_{field_key}"
                )
                st.session_state.parsed_data[field_key] = new_value

    # Mostrar datos de riesgos externos
    st.markdown("### 🌍 Riesgos Externos")
    
    # Riesgos cualitativos externos
    st.markdown("#####  Riesgos Cualitativos")
    external_qualitative_fields = {
        "genera_vecindario": "Condiciones generales del vecindario",
        "limpieza_vecindario": "Limpieza del vecindario",
        "manejo_basuras_vecindario": "Manejo de basuras del vecindario",
        "infraes_vecindario": "Infraestructura del vecindario",
        "ilumina_vecindario": "Iluminación del vecindario"
    }
    
    qualitative_options = ["🔴 Mala", "🟠 Regular", "🟡 Buena", "🟢 Excelente"]
    
    ext_qual_cols = st.columns(3)
    for idx, (field_key, field_label) in enumerate(external_qualitative_fields.items()):
        with ext_qual_cols[idx % 3]:
            if field_key in st.session_state.parsed_data:
                current_value = st.session_state.parsed_data[field_key]
                new_value = st.selectbox(
                    field_label,
                    options=qualitative_options,
                    index=qualitative_options.index(current_value) if current_value in qualitative_options else 2,
                    key=f"edit_{field_key}"
                )
                st.session_state.parsed_data[field_key] = new_value
    
    # Riesgos cuantitativos externos
    st.markdown("##### Riesgos Cuantitativos")
    external_quantitative_fields = {
        "animal_cercanias": "Presencia de animales en cercanías",
        "construccion_cerca": "Construcciones en la cercanía",
        "zonas_verdes_cerca": "Zonas verdes aledañas",
        "cuerpos_de_agua_cerca": "Cuerpos de agua aledaños",
        "desagues_cerca": "Presencia de desagües en cercanía",
        "locales_comida": "Locales de comida y bebida cercanos"
    }
    
    quantitative_options = ["🟢 Nada", "🟡 Pocas", "🟠 Bastantes", "🔴 Muchas"]
    
    ext_quant_cols = st.columns(3)
    for idx, (field_key, field_label) in enumerate(external_quantitative_fields.items()):
        with ext_quant_cols[idx % 3]:
            if field_key in st.session_state.parsed_data:
                current_value = st.session_state.parsed_data[field_key]
                new_value = st.selectbox(
                    field_label,
                    options=quantitative_options,
                    index=quantitative_options.index(current_value) if current_value in quantitative_options else 0,
                    key=f"edit_{field_key}"
                )
                st.session_state.parsed_data[field_key] = new_value

    # Mostrar datos de riesgos internos
    st.markdown("### 🏢 Riesgos Internos")
    
    # Riesgos cualitativos internos
    st.markdown("#####  Riesgos Cualitativos")
    internal_qualitative_fields = {
        "general_establecimiento": "Condiciones generales del establecimiento",
        "limpieza_establecimiento": "Limpieza del establecimiento",
        "almacenamiento_establecimiento": "Almacenamiento",
        "iluminacion_establecimiento": "Iluminación",
        "capacitacion_personal": "Capacitación del personal",
        "sellamiento_puertas": "Sellamiento de puertas",
        "ventilacion_establecimiento": "Ventilación del establecimiento"
    }
    
    qualitative_options = ["🔴 Mala", "🟠 Regular", "🟡 Buena", "🟢 Excelente"]
    
    int_qual_cols = st.columns(3)
    for idx, (field_key, field_label) in enumerate(internal_qualitative_fields.items()):
        with int_qual_cols[idx % 3]:
            if field_key in st.session_state.parsed_data:
                current_value = st.session_state.parsed_data[field_key]
                new_value = st.selectbox(
                    field_label,
                    options=qualitative_options,
                    index=qualitative_options.index(current_value) if current_value in qualitative_options else 2,
                    key=f"edit_{field_key}"
                )
                st.session_state.parsed_data[field_key] = new_value
    
    # Riesgos cuantitativos internos
    st.markdown("##### Riesgos Cuantitativos")
    internal_quantitative_fields = {
        "grietas_instalaciones": "Grietas o agujeros en las instalaciones",
        "entrada_salida_material": "Entrada y salida de material",
        "acumulacion_objetos": "Acumulación de objetos",
        "areas_manipulacion_comida": "Áreas de manipulación de comidas",
        "presencia_animales": "Presencia de animales/mascotas"
    }
    
    quantitative_options = ["🟢 Nada", "🟡 Pocas", "🟠 Bastantes", "🔴 Muchas"]
    
    int_quant_cols = st.columns(3)
    for idx, (field_key, field_label) in enumerate(internal_quantitative_fields.items()):
        with int_quant_cols[idx % 3]:
            if field_key in st.session_state.parsed_data:
                current_value = st.session_state.parsed_data[field_key]
                new_value = st.selectbox(
                    field_label,
                    options=quantitative_options,
                    index=quantitative_options.index(current_value) if current_value in quantitative_options else 0,
                    key=f"edit_{field_key}"
                )
                st.session_state.parsed_data[field_key] = new_value
    
    # Datos adicionales en un expander
    with st.expander("🔍 Ver Datos Técnicos Adicionales"):
        additional_fields = {
            "marca_temporal": "Marca Temporal",
            "identificador": "Identificador",
            "fidelidad": "Tipo de Cliente",
            "antecedentes": "Antecedentes"
        }
        
        for field_key, field_label in additional_fields.items():
            if field_key in st.session_state.parsed_data:
                current_value = st.session_state.parsed_data[field_key]
                if field_key == "antecedentes":
                    new_value = st.text_area(
                        field_label,
                        value=str(current_value),
                        key=f"edit_{field_key}",
                        height=200
                    )
                else:
                    new_value = st.text_input(
                        field_label,
                        value=str(current_value),
                        key=f"edit_{field_key}"
                    )
                st.session_state.parsed_data[field_key] = new_value
    
    st.markdown('</div>', unsafe_allow_html=True)

def generate_report() -> None:
    """Generar el informe técnico"""
    if not st.session_state.data_loaded or not st.session_state.config_instance:
        st.error("❌ Primero debe cargar y validar los datos")
        return
    
    try:
        with st.spinner("🔄 Generando informe técnico..."):
            # Obtener la configuración actual
            config = st.session_state.config_instance
            
            # Actualizar la configuración con los datos editados
            for key, value in st.session_state.parsed_data.items():
                # Manejar mapeo especial de nombres
                config_key = key.replace('tecnico_encargado', 'tec_encargado')
                
                # Para los campos de riesgo, actualizar tanto texto como valores numéricos
                risk_fields = [
                    'genera_vecindario', 'limpieza_vecindario', 'manejo_basuras_vecindario',
                    'infraes_vecindario', 'ilumina_vecindario', 'animal_cercanias',
                    'construccion_cerca', 'zonas_verdes_cerca', 'cuerpos_de_agua_cerca',
                    'desagues_cerca', 'locales_comida', 'general_establecimiento',
                    'limpieza_establecimiento', 'almacenamiento_establecimiento',
                    'iluminacion_establecimiento', 'capacitacion_personal',
                    'sellamiento_puertas', 'ventilacion_establecimiento',
                    'grietas_instalaciones', 'entrada_salida_material',
                    'acumulacion_objetos', 'areas_manipulacion_comida',
                    'presencia_animales'
                ]
                
                if config_key in risk_fields:
                    # Actualizar el valor de texto
                    text_key = f"{config_key}_text"
                    if hasattr(config, text_key):
                        setattr(config, text_key, value)
                    
                    # Actualizar el valor numérico
                    from utils import map_rating_to_score
                    if hasattr(config, config_key):
                        setattr(config, config_key, map_rating_to_score(value))
                
                elif hasattr(config, config_key):
                    setattr(config, config_key, value)
            
            # Recalcular los riesgos totales después de las actualizaciones
            from config import PESOS_RIESGO_EXTERNO, PESOS_RIESGO_INTERNO
            from utils import calculate_risk_score
            
            # Recalcular riesgos individuales
            external_risks = [
                'genera_vecindario', 'limpieza_vecindario', 'manejo_basuras_vecindario',
                'infraes_vecindario', 'ilumina_vecindario', 'animal_cercanias',
                'construccion_cerca', 'zonas_verdes_cerca', 'cuerpos_de_agua_cerca',
                'desagues_cerca', 'locales_comida'
            ]
            
            internal_risks = [
                'general_establecimiento', 'limpieza_establecimiento', 'almacenamiento_establecimiento',
                'iluminacion_establecimiento', 'capacitacion_personal', 'sellamiento_puertas',
                'ventilacion_establecimiento', 'grietas_instalaciones', 'entrada_salida_material',
                'acumulacion_objetos', 'areas_manipulacion_comida', 'presencia_animales'
            ]
            
            # Recalcular riesgos externos individuales
            for risk_field in external_risks:
                text_value = getattr(config, f"{risk_field}_text", "🟢 Nada")
                risk_score = calculate_risk_score(text_value, PESOS_RIESGO_EXTERNO[risk_field])
                setattr(config, f"risk_{risk_field}", risk_score)
            
            # Recalcular riesgos internos individuales  
            for risk_field in internal_risks:
                text_value = getattr(config, f"{risk_field}_text", "🟢 Nada")
                risk_score = calculate_risk_score(text_value, PESOS_RIESGO_INTERNO[risk_field])
                setattr(config, f"risk_{risk_field}", risk_score)
            
            # Recalcular riesgos totales
            config.riesgo_total_externo = sum(getattr(config, f"risk_{field}", 0) for field in external_risks)
            config.riesgo_total_interno = sum(getattr(config, f"risk_{field}", 0) for field in internal_risks)
            
            # Crear el generador de reportes con ruta temporal
            with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_file:
                temp_output_path = tmp_file.name
            
            generator = ReportGenerator(
                template_path=config.TEMPLATE_PATH,
                output_path=temp_output_path
            )
            
            # Progreso detallado
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Paso 1: Generar visualizaciones
            status_text.text("📊 Generando gráficos...")
            progress_bar.progress(20)
            
            if config.ENABLE_VISUALIZATIONS:
                # Gráfico de presencia de plagas
                if config.VIZ_1_ENABLED:
                    pest_data = config.get_pest_presence_data()
                    viz1 = generator.create_pest_presence_chart(pest_data)
                    generator.add_image_to_placeholder(
                        placeholder=config.VIZ_1_PLACEHOLDER,
                        image_path=viz1
                    )
                
                progress_bar.progress(40)
                
                # Matriz de riesgo
                if config.VIZ_2_ENABLED:
                    riesgo_interno, riesgo_externo = config.get_risk_scores()
                    viz2 = generator.create_risk_matrix(riesgo_interno, riesgo_externo)
                    generator.add_image_to_placeholder(
                        placeholder=config.VIZ_2_PLACEHOLDER,
                        image_path=viz2
                    )
                
                progress_bar.progress(60)
                
                # Gráfico de dona de riesgos externos
                if config.VIZ_3_ENABLED:
                    external_risk_data = config.get_external_risk_data()
                    viz3 = generator.create_external_risk_donut(*external_risk_data)
                    generator.add_image_to_placeholder(
                        placeholder=config.VIZ_3_PLACEHOLDER,
                        image_path=viz3,
                        width=12.0,
                        height=7.60
                    )
                
                progress_bar.progress(80)
                
                # Gráfico de dona de riesgos internos
                if config.VIZ_4_ENABLED:
                    internal_risk_data = config.get_internal_risk_data()
                    viz4 = generator.create_internal_risk_donut(*internal_risk_data)
                    generator.add_image_to_placeholder(
                        placeholder=config.VIZ_4_PLACEHOLDER,
                        image_path=viz4,
                        width=12.0,
                        height=7.60
                    )
            
            # Paso 2: Reemplazar marcadores de texto
            status_text.text("📝 Insertando datos en plantilla...")
            progress_bar.progress(90)
            
            generator.replace_placeholders(st.session_state.parsed_data)
            
            # Paso 2.5: Aplicar fuente consistente para evitar problemas de formato
            status_text.text("🔤 Aplicando formato consistente...")
            generator.apply_consistent_font(font_name="Roboto Mono")
            progress_bar.progress(95)
            
            # Paso 3: Guardar documento
            status_text.text("💾 Guardando documento...")
            generator.save()
            progress_bar.progress(100)
            
            # Completado
            status_text.text("✅ ¡Informe generado exitosamente!")
            
            st.session_state.report_generated = True
            st.session_state.report_count += 1
            
            st.success(f"✅ **¡Informe generado exitosamente!**")
            
            # Leer el archivo generado y ofrecer descarga
            try:
                with open(temp_output_path, "rb") as file:
                    file_data = file.read()
                
                # Crear nombre de archivo basado en cliente y fecha
                clean_cliente = config.cliente.replace("/", "-").replace("\\", "-").replace(":", "-").replace("*", "").replace("?", "").replace('"', "").replace("<", "").replace(">", "").replace("|", "")
                clean_fecha = config.fecha.replace("/", "-").replace("\\", "-")
                download_filename = f"INFORME TÉCNICO {clean_cliente} - {clean_fecha}.docx"
                
                # Botón de descarga
                st.download_button(
                    label="📄 Descargar Informe Técnico",
                    data=file_data,
                    file_name=download_filename,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    key=f"download_report_{st.session_state.get('report_count', 0)}",
                    type="primary"
                )
                
                # Limpiar archivo temporal inmediatamente
                try:
                    os.unlink(temp_output_path)
                except Exception:
                    pass
                    
            except Exception as e:
                st.error(f"❌ Error al preparar la descarga: {str(e)}")
                # Limpiar archivo temporal en caso de error
                try:
                    os.unlink(temp_output_path)
                except Exception:
                    pass
            
    except Exception as e:
        st.error(f"❌ **Error al generar el informe:** {str(e)}")
        st.session_state.report_generated = False

def main():
    """Función principal de la aplicación Streamlit"""
    # Inicializar estado de sesión
    initialize_session_state()
    
    # Logo en la parte superior - centrado y alta resolución
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        # Solo mostrar el logo si existe el archivo
        if os.path.exists("logo2021.png"):
            try:
                st.image("logo2021.png", use_container_width=True)
            except Exception:
                pass  # Si hay error cargando la imagen, simplemente no la mostramos
    
    # Espaciado después del logo
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Encabezado principal
    st.markdown("""
    <div class="main-header">
        <h1>Informe Técnico Final</h1>
        <p style="font-size: 1.2rem; margin-top: 1rem;">
            Generación automatizada de informes de control de plagas
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Instrucciones
    st.info("""
    **🚀 Instrucciones:**
    1. **Copie** una fila completa de su hoja de cálculo (Excel/Google Sheets)
    2. **Pegue** los datos en el área de texto a continuación  
    3. **Revise** los datos extraídos y edite si es necesario
    4. **Genere** el informe técnico en formato Word
    """)
    
    # === SECCIÓN 1: ENTRADA DE DATOS ===
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.header("1️⃣ Entrada de Datos")
    
    # Área de texto para pegar datos
    st.markdown("**Pegue aquí los datos de su hoja de cálculo:**")
    data_input = st.text_area(
        "Datos de la hoja de cálculo",
        placeholder="Pegue aquí la fila completa de su hoja de cálculo (Excel/Google Sheets)...\n\nEjemplo: 11/10/2025 19:28:13\t3692\tU.R. CAMINO VERDE DEL BOSQUE\t...",
        height=150,
        key="spreadsheet_input",
        label_visibility="hidden"
    )
    
    # Botón de carga de datos
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📥 Cargar Datos", type="primary", use_container_width=True):
            parse_data()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # === SECCIÓN 2: REVISIÓN DE DATOS ===
    if st.session_state.data_loaded:
        display_variables()
        
        # === SECCIÓN 3: GENERACIÓN DE INFORME ===
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.header("3️⃣ Generación de Informe")
        
        st.markdown("**Por favor revise los datos anteriores antes de continuar.**")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📄 Generar Informe Técnico", type="primary", use_container_width=True):
                generate_report()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    # Pie de página
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #7f8c8d; padding: 1rem;">
        <p>Sistema de Informes Técnicos - Control de Plagas</p>
        <p><small>Versión 1.1 | Desarrollado para automatizar la generación de informes con formato consistente</small></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()