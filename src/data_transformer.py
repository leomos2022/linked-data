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
            decision_uri = self.create_decision_uri(row['id_estudiante'], 
                                                   row['universidad_codigo'])
            
            # Tipo de entidad
            self.g.add((decision_uri, RDF.type, self.BEHAVIOR.AcademicDecision))
            
            # Relación estudiante -> decisión
            self.g.add((student_uri, self.BEHAVIOR.makes, decision_uri))\n            \n            # Información de la decisión\n            self.g.add((decision_uri, RDFS.label, \n                       Literal(f\"Decisión de {row['id_estudiante']} sobre {row['universidad_codigo']}\", lang=\"es\")))\n            \n            # Decisión final\n            if not pd.isna(row['eligio_universidad']):\n                final_decision = self.convert_boolean(row['eligio_universidad'])\n                self.g.add((decision_uri, self.BEHAVIOR.finalDecision, \n                           Literal(final_decision)))\n            \n            # Modalidad del programa\n            if not pd.isna(row['modalidad_programa']):\n                self.g.add((decision_uri, self.EDU.programModality, \n                           Literal(row['modalidad_programa'], lang=\"es\")))\n            \n            # Convenio internacional\n            if not pd.isna(row['convenio_internacional']):\n                has_agreement = self.convert_boolean(row['convenio_internacional'])\n                self.g.add((university_uri, self.UNIV.hasInternationalAgreement, \n                           Literal(has_agreement)))\n            \n            # Beca disponible\n            if not pd.isna(row['beca_disponible']):\n                has_scholarship = self.convert_boolean(row['beca_disponible'])\n                self.g.add((university_uri, self.UNIV.hasScholarship, \n                           Literal(has_scholarship)))\n            \n            # Relacionar decisión con universidad\n            self.g.add((decision_uri, DC.subject, university_uri))\n            \n            # Timestamp de creación\n            self.g.add((decision_uri, DCTERMS.created, \n                       Literal(datetime.now().isoformat(), datatype=XSD.dateTime)))\n            \n            self.stats['decisions'] += 1\n        \n        print(f\"Transformadas {self.stats['decisions']} decisiones académicas\")\n    \n    def add_metadata(self):\n        \"\"\"Agregar metadatos al dataset\"\"\"\n        print(\"Agregando metadatos del dataset...\")\n        \n        # URI del dataset\n        dataset_uri = self.UNIV[\"dataset_university_choices\"]\n        \n        # Información del dataset\n        self.g.add((dataset_uri, RDF.type, self.SCHEMA.Dataset))\n        self.g.add((dataset_uri, DC.title, \n                   Literal(\"Dataset de Decisiones Universitarias Colombia\", lang=\"es\")))\n        self.g.add((dataset_uri, DC.description, \n                   Literal(\"Datos sobre patrones de comportamiento estudiantil en la selección de universidades en Colombia\", lang=\"es\")))\n        self.g.add((dataset_uri, DCTERMS.created, \n                   Literal(datetime.now().isoformat(), datatype=XSD.dateTime)))\n        self.g.add((dataset_uri, DC.creator, \n                   Literal(\"Proyecto Linked Data - Web Semántica\", lang=\"es\")))\n        self.g.add((dataset_uri, DC.language, Literal(\"es\")))\n        self.g.add((dataset_uri, DCTERMS.spatial, \n                   Literal(\"Colombia\", lang=\"es\")))\n        \n        # Estadísticas del dataset\n        self.g.add((dataset_uri, self.SCHEMA.numberOfItems, \n                   Literal(len(self.df))))\n        \n        print(\"Metadatos agregados\")\n    \n    def generate_sample_triples(self, n=10):\n        \"\"\"Generar muestra de triples para revisión\"\"\"\n        print(f\"\\n=== MUESTRA DE {n} TRIPLES GENERADOS ===\")\n        count = 0\n        for s, p, o in self.g:\n            if count >= n:\n                break\n            print(f\"{s} {p} {o}\")\n            count += 1\n    \n    def save_rdf_data(self, filename):\n        \"\"\"Guardar datos RDF en diferentes formatos\"\"\"\n        print(\"Guardando datos RDF...\")\n        \n        # RDF/XML\n        with open(f\"/Users/leomos/Downloads/web_semantica/output/{filename}.rdf\", \"w\", encoding=\"utf-8\") as f:\n            f.write(self.g.serialize(format=\"xml\"))\n        \n        # Turtle\n        with open(f\"/Users/leomos/Downloads/web_semantica/output/{filename}.ttl\", \"w\", encoding=\"utf-8\") as f:\n            f.write(self.g.serialize(format=\"turtle\"))\n        \n        # N-Triples\n        with open(f\"/Users/leomos/Downloads/web_semantica/output/{filename}.nt\", \"w\", encoding=\"utf-8\") as f:\n            f.write(self.g.serialize(format=\"nt\"))\n        \n        # JSON-LD\n        with open(f\"/Users/leomos/Downloads/web_semantica/output/{filename}.jsonld\", \"w\", encoding=\"utf-8\") as f:\n            f.write(self.g.serialize(format=\"json-ld\"))\n        \n        print(f\"Datos RDF guardados como {filename}.* en múltiples formatos\")\n    \n    def print_transformation_stats(self):\n        \"\"\"Mostrar estadísticas de la transformación\"\"\"\n        self.stats['total_triples'] = len(self.g)\n        \n        print(\"\\n=== ESTADÍSTICAS DE TRANSFORMACIÓN ===\")\n        print(f\"Registros CSV procesados: {len(self.df)}\")\n        print(f\"Estudiantes transformados: {self.stats['students']}\")\n        print(f\"Universidades transformadas: {self.stats['universities']}\")\n        print(f\"Decisiones académicas: {self.stats['decisions']}\")\n        print(f\"Total de triples RDF: {self.stats['total_triples']}\")\n        \n        # Estadísticas por tipo de entidad\n        students_count = len(list(self.g.subjects(RDF.type, self.UNIV.Student)))\n        universities_count = len(list(self.g.subjects(RDF.type, self.UNIV.University)))\n        decisions_count = len(list(self.g.subjects(RDF.type, self.BEHAVIOR.AcademicDecision)))\n        areas_count = len(list(self.g.subjects(RDF.type, self.EDU.KnowledgeArea)))\n        cities_count = len(list(self.g.subjects(RDF.type, self.GEO.City)))\n        departments_count = len(list(self.g.subjects(RDF.type, self.GEO.Department)))\n        \n        print(\"\\n=== ENTIDADES CREADAS ===\")\n        print(f\"Estudiantes: {students_count}\")\n        print(f\"Universidades: {universities_count}\")\n        print(f\"Decisiones académicas: {decisions_count}\")\n        print(f\"Áreas de conocimiento: {areas_count}\")\n        print(f\"Ciudades: {cities_count}\")\n        print(f\"Departamentos: {departments_count}\")\n    \n    def validate_data_quality(self):\n        \"\"\"Validar calidad de los datos transformados\"\"\"\n        print(\"\\n=== VALIDACIÓN DE CALIDAD DE DATOS ===\")\n        \n        # Verificar que cada estudiante tenga al menos una aplicación\n        students_with_applications = set()\n        for s, p, o in self.g.triples((None, self.UNIV.appliesTo, None)):\n            students_with_applications.add(s)\n        \n        total_students = len(list(self.g.subjects(RDF.type, self.UNIV.Student)))\n        print(f\"Estudiantes con aplicaciones: {len(students_with_applications)}/{total_students}\")\n        \n        # Verificar que cada decisión tenga un resultado\n        decisions_with_result = 0\n        total_decisions = 0\n        for s, p, o in self.g.triples((None, RDF.type, self.BEHAVIOR.AcademicDecision)):\n            total_decisions += 1\n            if (s, self.BEHAVIOR.finalDecision, None) in self.g:\n                decisions_with_result += 1\n        \n        print(f\"Decisiones con resultado: {decisions_with_result}/{total_decisions}\")\n        \n        # Verificar integridad referencial\n        orphaned_decisions = 0\n        for s, p, o in self.g.triples((None, RDF.type, self.BEHAVIOR.AcademicDecision)):\n            # Verificar que la decisión esté vinculada a un estudiante\n            if not any(self.g.triples((None, self.BEHAVIOR.makes, s))):\n                orphaned_decisions += 1\n        \n        print(f\"Decisiones huérfanas (sin estudiante): {orphaned_decisions}\")\n        \n        if orphaned_decisions == 0 and decisions_with_result == total_decisions:\n            print(\"✓ Validación de calidad exitosa\")\n        else:\n            print(\"⚠ Se encontraron problemas de calidad de datos\")\n\ndef main():\n    \"\"\"Función principal para transformar datos\"\"\"\n    print(\"=== TRANSFORMACIÓN DE DATOS CSV A RDF ===\")\n    print(\"Convirtiendo dataset de estudiantes a formato Linked Data\\n\")\n    \n    # Inicializar transformador\n    transformer = DataTransformer(\n        csv_file_path=\"/Users/leomos/Downloads/web_semantica/ISOFV163_A8_Anexo.csv\",\n        ontology_file_path=\"/Users/leomos/Downloads/web_semantica/output/university_ontology.ttl\"\n    )\n    \n    # Realizar transformaciones\n    transformer.transform_students()\n    transformer.transform_universities()\n    transformer.transform_academic_decisions()\n    transformer.add_metadata()\n    \n    # Mostrar estadísticas\n    transformer.print_transformation_stats()\n    \n    # Validar calidad\n    transformer.validate_data_quality()\n    \n    # Generar muestra\n    transformer.generate_sample_triples()\n    \n    # Guardar resultados\n    transformer.save_rdf_data(\"university_linked_data\")\n    \n    print(\"\\n=== TRANSFORMACIÓN COMPLETADA ===\")\n    print(\"Archivos generados:\")\n    print(\"- output/university_linked_data.rdf (RDF/XML)\")\n    print(\"- output/university_linked_data.ttl (Turtle)\")\n    print(\"- output/university_linked_data.nt (N-Triples)\")\n    print(\"- output/university_linked_data.jsonld (JSON-LD)\")\n    \n    return transformer\n\nif __name__ == \"__main__\":\n    data_transformer = main()