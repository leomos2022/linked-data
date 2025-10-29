#!/usr/bin/env python3
"""
Transformación de Datos CSV a RDF - Proyecto Linked Data Universidades
Conversión del dataset de estudiantes a triples RDF basados en la ontología creada
"""

import pandas as pd
from rdflib import Graph, Namespace, RDF, RDFS, XSD, URIRef, Literal, BNode
from rdflib.namespace import FOAF, DC, DCTERMS
import hashlib
from datetime import datetime
import re

class DataTransformer:
    """Transformador de datos CSV a formato RDF"""
    
    def __init__(self, csv_file_path, ontology_file_path):
        """Inicializar con archivos CSV y ontología"""
        self.csv_path = csv_file_path
        self.ontology_path = ontology_file_path
        
        # Cargar datos CSV
        self.df = pd.read_csv(csv_file_path)
        print(f"Datos CSV cargados: {len(self.df)} registros")
        
        # Inicializar grafo RDF
        self.g = Graph()
        
        # Definir namespaces (mismos que en la ontología)
        self.UNIV = Namespace("http://example.org/university/")
        self.SCHEMA = Namespace("http://schema.org/")
        self.EDU = Namespace("http://example.org/education/")
        self.GEO = Namespace("http://example.org/geography/")
        self.BEHAVIOR = Namespace("http://example.org/behavior/")
        
        # Bind namespaces
        self.g.bind("univ", self.UNIV)
        self.g.bind("schema", self.SCHEMA)
        self.g.bind("edu", self.EDU)
        self.g.bind("geo", self.GEO)
        self.g.bind("behavior", self.BEHAVIOR)
        self.g.bind("foaf", FOAF)
        self.g.bind("dc", DC)
        self.g.bind("dcterms", DCTERMS)
        
        # Cargar ontología base
        self.load_base_ontology()
        
        # Contadores para estadísticas
        self.stats = {
            'students': 0,
            'universities': 0,
            'decisions': 0,
            'total_triples': 0
        }
    
    def load_base_ontology(self):
        """Cargar la ontología base si existe"""
        try:
            self.g.parse(self.ontology_path, format="turtle")
            print(f"Ontología base cargada desde: {self.ontology_path}")
        except Exception as e:
            print(f"No se pudo cargar la ontología base: {e}")
            print("Continuando sin ontología base...")
    
    def clean_uri_component(self, text):
        """Limpiar texto para usar en URIs"""
        if pd.isna(text):
            return "unknown"
        # Convertir a string y limpiar
        text = str(text).strip()
        # Reemplazar espacios y caracteres especiales
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'\s+', '_', text)
        return text.lower()
    
    def create_student_uri(self, student_id):
        """Crear URI para estudiante"""
        clean_id = self.clean_uri_component(student_id)
        return self.UNIV[f"student_{clean_id}"]
    
    def create_university_uri(self, university_code):
        """Crear URI para universidad"""
        clean_code = self.clean_uri_component(university_code)
        return self.UNIV[f"university_{clean_code}"]
    
    def create_area_uri(self, area_name):
        """Crear URI para área de conocimiento"""
        clean_area = self.clean_uri_component(area_name)
        return self.EDU[f"area_{clean_area}"]
    
    def create_city_uri(self, city_name):
        """Crear URI para ciudad"""
        clean_city = self.clean_uri_component(city_name)
        return self.GEO[f"city_{clean_city}"]
    
    def create_department_uri(self, dept_name):
        """Crear URI para departamento"""
        clean_dept = self.clean_uri_component(dept_name)
        return self.GEO[f"dept_{clean_dept}"]
    
    def create_decision_uri(self, student_id, university_code):
        """Crear URI para decisión académica"""
        # Crear hash único para la decisión
        decision_hash = hashlib.md5(f"{student_id}_{university_code}".encode()).hexdigest()[:8]
        return self.BEHAVIOR[f"decision_{decision_hash}"]
    
    def convert_boolean(self, value):
        """Convertir valores de string a boolean"""
        if pd.isna(value):
            return False
        return str(value).lower() in ['sí', 'si', 'yes', 'true', '1']
    
    def transform_students(self):
        """Transformar datos de estudiantes a RDF"""
        print("Transformando datos de estudiantes...")
        
        for index, row in self.df.iterrows():
            # URI del estudiante
            student_uri = self.create_student_uri(row['id_estudiante'])
            
            # Tipo de entidad
            self.g.add((student_uri, RDF.type, self.UNIV.Student))
            
            # Información básica
            self.g.add((student_uri, DC.identifier, Literal(row['id_estudiante'])))
            self.g.add((student_uri, RDFS.label, 
                       Literal(f"Estudiante {row['id_estudiante']}", lang="es")))
            
            # Datos demográficos
            if not pd.isna(row['edad']):
                self.g.add((student_uri, self.UNIV.age, Literal(int(row['edad']))))
            
            if not pd.isna(row['genero']):
                self.g.add((student_uri, self.UNIV.gender, Literal(row['genero'], lang="es")))
            
            if not pd.isna(row['estrato']):
                self.g.add((student_uri, self.UNIV.socioeconomicStratum, 
                           Literal(int(row['estrato']))))
            
            # Puntaje académico
            if not pd.isna(row['puntaje_saber11']):
                self.g.add((student_uri, self.EDU.saber11Score, 
                           Literal(float(row['puntaje_saber11']))))
            
            # Relación con ciudad de origen
            if not pd.isna(row['ciudad_origen']):
                city_uri = self.create_city_uri(row['ciudad_origen'])
                self.g.add((student_uri, self.GEO.originFrom, city_uri))
                
                # Crear ciudad si no existe
                self.g.add((city_uri, RDF.type, self.GEO.City))
                self.g.add((city_uri, RDFS.label, Literal(row['ciudad_origen'], lang="es")))
                self.g.add((city_uri, DC.identifier, Literal(row['ciudad_origen'])))
            
            # Relación con área de preferencia
            if not pd.isna(row['preferencia_area']):
                area_uri = self.create_area_uri(row['preferencia_area'])
                self.g.add((student_uri, self.EDU.prefersArea, area_uri))
                
                # Crear área si no existe
                self.g.add((area_uri, RDF.type, self.EDU.KnowledgeArea))
                self.g.add((area_uri, RDFS.label, Literal(row['preferencia_area'], lang="es")))
                self.g.add((area_uri, DC.identifier, Literal(row['preferencia_area'])))
            
            # Relación con universidad
            if not pd.isna(row['universidad_codigo']):
                university_uri = self.create_university_uri(row['universidad_codigo'])
                self.g.add((student_uri, self.UNIV.appliesTo, university_uri))
            
            self.stats['students'] += 1
        
        print(f"Transformados {self.stats['students']} estudiantes")
    
    def transform_universities(self):
        """Transformar datos de universidades a RDF"""
        print("Transformando datos de universidades...")
        
        # Obtener universidades únicas
        universities = self.df[['universidad_codigo', 'universidad_nombre', 
                               'universidad_departamento', 'universidad_tipo',
                               'universidad_acreditada', 'ranking_nacional']].drop_duplicates()
        
        for index, row in universities.iterrows():
            # URI de la universidad
            university_uri = self.create_university_uri(row['universidad_codigo'])
            
            # Tipo de entidad
            self.g.add((university_uri, RDF.type, self.UNIV.University))
            
            # Información básica
            self.g.add((university_uri, DC.identifier, Literal(row['universidad_codigo'])))
            self.g.add((university_uri, RDFS.label, 
                       Literal(row['universidad_nombre'], lang="es")))
            self.g.add((university_uri, DC.title, 
                       Literal(row['universidad_nombre'], lang="es")))
            
            # Tipo de universidad
            if not pd.isna(row['universidad_tipo']):
                self.g.add((university_uri, self.UNIV.hasType, 
                           Literal(row['universidad_tipo'], lang="es")))
            
            # Acreditación
            if not pd.isna(row['universidad_acreditada']):
                is_accredited = self.convert_boolean(row['universidad_acreditada'])
                self.g.add((university_uri, self.UNIV.isAccredited, 
                           Literal(is_accredited)))
            
            # Ranking nacional
            if not pd.isna(row['ranking_nacional']):
                self.g.add((university_uri, self.UNIV.nationalRanking, 
                           Literal(int(row['ranking_nacional']))))
            
            # Relación con departamento
            if not pd.isna(row['universidad_departamento']):
                dept_uri = self.create_department_uri(row['universidad_departamento'])
                self.g.add((university_uri, self.GEO.locatedIn, dept_uri))
                
                # Crear departamento si no existe
                self.g.add((dept_uri, RDF.type, self.GEO.Department))
                self.g.add((dept_uri, RDFS.label, 
                           Literal(row['universidad_departamento'], lang="es")))
                self.g.add((dept_uri, DC.identifier, 
                           Literal(row['universidad_departamento'])))
            
            self.stats['universities'] += 1
        
        print(f"Transformadas {self.stats['universities']} universidades")
    
    def transform_academic_decisions(self):
        """Transformar decisiones académicas a RDF"""
        print("Transformando decisiones académicas...")
        
        for index, row in self.df.iterrows():
            # URIs relacionadas
            student_uri = self.create_student_uri(row['id_estudiante'])
            university_uri = self.create_university_uri(row['universidad_codigo'])
            decision_uri = self.create_decision_uri(row['id_estudiante'], row['universidad_codigo'])
            
            # Tipo de entidad
            self.g.add((decision_uri, RDF.type, self.BEHAVIOR.AcademicDecision))
            
            # Relación estudiante -> decisión
            self.g.add((student_uri, self.BEHAVIOR.makes, decision_uri))
            
            # Información de la decisión
            self.g.add((decision_uri, RDFS.label, 
                       Literal(f"Decisión de {row['id_estudiante']} sobre {row['universidad_codigo']}", lang="es")))
            
            # Decisión final
            if not pd.isna(row['eligio_universidad']):
                final_decision = self.convert_boolean(row['eligio_universidad'])
                self.g.add((decision_uri, self.BEHAVIOR.finalDecision, Literal(final_decision)))
            
            # Modalidad del programa
            if not pd.isna(row['modalidad_programa']):
                self.g.add((decision_uri, self.EDU.programModality, 
                           Literal(row['modalidad_programa'], lang="es")))
            
            # Convenio internacional
            if not pd.isna(row['convenio_internacional']):
                has_agreement = self.convert_boolean(row['convenio_internacional'])
                self.g.add((university_uri, self.UNIV.hasInternationalAgreement, 
                           Literal(has_agreement)))
            
            # Beca disponible
            if not pd.isna(row['beca_disponible']):
                has_scholarship = self.convert_boolean(row['beca_disponible'])
                self.g.add((university_uri, self.UNIV.hasScholarship, Literal(has_scholarship)))
            
            # Relacionar decisión con universidad
            self.g.add((decision_uri, DC.subject, university_uri))
            
            # Timestamp de creación
            self.g.add((decision_uri, DCTERMS.created, 
                       Literal(datetime.now().isoformat(), datatype=XSD.dateTime)))
            
            self.stats['decisions'] += 1
        
        print(f"Transformadas {self.stats['decisions']} decisiones académicas")
    
    def add_metadata(self):
        """Agregar metadatos al dataset"""
        print("Agregando metadatos del dataset...")
        
        # URI del dataset
        dataset_uri = self.UNIV["dataset_university_choices"]
        
        # Información del dataset
        self.g.add((dataset_uri, RDF.type, self.SCHEMA.Dataset))
        self.g.add((dataset_uri, DC.title, 
                   Literal("Dataset de Decisiones Universitarias Colombia", lang="es")))
        self.g.add((dataset_uri, DC.description, 
                   Literal("Datos sobre patrones de comportamiento estudiantil en la selección de universidades en Colombia", lang="es")))
        self.g.add((dataset_uri, DCTERMS.created, 
                   Literal(datetime.now().isoformat(), datatype=XSD.dateTime)))
        self.g.add((dataset_uri, DC.creator, 
                   Literal("Proyecto Linked Data - Web Semántica", lang="es")))
        self.g.add((dataset_uri, DC.language, Literal("es")))
        self.g.add((dataset_uri, DCTERMS.spatial, Literal("Colombia", lang="es")))
        
        # Estadísticas del dataset
        self.g.add((dataset_uri, self.SCHEMA.numberOfItems, Literal(len(self.df))))
        
        print("Metadatos agregados")
    
    def save_rdf_data(self, filename):
        """Guardar datos RDF en diferentes formatos"""
        print("Guardando datos RDF...")
        
        # RDF/XML
        with open(f"/Users/leomos/Downloads/web_semantica/output/{filename}.rdf", "w", encoding="utf-8") as f:
            f.write(self.g.serialize(format="xml"))
        
        # Turtle
        with open(f"/Users/leomos/Downloads/web_semantica/output/{filename}.ttl", "w", encoding="utf-8") as f:
            f.write(self.g.serialize(format="turtle"))
        
        # N-Triples
        with open(f"/Users/leomos/Downloads/web_semantica/output/{filename}.nt", "w", encoding="utf-8") as f:
            f.write(self.g.serialize(format="nt"))
        
        # JSON-LD
        with open(f"/Users/leomos/Downloads/web_semantica/output/{filename}.jsonld", "w", encoding="utf-8") as f:
            f.write(self.g.serialize(format="json-ld"))
        
        print(f"Datos RDF guardados como {filename}.* en múltiples formatos")
    
    def print_transformation_stats(self):
        """Mostrar estadísticas de la transformación"""
        self.stats['total_triples'] = len(self.g)
        
        print("\n=== ESTADÍSTICAS DE TRANSFORMACIÓN ===")
        print(f"Registros CSV procesados: {len(self.df)}")
        print(f"Estudiantes transformados: {self.stats['students']}")
        print(f"Universidades transformadas: {self.stats['universities']}")
        print(f"Decisiones académicas: {self.stats['decisions']}")
        print(f"Total de triples RDF: {self.stats['total_triples']}")
        
        # Estadísticas por tipo de entidad
        students_count = len(list(self.g.subjects(RDF.type, self.UNIV.Student)))
        universities_count = len(list(self.g.subjects(RDF.type, self.UNIV.University)))
        decisions_count = len(list(self.g.subjects(RDF.type, self.BEHAVIOR.AcademicDecision)))
        areas_count = len(list(self.g.subjects(RDF.type, self.EDU.KnowledgeArea)))
        cities_count = len(list(self.g.subjects(RDF.type, self.GEO.City)))
        departments_count = len(list(self.g.subjects(RDF.type, self.GEO.Department)))
        
        print("\n=== ENTIDADES CREADAS ===")
        print(f"Estudiantes: {students_count}")
        print(f"Universidades: {universities_count}")
        print(f"Decisiones académicas: {decisions_count}")
        print(f"Áreas de conocimiento: {areas_count}")
        print(f"Ciudades: {cities_count}")
        print(f"Departamentos: {departments_count}")

def main():
    """Función principal para transformar datos"""
    print("=== TRANSFORMACIÓN DE DATOS CSV A RDF ===")
    print("Convirtiendo dataset de estudiantes a formato Linked Data\n")
    
    # Inicializar transformador
    transformer = DataTransformer(
        csv_file_path="/Users/leomos/Downloads/web_semantica/ISOFV163_A8_Anexo.csv",
        ontology_file_path="/Users/leomos/Downloads/web_semantica/output/university_ontology.ttl"
    )
    
    # Realizar transformaciones
    transformer.transform_students()
    transformer.transform_universities()
    transformer.transform_academic_decisions()
    transformer.add_metadata()
    
    # Mostrar estadísticas
    transformer.print_transformation_stats()
    
    # Guardar resultados
    transformer.save_rdf_data("university_linked_data")
    
    print("\n=== TRANSFORMACIÓN COMPLETADA ===")
    print("Archivos generados:")
    print("- output/university_linked_data.rdf (RDF/XML)")
    print("- output/university_linked_data.ttl (Turtle)")
    print("- output/university_linked_data.nt (N-Triples)")
    print("- output/university_linked_data.jsonld (JSON-LD)")
    
    return transformer

if __name__ == "__main__":
    data_transformer = main()