#!/usr/bin/env python3
"""
Creación de Ontología RDF - Proyecto Linked Data Universidades
Diseño e implementación de ontología para universidades, estudiantes y patrones de comportamiento
"""

from rdflib import Graph, Namespace, RDF, RDFS, OWL, XSD, URIRef, Literal, BNode
from rdflib.namespace import FOAF, DC, DCTERMS
import csv
import pandas as pd
from datetime import datetime

class UniversityOntologyCreator:
    """Creador de ontología RDF para el dominio universitario"""
    
    def __init__(self):
        """Inicializar namespaces y grafo RDF"""
        self.g = Graph()
        
        # Definir namespaces
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
        self.g.bind("owl", OWL)
        self.g.bind("rdfs", RDFS)
        
        self.create_ontology_schema()
    
    def create_ontology_schema(self):
        """Crear el esquema básico de la ontología"""
        print("Creando esquema de ontología...")
        
        # === CLASES PRINCIPALES ===
        
        # Universidad
        self.g.add((self.UNIV.University, RDF.type, OWL.Class))
        self.g.add((self.UNIV.University, RDFS.label, Literal("Universidad", lang="es")))
        self.g.add((self.UNIV.University, RDFS.comment, 
                   Literal("Institución de educación superior", lang="es")))
        self.g.add((self.UNIV.University, RDFS.subClassOf, self.SCHEMA.EducationalOrganization))
        
        # Estudiante
        self.g.add((self.UNIV.Student, RDF.type, OWL.Class))
        self.g.add((self.UNIV.Student, RDFS.label, Literal("Estudiante", lang="es")))
        self.g.add((self.UNIV.Student, RDFS.comment, 
                   Literal("Persona que estudia en una institución educativa", lang="es")))
        self.g.add((self.UNIV.Student, RDFS.subClassOf, FOAF.Person))
        
        # Programa Académico
        self.g.add((self.EDU.AcademicProgram, RDF.type, OWL.Class))
        self.g.add((self.EDU.AcademicProgram, RDFS.label, Literal("Programa Académico", lang="es")))
        self.g.add((self.EDU.AcademicProgram, RDFS.comment, 
                   Literal("Conjunto estructurado de actividades académicas", lang="es")))
        
        # Área de Conocimiento
        self.g.add((self.EDU.KnowledgeArea, RDF.type, OWL.Class))
        self.g.add((self.EDU.KnowledgeArea, RDFS.label, Literal("Área de Conocimiento", lang="es")))
        self.g.add((self.EDU.KnowledgeArea, RDFS.comment, 
                   Literal("Campo específico del conocimiento", lang="es")))
        
        # Departamento (Geográfico)
        self.g.add((self.GEO.Department, RDF.type, OWL.Class))
        self.g.add((self.GEO.Department, RDFS.label, Literal("Departamento", lang="es")))
        self.g.add((self.GEO.Department, RDFS.comment, 
                   Literal("División administrativa territorial en Colombia", lang="es")))
        self.g.add((self.GEO.Department, RDFS.subClassOf, self.SCHEMA.Place))
        
        # Ciudad
        self.g.add((self.GEO.City, RDF.type, OWL.Class))
        self.g.add((self.GEO.City, RDFS.label, Literal("Ciudad", lang="es")))
        self.g.add((self.GEO.City, RDFS.comment, 
                   Literal("Centro urbano de población", lang="es")))
        self.g.add((self.GEO.City, RDFS.subClassOf, self.SCHEMA.Place))
        
        # Patrón de Comportamiento
        self.g.add((self.BEHAVIOR.BehaviorPattern, RDF.type, OWL.Class))
        self.g.add((self.BEHAVIOR.BehaviorPattern, RDFS.label, Literal("Patrón de Comportamiento", lang="es")))
        self.g.add((self.BEHAVIOR.BehaviorPattern, RDFS.comment, 
                   Literal("Conjunto de decisiones y preferencias observables", lang="es")))
        
        # Decisión Académica
        self.g.add((self.BEHAVIOR.AcademicDecision, RDF.type, OWL.Class))
        self.g.add((self.BEHAVIOR.AcademicDecision, RDFS.label, Literal("Decisión Académica", lang="es")))
        self.g.add((self.BEHAVIOR.AcademicDecision, RDFS.comment, 
                   Literal("Elección realizada por un estudiante respecto a su educación", lang="es")))
        
        # === PROPIEDADES DE OBJETO ===
        
        # Estudiante -> Universidad
        self.g.add((self.UNIV.appliesTo, RDF.type, OWL.ObjectProperty))
        self.g.add((self.UNIV.appliesTo, RDFS.label, Literal("aplica a", lang="es")))
        self.g.add((self.UNIV.appliesTo, RDFS.domain, self.UNIV.Student))
        self.g.add((self.UNIV.appliesTo, RDFS.range, self.UNIV.University))
        
        # Estudiante -> Decisión
        self.g.add((self.BEHAVIOR.makes, RDF.type, OWL.ObjectProperty))
        self.g.add((self.BEHAVIOR.makes, RDFS.label, Literal("realiza", lang="es")))
        self.g.add((self.BEHAVIOR.makes, RDFS.domain, self.UNIV.Student))
        self.g.add((self.BEHAVIOR.makes, RDFS.range, self.BEHAVIOR.AcademicDecision))
        
        # Universidad -> Departamento
        self.g.add((self.GEO.locatedIn, RDF.type, OWL.ObjectProperty))
        self.g.add((self.GEO.locatedIn, RDFS.label, Literal("ubicada en", lang="es")))
        self.g.add((self.GEO.locatedIn, RDFS.domain, self.UNIV.University))
        self.g.add((self.GEO.locatedIn, RDFS.range, self.GEO.Department))
        
        # Estudiante -> Ciudad (origen)
        self.g.add((self.GEO.originFrom, RDF.type, OWL.ObjectProperty))
        self.g.add((self.GEO.originFrom, RDFS.label, Literal("originario de", lang="es")))
        self.g.add((self.GEO.originFrom, RDFS.domain, self.UNIV.Student))
        self.g.add((self.GEO.originFrom, RDFS.range, self.GEO.City))
        
        # Programa -> Área de Conocimiento
        self.g.add((self.EDU.belongsToArea, RDF.type, OWL.ObjectProperty))
        self.g.add((self.EDU.belongsToArea, RDFS.label, Literal("pertenece al área", lang="es")))
        self.g.add((self.EDU.belongsToArea, RDFS.domain, self.EDU.AcademicProgram))
        self.g.add((self.EDU.belongsToArea, RDFS.range, self.EDU.KnowledgeArea))
        
        # Estudiante -> Área (preferencia)
        self.g.add((self.EDU.prefersArea, RDF.type, OWL.ObjectProperty))
        self.g.add((self.EDU.prefersArea, RDFS.label, Literal("prefiere área", lang="es")))
        self.g.add((self.EDU.prefersArea, RDFS.domain, self.UNIV.Student))
        self.g.add((self.EDU.prefersArea, RDFS.range, self.EDU.KnowledgeArea))
        
        # Universidad -> Universidad (tipo de relación)
        self.g.add((self.UNIV.hasType, RDF.type, OWL.ObjectProperty))
        self.g.add((self.UNIV.hasType, RDFS.label, Literal("tiene tipo", lang="es")))
        self.g.add((self.UNIV.hasType, RDFS.domain, self.UNIV.University))
        
        # === PROPIEDADES DE DATOS ===
        
        # Información personal
        self.g.add((self.UNIV.age, RDF.type, OWL.DatatypeProperty))
        self.g.add((self.UNIV.age, RDFS.label, Literal("edad", lang="es")))
        self.g.add((self.UNIV.age, RDFS.domain, self.UNIV.Student))
        self.g.add((self.UNIV.age, RDFS.range, XSD.integer))
        
        self.g.add((self.UNIV.gender, RDF.type, OWL.DatatypeProperty))
        self.g.add((self.UNIV.gender, RDFS.label, Literal("género", lang="es")))
        self.g.add((self.UNIV.gender, RDFS.domain, self.UNIV.Student))
        self.g.add((self.UNIV.gender, RDFS.range, XSD.string))
        
        self.g.add((self.UNIV.socioeconomicStratum, RDF.type, OWL.DatatypeProperty))
        self.g.add((self.UNIV.socioeconomicStratum, RDFS.label, Literal("estrato socioeconómico", lang="es")))
        self.g.add((self.UNIV.socioeconomicStratum, RDFS.domain, self.UNIV.Student))
        self.g.add((self.UNIV.socioeconomicStratum, RDFS.range, XSD.integer))
        
        # Puntuaciones y rankings
        self.g.add((self.EDU.saber11Score, RDF.type, OWL.DatatypeProperty))
        self.g.add((self.EDU.saber11Score, RDFS.label, Literal("puntaje Saber 11", lang="es")))
        self.g.add((self.EDU.saber11Score, RDFS.domain, self.UNIV.Student))
        self.g.add((self.EDU.saber11Score, RDFS.range, XSD.decimal))
        
        self.g.add((self.UNIV.nationalRanking, RDF.type, OWL.DatatypeProperty))
        self.g.add((self.UNIV.nationalRanking, RDFS.label, Literal("ranking nacional", lang="es")))
        self.g.add((self.UNIV.nationalRanking, RDFS.domain, self.UNIV.University))
        self.g.add((self.UNIV.nationalRanking, RDFS.range, XSD.integer))
        
        # Propiedades de universidad
        self.g.add((self.UNIV.isAccredited, RDF.type, OWL.DatatypeProperty))
        self.g.add((self.UNIV.isAccredited, RDFS.label, Literal("está acreditada", lang="es")))
        self.g.add((self.UNIV.isAccredited, RDFS.domain, self.UNIV.University))
        self.g.add((self.UNIV.isAccredited, RDFS.range, XSD.boolean))
        
        # Modalidades y convenios
        self.g.add((self.EDU.programModality, RDF.type, OWL.DatatypeProperty))
        self.g.add((self.EDU.programModality, RDFS.label, Literal("modalidad del programa", lang="es")))
        self.g.add((self.EDU.programModality, RDFS.domain, self.EDU.AcademicProgram))
        self.g.add((self.EDU.programModality, RDFS.range, XSD.string))
        
        self.g.add((self.UNIV.hasInternationalAgreement, RDF.type, OWL.DatatypeProperty))
        self.g.add((self.UNIV.hasInternationalAgreement, RDFS.label, Literal("tiene convenio internacional", lang="es")))
        self.g.add((self.UNIV.hasInternationalAgreement, RDFS.domain, self.UNIV.University))
        self.g.add((self.UNIV.hasInternationalAgreement, RDFS.range, XSD.boolean))
        
        self.g.add((self.UNIV.hasScholarship, RDF.type, OWL.DatatypeProperty))
        self.g.add((self.UNIV.hasScholarship, RDFS.label, Literal("tiene beca disponible", lang="es")))
        self.g.add((self.UNIV.hasScholarship, RDFS.domain, self.UNIV.University))
        self.g.add((self.UNIV.hasScholarship, RDFS.range, XSD.boolean))
        
        # Decisión final
        self.g.add((self.BEHAVIOR.finalDecision, RDF.type, OWL.DatatypeProperty))
        self.g.add((self.BEHAVIOR.finalDecision, RDFS.label, Literal("decisión final", lang="es")))
        self.g.add((self.BEHAVIOR.finalDecision, RDFS.domain, self.BEHAVIOR.AcademicDecision))
        self.g.add((self.BEHAVIOR.finalDecision, RDFS.range, XSD.boolean))
        
        print("Esquema de ontología creado exitosamente.")
    
    def create_knowledge_areas(self):
        """Crear instancias de áreas de conocimiento"""
        areas = ['Salud', 'Artes', 'Ingeniería', 'Ciencias Sociales', 'Administración']
        
        for area in areas:
            area_uri = self.EDU[f"area_{area.replace(' ', '_').lower()}"]
            self.g.add((area_uri, RDF.type, self.EDU.KnowledgeArea))
            self.g.add((area_uri, RDFS.label, Literal(area, lang="es")))
            self.g.add((area_uri, DC.identifier, Literal(area)))
        
        print(f"Creadas {len(areas)} áreas de conocimiento.")
    
    def create_departments_and_cities(self):
        """Crear instancias de departamentos y ciudades"""
        # Departamentos
        departments = ['Valle del Cauca', 'Antioquia', 'Cundinamarca', 'Atlántico', 'Santander']
        for dept in departments:
            dept_uri = self.GEO[f"dept_{dept.replace(' ', '_').lower()}"]
            self.g.add((dept_uri, RDF.type, self.GEO.Department))
            self.g.add((dept_uri, RDFS.label, Literal(dept, lang="es")))
            self.g.add((dept_uri, DC.identifier, Literal(dept)))
        
        # Ciudades
        cities = ['Bucaramanga', 'Medellín', 'Bogotá', 'Barranquilla', 'Cali']
        for city in cities:
            city_uri = self.GEO[f"city_{city.lower()}"]
            self.g.add((city_uri, RDF.type, self.GEO.City))
            self.g.add((city_uri, RDFS.label, Literal(city, lang="es")))
            self.g.add((city_uri, DC.identifier, Literal(city)))
        
        print(f"Creados {len(departments)} departamentos y {len(cities)} ciudades.")
    
    def create_universities(self):
        """Crear instancias de universidades"""
        universities_data = [
            ('U001', 'Universidad Nacional', 'Cundinamarca', 'Pública', True, 1),
            ('U002', 'Universidad de los Andes', 'Cundinamarca', 'Privada', True, 2),
            ('U003', 'Universidad del Valle', 'Valle del Cauca', 'Pública', True, 10),
            ('U004', 'Universidad de Antioquia', 'Antioquia', 'Pública', True, 5),
            ('U005', 'Universidad Autónoma', 'Atlántico', 'Privada', False, 30)
        ]
        
        for code, name, dept, tipo, accredited, ranking in universities_data:
            univ_uri = self.UNIV[f"university_{code.lower()}"]
            dept_uri = self.GEO[f"dept_{dept.replace(' ', '_').lower()}"]
            
            # Información básica
            self.g.add((univ_uri, RDF.type, self.UNIV.University))
            self.g.add((univ_uri, RDFS.label, Literal(name, lang="es")))
            self.g.add((univ_uri, DC.identifier, Literal(code)))
            self.g.add((univ_uri, DC.title, Literal(name, lang="es")))
            
            # Propiedades específicas
            self.g.add((univ_uri, self.GEO.locatedIn, dept_uri))
            self.g.add((univ_uri, self.UNIV.hasType, Literal(tipo, lang="es")))
            self.g.add((univ_uri, self.UNIV.isAccredited, Literal(accredited)))
            self.g.add((univ_uri, self.UNIV.nationalRanking, Literal(ranking)))
        
        print(f"Creadas {len(universities_data)} universidades.")
    
    def save_ontology(self, filename):
        """Guardar la ontología en diferentes formatos"""
        # RDF/XML
        with open(f"/Users/leomos/Downloads/web_semantica/output/{filename}.rdf", "w", encoding="utf-8") as f:
            f.write(self.g.serialize(format="xml"))
        
        # Turtle
        with open(f"/Users/leomos/Downloads/web_semantica/output/{filename}.ttl", "w", encoding="utf-8") as f:
            f.write(self.g.serialize(format="turtle"))
        
        # N-Triples
        with open(f"/Users/leomos/Downloads/web_semantica/output/{filename}.nt", "w", encoding="utf-8") as f:
            f.write(self.g.serialize(format="nt"))
        
        print(f"Ontología guardada en formatos RDF/XML, Turtle y N-Triples como {filename}.*")
    
    def print_ontology_stats(self):
        """Mostrar estadísticas de la ontología"""
        total_triples = len(self.g)
        classes = len(list(self.g.subjects(RDF.type, OWL.Class)))
        object_properties = len(list(self.g.subjects(RDF.type, OWL.ObjectProperty)))
        datatype_properties = len(list(self.g.subjects(RDF.type, OWL.DatatypeProperty)))
        
        print("\n=== ESTADÍSTICAS DE LA ONTOLOGÍA ===")
        print(f"Total de triples: {total_triples}")
        print(f"Clases definidas: {classes}")
        print(f"Propiedades de objeto: {object_properties}")
        print(f"Propiedades de datos: {datatype_properties}")
        
        # Listar clases principales
        print("\nClases principales:")
        for s in self.g.subjects(RDF.type, OWL.Class):
            label = self.g.value(s, RDFS.label)
            if label:
                print(f"- {label}")
    
    def create_documentation(self):
        """Crear documentación de la ontología"""
        doc = f"""# Ontología del Dominio Universitario
## Proyecto Linked Data - Análisis de Patrones de Comportamiento Estudiantil

### Descripción
Esta ontología modela el dominio universitario incluyendo universidades, estudiantes, 
programas académicos y patrones de comportamiento en la selección universitaria.

### Namespaces Utilizados
- univ: http://example.org/university/
- edu: http://example.org/education/
- geo: http://example.org/geography/
- behavior: http://example.org/behavior/
- schema: http://schema.org/
- foaf: http://xmlns.com/foaf/0.1/

### Clases Principales
1. **Universidad (univ:University)**: Institución de educación superior
2. **Estudiante (univ:Student)**: Persona que estudia o aplica a una universidad
3. **Programa Académico (edu:AcademicProgram)**: Conjunto estructurado de actividades académicas
4. **Área de Conocimiento (edu:KnowledgeArea)**: Campo específico del conocimiento
5. **Departamento (geo:Department)**: División administrativa territorial
6. **Ciudad (geo:City)**: Centro urbano de población
7. **Patrón de Comportamiento (behavior:BehaviorPattern)**: Conjunto de decisiones observables
8. **Decisión Académica (behavior:AcademicDecision)**: Elección educativa de un estudiante

### Propiedades de Objeto Principales
- univ:appliesTo: Relaciona estudiante con universidad
- behavior:makes: Relaciona estudiante con decisión académica
- geo:locatedIn: Relaciona universidad con departamento
- geo:originFrom: Relaciona estudiante con ciudad de origen
- edu:prefersArea: Relaciona estudiante con área de preferencia

### Propiedades de Datos Principales
- univ:age: Edad del estudiante
- univ:gender: Género del estudiante
- univ:socioeconomicStratum: Estrato socioeconómico
- edu:saber11Score: Puntaje en pruebas Saber 11
- univ:nationalRanking: Ranking nacional de la universidad
- behavior:finalDecision: Decisión final del estudiante

### Vocabularios Estándar Utilizados
- **FOAF (Friend of a Friend)**: Para información personal de estudiantes
- **Dublin Core**: Para metadatos básicos
- **Schema.org**: Para estructuras organizacionales y educativas
- **OWL**: Para definiciones ontológicas

### Patrones de Diseño Aplicados
1. **Separación de conceptos**: Diferentes namespaces para diferentes dominios
2. **Reutilización de vocabularios**: Uso de estándares existentes
3. **Jerarquías de clases**: Herencia desde clases más generales
4. **Propiedades tipadas**: Uso correcto de tipos de datos XSD

Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        with open("/Users/leomos/Downloads/web_semantica/output/ontology_documentation.md", "w", encoding="utf-8") as f:
            f.write(doc)
        
        print("Documentación de la ontología creada en: output/ontology_documentation.md")

def main():
    """Función principal para crear la ontología"""
    print("=== CREACIÓN DE ONTOLOGÍA RDF - PROYECTO LINKED DATA ===")
    print("Diseñando ontología para el dominio universitario y patrones de comportamiento\n")
    
    # Crear ontología
    creator = UniversityOntologyCreator()
    
    # Crear instancias básicas
    creator.create_knowledge_areas()
    creator.create_departments_and_cities()
    creator.create_universities()
    
    # Mostrar estadísticas
    creator.print_ontology_stats()
    
    # Guardar ontología
    creator.save_ontology("university_ontology")
    
    # Crear documentación
    creator.create_documentation()
    
    print("\n=== ONTOLOGÍA CREADA EXITOSAMENTE ===")
    print("Archivos generados:")
    print("- output/university_ontology.rdf (RDF/XML)")
    print("- output/university_ontology.ttl (Turtle)")
    print("- output/university_ontology.nt (N-Triples)")
    print("- output/ontology_documentation.md (Documentación)")
    
    return creator

if __name__ == "__main__":
    ontology_creator = main()