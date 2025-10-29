#!/usr/bin/env python3
"""
Análisis Exploratorio de Datos - Proyecto Linked Data Universidades
Análisis de patrones de comportamiento estudiantil en la selección universitaria
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Configuración de estilo
plt.style.use('default')
sns.set_palette("husl")

class UniversityDataAnalyzer:
    """Analizador de datos de estudiantes y universidades"""
    
    def __init__(self, csv_file_path):
        """Inicializar con el archivo CSV"""
        self.csv_path = csv_file_path
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Cargar y limpiar los datos"""
        try:
            self.df = pd.read_csv(self.csv_path)
            print(f"Dataset cargado exitosamente: {len(self.df)} registros")
            print(f"Columnas: {list(self.df.columns)}")
            
            # Información básica del dataset
            print("\n=== INFORMACIÓN BÁSICA DEL DATASET ===")
            print(self.df.info())
            print("\n=== ESTADÍSTICAS DESCRIPTIVAS ===")
            print(self.df.describe())
            
        except Exception as e:
            print(f"Error al cargar el dataset: {e}")
    
    def analyze_universities(self):
        """Análisis de universidades y distribución"""
        print("\n=== ANÁLISIS DE UNIVERSIDADES ===")
        
        # Universidades únicas
        universities = self.df.groupby(['universidad_codigo', 'universidad_nombre', 
                                      'universidad_departamento', 'universidad_tipo']).size().reset_index(name='estudiantes')
        print(f"Total de universidades en el dataset: {len(universities)}")
        print("\nUniversidades ordenadas por número de estudiantes:")
        universities_sorted = universities.sort_values('estudiantes', ascending=False)
        for _, row in universities_sorted.iterrows():
            print(f"- {row['universidad_nombre']} ({row['universidad_tipo']}, {row['universidad_departamento']}): {row['estudiantes']} estudiantes")
        
        return universities_sorted
    
    def analyze_behavioral_patterns(self):
        """Análisis de patrones de comportamiento estudiantil"""
        print("\n=== ANÁLISIS DE PATRONES DE COMPORTAMIENTO ===")
        
        # 1. Distribución por área de preferencia
        pref_area = self.df['preferencia_area'].value_counts()
        print("\nDistribución por área de preferencia:")
        for area, count in pref_area.items():
            pct = (count/len(self.df))*100
            print(f"- {area}: {count} estudiantes ({pct:.1f}%)")
        
        # 2. Modalidad de programa
        modalidad = self.df['modalidad_programa'].value_counts()
        print("\nDistribución por modalidad de programa:")
        for mod, count in modalidad.items():
            pct = (count/len(self.df))*100
            print(f"- {mod}: {count} estudiantes ({pct:.1f}%)")
        
        # 3. Tipo de universidad (pública vs privada)
        tipo_univ = self.df['universidad_tipo'].value_counts()
        print("\nPreferencia por tipo de universidad:")
        for tipo, count in tipo_univ.items():
            pct = (count/len(self.df))*100
            print(f"- {tipo}: {count} estudiantes ({pct:.1f}%)")
        
        # 4. Decisión final (eligió la universidad o no)
        decision = self.df['eligio_universidad'].value_counts()
        print("\nDecisión final de los estudiantes:")
        for dec, count in decision.items():
            pct = (count/len(self.df))*100
            print(f"- {'Eligió' if dec == 'Sí' else 'No eligió'}: {count} estudiantes ({pct:.1f}%)")
        
        return {
            'preferencia_area': pref_area,
            'modalidad': modalidad,
            'tipo_universidad': tipo_univ,
            'decision': decision
        }
    
    def analyze_geographical_patterns(self):
        """Análisis de patrones geográficos"""
        print("\n=== ANÁLISIS DE PATRONES GEOGRÁFICOS ===")
        
        # Distribución por departamento de origen
        dep_origen = self.df['departamento_origen'].value_counts()
        print("\nEstudiantes por departamento de origen:")
        for dep, count in dep_origen.items():
            pct = (count/len(self.df))*100
            print(f"- {dep}: {count} estudiantes ({pct:.1f}%)")
        
        # Distribución por departamento de universidad
        dep_univ = self.df['universidad_departamento'].value_counts()
        print("\nUniversidades por departamento:")
        for dep, count in dep_univ.items():
            pct = (count/len(self.df))*100
            print(f"- {dep}: {count} estudiantes ({pct:.1f}%)")
        
        # Patrón de migración académica
        migration = self.df.groupby(['departamento_origen', 'universidad_departamento']).size().reset_index(name='count')
        migration = migration.sort_values('count', ascending=False)
        print("\nPrincipales flujos de migración académica:")
        for _, row in migration.head(10).iterrows():
            if row['departamento_origen'] != row['universidad_departamento']:
                print(f"- {row['departamento_origen']} → {row['universidad_departamento']}: {row['count']} estudiantes")
        
        return {
            'origen': dep_origen,
            'destino': dep_univ,
            'migracion': migration
        }
    
    def analyze_socioeconomic_patterns(self):
        """Análisis de patrones socioeconómicos"""
        print("\n=== ANÁLISIS DE PATRONES SOCIOECONÓMICOS ===")
        
        # Distribución por estrato
        estrato_dist = self.df['estrato'].value_counts().sort_index()
        print("\nDistribución por estrato socioeconómico:")
        for estrato, count in estrato_dist.items():
            pct = (count/len(self.df))*100
            print(f"- Estrato {estrato}: {count} estudiantes ({pct:.1f}%)")
        
        # Relación estrato vs tipo de universidad
        estrato_univ = pd.crosstab(self.df['estrato'], self.df['universidad_tipo'], normalize='index') * 100
        print("\nPreferencia por tipo de universidad según estrato (%):")
        print(estrato_univ.round(1))
        
        # Puntaje promedio por estrato
        puntaje_estrato = self.df.groupby('estrato')['puntaje_saber11'].agg(['mean', 'std']).round(2)
        print("\nPuntaje Saber 11 promedio por estrato:")
        print(puntaje_estrato)
        
        return {
            'estrato_dist': estrato_dist,
            'estrato_universidad': estrato_univ,
            'puntaje_estrato': puntaje_estrato
        }
    
    def create_visualizations(self):
        """Crear visualizaciones de los patrones encontrados"""
        print("\n=== CREANDO VISUALIZACIONES ===")
        
        # Configurar subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Distribución por Área de Preferencia', 
                          'Modalidad de Programa',
                          'Tipo de Universidad',
                          'Decisión Final'),
            specs=[[{"type": "pie"}, {"type": "bar"}],
                   [{"type": "pie"}, {"type": "bar"}]]
        )
        
        # Gráfico 1: Área de preferencia
        pref_area = self.df['preferencia_area'].value_counts()
        fig.add_trace(go.Pie(labels=pref_area.index, values=pref_area.values, name="Preferencia"),
                     row=1, col=1)
        
        # Gráfico 2: Modalidad
        modalidad = self.df['modalidad_programa'].value_counts()
        fig.add_trace(go.Bar(x=modalidad.index, y=modalidad.values, name="Modalidad"),
                     row=1, col=2)
        
        # Gráfico 3: Tipo de universidad
        tipo_univ = self.df['universidad_tipo'].value_counts()
        fig.add_trace(go.Pie(labels=tipo_univ.index, values=tipo_univ.values, name="Tipo"),
                     row=2, col=1)
        
        # Gráfico 4: Decisión final
        decision = self.df['eligio_universidad'].value_counts()
        fig.add_trace(go.Bar(x=decision.index, y=decision.values, name="Decisión"),
                     row=2, col=2)
        
        fig.update_layout(height=800, showlegend=False, 
                         title_text="Análisis de Patrones de Comportamiento Estudiantil")
        
        # Guardar visualización
        fig.write_html("/Users/leomos/Downloads/web_semantica/visualizations/patrones_comportamiento.html")
        print("Visualización guardada en: visualizations/patrones_comportamiento.html")
        
        # Crear mapa de flujos de migración académica
        migration = self.df.groupby(['departamento_origen', 'universidad_departamento']).size().reset_index(name='estudiantes')
        migration_top = migration.sort_values('estudiantes', ascending=False).head(15)
        
        fig_migration = px.bar(migration_top, 
                              x='estudiantes', 
                              y=[f"{row['departamento_origen']} → {row['universidad_departamento']}" 
                                 for _, row in migration_top.iterrows()],
                              orientation='h',
                              title="Principales Flujos de Migración Académica",
                              labels={'estudiantes': 'Número de Estudiantes', 'y': 'Flujo Origen → Destino'})
        
        fig_migration.write_html("/Users/leomos/Downloads/web_semantica/visualizations/migracion_academica.html")
        print("Visualización de migración guardada en: visualizations/migracion_academica.html")
        
        return fig, fig_migration
    
    def generate_insights_report(self):
        """Generar reporte de insights para el documento"""
        insights = {
            'dataset_size': len(self.df),
            'universities_count': len(self.df['universidad_codigo'].unique()),
            'departments_count': len(self.df['universidad_departamento'].unique()),
            'behavioral_patterns': {},
            'geographical_patterns': {},
            'socioeconomic_patterns': {}
        }
        
        # Patrones de comportamiento
        decision_rate = (self.df['eligio_universidad'] == 'Sí').sum() / len(self.df) * 100
        most_popular_area = self.df['preferencia_area'].mode()[0]
        most_popular_modality = self.df['modalidad_programa'].mode()[0]
        
        insights['behavioral_patterns'] = {
            'decision_rate': round(decision_rate, 1),
            'most_popular_area': most_popular_area,
            'most_popular_modality': most_popular_modality
        }
        
        # Patrones geográficos
        most_common_origin = self.df['departamento_origen'].mode()[0]
        most_common_destination = self.df['universidad_departamento'].mode()[0]
        
        insights['geographical_patterns'] = {
            'most_common_origin': most_common_origin,
            'most_common_destination': most_common_destination
        }
        
        # Patrones socioeconómicos
        avg_score = round(self.df['puntaje_saber11'].mean(), 1)
        public_preference = (self.df['universidad_tipo'] == 'Pública').sum() / len(self.df) * 100
        
        insights['socioeconomic_patterns'] = {
            'avg_saber11_score': avg_score,
            'public_university_preference': round(public_preference, 1)
        }
        
        return insights

def main():
    """Función principal"""
    print("=== ANÁLISIS EXPLORATORIO DE DATOS - PROYECTO LINKED DATA ===")
    print("Analizando patrones de comportamiento estudiantil en la selección universitaria\n")
    
    # Inicializar analizador
    analyzer = UniversityDataAnalyzer('/Users/leomos/Downloads/web_semantica/ISOFV163_A8_Anexo.csv')
    
    # Realizar análisis
    universities = analyzer.analyze_universities()
    behavioral_patterns = analyzer.analyze_behavioral_patterns()
    geographical_patterns = analyzer.analyze_geographical_patterns()
    socioeconomic_patterns = analyzer.analyze_socioeconomic_patterns()
    
    # Crear visualizaciones
    fig1, fig2 = analyzer.create_visualizations()
    
    # Generar reporte de insights
    insights = analyzer.generate_insights_report()
    
    print("\n=== RESUMEN DE INSIGHTS CLAVE ===")
    print(f"- Dataset con {insights['dataset_size']} estudiantes de {insights['universities_count']} universidades")
    print(f"- Tasa de decisión final: {insights['behavioral_patterns']['decision_rate']}%")
    print(f"- Área más popular: {insights['behavioral_patterns']['most_popular_area']}")
    print(f"- Modalidad preferida: {insights['behavioral_patterns']['most_popular_modality']}")
    print(f"- Preferencia por universidades públicas: {insights['socioeconomic_patterns']['public_university_preference']}%")
    print(f"- Puntaje promedio Saber 11: {insights['socioeconomic_patterns']['avg_saber11_score']}")
    
    print("\n=== ANÁLISIS COMPLETADO ===")
    print("Los resultados han sido guardados en el directorio 'visualizations/'")
    
    return analyzer, insights

if __name__ == "__main__":
    analyzer, insights = main()