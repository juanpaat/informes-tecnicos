from docx import Document
from docx.shared import Inches, Cm
import matplotlib.pyplot as plt
import matplotlib
import os
import tempfile
from typing import Dict, Any, Tuple, List
import re
import numpy as np

# Usar backend no interactivo para matplotlib
matplotlib.use('Agg')


class ReportGenerator:
    """Clase principal para generar informes desde plantillas DOCX"""
    
    def __init__(self, template_path: str, output_path: str):
        """
        Inicializar el generador de informes
        
        Args:
            template_path: Ruta al archivo de plantilla .docx
            output_path: Ruta donde se guardará el informe final
        """
        self.template_path = template_path
        self.output_path = output_path
        self.document = Document(template_path)
        self.temp_images = []
        
    def replace_placeholders(self, data: Dict[str, Any]) -> None:
        """
        Reemplazar todos los marcadores {{placeholder}} en el documento con datos reales
        
        Args:
            data: Diccionario con nombres de marcadores como claves y valores de reemplazo
                  Ejemplo: {'cliente': 'Empresa ABC', 'fecha': '2024-01-01'}
        """
        replaced_count = 0
        total_placeholders = len(data)
        
        # Reemplazar en párrafos principales del documento
        for i, paragraph in enumerate(self.document.paragraphs):
            replaced_count += self._replace_in_paragraph(paragraph, data, f"Para-{i+1}")
            
        # Reemplazar en tablas (muchas plantillas usan tablas para el diseño)
        for table_idx, table in enumerate(self.document.tables):
            for row_idx, row in enumerate(table.rows):
                for cell_idx, cell in enumerate(row.cells):
                    for para_idx, paragraph in enumerate(cell.paragraphs):
                        replaced_count += self._replace_in_paragraph(
                            paragraph, data, 
                            f"Table-{table_idx+1}-Row-{row_idx+1}-Cell-{cell_idx+1}-Para-{para_idx+1}"
                        )
        
        print(f"✅ Reemplazados exitosamente: {replaced_count} marcadores")
    
    def _replace_in_paragraph(self, paragraph, data: Dict[str, Any], location: str = "") -> int:
        """
        Reemplazar marcadores en un solo párrafo
        
        Args:
            paragraph: Objeto párrafo de Word
            data: Diccionario de mapeos marcador -> valor
            location: Descripción de dónde está este párrafo (para depuración)
        
        Returns:
            Número de marcadores realmente reemplazados en este párrafo
        """
        replaced_in_paragraph = 0
        paragraph_text = paragraph.text
        
        # Saltar párrafos vacíos
        if not paragraph_text.strip():
            return 0
        
        # Verificar si este párrafo contiene marcadores
        has_placeholders = False
        for key in data.keys():
            placeholder = f"{{{{{key}}}}}"
            if placeholder in paragraph_text:
                has_placeholders = True
                break
        
        if not has_placeholders:
            return 0
            
        for key, value in data.items():
            placeholder = f"{{{{{key}}}}}"  # Creates "{{key}}" format
            
            # Verificar si el marcador existe en este párrafo
            if placeholder in paragraph_text:
                # Word a veces divide marcadores en múltiples "runs" 
                # debido a cambios de formato. Necesitamos verificar cada run.
                replacement_made = False
                for run_idx, run in enumerate(paragraph.runs):
                    if placeholder in run.text:
                        run.text = run.text.replace(placeholder, str(value))
                        replaced_in_paragraph += 1
                        replacement_made = True
                        break  # Solo reemplazar una vez por párrafo
                
                if not replacement_made:
                    # El marcador podría abarcar múltiples runs - intentar enfoque de reconstrucción
                    if self._replace_across_runs(paragraph, placeholder, str(value)):
                        replaced_in_paragraph += 1
        
        return replaced_in_paragraph
    
    def _replace_across_runs(self, paragraph, placeholder: str, replacement: str) -> bool:
        """
        Manejar marcadores que abarcan múltiples runs debido al formato
        
        Args:
            paragraph: El párrafo que contiene el marcador
            placeholder: El marcador a reemplazar (ej., "{{key}}")
            replacement: El texto de reemplazo
            
        Returns:
            True si el reemplazo fue exitoso, False en caso contrario
        """
        # Obtener el texto completo para confirmar que el marcador existe
        full_text = paragraph.text
        if placeholder not in full_text:
            return False
        
        # Estrategia: Limpiar todos los runs y crear uno nuevo con texto reemplazado
        try:
            # Reemplazar en el texto completo
            new_text = full_text.replace(placeholder, replacement)
            
            # Limpiar todos los runs existentes
            for run in paragraph.runs[::-1]:  # Orden inverso para evitar problemas de índice
                run._element.getparent().remove(run._element)
            
            # Agregar nuevo run con el texto reemplazado
            new_run = paragraph.add_run(new_text)
            
            return True
            
        except Exception:
            return False
    
    def create_visualization(
        self,
        data: Dict[str, Any],
        viz_type: str = 'bar',
        title: str = '',
        xlabel: str = '',
        ylabel: str = '',
        figsize: Tuple[int, int] = (10, 6)
    ) -> str:
        """
        Crear una visualización matplotlib y guardarla temporalmente
        
        Args:
            data: Diccionario con datos x e y {'x': [...], 'y': [...]}
            viz_type: Tipo de gráfico ('bar', 'line', 'pie', 'scatter')
            title: Título del gráfico
            xlabel: Etiqueta del eje X
            ylabel: Etiqueta del eje Y
            figsize: Tamaño de la figura como (ancho, alto)
            
        Returns:
            Ruta al archivo de imagen temporal
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        # Crear visualización según el tipo
        if viz_type == 'bar':
            ax.bar(data['x'], data['y'])
        elif viz_type == 'line':
            ax.plot(data['x'], data['y'], marker='o')
        elif viz_type == 'pie':
            ax.pie(data['y'], labels=data['x'], autopct='%1.1f%%')
        elif viz_type == 'scatter':
            ax.scatter(data['x'], data['y'])
        else:
            raise ValueError(f"Tipo de visualización no soportado: {viz_type}")
        
        # Establecer etiquetas y título
        if title:
            ax.set_title(title, fontsize=14, fontweight='bold')
        if xlabel and viz_type != 'pie':
            ax.set_xlabel(xlabel)
        if ylabel and viz_type != 'pie':
            ax.set_ylabel(ylabel)
        
        plt.tight_layout()
        
        # Guardar en archivo temporal
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        plt.savefig(temp_file.name, dpi=300, bbox_inches='tight')
        plt.close()
        
        self.temp_images.append(temp_file.name)
        return temp_file.name
    
    def add_image_to_placeholder(
        self,
        placeholder: str,
        image_path: str,
        width: float = 7.2,
        height: float = 4.55
    ) -> None:
        """
        Reemplazar un marcador con una imagen
        
        Args:
            placeholder: Texto del marcador a reemplazar (ej., '{{img_1}}')
            image_path: Ruta al archivo de imagen
            width: Ancho de la imagen en cm (por defecto 7.2 cm)
            height: Alto de la imagen en cm (por defecto 4.55 cm)
        """
        # Buscar en párrafos principales del documento
        for paragraph in self.document.paragraphs:
            if placeholder in paragraph.text:
                self._replace_placeholder_with_image_in_paragraph(paragraph, placeholder, image_path, width, height)
                return
        
        # Buscar en tablas  
        for table in self.document.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        if placeholder in paragraph.text:
                            self._replace_placeholder_with_image_in_paragraph(paragraph, placeholder, image_path, width, height)
                            return
    
    def _replace_placeholder_with_image_in_paragraph(self, paragraph, placeholder: str, image_path: str, width: float, height: float):
        """
        Reemplazar marcador con imagen en un párrafo específico preservando estructura
        """
        # Verificar si el marcador abarca múltiples runs (común con formato)
        full_text = paragraph.text
        if placeholder in full_text:
            # Encontrar qué run(s) contienen el marcador
            for run in paragraph.runs:
                if placeholder in run.text:
                    # Reemplazar en este run específico
                    run.text = run.text.replace(placeholder, '')
                    # Agregar imagen al mismo run con dimensiones específicas en cm
                    run.add_picture(image_path, width=Cm(width), height=Cm(height))
                    return
            
            # Si el marcador abarca múltiples runs, necesitamos un enfoque diferente
            # Limpiar el texto del párrafo y agregar imagen en nuevo run
            paragraph.clear()
            run = paragraph.add_run()
            run.add_picture(image_path, width=Cm(width), height=Cm(height))
    
    def save(self) -> None:
        """Guardar el documento y limpiar archivos temporales"""
        self.document.save(self.output_path)
        
        # Limpiar archivos de imagen temporales
        for temp_file in self.temp_images:
            try:
                os.remove(temp_file)
            except Exception:
                pass
    
    def __del__(self):
        """Limpiar cuando el objeto es destruido"""
        for temp_file in self.temp_images:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except Exception:
                pass


def parse_spreadsheet_line(line: str, delimiter: str = '\t') -> List[str]:
    """
    Analizar una línea de hoja de cálculo (delimitada por tabulaciones o comas)
    
    Args:
        line: La línea de hoja de cálculo pegada
        delimiter: Delimitador utilizado (tabulación por defecto, puede ser ',' para CSV)
        
    Returns:
        Lista de valores
    """
    return [value.strip() for value in line.split(delimiter)]

def map_rating_to_score(rating: str) -> int:
    """
    Mapear calificaciones emoji en español a puntajes numéricos
    
    Args:
        rating: Cadena de calificación con emoji (ej., "🔴 Mala", "🟢 Excelente")
        
    Returns:
        Puntaje numérico (1-4)
        
    Raises:
        ValueError: Si la calificación no es reconocida
    """
    rating_map = {
        "🔴 Mala": 1,
        "🔴 Muchas": 1,
        "🔴 Mucha evidencia": 3,
        "🟠 Regular": 2,
        "🟠 Bastantes": 2,
        "🟠 Considerable evidencia": 2,
        "🟡 Buena": 3,
        "🟡 Pocas": 3,
        "🟡 Poca evidencia": 1,
        "🟢 Excelente": 4,
        "🟢 Nada": 4,
        "🟢 Sin evidencia": 0.05
    }
     
    # Quitar espacios en blanco e intentar coincidencia exacta
    rating = rating.strip()
    
    if rating in rating_map:
        return rating_map[rating]
    
    # Intentar coincidencia parcial (en caso de ligeras variaciones)
    for key, value in rating_map.items():
        if key in rating or rating in key:
            return value
    
    # Si no se encuentra coincidencia, lanzar error
    raise ValueError(
        f"Calificación desconocida: '{rating}'. Se esperaba una de: "
        f"{', '.join(rating_map.keys())}"
    )

def calculate_risk_score(rating: str, weight: float) -> float:
    """
    Calcular puntaje de riesgo para una métrica basada en calificación y peso
    
    Fórmula: peso * (4 - puntaje_mapeado)
    
    Args:
        rating: Cadena de calificación con emoji (ej., "🔴 Mala", "🟢 Excelente")
        weight: Peso/importancia de esta métrica (0-1)
        
    Returns:
        Puntaje de contribución al riesgo
    """
    mapped_score = map_rating_to_score(rating)
    risk_contribution = weight * (4 - mapped_score)
    return risk_contribution


def create_risk_matrix_plot(
    riesgo_interno: float,
    riesgo_externo: float,
    figsize: Tuple[int, int] = (2.76, 1.77),
    save_path: str = None) -> str:
    """
    Crear una visualización de matriz de riesgo (Diagnóstico de Riesgos)
    
    Args:
        riesgo_interno: Puntaje de riesgo interno (1-4, donde 1=Bajo, 4=Alto)
        riesgo_externo: Puntaje de riesgo externo (1-4, donde 1=Bajo, 4=Alto)
        figsize: Tamaño de la figura como (ancho, alto)
        save_path: Ruta opcional para guardar la imagen
        
    Returns:
        Ruta al archivo de imagen guardado
    """

    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Definir colores de la matriz de riesgo (de la imagen)
    # La matriz está organizada como [fila][col] donde fila=externo (arriba a abajo), col=interno (derecha a izquierda)
    colors = [
        ['#D32F2F', '#D32F2F', '#FFB300'],  # Alto externo: I, II, III
        ['#D32F2F', '#FFB300', '#4DB6AC'],  # Medio externo: IV, V, VI
        ['#FFB300', '#4DB6AC', '#4DB6AC']   # Bajo externo: VII, VIII, IX
    ]
    
    # Etiquetas de nivel de riesgo para cada celda
    labels = [
        ['I', 'II', 'III'],
        ['IV', 'V', 'VI'],
        ['VII', 'VIII', 'IX']
    ]
    
    # Crear la cuadrícula (3x3)
    for i in range(3):
        for j in range(3):
            # Dibujar rectángulo
            rect = plt.Rectangle((j, 2-i), 1, 1, 
                                facecolor=colors[i][j], 
                                edgecolor='white', 
                                linewidth=2)
            ax.add_patch(rect)
            
            # Agregar etiqueta con número romano
            ax.text(j + 0.5, 2-i + 0.5, labels[i][j],
                   ha='center', va='center',
                   fontsize=10, fontweight='light',
                   color='white')
    
    riesgo_interno += 1
    riesgo_externo += 1

    # Mapear puntajes de riesgo a posiciones de cuadrícula
    # Interno (eje x): 1=Bajo (derecha), 4=Alto (izquierda)
    # Necesitamos invertir: 1->2.5, 2->1.5, 3->0.5, 4->-0.5 luego fijar a 0-3
    x_pos = 3 - (riesgo_interno - 1)
    
    # Externo (eje y): 1=Bajo (abajo), 4=Alto (arriba)
    y_pos = riesgo_externo - 1
    
    # Graficar el punto
    ax.plot(x_pos, y_pos, 'o', 
           markersize=8, 
           color='darkblue', 
           markeredgecolor='black', 
           markeredgewidth=1,
           zorder=10)
    
    # Establecer límites de ejes
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 3)
    
    # Establecer marcas y etiquetas
    # Eje X (Interno): invertido de derecha a izquierda
    ax.set_xticks([0.5, 1.5, 2.5])
    ax.set_xticklabels(['Alto', 'Medio', 'Bajo'], fontsize=8, fontweight='light')
    ax.set_xlabel('Riesgo Interno', fontsize=9, fontweight='bold', labelpad=5)
    
    # Eje Y (Externo): normal de abajo hacia arriba
    ax.set_yticks([0.5, 1.5, 2.5])
    ax.set_yticklabels(['Bajo', 'Medio', 'Alto'], fontsize=8, fontweight='light')
    ax.set_ylabel('Riesgo Externo', fontsize=9, fontweight='bold', labelpad=5)
    
    # Quitar bordes
    for spine in ax.spines.values():
        spine.set_visible(False)

    
    plt.tight_layout()
    
    # Guardar en archivo
    if save_path is None:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        save_path = temp_file.name
    
    plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='none', transparent=True)
    plt.close()
    
    return save_path


class ReportGeneratorMethods:
    """Métodos adicionales para la clase ReportGenerator"""
    pass


# Agregar métodos a la clase ReportGenerator
def create_risk_matrix(
    self,
    riesgo_interno: float,
    riesgo_externo: float) -> str:
    """
    Crear visualización de matriz de riesgo
    
    Args:
        riesgo_interno: Puntaje de riesgo interno (1-4)
        riesgo_externo: Puntaje de riesgo externo (1-4)
        
    Returns:
        Ruta al archivo de imagen temporal
    """
    image_path = create_risk_matrix_plot(riesgo_interno, riesgo_externo)
    self.temp_images.append(image_path)
    return image_path

def create_pest_presence_chart(self, pest_values: list) -> str:
    """
    Crear visualización de presencia de plagas
    
    Args:
        pest_values: Lista de niveles de infestación de plagas
        
    Returns:
        Ruta al archivo de imagen temporal
    """
    # Guardar en archivo temporal
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    plot_presencia_plagas(pest_values, temp_file.name)
    self.temp_images.append(temp_file.name)
    return temp_file.name

# Agregar métodos a la clase ReportGenerator
def create_external_risk_donut(
    self,
    risk_genera_vecindario: float,
    risk_limpieza_vecindario: float, 
    risk_manejo_basuras_vecindario: float,
    risk_infraes_vecindario: float,
    risk_ilumina_vecindario: float,
    risk_animal_cercanias: float,
    risk_construccion_cerca: float,
    risk_zonas_verdes_cerca: float,
    risk_cuerpos_de_agua_cerca: float,
    risk_desagues_cerca: float,
    risk_locales_comida: float) -> str:
    """
    Crear visualización de gráfico de dona para riesgos externos
    
    Returns:
        Ruta al archivo de imagen temporal
    """
    image_path = create_external_risk_donut_plot(
        risk_genera_vecindario, risk_limpieza_vecindario, risk_manejo_basuras_vecindario,
        risk_infraes_vecindario, risk_ilumina_vecindario, risk_animal_cercanias,
        risk_construccion_cerca, risk_zonas_verdes_cerca, risk_cuerpos_de_agua_cerca,
        risk_desagues_cerca, risk_locales_comida
    )
    self.temp_images.append(image_path)
    return image_path

def create_internal_risk_donut(
    self,
    risk_general_establecimiento: float,
    risk_limpieza_establecimiento: float,
    risk_almacenamiento_establecimiento: float,
    risk_iluminacion_establecimiento: float,
    risk_capacitacion_personal: float,
    risk_sellamiento_puertas: float,
    risk_ventilacion_establecimiento: float,
    risk_grietas_instalaciones: float,
    risk_entrada_salida_material: float,
    risk_acumulacion_objetos: float,
    risk_areas_manipulacion_comida: float,
    risk_presencia_animales: float) -> str:
    """
    Crear visualización de gráfico de dona para riesgos internos
    
    Returns:
        Ruta al archivo de imagen temporal
    """
    image_path = create_internal_risk_donut_plot(
        risk_general_establecimiento, risk_limpieza_establecimiento,
        risk_almacenamiento_establecimiento, risk_iluminacion_establecimiento,
        risk_capacitacion_personal, risk_sellamiento_puertas,
        risk_ventilacion_establecimiento, risk_grietas_instalaciones,
        risk_entrada_salida_material, risk_acumulacion_objetos,
        risk_areas_manipulacion_comida, risk_presencia_animales
    )
    self.temp_images.append(image_path)
    return image_path

# Adjuntar métodos a la clase ReportGenerator
ReportGenerator.create_risk_matrix = create_risk_matrix
ReportGenerator.create_pest_presence_chart = create_pest_presence_chart
ReportGenerator.create_external_risk_donut = create_external_risk_donut
ReportGenerator.create_internal_risk_donut = create_internal_risk_donut


def plot_presencia_plagas(values, save_path=None):
    """
    Crea un gráfico de barras mostrando la presencia (nivel de infestación) de diferentes plagas.

    Parámetros
    ----------
    values : list o tuple
        Lista de niveles de infestación en el siguiente orden:
        [Cucarachas, Hormigas, Moscas, Mosquitos, Zancudos, 
         Ratón Casero, Rata Noruega, Ratón de Tejado, Larvas de Mosquitos]
    save_path : str, opcional
        Si se proporciona, guarda la figura en la ruta de archivo dada en lugar de mostrarla.
    """

    # Etiquetas
    plagas = [
        "Cucarachas",
        "Hormigas",
        "Moscas",
        "Mosquitos",
        "Zancudos",
        "Ratón Casero",
        "Rata Noruega",
        "Ratón de Tejado",
        "Larvas de Mosquitos"
    ]

    # Crear figura
    plt.figure(figsize=(2.76, 1.77))
    bars = plt.bar(plagas, values, color='#65B6C9', width=0.6)

    # Título y etiquetas de ejes
    plt.ylabel("Nivel de infestación", fontsize=6)
    plt.xticks(rotation=45, ha='right', fontsize=4)
    plt.yticks([0, 1, 2, 3, 4], fontsize=6)

    # Límite del eje Y (ajustar según sea necesario)
    plt.ylim(0, 4)

    # Estilo de cuadrícula y diseño
    plt.grid(axis='y', linestyle='-', linewidth=0.5, alpha=0.5)
    plt.box(False)
    plt.tight_layout()

    # Guardar o mostrar el gráfico
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='none', transparent=True)
        plt.close()
    else:
        plt.show()


def remove_double_spaces(text: str) -> str:
    """
    Remover espacios dobles y múltiples de una cadena de texto
    
    Args:
        text: Texto a limpiar
        
    Returns:
        Texto con espacios múltiples reemplazados por espacios simples
    """
    import re
    # Usar regex para reemplazar múltiples espacios en blanco con uno solo
    return re.sub(r'\s+', ' ', text.strip())


def validate_file_path(path: str, must_exist: bool = True) -> bool:
    """
    Validar una ruta de archivo
    
    Args:
        path: Ruta a validar
        must_exist: Si el archivo debe existir ya
        
    Returns:
        True si es válido, False en caso contrario
    """
    if must_exist:
        return os.path.isfile(path)
    else:
        # Verificar si el directorio existe y es escribible
        directory = os.path.dirname(path) or '.'
        return os.path.isdir(directory) and os.access(directory, os.W_OK)


def scan_template_placeholders(document) -> List[str]:
    """
    Escanear un documento de Word para encontrar todos los patrones {{placeholder}}
    
    Args:
        document: Objeto Document de python-docx
        
    Returns:
        Lista de nombres de marcadores encontrados en plantilla (sin los corchetes {{ }})
    """
    placeholders = set()
    
    # Escanear párrafos principales del documento
    for paragraph in document.paragraphs:
        placeholders.update(_extract_placeholders_from_text(paragraph.text))
    
    # Escanear tablas
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    placeholders.update(_extract_placeholders_from_text(paragraph.text))
    
    return sorted(list(placeholders))


def sentence_case_after_period(text):
    """
    Capitaliza el primer carácter después de un punto, independientemente del 
    número de espacios u otros caracteres entre ellos.
    
    El patrón busca:
    1. Un punto (`.`)
    2. Cualquier cantidad de espacios en blanco o caracteres no de nueva línea (perezosamente: `.*?`)
    3. La primera letra (capturada en el grupo 1: `([a-z])`)
    """

    # 1. Comenzar haciendo toda la cadena en minúsculas para manejar casos mixtos existentes
    #    (Esto es opcional, pero es parte del formateo de "caso apropiado")
    text = text.lower()
    
    # 2. Capitalizar la primera letra de *toda* la cadena
    if text:
        text = text[0].upper() + text[1:]

    # 3. Usar regex para encontrar y capitalizar la letra después de un punto
    # El regex: (\. *)([a-z])
    # Grupo 1: (\. *) coincide con el punto y cualquier espacio siguiente (ej., ". ")
    # Grupo 2: ([a-z]) coincide y captura la primera letra minúscula
    def capitalize_match(match):
        # match.group(1) es el punto y espacios (". ")
        # match.group(2) es la letra a capitalizar ("a")
        return match.group(1) + match.group(2).upper()

    # La función re.sub aplica la lógica de reemplazo a cada coincidencia
    corrected_text = re.sub(r'(\. *)([a-z])', capitalize_match, text)
    
    return corrected_text


def create_external_risk_donut_plot(
    risk_genera_vecindario: float,
    risk_limpieza_vecindario: float, 
    risk_manejo_basuras_vecindario: float,
    risk_infraes_vecindario: float,
    risk_ilumina_vecindario: float,
    risk_animal_cercanias: float,
    risk_construccion_cerca: float,
    risk_zonas_verdes_cerca: float,
    risk_cuerpos_de_agua_cerca: float,
    risk_desagues_cerca: float,
    risk_locales_comida: float,
    figsize: Tuple[int, int] = (4.72, 3.07),
    save_path: str = None) -> str:
    """
    Crear una visualización de gráfico de dona para el Diagnóstico de Riesgos Externos
    
    Args:
        risk_genera_vecindario: Puntaje de riesgo de generación del vecindario
        risk_limpieza_vecindario: Puntaje de riesgo de limpieza del vecindario
        risk_manejo_basuras_vecindario: Puntaje de riesgo de manejo de basuras del vecindario
        risk_infraes_vecindario: Puntaje de riesgo de infraestructura del vecindario
        risk_ilumina_vecindario: Puntaje de riesgo de iluminación del vecindario
        risk_animal_cercanias: Puntaje de riesgo de animales en cercanías
        risk_construccion_cerca: Puntaje de riesgo de construcción cerca
        risk_zonas_verdes_cerca: Puntaje de riesgo de zonas verdes cerca
        risk_cuerpos_de_agua_cerca: Puntaje de riesgo de cuerpos de agua cerca
        risk_desagues_cerca: Puntaje de riesgo de desagües cerca
        risk_locales_comida: Puntaje de riesgo de locales de comida
        figsize: Tamaño de la figura como (ancho, alto)
        save_path: Ruta opcional para guardar la imagen
        
    Returns:
        Ruta al archivo de imagen guardado
    """
    
    # Datos para el gráfico
    nombres = [
        'Otros',
        'Limpieza del vecindario', 
        'Manejo de basuras del vecindario',
        'Infraestructura del vecindario',
        'Iluminación del vecindario',
        'Presencia de animales en cercanías',
        'Construcciones cercanas',
        'Zonas Verdes aledañas',
        'Cuerpos de agua cercanos',
        'Presencia de deshagües en la cercania',
        'Locales de comida cerca'
    ]
    
    valores = [
        risk_genera_vecindario,
        risk_limpieza_vecindario,
        risk_manejo_basuras_vecindario,
        risk_infraes_vecindario,
        risk_ilumina_vecindario,
        risk_animal_cercanias,
        risk_construccion_cerca,
        risk_zonas_verdes_cerca,
        risk_cuerpos_de_agua_cerca,
        risk_desagues_cerca,
        risk_locales_comida
    ]
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Crear el círculo central para hacer el gráfico de dona
    circulo_central = plt.Circle((0, 0), 0.7, color='white')
    
    # Crear el gráfico de torta con propiedades personalizadas
    colores = plt.cm.Reds(np.linspace(0.3, 0.9, len(valores)))
    
    wedges, texts, autotexts = ax.pie(valores, labels=nombres, 
                                     wedgeprops={'linewidth': 2, 'edgecolor': 'white'},
                                     colors=colores,
                                     autopct='%1.1f%%',
                                     textprops={'fontsize': 6},
                                     pctdistance=0.85,
                                     labeldistance=1.2,
                                     rotatelabels=False,
                                     frame=False)
    
    # Agregar el círculo central
    ax.add_artist(circulo_central)
    
    # Agregar título en el centro
    plt.text(0, 0, 'Riesgos\nExternos', ha='center', va='center', 
             fontsize=6, fontweight='bold', color='#333333')
    
    plt.tight_layout()
    
    # Guardar en archivo
    if save_path is None:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        save_path = temp_file.name
    
    plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='none', transparent=True)
    plt.close()
    
    return save_path


def create_internal_risk_donut_plot(
    risk_general_establecimiento: float,
    risk_limpieza_establecimiento: float,
    risk_almacenamiento_establecimiento: float,
    risk_iluminacion_establecimiento: float,
    risk_capacitacion_personal: float,
    risk_sellamiento_puertas: float,
    risk_ventilacion_establecimiento: float,
    risk_grietas_instalaciones: float,
    risk_entrada_salida_material: float,
    risk_acumulacion_objetos: float,
    risk_areas_manipulacion_comida: float,
    risk_presencia_animales: float,
    figsize: Tuple[int, int] = (4.72, 3.07),
    save_path: str = None) -> str:
    """
    Crear una visualización de gráfico de dona para el Diagnóstico de Riesgos Internos
    
    Args:
        risk_general_establecimiento: Puntaje de riesgo general del establecimiento
        risk_limpieza_establecimiento: Puntaje de riesgo de limpieza del establecimiento
        risk_almacenamiento_establecimiento: Puntaje de riesgo de almacenamiento del establecimiento
        risk_iluminacion_establecimiento: Puntaje de riesgo de iluminación del establecimiento
        risk_capacitacion_personal: Puntaje de riesgo de capacitación del personal
        risk_sellamiento_puertas: Puntaje de riesgo de sellamiento de puertas
        risk_ventilacion_establecimiento: Puntaje de riesgo de ventilación del establecimiento
        risk_grietas_instalaciones: Puntaje de riesgo de grietas en instalaciones
        risk_entrada_salida_material: Puntaje de riesgo de entrada y salida de material
        risk_acumulacion_objetos: Puntaje de riesgo de acumulación de objetos
        risk_areas_manipulacion_comida: Puntaje de riesgo de áreas de manipulación de comida
        risk_presencia_animales: Puntaje de riesgo de presencia de animales
        figsize: Tamaño de la figura como (ancho, alto)
        save_path: Ruta opcional para guardar la imagen
        
    Returns:
        Ruta al archivo de imagen guardado
    """
    
    # Datos para el gráfico
    nombres = [
        'Otros',
        'Limpieza del establecimiento',
        'Almacenamiento',
        'Iluminación',
        'Capacitación del personal',
        'Sellamiento de puertas',
        'Ventilación del establecimiento',
        'Grietas en instalaciones',
        'Entrada/Salida de material',
        'Acumulación de objetos',
        'Áreas de manipulación de comida',
        'Presencia de animales/mascotas'
    ]
    
    valores = [
        risk_general_establecimiento,
        risk_limpieza_establecimiento,
        risk_almacenamiento_establecimiento,
        risk_iluminacion_establecimiento,
        risk_capacitacion_personal,
        risk_sellamiento_puertas,
        risk_ventilacion_establecimiento,
        risk_grietas_instalaciones,
        risk_entrada_salida_material,
        risk_acumulacion_objetos,
        risk_areas_manipulacion_comida,
        risk_presencia_animales
    ]
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Crear el círculo central para hacer el gráfico de dona
    circulo_central = plt.Circle((0, 0), 0.5, color='white')
    
    # Crear el gráfico de torta con propiedades personalizadas
    colores = plt.cm.Blues(np.linspace(0.3, 0.9, len(valores)))
    
    wedges, texts, autotexts = ax.pie(valores, labels=nombres, 
                                     wedgeprops={'linewidth': 1, 'edgecolor': 'white'},
                                     colors=colores,
                                     autopct='%1.1f%%',
                                     textprops={'fontsize': 6},
                                     pctdistance=0.85)
    
    # Agregar el círculo central
    ax.add_artist(circulo_central)
    
    # Agregar título en el centro
    plt.text(0, 0, 'Riesgos\nInternos', ha='center', va='center', 
             fontsize=6, fontweight='bold', color='#333333')
    
    plt.tight_layout()
    
    # Guardar en archivo
    if save_path is None:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        save_path = temp_file.name
    
    plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='none', transparent=True)
    plt.close()
    
    return save_path


def _extract_placeholders_from_text(text: str) -> List[str]:
    """
    Extraer patrones {{placeholder}} del texto usando regex
    
    Args:
        text: Texto para buscar marcadores
        
    Returns:
        Lista de nombres de marcadores (sin corchetes)
    """
    import re
    # Patrón para coincidir con {{cualquier_cosa}} pero capturar solo el contenido interno
    pattern = r'\{\{([^}]+)\}\}'
    matches = re.findall(pattern, text)
    # Quitar espacios en blanco de las coincidencias en caso de que haya espacios
    return [match.strip() for match in matches]