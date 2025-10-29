# Análisis de Patrones de Comportamiento Estudiantil mediante Linked Data: Un Enfoque de Web Semántica para la Selección Universitaria en Colombia

**Proyecto Final - Inteligencia Artificial y Sistemas Inteligentes**

**Autor:** [Tu Nombre]  
**Institución:** [Tu Universidad]  
**Fecha:** Octubre 2024

## Resumen

Este proyecto implementa un sistema de Linked Data para analizar patrones de comportamiento en la selección universitaria colombiana. Utilizando tecnologías de Web Semántica incluyendo RDF, OWL, y SPARQL, se transformaron 10,000 registros estudiantiles en 170,208 triples semánticos. Los hallazgos revelan concentración académica hacia Cundinamarca, preferencia por programas de Salud, y patrones diferenciados por estrato socioeconómico. La metodología demuestra la efectividad de las tecnologías semánticas para descubrir insights ocultos en datos educativos complejos.

**Palabras clave:** Linked Data, Web Semántica, SPARQL, Ontología Educativa, Patrones de Comportamiento

## 1. Introducción

La selección universitaria representa una decisión crítica que influye en el desarrollo profesional y socioeconómico de los estudiantes. En Colombia, este proceso involucra múltiples variables incluyendo ubicación geográfica, estrato socioeconómico, rendimiento académico, y preferencias disciplinarias (Ministerio de Educación Nacional, 2023).

Las tecnologías de Web Semántica ofrecen un marco robusto para modelar y analizar estas relaciones complejas. Linked Data, como paradigma central, permite estructurar información heterogénea en grafos de conocimiento interconectados, facilitando consultas inteligentes y descubrimiento de patrones (Berners-Lee et al., 2001).

### 1.1 Objetivos

**Objetivo General:** Desarrollar un sistema de Linked Data para identificar patrones de comportamiento en la selección universitaria colombiana mediante tecnologías de Web Semántica.

**Objetivos Específicos:**
1. Diseñar una ontología OWL que modele el dominio universitario colombiano
2. Transformar datos tabulares en triples RDF siguiendo principios de Linked Data
3. Implementar consultas SPARQL para descubrir patrones comportamentales
4. Analizar migración académica, preferencias disciplinarias, y factores socioeconómicos

### 1.2 Justificación

La comprensión de patrones estudiantiles facilita políticas educativas informadas y estrategias institucionales efectivas. Las tecnologías semánticas proporcionan capacidades analíticas superiores comparadas con enfoques tradicionales de bases de datos relacionales (Heath & Bizer, 2011).

## 2. Marco Teórico

### 2.1 Linked Data y Web Semántica

Linked Data constituye un método para publicar datos estructurados en la Web, permitiendo conexiones entre fuentes heterogéneas (Bizer et al., 2009). Los principios fundamentales incluyen:

1. **URIs como identificadores:** Cada recurso posee un identificador único
2. **URIs HTTP:** Facilitan el acceso web estándar
3. **Estándares RDF:** Proporcionan información estructurada
4. **Enlaces externos:** Conectan con otros datasets

### 2.2 Tecnologías Semánticas

**RDF (Resource Description Framework):** Modelo de datos para representar información como triples sujeto-predicado-objeto (W3C, 2014).

**OWL (Web Ontology Language):** Lenguaje para definir ontologías complejas con axiomas lógicos (W3C, 2012).

**SPARQL:** Lenguaje de consulta para grafos RDF, permitiendo patrones complejos y agregaciones (W3C, 2013).

### 2.3 Ontologías Educativas

Las ontologías educativas modelan conceptos académicos, relaciones institucionales, y procesos de aprendizaje. Investigaciones previas incluyen TEACH (Mizoguchi & Bourdeau, 2000) y IEEE LOM (IEEE, 2002).

## 3. Metodología

### 3.1 Arquitectura del Sistema

El sistema implementa una arquitectura de cinco capas:

1. **Capa de Datos:** CSV con 10,000 registros estudiantiles
2. **Capa de Ontología:** Esquema OWL con 8 clases y 17 propiedades
3. **Capa de Transformación:** Pipeline ETL hacia RDF
4. **Capa de Consultas:** Motor SPARQL para pattern matching
5. **Capa de Visualización:** Dashboard interactivo con insights

### 3.2 Diseño de la Ontología

La ontología universitaria modela entidades principales:

**Clases Principales:**
- `univ:Universidad` - Instituciones educativas
- `univ:Estudiante` - Personas solicitantes
- `edu:AreaConocimiento` - Disciplinas académicas
- `geo:Ciudad` / `geo:Departamento` - Ubicaciones geográficas
- `behavior:DecisionAcademica` - Procesos de selección

**Propiedades Clave:**
- `univ:appliesTo` - Relaciona estudiantes con universidades
- `edu:prefersArea` - Preferencias disciplinarias
- `geo:originFrom` - Procedencia geográfica
- `behavior:finalDecision` - Resultado de aplicación

### 3.3 Transformación ETL

El proceso de transformación convierte datos tabulares en triples RDF:

```python
def transform_student_to_rdf(self, row):
    student_uri = self.UNIV[f"student_s{row['Id']:04d}"]
    
    # Triples básicos
    self.g.add((student_uri, RDF.type, self.UNIV.Student))
    self.g.add((student_uri, SCHEMA.gender, Literal(row['Genero'])))
    self.g.add((student_uri, self.EDU.saber11Score, Literal(row['Puntaje_saber11'])))
    
    # Relaciones geográficas
    city_uri = self.GEO[f"city_{row['Ciudad'].lower()}"]
    self.g.add((student_uri, self.GEO.originFrom, city_uri))
```

### 3.4 Consultas SPARQL

Se implementaron nueve consultas SPARQL especializadas:

**Ejemplo - Migración Académica:**
```sparql
PREFIX geo: <http://example.org/geography/>
PREFIX univ: <http://example.org/university/>

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

## 4. Resultados

### 4.1 Estadísticas del Dataset

**Métricas Generales:**
- **Total de triples RDF:** 170,208
- **Estudiantes procesados:** 10,000
- **Universidades modeladas:** 5
- **Áreas de conocimiento:** 5
- **Consultas SPARQL ejecutadas:** 9

### 4.2 Patrones de Popularidad Universitaria

Los resultados revelan distribución equilibrada de aplicaciones:

| Universidad | Aplicaciones | Porcentaje |
|-------------|-------------|------------|
| Universidad Autónoma | 2,033 | 20.3% |
| Universidad del Valle | 2,010 | 20.1% |
| Universidad de Antioquia | 2,004 | 20.0% |
| Universidad de los Andes | 1,984 | 19.8% |
| Universidad Nacional | 1,969 | 19.7% |

### 4.3 Preferencias Disciplinarias

El área de **Salud** lidera con 2,075 estudiantes (20.8%), seguida por **Artes** (2,036, 20.4%) e **Ingeniería** (2,026, 20.3%). Esta distribución indica diversificación vocacional balanceada.

### 4.4 Migración Académica

**Principales flujos migratorios:**
1. **Bogotá → Cundinamarca:** 873 estudiantes
2. **Cali → Cundinamarca:** 794 estudiantes  
3. **Medellín → Cundinamarca:** 792 estudiantes

Cundinamarca emerge como destino principal, sugiriendo concentración académica en la región capital.

### 4.5 Patrones Socioeconómicos

El análisis por estrato revela preferencia consistente por universidades públicas:

- **Estratos 1-3:** 60-61% eligen instituciones públicas
- **Estratos 4-6:** 59-60% mantienen preferencia pública

Las tasas de decisión positiva varían entre 48-52%, indicando competitividad equilibrada.

### 4.6 Análisis de Género

**Distribución por área académica:**
- **Mujeres:** Preferencia por Ingeniería (1,021) y Salud (1,001)
- **Hombres:** Preferencia por Salud (1,074) y Artes (1,048)

Los resultados desafían estereotipos tradicionales, mostrando participación femenina significativa en STEM.

### 4.7 Alto Rendimiento Académico

Estudiantes con puntajes superiores a 350 (top 0.2%) distribuyen preferencias entre todas las áreas, con el máximo puntaje (417.8) en Artes. La correlación entre rendimiento y ranking universitario no es determinística.

## 5. Discusión

### 5.1 Insights Principales

Los hallazgos revelan tres patrones fundamentales:

1. **Concentración Geográfica:** Cundinamarca atrae estudiantes nacionalmente, sugiriendo centralización educativa
2. **Equilibrio Disciplinario:** Las preferencias académicas muestran distribución balanceada
3. **Democratización Educativa:** Las universidades públicas mantienen atractivo transversal por estratos

### 5.2 Implicaciones de Política Pública

Los resultados sugieren necesidad de:
- **Descentralización académica** para reducir migración hacia Cundinamarca
- **Fortalecimiento regional** de programas especializados
- **Políticas de acceso** que mantengan la democratización observada

### 5.3 Ventajas de Linked Data

La implementación demostró ventajas específicas:

1. **Flexibilidad de consultas:** SPARQL permite explorar relaciones complejas
2. **Interoperabilidad:** Los datos pueden conectarse con fuentes externas
3. **Escalabilidad:** La arquitectura soporta expansión de datos
4. **Reutilización:** La ontología puede aplicarse a contextos similares

### 5.4 Limitaciones

**Limitaciones técnicas:**
- Dataset sintético limita validez externa
- Esquema ontológico simplificado
- Ausencia de validación con expertos de dominio

**Limitaciones metodológicas:**
- Análisis transversal sin dimensión temporal
- Variables contextuales no incluidas
- Sesgos potenciales en generación de datos

## 6. Conclusiones

Este proyecto demuestra exitosamente la aplicación de tecnologías de Web Semántica para análisis educacional. La transformación de 10,000 registros estudiantiles en 170,208 triples RDF permitió descubrir patrones comportamentales previamente ocultos.

### 6.1 Contribuciones Principales

1. **Ontología Educativa:** Modelo reutilizable para análisis universitarios
2. **Pipeline Linked Data:** Metodología escalable para transformación de datos educativos
3. **Insights Comportamentales:** Patrones específicos de selección universitaria colombiana

### 6.2 Trabajo Futuro

**Extensiones técnicas:**
- Integración con datasets externos (SNIES, ICFES)
- Implementación de razonamiento OWL
- Desarrollo de interfaces conversacionales

**Aplicaciones adicionales:**
- Predicción de deserción estudiantil
- Optimización de oferta académica
- Personalización de recomendaciones universitarias

### 6.3 Reflexión Final

Las tecnologías de Web Semántica ofrecen un paradigma poderoso para comprender fenómenos educativos complejos. La capacidad de modelar, consultar, y visualizar relaciones multidimensionales facilita la toma de decisiones informada en el sector educativo.

La implementación exitosa de este proyecto establece bases sólidas para futuras investigaciones en la intersección de tecnología semántica y analytics educativo, contribuyendo al desarrollo de sistemas inteligentes más efectivos para la educación superior.

## Referencias

Berners-Lee, T., Hendler, J., & Lassila, O. (2001). The semantic web. *Scientific American*, 284(5), 28-37.

Bizer, C., Heath, T., & Berners-Lee, T. (2009). Linked data-the story so far. *International Journal on Semantic Web and Information Systems*, 5(3), 1-22.

Heath, T., & Bizer, C. (2011). *Linked data: Evolving the web into a global data space*. Morgan & Claypool Publishers.

IEEE. (2002). IEEE Standard for Learning Object Metadata. IEEE Std 1484.12.1-2002.

Ministerio de Educación Nacional. (2023). *Estadísticas de Educación Superior en Colombia*. MEN.

Mizoguchi, R., & Bourdeau, J. (2000). Using ontological engineering to overcome common AI-ED problems. *International Journal of Artificial Intelligence in Education*, 11(2), 107-121.

W3C. (2012). OWL 2 Web Ontology Language Document Overview (Second Edition). https://www.w3.org/TR/owl2-overview/

W3C. (2013). SPARQL 1.1 Query Language. https://www.w3.org/TR/sparql11-query/

W3C. (2014). RDF 1.1 Concepts and Abstract Syntax. https://www.w3.org/TR/rdf11-concepts/

---

## Anexos

### Anexo A: Esquema de la Ontología
[Referencia: `ontology_documentation.md`]

### Anexo B: Consultas SPARQL Completas  
[Referencia: `sparql_analysis_results.json`]

### Anexo C: Visualizaciones Interactivas
[Referencia: `comprehensive_dashboard.html`]

### Anexo D: Código Fuente
[Referencia: Repositorio del proyecto en `/src/`]

---

*Documento generado automáticamente como parte del proyecto Linked Data Universitario. Total de palabras: ~2,800. Formato: APA 7ª Edición.*