"""
Configuración para generación de informes
Contiene configuración de archivos, parseo de datos y cálculos de riesgo
"""

import os
from typing import Dict, Any
from utils import parse_spreadsheet_line, validate_file_path, map_rating_to_score, calculate_risk_score, sentence_case_after_period, remove_double_spaces

# Definir pesos para cada métrica
PESOS_RIESGO_EXTERNO = {
    'genera_vecindario': 0.05,
    'limpieza_vecindario': 0.13,
    'manejo_basuras_vecindario': 0.13,
    'infraes_vecindario': 0.10,
    'ilumina_vecindario': 0.05,
    'animal_cercanias': 0.10,
    'construccion_cerca': 0.05,
    'zonas_verdes_cerca': 0.10,
    'cuerpos_de_agua_cerca': 0.10,
    'desagues_cerca': 0.05,
    'locales_comida': 0.14
}

PESOS_RIESGO_INTERNO = {
    'general_establecimiento': 0.05 ,
    'limpieza_establecimiento': 0.17 , 
    'almacenamiento_establecimiento': 0.07,
    'iluminacion_establecimiento': 0.05,
    'capacitacion_personal': 0.05,
    'sellamiento_puertas': 0.1,
    'ventilacion_establecimiento': 0.08,
    'grietas_instalaciones': 0.07,
    'entrada_salida_material': 0.1,
    'acumulacion_objetos': 0.08,
    'areas_manipulacion_comida': 0.11,
    'presencia_animales': 0.07
}

# Plantilla de prompt para reescritura de observaciones generales con contexto completo
LANGCHAIN_PROMPT_TEMPLATE = """Eres un redactor técnico experto en informes de control integrado de plagas de salud pública en Colombia.

Tu tarea es revisar y mejorar el texto de observaciones generales de un informe de visita de control de plagas, integrando de manera natural y coherente la información disponible sobre condiciones higiénicas y locativas.

DATOS DEL SERVICIO:
- Sector: {sector}
- Tipo de control: {tipo_control}
- Método de control: {metodo_control}

PLAGAS ENCONTRADAS EN LA VISITA:
{pests_found}

CONDICIONES HIGIÉNICAS Y LOCATIVAS EXTERNAS (entorno y vecindario):
{external_conditions}

CONDICIONES HIGIÉNICAS Y LOCATIVAS INTERNAS (establecimiento):
{internal_conditions}

TEXTO ORIGINAL DE OBSERVACIONES:
{text}

INSTRUCCIONES:
1. Mantén la información técnica y el significado del texto original.
2. Mejora la ortografía, gramática, puntuación, coherencia y cohesión del texto.
3. Integra de forma natural en la narrativa los factores de riesgo relevantes derivados de las condiciones higiénicas y locativas. Incluye solo los que sean pertinentes según el nivel de riesgo (calificaciones como "Regular", "Bastantes" o "Muchas" indican riesgo significativo). No menciones condiciones en buen estado si no aportan al análisis.
4. Asegúrate de que el texto sea coherente con los datos:
   - Si se mencionan condiciones que contradicen los datos (ej. "buenas condiciones" pero hay riesgos marcados), corrígelo.
   - Si hay factores de riesgo externos significativos (ej. zonas verdes cercanas, cuerpos de agua, locales de comida, animales en cercanías) no mencionados, inclúyelos de forma breve y apropiada para el sector.
   - Si hay factores de riesgo internos significativos (ej. grietas, acumulación de objetos, sellamiento deficiente) no mencionados, inclúyelos en la narrativa.
5. Las plagas mencionadas deben ser coherentes con los datos de "PLAGAS ENCONTRADAS EN LA VISITA".
6. REGLA OBLIGATORIA: Siempre escribe "roedores (plaga menor)" — nunca "roedores plaga menor", "Roedores plaga menor", "roedores considerados plaga menor" ni ninguna otra variación. Elimina la palabra "considerados" en cualquier contexto similar.
7. REGLA OBLIGATORIA: Nunca uses la palabra "reinfestación". Este informe corresponde únicamente a la visita actual, no a un seguimiento en el tiempo. Usa siempre "infestación" si aplica.
8. Mantén un tono técnico, formal y propio de informes de salud pública en Colombia.
9. Usa conectores adecuados y asegúrate de que el texto fluya como un párrafo cohesivo. No uses listas ni viñetas.
10. No inventes información que no esté respaldada por los datos proporcionados.
11. Si el texto ya está bien redactado e integrado con los datos, realiza solo las correcciones mínimas necesarias.

Devuelve únicamente el texto mejorado, sin explicaciones, comentarios ni encabezados adicionales.

Texto mejorado:
"""

# Plantilla de prompt para generación de recomendaciones
RECOMMENDATIONS_PROMPT_TEMPLATE = """Eres un redactor técnico especializado en informes de control integrado de plagas de salud pública en Colombia.

Con base en los datos de la siguiente visita, redacta recomendaciones para el cliente.

DATOS DEL SERVICIO:
- Sector: {sector}
- Tipo de control: {tipo_control}
- Método de control: {metodo_control}
- Plaguicidas utilizados: {plaguicidas}

PLAGAS ENCONTRADAS EN LA VISITA:
{pests_found}

CONDICIONES HIGIÉNICAS Y LOCATIVAS EXTERNAS:
{external_conditions}

CONDICIONES HIGIÉNICAS Y LOCATIVAS INTERNAS:
{internal_conditions}

OBSERVACIONES GENERALES DE LA VISITA:
{obs_generales}

RECOMENDACIONES ORIGINALES DEL TÉCNICO (como referencia):
- General: {reco_generales_original}
- Específica 1: {reco_especificas_1_original}
- Específica 2: {reco_especificas_2_original}
- Específica 3: {reco_especificas_3_original}

INSTRUCCIONES:
Genera exactamente 4 recomendaciones complementarias entre sí (sin redundancias) con las siguientes claves:
- "reco_generales": Orientada al cuidado del tratamiento aplicado por el técnico (ej. conservar los plaguicidas aplicados, evitar mojar superficies tratadas, mantener la continuidad del programa de control). No incluyas aspectos de higiene ni locativos que se cubran en las específicas.
- "reco_especificas_1": Sugerencia general sobre un aspecto higiénico o locativo relevante según los datos (ej. sellamiento, accesos, residuos).
- "reco_especificas_2": Sugerencia sobre un aspecto diferente a los anteriores (ej. almacenamiento, orden, manejo de alimentos).
- "reco_especificas_3": Sugerencia sobre un tercer aspecto diferente (ej. condiciones locativas, ventilación, drenajes, iluminación).

CRITERIOS DE REDACCIÓN — MUY IMPORTANTES:
- Tono sugerente y amable: usa frases como "se sugiere", "se recomienda", "es conveniente", "se aconseja mantener". Nunca uses imperativos ni lenguaje obligatorio.
- Sin urgencia ni plazos: no incluyas palabras como "inmediatamente", "en X días", "urgente" ni ningún tipo de plazo.
- Sin detalles excesivos: menciona el área o aspecto general si está disponible en los datos, pero no especifiques materiales, métodos exactos ni procedimientos técnicos detallados. El objetivo es orientar, no instruir.
- Sin acciones propias del servicio: no recomiendes actividades de monitoreo, aplicación de productos, instalación de estaciones ni ninguna tarea que sea parte del servicio de control de plagas ya prestado. Esto podría sugerir que el trabajo no fue realizado.
- Cada recomendación cubre un ángulo distinto y ninguna repite ni parafrasea lo dicho en otra.
- Basa las recomendaciones en los datos proporcionados. Si los datos son genéricos, genera sugerencias apropiadas para el sector.
- Mantén coherencia con las observaciones generales.
- NO uses "roedores plaga menor" ni "roedores considerados plaga menor"; usa "roedores (plaga menor)" si aplica.
- REGLA OBLIGATORIA: Nunca uses la palabra "reinfestación". Este informe corresponde únicamente a la visita actual, no a un seguimiento en el tiempo. Usa siempre "infestación" si aplica.
- Tono técnico, formal y profesional, pero siempre cortés y no prescriptivo.

EJEMPLOS DE TONO CORRECTO:
- "Sellamiento de accesos: se sugiere revisar y mejorar el sellado en áreas donde puedan existir puntos de ingreso, con el fin de reducir el acceso de plagas."
- "Manejo de residuos: se recomienda mantener las zonas de manejo de alimentos y residuos limpias y ordenadas, asegurando una correcta gestión para evitar que se conviertan en focos de atracción."

EJEMPLOS DE TONO INCORRECTO (evitar):
- "Sellar en los próximos 7 días las grietas con silicona sanitaria e instalar burletes en todas las puertas."
- "Retirar inmediatamente los residuos y usar contenedores con tapa hermética, vaciándolos diariamente."

Devuelve únicamente el JSON, sin texto adicional ni bloques de código markdown.

Formato de respuesta:
{{"reco_generales": "...", "reco_especificas_1": "...", "reco_especificas_2": "...", "reco_especificas_3": "..."}}
"""

class ReportConfig:
    """Clase de configuración para generación de informes"""
    
    # ============================================================================
    # PASO 1: PEGAR LÍNEA DE HOJA DE CÁLCULO AQUÍ (separada por tabulaciones o comas)
    # ============================================================================
    SPREADSHEET_LINE = "11/10/2025 19:28:13	3692	U.R. CAMINO VERDE DEL BOSQUE	No aplica	Cl.  39SUR   #   27 - 55	ENVIGADO	302 36 15 -          320 632 29 27	Residencial	Esporádico	11/10/2025	15:30:00	15:30:00	16:10:00	Yakelin Espinoza 	Propietario 	Adolfo Guerrero, Jose Garizado	Jose Garizado	(Control general) Rastreros, voladores y roedores plaga menor	Aspersión, Inyección	Apartamentos	🟢 Sin evidencia	🟢 Sin evidencia	🟢 Sin evidencia	🟢 Sin evidencia	🟢 Sin evidencia	🟢 Sin evidencia	🟢 Sin evidencia	🟢 Sin evidencia	🟢 Sin evidencia	Black Jack gel, I con 10 me 	En el momento de realizar el control integrado de plagas no se manifestó ninguna clase de vectores ni roedores plaga menor esto debido a la efectividad de controles anteriores a la buena conservación de plaguicidas aplicadas y a las buenas condiciones higiénicas por otro lado se pudo observar fisuras que son factor claves para el albergue de plagas además de que el ingreso de plagas puede ser a través del transporte indirecto de productos o enseres	Conservar plaguicidas aplicados. No mojar y no retirar, Mejorar condiciones higiénicas y locativas, Realizar controles periódicos	Sellar fisuras y hendiduras	Mantener una limpieza profunda y constante	Tener almacenamiento adecuado de alimentos	6 meses	🟡 Buena	🟡 Buena	🟡 Buena	🟡 Buena	🟡 Buena	🟡 Pocas	🟡 Pocas	🟡 Pocas	🟡 Pocas	🟡 Pocas	🟡 Pocas	🟡 Buena	🟡 Buena	🟡 Buena	🟡 Buena	🟡 Buena	🟡 Buena	🟡 Buena	🟡 Pocas	🟡 Pocas	🟡 Pocas	🟡 Pocas	🟡 Pocas	10/10/2025 vivienda ubicada en U.R. Camino verde del bosque que requiere control general apto 802 (incluye el cuarto útil); Favor hacer adecuada inspección buscando sitios de proliferación y alojamiento, hacer una adecuada aplicación del producto de acuerdo al grado de infestación y los sitios donde se va a aplicar, asesorar constantemente en campo teniendo en cuenta aquellos aspectos a mejorar en el lugar y realizar un adecuado informe técnico con las recomendaciones halladas. Se coordinó con la sra.  Jackeline Espinosa / residente / 320 632 29 27"
    #SPREADSHEET_LINE = "14/07/2025 19:19:56	5202	OBRA HOTELERA MEDELLIN	No aplica	Cl.   9ASUR   #   43A - 45	MEDELLIN	321 795 15 04	Servicios	Esporádico	14/07/2025	4:00:00	4:40:00	5:40:00	Andrey orozco 	Vijilante 	Brayan Fontalvo	Brayan Fontalvo	Visita de Monitoreo	Nebulización, Cebado	Áreas abiertas	🟢 Sin evidencia	🟢 Sin evidencia	🟢 Sin evidencia	🟢 Sin evidencia	🟠 Considerable evidencia	🟢 Sin evidencia	🟠 Considerable evidencia	🟢 Sin evidencia	🟢 Sin evidencia	Rutto, Skeeter 1% SG, Ratimor	Realizada la visita de monitoreo se hizo utilizando el mecanismos de Nebulización en area en general, una aplicación de cebos rodenticida en área perimetral, y una aplicación de larvicidas en empozamiento de agua. Ya que manifiestan roedores y zancudos. La zona externa cuenta con quebrada y es factor de riesgo para el ingreso de roedores, también en área interna se observa empozamiento de aguas debido a su actividad principal en obra, es importante hacer controles periódicos para poder así tener un ambiente tolerable y libre de plaga de importancia en salud pública 	Conservar plaguicidas aplicados. No mojar y no retirar, Mantener las buenas condiciones higiénicas y locativas, Mejorar condiciones higiénicas y locativas, Evitar saturación de objetos, Analizar si se requiere Eliminar objetos en desuso, Realizar controles periódicos	Hacer controles periódicos 	Conservar plaguicidas aplicados 	Evitar saturaron de objetos 	1 mes	🟡 Buena	🟡 Buena	🟡 Buena	🟡 Buena	🟡 Buena	🟡 Pocas	🟢 Nada	🟡 Pocas	🟡 Pocas	🟡 Pocas	🟢 Nada	🟠 Regular	🟠 Regular	🟠 Regular	🟡 Buena	🟡 Buena	🟠 Regular	🟡 Buena	🟢 Nada	🟠 Bastantes	🟠 Bastantes	🟡 Pocas	🟢 Nada	11/07/2025: CLIENTE ESPORADICO QUE SE LE RAELIZO CONTROL GENERAL CON ENFASIS EN ROEDORES PLAGA MENOR EN SECTOR CERCANO A QUEBRADA Y MOSQUITOS POR EMPOZAMIENTOS DE AGUA, REVISAR Y REFORZAR LA PASADA APLICACION Y BRINDAR COMPLETA ASESORIA SOBRE ADECUADO MANEJO DE RESIDUOS ORGANICOS"
    # Alternativa para CSV: "Juan Pérez,Ingeniería,85000,2024,Bogotá,5,Excelente,95"
    
    # Establecer delimitador basado en formato de hoja de cálculo
    DELIMITER = '\t'  # Usar '\t' para Excel/Google Sheets, ',' para CSV
    
    # ============================================================================
    # PASO 2: ANALIZAR LA LÍNEA EN VARIABLES
    # ============================================================================
    def __init__(self):
        """Inicializar configuración analizando la línea de hoja de cálculo"""
        # Analizar la línea de hoja de cálculo
        values = parse_spreadsheet_line(self.SPREADSHEET_LINE, self.DELIMITER)
        
        # Si solo hay 59 valores (falta el último campo), agregar valor por defecto
        if len(values) == 59:
            values.append("Sin información")
        
        # Asignar cada valor a una variable nombrada
        # PERSONALIZAR ESTOS BASÁNDOSE EN COLUMNAS DE HOJA DE CÁLCULO
        try:
            self.marca_temporal = values[0]
            self.identificador = values[1]
            self.cliente = values[2].title()
            self.sede = values[3].title()
            self.direccion = remove_double_spaces(values[4]).title()
            self.municipio = values[5].title()
            self.telefono = values[6]
            self.sector = values[7].title()
            self.fidelidad = values[8]
            self.fecha = values[9]
            self.hora_programada = values[10]
            self.hora_ingreso = values[11]
            self.hora_salida = values[12]
            self.acompanante = values[13].title()
            self.cargo = values[14].title()
            self.tecnicos = values[15]
            self.tec_encargado = values[16]
            self.tipo_control = values[17]
            self.metodo_control = values[18]
            self.areas = values[19]
            self.cucarachas = values[20]
            self.hormigas = values[21]
            self.moscas = values[22]
            self.mosquitos = values[23]
            self.zancudo = values[24]
            self.raton_casero = values[25]
            self.rata_noruega = values[26]
            self.raton_tejado = values[27]
            self.larvas_mosquitos = values[28]
            self.plaguicidas = values[29]
            self.observaciones = sentence_case_after_period(values[30])
            self.reco_generales = values[31]
            self.reco_especificas_1 = values[32]
            self.reco_especificas_2 = values[33]
            self.reco_especificas_3 = values[34]
            self.periodicidad = values[35]
            
            # Almacenar valores originales de texto para la interfaz
            self.genera_vecindario_text = values[36]
            self.limpieza_vecindario_text = values[37]
            self.manejo_basuras_vecindario_text = values[38]
            self.infraes_vecindario_text = values[39]
            self.ilumina_vecindario_text = values[40]
            self.animal_cercanias_text = values[41]
            self.construccion_cerca_text = values[42]
            self.zonas_verdes_cerca_text = values[43]
            self.cuerpos_de_agua_cerca_text = values[44]
            self.desagues_cerca_text = values[45]
            self.locales_comida_text = values[46]
            self.general_establecimiento_text = values[47]
            self.limpieza_establecimiento_text = values[48]
            self.almacenamiento_establecimiento_text = values[49]
            self.iluminacion_establecimiento_text = values[50]
            self.capacitacion_personal_text = values[51]
            self.sellamiento_puertas_text = values[52]
            self.ventilacion_establecimiento_text = values[53]
            self.grietas_instalaciones_text = values[54]
            self.entrada_salida_material_text = values[55]
            self.acumulacion_objetos_text = values[56]
            self.areas_manipulacion_comida_text = values[57]
            self.presencia_animales_text = values[58]
            
            # Convertir a valores numéricos para cálculos
            self.genera_vecindario = map_rating_to_score(values[36])
            self.limpieza_vecindario = map_rating_to_score(values[37])
            self.manejo_basuras_vecindario = map_rating_to_score(values[38])
            self.infraes_vecindario = map_rating_to_score(values[39])
            self.ilumina_vecindario = map_rating_to_score(values[40])
            self.animal_cercanias = map_rating_to_score(values[41])
            self.construccion_cerca = map_rating_to_score(values[42])
            self.zonas_verdes_cerca = map_rating_to_score(values[43])
            self.cuerpos_de_agua_cerca = map_rating_to_score(values[44])
            self.desagues_cerca = map_rating_to_score(values[45])
            self.locales_comida = map_rating_to_score(values[46])
            self.general_establecimiento = map_rating_to_score(values[47])
            self.limpieza_establecimiento = map_rating_to_score(values[48])
            self.almacenamiento_establecimiento = map_rating_to_score(values[49])
            self.iluminacion_establecimiento = map_rating_to_score(values[50])
            self.capacitacion_personal = map_rating_to_score(values[51])
            self.sellamiento_puertas = map_rating_to_score(values[52])
            self.ventilacion_establecimiento = map_rating_to_score(values[53])
            self.grietas_instalaciones = map_rating_to_score(values[54])
            self.entrada_salida_material = map_rating_to_score(values[55])
            self.acumulacion_objetos = map_rating_to_score(values[56])
            self.areas_manipulacion_comida = map_rating_to_score(values[57])
            self.presencia_animales = map_rating_to_score(values[58])
            self.antecedentes = sentence_case_after_period(values[59])
        
            # Calcular riesgos externos 
            self.risk_genera_vecindario = calculate_risk_score(values[36], PESOS_RIESGO_EXTERNO['genera_vecindario'])
            self.risk_limpieza_vecindario = calculate_risk_score(values[37], PESOS_RIESGO_EXTERNO['limpieza_vecindario'])
            self.risk_manejo_basuras_vecindario = calculate_risk_score(values[38], PESOS_RIESGO_EXTERNO['manejo_basuras_vecindario'])
            self.risk_infraes_vecindario = calculate_risk_score(values[39], PESOS_RIESGO_EXTERNO['infraes_vecindario'])
            self.risk_ilumina_vecindario = calculate_risk_score(values[40], PESOS_RIESGO_EXTERNO['ilumina_vecindario'])
            self.risk_animal_cercanias = calculate_risk_score(values[41], PESOS_RIESGO_EXTERNO['animal_cercanias'])
            self.risk_construccion_cerca = calculate_risk_score(values[42], PESOS_RIESGO_EXTERNO['construccion_cerca'])
            self.risk_zonas_verdes_cerca = calculate_risk_score(values[43], PESOS_RIESGO_EXTERNO['zonas_verdes_cerca'])
            self.risk_cuerpos_de_agua_cerca = calculate_risk_score(values[44], PESOS_RIESGO_EXTERNO['cuerpos_de_agua_cerca'])
            self.risk_desagues_cerca = calculate_risk_score(values[45], PESOS_RIESGO_EXTERNO['desagues_cerca'])
            self.risk_locales_comida = calculate_risk_score(values[46], PESOS_RIESGO_EXTERNO['locales_comida'])

            # Calcular riesgos internos
            self.risk_general_establecimiento = calculate_risk_score(values[47], PESOS_RIESGO_INTERNO['general_establecimiento'])
            self.risk_limpieza_establecimiento = calculate_risk_score(values[48], PESOS_RIESGO_INTERNO['limpieza_establecimiento'])
            self.risk_almacenamiento_establecimiento = calculate_risk_score(values[49], PESOS_RIESGO_INTERNO['almacenamiento_establecimiento'])
            self.risk_iluminacion_establecimiento = calculate_risk_score(values[50], PESOS_RIESGO_INTERNO['iluminacion_establecimiento'])
            self.risk_capacitacion_personal = calculate_risk_score(values[51], PESOS_RIESGO_INTERNO['capacitacion_personal'])
            self.risk_sellamiento_puertas = calculate_risk_score(values[52], PESOS_RIESGO_INTERNO['sellamiento_puertas'])
            self.risk_ventilacion_establecimiento = calculate_risk_score(values[53], PESOS_RIESGO_INTERNO['ventilacion_establecimiento'])
            self.risk_grietas_instalaciones = calculate_risk_score(values[54], PESOS_RIESGO_INTERNO['grietas_instalaciones'])
            self.risk_entrada_salida_material = calculate_risk_score(values[55], PESOS_RIESGO_INTERNO['entrada_salida_material'])
            self.risk_acumulacion_objetos = calculate_risk_score(values[56], PESOS_RIESGO_INTERNO['acumulacion_objetos'])
            self.risk_areas_manipulacion_comida = calculate_risk_score(values[57], PESOS_RIESGO_INTERNO['areas_manipulacion_comida'])
            self.risk_presencia_animales = calculate_risk_score(values[58], PESOS_RIESGO_INTERNO['presencia_animales'])


            # calcular riesgo total externo
            self.riesgo_total_externo = (
                self.risk_genera_vecindario +
                self.risk_limpieza_vecindario +
                self.risk_manejo_basuras_vecindario +
                self.risk_infraes_vecindario +
                self.risk_ilumina_vecindario +
                self.risk_animal_cercanias +
                self.risk_construccion_cerca +
                self.risk_zonas_verdes_cerca +
                self.risk_cuerpos_de_agua_cerca +
                self.risk_desagues_cerca +
                self.risk_locales_comida
            )
            # Calcular riesgo total interno
            self.riesgo_total_interno =(
                self.risk_general_establecimiento +
                self.risk_limpieza_establecimiento +
                self.risk_almacenamiento_establecimiento +
                self.risk_iluminacion_establecimiento +
                self.risk_capacitacion_personal +
                self.risk_sellamiento_puertas +
                self.risk_ventilacion_establecimiento +
                self.risk_grietas_instalaciones +
                self.risk_entrada_salida_material +
                self.risk_acumulacion_objetos +
                self.risk_areas_manipulacion_comida +
                self.risk_presencia_animales
            )
            
        
        except IndexError:
            raise ValueError(
                f"Expected 60 values in spreadsheet line, got {len(values)}. "
                f"Please check your SPREADSHEET_LINE in config.py"
            )
        
        # ========================================================================
        # PASO 3: RUTAS DE ARCHIVOS
        # ========================================================================
        self.TEMPLATE_PATH = "INFORME TÉCNICO FINAL.docx" 
        
        # Clean filename by replacing invalid characters
        clean_cliente = self.cliente.replace("/", "-").replace("\\", "-").replace(":", "-").replace("*", "").replace("?", "").replace('"', "").replace("<", "").replace(">", "").replace("|", "")
        clean_fecha = self.fecha.replace("/", "-").replace("\\", "-")
        self.OUTPUT_PATH = f"Informe_{clean_cliente}_{clean_fecha}.docx"
        
        # ========================================================================
        # PASO 4: CONFIGURACIÓN DE VISUALIZACIONES
        # ========================================================================
        self.ENABLE_VISUALIZATIONS = True
        
        # Configuración de Visualización 1 - Gráfico de Presencia de Plagas
        self.VIZ_1_ENABLED = True
        self.VIZ_1_PLACEHOLDER = '{{img_1}}'
        
        # Configuración de Visualización 2 - Matriz de Riesgo
        self.VIZ_2_ENABLED = True
        self.VIZ_2_PLACEHOLDER = '{{img_2}}'
        
        # Configuración de Visualización 3 - Gráfico de Dona de Riesgos Externos
        self.VIZ_3_ENABLED = True
        self.VIZ_3_PLACEHOLDER = '{{riesgos_externos_plot}}'
        
        # Configuración de Visualización 4 - Gráfico de Dona de Riesgos Internos
        self.VIZ_4_ENABLED = True
        self.VIZ_4_PLACEHOLDER = '{{riesgos_internos_plot}}'
    
    # ============================================================================
    # MÉTODOS DE AYUDA
    # ============================================================================
    
    def get_data_dict(self) -> Dict[str, Any]:
        """
        Retornar todos los datos como diccionario para reemplazo de marcadores
        Las claves deben coincidir con nombres de {{marcador}} en la plantilla
        """
        return {
            'marca_temporal' : self.marca_temporal,
            'identificador' : self.identificador,
            'cliente' : self.cliente, 
            'sede' : self.sede, 
            'direccion' : self.direccion, 
            'municipio' : self.municipio, 
            'telefono' : self.telefono, 
            'sector' : self.sector, 
            'fidelidad' : self.fidelidad, 
            'fecha' : self.fecha, 
            'hora' : self.hora_programada, 
            'h_inicio' : self.hora_ingreso, 
            'h_salida' : self.hora_salida, 
            'acompanante' : self.acompanante, 
            'cargo' : self.cargo, 
            'tecnicos' : self.tecnicos, 
            'tecnico_encargado' : self.tec_encargado, 
            'tipo_de_control' : self.tipo_control, 
            'metodo_control' : self.metodo_control, 
            'areas_controladas' : self.areas, 
            'cucarachas' : self.cucarachas,
            'hormigas' : self.hormigas,
            'moscas' : self.moscas,
            'mosquitos' : self.mosquitos,
            'zancudo' : self.zancudo,
            'raton_casero' : self.raton_casero,
            'rata_noruega' : self.rata_noruega,
            'raton_tejado' : self.raton_tejado,
            'larvas_mosquitos' : self.larvas_mosquitos,
            'obs_generales' : self.observaciones, 
            'reco_general' : self.reco_generales, 
            'reco_especificas_1' : self.reco_especificas_1, 
            'reco_especificas_2' : self.reco_especificas_2, 
            'reco_especificas_3' : self.reco_especificas_3, 
            'plaguicidas': self.plaguicidas,
            'antecedentes' : self.antecedentes,
            'periodicidad' : self.periodicidad,
            'tecnico encargado' : self.tec_encargado, 
        }
    
    def get_pest_presence_data(self) -> list:
        """
        Retornar datos de presencia de plagas para visualización 1
        """
        return [
            map_rating_to_score(self.cucarachas),
            map_rating_to_score(self.hormigas),
            map_rating_to_score(self.moscas),
            map_rating_to_score(self.mosquitos),
            map_rating_to_score(self.zancudo),
            map_rating_to_score(self.raton_casero),
            map_rating_to_score(self.rata_noruega),
            map_rating_to_score(self.raton_tejado),
            map_rating_to_score(self.larvas_mosquitos)
        ]
    
    def get_risk_scores(self) -> tuple:
        """
        Retornar puntajes de riesgo para visualización de matriz de riesgo
        """
        return (self.riesgo_total_interno, self.riesgo_total_externo)
    
    def get_external_risk_data(self) -> tuple:
        """
        Retornar datos de riesgos externos para visualización de gráfico de dona
        """
        return (
            self.risk_genera_vecindario,
            self.risk_limpieza_vecindario, 
            self.risk_manejo_basuras_vecindario,
            self.risk_infraes_vecindario,
            self.risk_ilumina_vecindario,
            self.risk_animal_cercanias,
            self.risk_construccion_cerca,
            self.risk_zonas_verdes_cerca,
            self.risk_cuerpos_de_agua_cerca,
            self.risk_desagues_cerca,
            self.risk_locales_comida
        )
    
    def get_internal_risk_data(self) -> tuple:
        """
        Retornar datos de riesgos internos para visualización de gráfico de dona
        """
        return (
            self.risk_general_establecimiento,
            self.risk_limpieza_establecimiento,
            self.risk_almacenamiento_establecimiento,
            self.risk_iluminacion_establecimiento,
            self.risk_capacitacion_personal,
            self.risk_sellamiento_puertas,
            self.risk_ventilacion_establecimiento,
            self.risk_grietas_instalaciones,
            self.risk_entrada_salida_material,
            self.risk_acumulacion_objetos,
            self.risk_areas_manipulacion_comida,
            self.risk_presencia_animales
        )
    
    def validate(self) -> bool:
        """Validar la configuración"""
        # Verificar si la plantilla existe
        if not validate_file_path(self.TEMPLATE_PATH, must_exist=True):
            print(f"✗ Error: Archivo de plantilla no encontrado: {self.TEMPLATE_PATH}")
            return False
        
        # Verificar si la ruta de salida es escribible
        if not validate_file_path(self.OUTPUT_PATH, must_exist=False):
            print(f"✗ Error: No se puede escribir en ruta de salida: {self.OUTPUT_PATH}")
            return False
        
        return True