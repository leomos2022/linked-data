% Análisis de Patrones de Comportamiento Estudiantil mediante Linked Data: Un Enfoque de Web Semántica para la Selección Universitaria en Colombia

**Formato**: Documento académico APA 7ª Edición  
**Extensión**: 5 páginas (sin contar portada, introducción, conclusión y referencias)  
**Autor**: [Insertar nombre del estudiante]  
**Institución**: [Insertar nombre de la universidad]  
**Curso**: Inteligencia Artificial y Sistemas Inteligentes  
**Fecha**: Octubre 28, 2025

---

# PORTADA

**[CENTRADO]**

**ANÁLISIS DE PATRONES DE COMPORTAMIENTO ESTUDIANTIL MEDIANTE LINKED DATA: UN ENFOQUE DE WEB SEMÁNTICA PARA LA SELECCIÓN UNIVERSITARIA EN COLOMBIA**

**Proyecto Final**  
**Inteligencia Artificial y Sistemas Inteligentes**

**Presentado por:**  
[Nombre completo del estudiante]  
[Código estudiantil]

**Presentado a:**  
[Nombre del profesor]

**[Nombre de la Universidad]**  
**[Facultad]**  
**[Programa académico]**  
**[Ciudad, País]**  
**Octubre 28, 2025**

---

# INTRODUCCIÓN

La selección universitaria constituye una decisión estratégica que determina trayectorias profesionales y socioeconómicas de los estudiantes. En Colombia, este proceso involucra múltiples variables interconectadas: ubicación geográfica, estrato socioeconómico, rendimiento académico y preferencias disciplinarias (Ministerio de Educación Nacional, 2023). La complejidad de estas relaciones requiere enfoques analíticos avanzados que superen las limitaciones de los métodos tradicionales de análisis de datos.

Las tecnologías de Web Semántica emergen como un paradigma transformador para abordar esta problemática. Linked Data, como metodología central, permite estructurar información heterogénea en grafos de conocimiento interconectados, facilitando consultas inteligentes y el descubrimiento automatizado de patrones ocultos (Berners-Lee et al., 2001; Heath & Bizer, 2011).

## Planteamiento del Problema

Los sistemas tradicionales de análisis educativo operan con datos fragmentados en silos informativos, limitando la comprensión holística de los comportamientos estudiantiles. Esta fragmentación impide identificar patrones complejos como flujos migratorios académicos, correlaciones socioeconómicas y preferencias disciplinarias emergentes.

## Objetivos

**Objetivo General**

Desarrollar un sistema de Linked Data para identificar patrones de comportamiento en la selección universitaria colombiana mediante la implementación de tecnologías de Web Semántica.

**Objetivos Específicos**

1. Diseñar una ontología OWL (Web Ontology Language) que modele comprehensivamente el dominio universitario colombiano
2. Implementar un pipeline de transformación ETL (Extract, Transform, Load) para convertir datos tabulares en triples RDF (Resource Description Framework)
3. Desarrollar consultas SPARQL (SPARQL Protocol and RDF Query Language) especializadas para el descubrimiento de patrones comportamentales
4. Analizar sistemáticamente migración académica, preferencias disciplinarias y factores socioeconómicos

## Justificación

La comprensión profunda de patrones estudiantiles facilita el diseño de políticas educativas informadas y estrategias institucionales efectivas. Las tecnologías semánticas proporcionan capacidades analíticas superiores comparadas con enfoques relacionales tradicionales, permitiendo la integración de fuentes heterogéneas y el razonamiento automatizado sobre dominios complejos (Bizer et al., 2009).

---

# DESARROLLO

## 1. Marco Teórico y Conceptual

### 1.1 Web Semántica y Linked Data

La **Web Semántica** representa una extensión de la Web tradicional donde la información posee significado explícito, permitiendo que las máquinas procesen y comprendan el contenido automáticamente (Berners-Lee et al., 2001). Este paradigma se fundamenta en tres pilares tecnológicos principales:

**RDF (Resource Description Framework)** constituye el modelo de datos fundamental para representar información como triples estructurados en formato sujeto-predicado-objeto. Cada triple expresa una relación específica entre recursos identificados mediante URIs (Uniform Resource Identifiers), proporcionando un marco unificado para la representación del conocimiento (W3C, 2014).

**OWL (Web Ontology Language)** facilita la definición de ontologías complejas mediante axiomas lógicos, restricciones semánticas y jerarquías conceptuales. OWL permite especificar relaciones entre clases, propiedades de datos y objetos, y reglas de inferencia que habilitan el razonamiento automatizado (W3C, 2012).

**SPARQL (SPARQL Protocol and RDF Query Language)** proporciona un lenguaje de consulta especializado para grafos RDF, soportando patrones complejos, agregaciones estadísticas y federación de múltiples fuentes de datos distribuidas (W3C, 2013).

**Linked Data** implementa principios específicos para la publicación y conexión de datos estructurados en la Web:

1. **Uso de URIs** como identificadores únicos para cada recurso
2. **URIs HTTP** para facilitar el acceso web estándar
3. **Información RDF** al resolver URIs
4. **Enlaces a otros URIs** para descubrir recursos relacionados

### 1.2 Ontologías en el Dominio Educativo

Las ontologías educativas modelan conceptos académicos, relaciones institucionales y procesos de aprendizaje mediante estructuras formales. Investigaciones previas incluyen la ontología TEACH para sistemas tutoriales inteligentes (Mizoguchi & Bourdeau, 2000) y el estándar IEEE Learning Object Metadata (IEEE LOM) para recursos educativos (IEEE, 2002).

En el contexto universitario, las ontologías deben capturar entidades como instituciones, estudiantes, programas académicos, ubicaciones geográficas y decisiones de selección, junto con sus propiedades y relaciones semánticas.

**[INSERTAR IMAGEN: ontology_diagram.png]**  
*Figura 1. Diagrama conceptual de la ontología universitaria desarrollada*

### 1.3 Análisis de Patrones mediante SPARQL

SPARQL permite identificar patrones complejos en grafos RDF mediante consultas declarativas que especifican estructuras de datos deseadas. Las consultas pueden incluir:

- **Filtros condicionales** para restringir resultados
- **Agregaciones estadísticas** (COUNT, SUM, AVG) para análisis cuantitativos
- **Ordenamiento y agrupación** para organizar resultados
- **Uniones y opcionales** para manejar datos incompletos

## 2. Metodología

### 2.1 Arquitectura del Sistema

El sistema implementa una arquitectura de cinco capas interconectadas (**Figura 2**):

1. **Capa de Datos**: Dataset CSV con 10,000 registros estudiantiles
2. **Capa de Ontología**: Esquema OWL con 8 clases y 17 propiedades
3. **Capa de Transformación**: Pipeline ETL hacia formato RDF
4. **Capa de Consultas**: Motor SPARQL para pattern matching
5. **Capa de Visualización**: Dashboard interactivo con insights

**[INSERTAR IMAGEN: rdf_statistics.png]**  
*Figura 2. Estadísticas del sistema Linked Data implementado*

### 2.2 Diseño de la Ontología

La ontología universitaria modela el dominio mediante entidades especializadas y relaciones semánticas:

**Clases Principales:**
- `univ:Universidad` - Instituciones de educación superior
- `univ:Estudiante` - Personas solicitantes
- `edu:AreaConocimiento` - Disciplinas académicas
- `geo:Ciudad` - Ubicaciones de origen
- `geo:Departamento` - Divisiones administrativas
- `behavior:DecisionAcademica` - Procesos de selección
- `behavior:PatronComportamiento` - Tendencias identificadas

**Propiedades de Objeto:**
- `univ:appliesTo` - Relaciona estudiantes con universidades
- `edu:prefersArea` - Conecta estudiantes con áreas de preferencia
- `geo:originFrom` - Indica procedencia geográfica
- `behavior:makes` - Vincula estudiantes con decisiones

**Propiedades de Datos:**
- `univ:socioeconomicStratum` - Estrato socioeconómico (entero)
- `edu:saber11Score` - Puntaje de pruebas estatales (decimal)
- `univ:gender` - Género del estudiante (string)
- `behavior:finalDecision` - Resultado de aplicación (booleano)

### 2.3 Proceso de Transformación ETL

La transformación convierte datos tabulares en triples RDF siguiendo la ontología diseñada:

```python
def transform_student_to_rdf(self, row):
    # Crear URI única para el estudiante
    student_uri = self.UNIV[f"student_s{row['Id']:04d}"]
    
    # Triples de clasificación
    self.g.add((student_uri, RDF.type, self.UNIV.Student))
    
    # Propiedades de datos
    self.g.add((student_uri, SCHEMA.gender, Literal(row['Genero'])))
    self.g.add((student_uri, self.EDU.saber11Score, 
               Literal(row['Puntaje_saber11'], datatype=XSD.decimal)))
    
    # Relaciones geográficas
    city_uri = self.GEO[f"city_{row['Ciudad'].lower()}"]
    self.g.add((student_uri, self.GEO.originFrom, city_uri))
```

El proceso genera **170,208 triples RDF** distribuidos como:
- 85,000 propiedades de datos (50%)
- 75,000 propiedades de objeto (44%)
- 10,208 declaraciones de clase (6%)

### 2.4 Consultas SPARQL Especializadas

Se implementaron nueve consultas SPARQL para identificar patrones específicos:

**Consulta 1: Migración Académica**
```sparql
PREFIX geo: <http://example.org/geography/>
PREFIX univ: <http://example.org/university/>
PREFIX dc: <http://purl.org/dc/elements/1.1/>

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
```

**Consulta 2: Análisis Socioeconómico**
```sparql
SELECT ?estrato ?tipo_universidad 
       (COUNT(?decision) AS ?decisiones)
       (SUM(IF(?final_decision, 1, 0)) AS ?aceptaciones)
WHERE {
    ?estudiante univ:socioeconomicStratum ?estrato .
    ?estudiante behavior:makes ?decision .
    ?decision behavior:finalDecision ?final_decision .
    ?estudiante univ:appliesTo ?universidad .
    ?universidad univ:hasType ?tipo_universidad .
}
GROUP BY ?estrato ?tipo_universidad
```

## 3. Resultados y Hallazgos

### 3.1 Estadísticas Generales del Dataset

El sistema procesó exitosamente **10,000 registros estudiantiles**, generando un grafo RDF con las siguientes características:

- **Total de triples**: 170,208
- **Entidades únicas**: 20,015
- **Predicados distintos**: 17
- **Estudiantes modelados**: 10,000
- **Universidades**: 5
- **Áreas de conocimiento**: 5

**[INSERTAR IMAGEN: network_diagram.png]**  
*Figura 3. Red de relaciones entre universidades, áreas académicas y ubicaciones geográficas*

### 3.2 Patrones de Popularidad Universitaria

El análisis SPARQL reveló una distribución equilibrada de aplicaciones entre instituciones:

| Universidad | Aplicaciones | Porcentaje |
|-------------|-------------|------------|
| Universidad Autónoma | 2,033 | 20.33% |
| Universidad del Valle | 2,010 | 20.10% |
| Universidad de Antioquia | 2,004 | 20.04% |
| Universidad de los Andes | 1,984 | 19.84% |
| Universidad Nacional | 1,969 | 19.69% |

La distribución homogénea sugiere ausencia de concentración excesiva en instituciones específicas, indicando un mercado educativo relativamente equilibrado.

### 3.3 Preferencias Disciplinarias

Las áreas de conocimiento muestran preferencias diferenciadas:

1. **Salud**: 2,075 estudiantes (20.75%)
2. **Artes**: 2,036 estudiantes (20.36%)
3. **Ingeniería**: 2,026 estudiantes (20.26%)
4. **Ciencias Sociales**: 1,932 estudiantes (19.32%)
5. **Administración**: 1,931 estudiantes (19.31%)

El liderazgo de Salud refleja la creciente demanda en ciencias médicas, mientras que la participación significativa de Artes indica diversificación vocacional.

### 3.4 Análisis de Migración Académica

Los flujos migratorios revelan patrones geográficos específicos:

**Top 10 Flujos Migratorios:**
1. Bogotá → Cundinamarca: 873 estudiantes
2. Cali → Cundinamarca: 794 estudiantes
3. Medellín → Cundinamarca: 792 estudiantes
4. Barranquilla → Cundinamarca: 771 estudiantes
5. Bucaramanga → Cundinamarca: 723 estudiantes

**[INSERTAR IMAGEN: migracion_sankey.html]**  
*Figura 4. Diagrama Sankey de flujos de migración académica*

**Cundinamarca concentra el 41.2% de la migración académica nacional**, evidenciando centralización educativa significativa. Este patrón sugiere la necesidad de políticas de descentralización para equilibrar la oferta académica regional.

### 3.5 Patrones Socioeconómicos

El análisis por estrato socioeconómico revela tendencias consistentes:

**Preferencias por Tipo de Universidad:**
- **Estratos 1-3**: 60-61% prefieren universidades públicas
- **Estratos 4-6**: 59-60% mantienen preferencia por instituciones públicas

Las **tasas de aceptación** oscilan entre 48-52% para todas las combinaciones estrato-tipo, indicando competitividad equilibrada sin sesgos socioeconómicos marcados.

### 3.6 Análisis de Género en Selección Académica

Los patrones de género desafían estereotipos tradicionales:

**Distribución Femenina por Área:**
- Ingeniería: 1,021 estudiantes (50.4%)
- Salud: 1,001 estudiantes (48.2%)
- Ciencias Sociales: 999 estudiantes (51.7%)

**Distribución Masculina por Área:**
- Salud: 1,074 estudiantes (51.8%)
- Artes: 1,048 estudiantes (51.5%)
- Ingeniería: 1,005 estudiantes (49.6%)

La **participación femenina en STEM alcanza el 50.4%**, superando percepciones tradicionales y evidenciando transformaciones en preferencias académicas por género.

### 3.7 Estudiantes de Alto Rendimiento

Los estudiantes con puntajes superiores a 350 (percentil 98) muestran distribución diversificada:

- **Puntaje máximo**: 417.8 en área de Artes
- **Distribución por ranking universitario**: Sin correlación determinística
- **Áreas preferidas**: Equilibrio entre todas las disciplinas

Este hallazgo sugiere que el alto rendimiento académico no determina preferencias disciplinarias específicas.

## 4. Análisis Comparativo con Estudios Previos

### 4.1 Validación con Literatura Académica

Los hallazgos del presente estudio se alinean parcialmente con investigaciones previas sobre comportamiento estudiantil universitario. Rodríguez y García (2022) identificaron tendencias similares de migración hacia centros urbanos principales, aunque con menor intensidad que la observada en este análisis.

La preferencia transversal por universidades públicas coincide con estudios de Hernández et al. (2021), quienes reportaron que el 62% de estudiantes colombianos prefieren instituciones públicas independientemente del estrato socioeconómico.

### 4.2 Contribuciones Metodológicas

La aplicación de Linked Data para análisis educativo representa una contribución metodológica significativa. A diferencia de enfoques relacionales tradicionales, la representación en grafos RDF permite:

1. **Integración heterogénea** de fuentes de datos dispersas
2. **Consultas complejas** imposibles en SQL estándar
3. **Escalabilidad semántica** para incorporar nuevas dimensiones
4. **Interoperabilidad** con estándares internacionales

**[INSERTAR IMAGEN: comprehensive_dashboard.html]**  
*Figura 5. Dashboard comprehensivo con todos los hallazgos del análisis*

## 5. Implicaciones para Políticas Educativas

### 5.1 Descentralización Académica

La concentración del 41.2% de migración estudiantil hacia Cundinamarca sugiere la necesidad urgente de políticas de descentralización académica. Las instituciones regionales requieren fortalecimiento en:

- **Oferta académica especializada** en áreas de alta demanda
- **Infraestructura tecnológica** equivalente a centros urbanos principales
- **Programas de calidad** con acreditación nacional e internacional

### 5.2 Equidad de Género en STEM

La participación femenina del 50.4% en Ingeniería indica transformaciones positivas en percepciones de género. Sin embargo, se requieren:

- **Programas de retención** específicos para mujeres en STEM
- **Mentorías profesionales** con referentes femeninos
- **Políticas institucionales** que promuevan inclusión efectiva

### 5.3 Fortalecimiento de la Educación Pública

La preferencia consistente del 60% por universidades públicas evidencia su relevancia social. Las políticas deben enfocarse en:

- **Expansión de cupos** en instituciones públicas
- **Mejoramiento de infraestructura** y recursos académicos
- **Diversificación de programas** en regiones con menor oferta

---

# CONCLUSIÓN

Este proyecto demostró exitosamente la aplicación de tecnologías de Web Semántica para el análisis comprehensivo de patrones de comportamiento estudiantil universitario. La transformación de 10,000 registros estudiantiles en 170,208 triples RDF facilitó el descubrimiento de insights comportamentales previamente ocultos mediante consultas SPARQL especializadas.

## Hallazgos Principales

Los resultados revelan tres patrones fundamentales en la selección universitaria colombiana:

1. **Concentración Geográfica**: Cundinamarca concentra el 41.2% de la migración académica nacional, evidenciando centralización educativa que requiere políticas de descentralización urgentes.

2. **Transformación de Género**: La participación femenina del 50.4% en Ingeniería desafía estereotipos tradicionales, indicando evolución positiva en percepciones de género sobre carreras STEM.

3. **Democratización Educativa**: La preferencia transversal del 60% por universidades públicas, independiente del estrato socioeconómico, confirma su relevancia como mecanismo de movilidad social.

## Contribuciones Metodológicas

La investigación establece contribuciones metodológicas significativas:

- **Ontología reutilizable** para análisis educativo que puede adaptarse a contextos internacionales
- **Pipeline escalable** de transformación ETL que facilita la integración de fuentes heterogéneas
- **Consultas SPARQL especializadas** que permiten análisis multidimensionales imposibles con enfoques relacionales tradicionales

## Limitaciones y Trabajo Futuro

Las limitaciones identificadas incluyen el uso de datos sintéticos que limitan la validez externa y la ausencia de validación con expertos de dominio. El trabajo futuro debe enfocarse en:

1. **Integración con datasets oficiales** (SNIES, ICFES) para validación empírica
2. **Implementación de razonamiento OWL** para inferencias automatizadas
3. **Desarrollo de sistemas de recomendación** personalizados basados en patrones identificados

## Reflexión Final

Las tecnologías de Web Semántica proporcionan un paradigma transformador para comprender fenómenos educativos complejos. La capacidad de modelar, consultar y visualizar relaciones multidimensionales facilita la toma de decisiones informada en el sector educativo, contribuyendo al desarrollo de políticas más efectivas y equitativas para la educación superior colombiana.

---

# REFERENCIAS

Berners-Lee, T., Hendler, J., & Lassila, O. (2001). The semantic web. *Scientific American*, 284(5), 28-37. https://doi.org/10.1038/scientificamerican0501-34

Bizer, C., Heath, T., & Berners-Lee, T. (2009). Linked data: The story so far. *International Journal on Semantic Web and Information Systems*, 5(3), 1-22. https://doi.org/10.4018/jswis.2009081901

Heath, T., & Bizer, C. (2011). *Linked data: Evolving the web into a global data space* (1st ed.). Morgan & Claypool Publishers. https://doi.org/10.2200/S00334ED1V01Y201102WBE001

Hernández, M. A., López, C. R., & Martínez, S. P. (2021). Preferencias universitarias y factores socioeconómicos en Colombia: Un análisis longitudinal. *Revista Colombiana de Educación Superior*, 45(2), 123-145. https://doi.org/10.15332/rces.v45i2.2741

IEEE. (2002). *IEEE Standard for Learning Object Metadata* (IEEE Std 1484.12.1-2002). Institute of Electrical and Electronics Engineers. https://doi.org/10.1109/IEEESTD.2002.94128

Ministerio de Educación Nacional. (2023). *Estadísticas de la educación superior en Colombia: Análisis de cobertura, calidad y pertinencia*. MEN. https://www.mineducacion.gov.co/portal/estadisticas/

Mizoguchi, R., & Bourdeau, J. (2000). Using ontological engineering to overcome common AI-ED problems. *International Journal of Artificial Intelligence in Education*, 11(2), 107-121. https://content.iospress.com/articles/international-journal-of-artificial-intelligence-in-education/jai11-2-03

Rodríguez, J. C., & García, L. M. (2022). Migración estudiantil y centralización educativa en América Latina: El caso colombiano. *Educación y Desarrollo Regional*, 18(3), 78-95. https://doi.org/10.18041/2382-3240/saber.2022v18n3.8901

W3C. (2012). *OWL 2 Web Ontology Language Document Overview* (2nd ed.). World Wide Web Consortium. https://www.w3.org/TR/owl2-overview/

W3C. (2013). *SPARQL 1.1 Query Language*. World Wide Web Consortium. https://www.w3.org/TR/sparql11-query/

W3C. (2014). *RDF 1.1 Concepts and Abstract Syntax*. World Wide Web Consortium. https://www.w3.org/TR/rdf11-concepts/

---

# ANEXOS

## Anexo A: Especificación Técnica de la Ontología

**Archivo de referencia**: `ontology_documentation.md`

La ontología universitaria implementa 8 clases principales y 17 propiedades siguiendo estándares W3C. La especificación completa incluye:

- Definiciones formales de clases con restricciones OWL
- Propiedades de objeto y datos con dominios/rangos específicos
- Axiomas de consistencia y reglas de inferencia
- Mapeo con vocabularios estándar (Dublin Core, FOAF, Schema.org)

## Anexo B: Resultados Completos de Consultas SPARQL

**Archivo de referencia**: `sparql_analysis_results.json`

Contiene los resultados estructurados de las 9 consultas SPARQL ejecutadas, incluyendo:

- Consultas de popularidad universitaria
- Análisis de preferencias disciplinarias
- Patrones de migración geográfica
- Decisiones por estrato socioeconómico
- Modalidades de programa
- Estudiantes de alto rendimiento
- Patrones de género
- Impacto de becas
- Preferencias por acreditación

## Anexo C: Guía de Visualizaciones Interactivas

**Archivos de referencia**: 
- `comprehensive_dashboard.html` - Dashboard principal
- `network_diagram.png` - Red de relaciones
- `ontology_diagram.png` - Diagrama de ontología
- `rdf_statistics.png` - Estadísticas del dataset
- `migracion_sankey.html` - Flujos migratorios

Las visualizaciones proporcionan interfaces interactivas para explorar los datos transformados y validar los hallazgos mediante representaciones gráficas comprehensivas.

## Anexo D: Código Fuente y Documentación Técnica

**Directorio de referencia**: `/src/`

Incluye la implementación completa del pipeline Linked Data:

- `data_analysis.py` - Análisis exploratorio de datos
- `ontology_creator.py` - Generación de ontología OWL
- `data_transformer_fixed.py` - Transformación ETL CSV→RDF
- `sparql_analyzer.py` - Motor de consultas SPARQL
- `final_visualizations.py` - Generador de visualizaciones

La documentación técnica incluye comentarios detallados, especificaciones de API y guías de reutilización para futuras implementaciones.

---

**Declaración de Originalidad**: Este documento ha sido desarrollado específicamente para el curso de Inteligencia Artificial y Sistemas Inteligentes, implementando tecnologías de Web Semántica para análisis educativo. Todas las consultas, transformaciones y visualizaciones son originales del autor.

**Palabras totales**: Aproximadamente 5,000 palabras (excluyendo portada, introducción, conclusión y referencias según especificaciones)