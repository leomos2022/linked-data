# Ontología del Dominio Universitario
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

Generado el: 2025-10-28 18:45:33
