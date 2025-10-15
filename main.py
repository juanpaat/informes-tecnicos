from utils import ReportGenerator
from config import ReportConfig
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Función principal de ejecución"""
    try:
        # ============================================================================
        # PASO 1: CARGAR CONFIGURACIÓN Y PROCESAR DATOS DE HOJA DE CÁLCULO
        # ============================================================================
        logger.info("Cargando configuración...")
        config = ReportConfig()
        
        # Validar configuración (verifica rutas de plantilla y salida)
        if not config.validate():
            logger.error("Error en validación de configuración. Revisar config.py")
            return
        
        # ============================================================================
        # PASO 2: INICIALIZAR GENERADOR DE INFORMES CON PLANTILLA
        # ============================================================================
        logger.info("Inicializando generador de informes...")
        generator = ReportGenerator(
            template_path=config.TEMPLATE_PATH,  # Debe existir: "INFORME TÉCNICO FINAL.docx"
            output_path=config.OUTPUT_PATH       # Se creará automáticamente
        )
        
        # ============================================================================
        # PASO 3: REEMPLAZAR TODOS LOS {{MARCADORES}} EN LA PLANTILLA CON DATOS REALES
        # ============================================================================
        logger.info("Reemplazando marcadores en plantilla...")
        data_dict = config.get_data_dict()
        
        # ============================================================================
        # PASO 3.5: GENERAR E INSERTAR VISUALIZACIONES PRIMERO (ANTES DEL TEXTO)
        # ============================================================================
        # IMPORTANTE: Procesar imágenes ANTES que texto para evitar disrupciones en estructura
        if config.ENABLE_VISUALIZATIONS:
            logger.info("Generando e insertando visualizaciones...")
            
            # Generar gráfico de presencia de plagas y reemplazar {{img_1}}
            if config.VIZ_1_ENABLED:
                pest_data = config.get_pest_presence_data()
                viz1 = generator.create_pest_presence_chart(pest_data)
                generator.add_image_to_placeholder(
                    placeholder=config.VIZ_1_PLACEHOLDER,  # "{{img_1}}"
                    image_path=viz1
                )
            
            # Generar matriz de riesgo y reemplazar {{img_2}}
            if config.VIZ_2_ENABLED:
                riesgo_interno, riesgo_externo = config.get_risk_scores()
                viz2 = generator.create_risk_matrix(riesgo_interno, riesgo_externo)
                generator.add_image_to_placeholder(
                    placeholder=config.VIZ_2_PLACEHOLDER,  # "{{img_2}}"
                    image_path=viz2
                )
            
            # Generar gráfico de dona de riesgos externos y reemplazar {{riesgos_externos_plot}}
            if config.VIZ_3_ENABLED:
                external_risk_data = config.get_external_risk_data()
                viz3 = generator.create_external_risk_donut(*external_risk_data)
                generator.add_image_to_placeholder(
                    placeholder=config.VIZ_3_PLACEHOLDER,  # "{{riesgos_externos_plot}}"
                    image_path=viz3,
                    width=12.0,
                    height=7.60
                )
            
            # Generar gráfico de dona de riesgos internos y reemplazar {{riesgos_internos_plot}}
            if config.VIZ_4_ENABLED:
                internal_risk_data = config.get_internal_risk_data()
                viz4 = generator.create_internal_risk_donut(*internal_risk_data)
                generator.add_image_to_placeholder(
                    placeholder=config.VIZ_4_PLACEHOLDER,  # "{{riesgos_internos_plot}}"
                    image_path=viz4,
                    width=12.0,
                    height=7.60
                )
        
        # ============================================================================
        # PASO 4: REEMPLAZAR MARCADORES DE TEXTO (DESPUÉS DE IMÁGENES PARA EVITAR PROBLEMAS)
        # ============================================================================
        logger.info("Reemplazando marcadores de texto...")
        
        # Esta función busca en todo el documento patrones {{key}} y los reemplaza
        generator.replace_placeholders(data_dict)
        
        # ============================================================================
        # PASO 4.5: APLICAR FUENTE CONSISTENTE PARA EVITAR PROBLEMAS DE FORMATO
        # ============================================================================
        logger.info("Aplicando formato de fuente consistente...")
        generator.apply_consistent_font(font_name="Roboto Mono")
        
        # ============================================================================
        # PASO 5: GUARDAR DOCUMENTO FINAL
        # ============================================================================
        logger.info(f"Guardando informe en {config.OUTPUT_PATH}...")
        generator.save()
        
        logger.info("✅ Generación de informe completada exitosamente!")
        print(f"✅ Informe guardado en: {config.OUTPUT_PATH}")
        
    except FileNotFoundError as e:
        logger.error(f"Archivo no encontrado: {e}")
        print(f"✗ Error: {e}")
    except Exception as e:
        logger.error(f"Ocurrió un error: {e}", exc_info=True)
        print(f"✗ Error: {e}")


if __name__ == "__main__":
    main()