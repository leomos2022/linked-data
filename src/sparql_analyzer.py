#!/usr/bin/env python3
"""
Análisis de Patrones con SPARQL - Proyecto Linked Data Universidades
Consultas SPARQL para identificar patrones de comportamiento estudiantil
"""

from rdflib import Graph, Namespace
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json

class SPARQLPatternAnalyzer:
    """Analizador de patrones de comportamiento usando consultas SPARQL"""
    
    def __init__(self, rdf_file_path):
        """Inicializar con archivo RDF"""
        self.rdf_path = rdf_file_path
        self.g = Graph()
        
        # Definir namespaces
        self.UNIV = Namespace("http://example.org/university/")
        self.SCHEMA = Namespace("http://schema.org/")
        self.EDU = Namespace("http://example.org/education/")
        self.GEO = Namespace("http://example.org/geography/")
        self.BEHAVIOR = Namespace("http://example.org/behavior/")
        
        # Cargar datos RDF
        self.load_rdf_data()
        
        # Almacenar resultados de consultas
        self.query_results = {}
    
    def load_rdf_data(self):
        """Cargar datos RDF"""
        try:
            self.g.parse(self.rdf_path, format="turtle")
            print(f"Datos RDF cargados exitosamente: {len(self.g)} triples")
        except Exception as e:
            print(f"Error al cargar datos RDF: {e}")
    
    def execute_sparql_query(self, query_name, query, description):
        """Ejecutar consulta SPARQL y almacenar resultados"""
        print(f"\n=== {query_name.upper()} ===")
        print(f"Descripción: {description}")
        print(f"Consulta SPARQL:")
        print(query)
        print("\nResultados:")
        
        try:
            results = self.g.query(query)
            result_list = []
            
            for row in results:
                result_dict = {}
                for i, var in enumerate(results.vars):
                    result_dict[str(var)] = str(row[i]) if row[i] else None
                result_list.append(result_dict)
                
                # Mostrar resultado
                formatted_row = " | ".join([f"{var}: {row[i]}" for i, var in enumerate(results.vars)])
                print(f"  {formatted_row}")
            
            # Almacenar resultados
            self.query_results[query_name] = {
                'description': description,
                'query': query,
                'results': result_list,
                'count': len(result_list)
            }
            
            print(f"Total de resultados: {len(result_list)}")
            return result_list
            
        except Exception as e:
            print(f"Error ejecutando consulta: {e}")
            return []
    
    def analyze_university_popularity(self):
        """Analizar popularidad de universidades"""
        query = """
        PREFIX univ: <http://example.org/university/>
        PREFIX dc: <http://purl.org/dc/elements/1.1/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT ?universidad ?nombre (COUNT(?estudiante) AS ?aplicaciones)
        WHERE {
            ?estudiante univ:appliesTo ?universidad .
            ?universidad dc:title ?nombre .
        }
        GROUP BY ?universidad ?nombre
        ORDER BY DESC(?aplicaciones)
        """
        
        return self.execute_sparql_query(
            "popularidad_universidades",
            query,
            "Número de aplicaciones por universidad (popularidad)"
        )
    
    def analyze_area_preferences(self):
        """Analizar preferencias por área de conocimiento"""
        query = """
        PREFIX edu: <http://example.org/education/>
        PREFIX dc: <http://purl.org/dc/elements/1.1/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT ?area ?nombre (COUNT(?estudiante) AS ?estudiantes)
        WHERE {
            ?estudiante edu:prefersArea ?area .
            ?area dc:identifier ?nombre .
        }
        GROUP BY ?area ?nombre
        ORDER BY DESC(?estudiantes)
        """
        
        return self.execute_sparql_query(
            "preferencias_area",
            query,
            "Distribución de estudiantes por área de preferencia"
        )
    
    def analyze_geographic_migration(self):
        """Analizar migración académica geográfica"""
        query = """
        PREFIX geo: <http://example.org/geography/>
        PREFIX univ: <http://example.org/university/>
        PREFIX dc: <http://purl.org/dc/elements/1.1/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT ?ciudad_origen ?dept_destino (COUNT(?estudiante) AS ?flujo)
        WHERE {
            ?estudiante geo:originFrom ?ciudad .
            ?ciudad dc:identifier ?ciudad_origen .
            ?estudiante univ:appliesTo ?universidad .
            ?universidad geo:locatedIn ?departamento .
            ?departamento dc:identifier ?dept_destino .
        }
        GROUP BY ?ciudad_origen ?dept_destino
        HAVING (COUNT(?estudiante) > 50)
        ORDER BY DESC(?flujo)
        """
        
        return self.execute_sparql_query(
            "migracion_geografica",
            query,
            "Flujos de migración académica (ciudad origen → departamento destino)"
        )
    
    def analyze_decision_patterns_by_stratum(self):
        """Analizar patrones de decisión por estrato socioeconómico"""
        query = """
        PREFIX univ: <http://example.org/university/>
        PREFIX behavior: <http://example.org/behavior/>
        
        SELECT ?estrato ?tipo_universidad 
               (COUNT(?decision) AS ?decisiones)
               (SUM(IF(?final_decision, 1, 0)) AS ?decisiones_positivas)
        WHERE {
            ?estudiante univ:socioeconomicStratum ?estrato .
            ?estudiante behavior:makes ?decision .
            ?decision behavior:finalDecision ?final_decision .
            ?estudiante univ:appliesTo ?universidad .
            ?universidad univ:hasType ?tipo_universidad .
        }
        GROUP BY ?estrato ?tipo_universidad
        ORDER BY ?estrato ?tipo_universidad
        """
        
        return self.execute_sparql_query(
            "decisiones_por_estrato",
            query,
            "Patrones de decisión por estrato socioeconómico y tipo de universidad"
        )
    
    def analyze_modality_preferences(self):
        """Analizar preferencias por modalidad de programa"""
        query = """
        PREFIX edu: <http://example.org/education/>
        PREFIX behavior: <http://example.org/behavior/>
        
        SELECT ?modalidad (COUNT(?decision) AS ?decisiones)
               (AVG(IF(?final_decision, 1.0, 0.0)) AS ?tasa_aceptacion)
        WHERE {
            ?decision edu:programModality ?modalidad .
            ?decision behavior:finalDecision ?final_decision .
        }
        GROUP BY ?modalidad
        ORDER BY DESC(?decisiones)
        """
        
        return self.execute_sparql_query(
            "preferencias_modalidad",
            query,
            "Preferencias por modalidad de programa y tasa de aceptación"
        )
    
    def analyze_high_performers(self):
        """Analizar estudiantes de alto rendimiento"""
        query = """
        PREFIX edu: <http://example.org/education/>
        PREFIX univ: <http://example.org/university/>
        PREFIX geo: <http://example.org/geography/>
        PREFIX dc: <http://purl.org/dc/elements/1.1/>
        
        SELECT ?puntaje ?area_pref ?universidad ?ranking
        WHERE {
            ?estudiante edu:saber11Score ?puntaje .
            ?estudiante edu:prefersArea ?area .
            ?area dc:identifier ?area_pref .
            ?estudiante univ:appliesTo ?universidad .
            ?universidad univ:nationalRanking ?ranking .
            FILTER(?puntaje > 350)
        }
        ORDER BY DESC(?puntaje)
        LIMIT 20
        """
        
        return self.execute_sparql_query(
            "alto_rendimiento",
            query,
            "Estudiantes de alto rendimiento (puntaje > 350) y sus elecciones"
        )
    
    def analyze_scholarship_impact(self):
        """Analizar impacto de becas en decisiones"""
        query = """
        PREFIX univ: <http://example.org/university/>
        PREFIX behavior: <http://example.org/behavior/>
        PREFIX dc: <http://purl.org/dc/elements/1.1/>
        
        SELECT ?tiene_beca ?universidad_nombre
               (COUNT(?decision) AS ?aplicaciones)
               (AVG(IF(?final_decision, 1.0, 0.0)) AS ?tasa_eleccion)
        WHERE {
            ?estudiante univ:appliesTo ?universidad .
            ?universidad univ:hasScholarship ?tiene_beca .
            ?universidad dc:title ?universidad_nombre .
            ?estudiante behavior:makes ?decision .
            ?decision behavior:finalDecision ?final_decision .
        }
        GROUP BY ?tiene_beca ?universidad_nombre
        ORDER BY ?tiene_beca DESC(?tasa_eleccion)
        """
        
        return self.execute_sparql_query(
            "impacto_becas",
            query,
            "Impacto de disponibilidad de becas en las decisiones estudiantiles"
        )
    
    def analyze_gender_patterns(self):
        """Analizar patrones por género"""
        query = """
        PREFIX univ: <http://example.org/university/>
        PREFIX edu: <http://example.org/education/>
        PREFIX dc: <http://purl.org/dc/elements/1.1/>
        
        SELECT ?genero ?area_pref (COUNT(?estudiante) AS ?estudiantes)
        WHERE {
            ?estudiante univ:gender ?genero .
            ?estudiante edu:prefersArea ?area .
            ?area dc:identifier ?area_pref .
        }
        GROUP BY ?genero ?area_pref
        ORDER BY ?genero DESC(?estudiantes)
        """
        
        return self.execute_sparql_query(
            "patrones_genero",
            query,
            "Distribución de preferencias académicas por género"
        )
    
    def analyze_accreditation_preference(self):
        """Analizar preferencia por universidades acreditadas"""
        query = """
        PREFIX univ: <http://example.org/university/>
        PREFIX behavior: <http://example.org/behavior/>
        
        SELECT ?acreditada 
               (COUNT(?aplicacion) AS ?aplicaciones)
               (AVG(IF(?final_decision, 1.0, 0.0)) AS ?tasa_eleccion)
        WHERE {
            ?estudiante univ:appliesTo ?universidad .
            ?universidad univ:isAccredited ?acreditada .
            ?estudiante behavior:makes ?decision .
            ?decision behavior:finalDecision ?final_decision .
        }
        GROUP BY ?acreditada
        """
        
        return self.execute_sparql_query(
            "preferencia_acreditacion",
            query,
            "Preferencia por universidades acreditadas vs no acreditadas"
        )
    
    def create_pattern_visualizations(self):
        """Crear visualizaciones de los patrones encontrados"""
        print("\n=== CREANDO VISUALIZACIONES DE PATRONES ===")
        
        # Configurar subplot principal
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Popularidad de Universidades', 
                          'Preferencias por Área',
                          'Preferencias por Modalidad',
                          'Impacto de Becas'),
            specs=[[{"type": "bar"}, {"type": "pie"}],
                   [{"type": "bar"}, {"type": "bar"}]]
        )
        
        # Gráfico 1: Popularidad de universidades
        if 'popularidad_universidades' in self.query_results:
            data = self.query_results['popularidad_universidades']['results']
            nombres = [row['nombre'] for row in data]
            aplicaciones = [int(row['aplicaciones']) for row in data]
            
            fig.add_trace(go.Bar(
                x=nombres, y=aplicaciones, name="Aplicaciones",
                marker_color='lightblue'
            ), row=1, col=1)
        
        # Gráfico 2: Preferencias por área
        if 'preferencias_area' in self.query_results:
            data = self.query_results['preferencias_area']['results']
            areas = [row['nombre'] for row in data]
            estudiantes = [int(row['estudiantes']) for row in data]
            
            fig.add_trace(go.Pie(
                labels=areas, values=estudiantes, name="Área"
            ), row=1, col=2)
        
        # Gráfico 3: Preferencias por modalidad
        if 'preferencias_modalidad' in self.query_results:
            data = self.query_results['preferencias_modalidad']['results']
            modalidades = [row['modalidad'] for row in data]
            decisiones = [int(row['decisiones']) for row in data]
            
            fig.add_trace(go.Bar(
                x=modalidades, y=decisiones, name="Decisiones",
                marker_color='lightgreen'
            ), row=2, col=1)
        
        # Gráfico 4: Impacto de becas
        if 'impacto_becas' in self.query_results:
            data = self.query_results['impacto_becas']['results']
            # Agrupar por disponibilidad de beca
            con_beca = [row for row in data if row['tiene_beca'] == 'true']
            sin_beca = [row for row in data if row['tiene_beca'] == 'false']
            
            categorias = ['Con Beca', 'Sin Beca']
            tasas = [
                sum(float(row['tasa_eleccion']) for row in con_beca) / len(con_beca) if con_beca else 0,
                sum(float(row['tasa_eleccion']) for row in sin_beca) / len(sin_beca) if sin_beca else 0
            ]
            
            fig.add_trace(go.Bar(
                x=categorias, y=tasas, name="Tasa Elección",
                marker_color='orange'
            ), row=2, col=2)
        
        fig.update_layout(height=800, showlegend=False, 
                         title_text="Análisis de Patrones de Comportamiento con SPARQL")
        
        # Guardar visualización principal
        fig.write_html("/Users/leomos/Downloads/web_semantica/visualizations/sparql_patterns.html")
        print("Visualización principal guardada en: visualizations/sparql_patterns.html")
        
        # Crear visualización de migración geográfica
        if 'migracion_geografica' in self.query_results:
            self.create_migration_visualization()
    
    def create_migration_visualization(self):
        """Crear visualización específica de migración académica"""
        data = self.query_results['migracion_geografica']['results']
        
        # Preparar datos para sankey diagram
        origins = list(set([row['ciudad_origen'] for row in data]))
        destinations = list(set([row['dept_destino'] for row in data]))
        
        # Crear mapeo de índices
        all_nodes = origins + destinations
        node_indices = {node: i for i, node in enumerate(all_nodes)}
        
        # Preparar enlaces
        source_indices = [node_indices[row['ciudad_origen']] for row in data]
        target_indices = [node_indices[row['dept_destino']] + len(origins) for row in data]
        values = [int(row['flujo']) for row in data]
        
        # Crear diagrama Sankey
        fig_sankey = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=all_nodes,
                color="blue"
            ),
            link=dict(
                source=source_indices,
                target=target_indices,
                value=values
            )
        )])
        
        fig_sankey.update_layout(
            title_text="Flujos de Migración Académica (Ciudad Origen → Departamento Universidad)",
            font_size=10
        )
        
        fig_sankey.write_html("/Users/leomos/Downloads/web_semantica/visualizations/migracion_sankey.html")
        print("Diagrama Sankey de migración guardado en: visualizations/migracion_sankey.html")
    
    def save_results_summary(self):
        """Guardar resumen de resultados en JSON"""
        summary = {
            'timestamp': pd.Timestamp.now().isoformat(),
            'total_queries': len(self.query_results),
            'total_triples': len(self.g),
            'insights': {},
            'queries': self.query_results
        }
        
        # Generar insights clave
        if 'popularidad_universidades' in self.query_results:
            pop_data = self.query_results['popularidad_universidades']['results']
            summary['insights']['universidad_mas_popular'] = pop_data[0]['nombre'] if pop_data else None
        
        if 'preferencias_area' in self.query_results:
            area_data = self.query_results['preferencias_area']['results']
            summary['insights']['area_mas_popular'] = area_data[0]['nombre'] if area_data else None
        
        if 'alto_rendimiento' in self.query_results:
            perf_data = self.query_results['alto_rendimiento']['results']
            summary['insights']['mejor_puntaje'] = float(perf_data[0]['puntaje']) if perf_data else None
        
        # Guardar en archivo JSON
        with open("/Users/leomos/Downloads/web_semantica/output/sparql_analysis_results.json", "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print("Resumen de resultados guardado en: output/sparql_analysis_results.json")
        return summary

def main():
    """Función principal para análisis SPARQL"""
    print("=== ANÁLISIS DE PATRONES CON SPARQL ===")
    print("Identificando patrones de comportamiento estudiantil mediante consultas semánticas\n")
    
    # Inicializar analizador
    analyzer = SPARQLPatternAnalyzer(
        "/Users/leomos/Downloads/web_semantica/output/university_linked_data.ttl"
    )
    
    # Ejecutar consultas de análisis
    print("Ejecutando consultas SPARQL para identificar patrones...")
    
    analyzer.analyze_university_popularity()
    analyzer.analyze_area_preferences()
    analyzer.analyze_geographic_migration()
    analyzer.analyze_decision_patterns_by_stratum()
    analyzer.analyze_modality_preferences()
    analyzer.analyze_high_performers()
    analyzer.analyze_scholarship_impact()
    analyzer.analyze_gender_patterns()
    analyzer.analyze_accreditation_preference()
    
    # Crear visualizaciones
    analyzer.create_pattern_visualizations()
    
    # Guardar resumen
    summary = analyzer.save_results_summary()
    
    print(f"\n=== ANÁLISIS SPARQL COMPLETADO ===")
    print(f"Total de consultas ejecutadas: {len(analyzer.query_results)}")
    print(f"Total de triples analizados: {len(analyzer.g)}")
    print("\nArchivos generados:")
    print("- visualizations/sparql_patterns.html")
    print("- visualizations/migracion_sankey.html")
    print("- output/sparql_analysis_results.json")
    
    return analyzer, summary

if __name__ == "__main__":
    analyzer, summary = main()