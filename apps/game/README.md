# Hello World Game - Aprende a Programar con un Videojuego Educativo

## Descripción

**Hello World Game** es un videojuego educativo diseñado para enseñar fundamentos de programación a través de una novela visual y puzzles interactivos. El juego adapta su dificultad al rendimiento del estudiante mediante un agente inteligente que modifica dinámicamente los niveles, proporciona retroalimentación automática y registra el progreso en una base de datos.

## Características Principales

- **Aprendizaje Basado en Juegos**: Enseñanza de conceptos de programación a través de mecánicas de juego atractivas
- **Adaptación Inteligente**: Dificultad que se ajusta automáticamente según el rendimiento del estudiante
- **Novela Visual**: Historia envolvente que contextualiza los problemas de programación
- **Puzzles Interactivos**: Problemas del mundo real que se resuelven con programación visual
- **Registro de Progreso**: Seguimiento detallado del avance del estudiante
- **Sistema de Feedback Automático**: Respuestas inmediatas al código del estudiante

## Arquitectura del Proyecto

### Estructura de Carpetas
```
hello-world!!/
├── models/           # Capa Models - Clases que se mapean en la base de datos
├── scripts/          # Capa Controller - Lógica del juego
│   ├── agent/        # Agente inteligente adaptativo
│   ├── controllers/  # Controladores de escenas
│   ├── database/     # Acceso a la base de datos
│   ├── engine/       # Motor de ejecución y contextos de problemas
│   └── blocks/       # Implementaciones de bloques de programación
├── scenes/           # Capa View - Escenas y componentes de UI
├── data/             # Base de datos local
├── assets/           # Recursos: imágenes, sprites, sonidos
├── config/           # Configuraciones del juego
├── dialogue/         # Diálogos de la novela visual
├── docs/             # Documentación del proyecto
├── test/             # Pruebas del proyecto
└── addons/           # Plugins de Godot
```

### Componentes Principales

#### 1. Motor de Ejecución
Implementado en `scripts/engine/`, incluye:
- `ExecutionEngine.gd`: Intérprete que ejecuta los programas visuales creados por el jugador
- `BaseProblemContext.gd`: Clase base abstracta para contextos de problemas
- `CafeteriaProblemContext.gd`: Ejemplo de contexto específico para problemas de cafetería

#### 2. Sistema de Bloques
- `Block.gd`: Clase base para todos los bloques de programación
- `block_execute.gd`, `block_if.gd`, `block_while.gd`, etc.: Implementaciones específicas
- Cada bloque puede contener lógica específica del dominio del problema

#### 3. Agente Inteligente Adaptativo
- `AdaptiveAgent.gd`: Modifica la dificultad según el rendimiento del estudiante
- Utiliza un archivo estándar de configuración para todos los niveles
- Ajusta parámetros como tamaño de cola, recursos disponibles y limitaciones de tiempo

#### 4. Sistema de Persistencia
- Base de datos SQLite local para almacenar progreso
- Estructura de tablas para niveles, segmentos, problemas y soluciones
- Integración con backend para sincronización de datos

## Funcionamiento

### Niveles de Programación
Cada nivel representa una situación del mundo real (cafetería, biblioteca, etc.) que se resuelve usando programación visual. Los niveles se componen de 6 subniveles:
1. Un subnivel de aprendizaje para introducir conceptos
2. Cinco subniveles de juego con dificultad escalonable

### Programación Visual
Los jugadores construyen programas usando bloques:
- **Inicio/Fin**: Delimitadores de programa
- **If**: Estructuras condicionales
- **While**: Bucles
- **Execute**: Acciones específicas del dominio

### Adaptación Inteligente
1. El agente monitorea el rendimiento del estudiante
2. Calcula un puntaje basado en éxito y eficiencia de tiempo
3. Ajusta parámetros del nivel (cola de trabajo, recursos, etc.)
4. Almacena la nueva configuración para sesiones futuras

## Configuración del Proyecto

### Requisitos
- Godot Engine 4.x
- SQLite (para base de datos local)

### Instalación
1. Clonar el repositorio
2. Abrir con Godot Engine
3. Importar y configurar dependencias necesarias

### Configuración Inicial
1. Asegurar que la base de datos esté correctamente configurada
2. Verificar que los contextos de problemas estén implementados
3. Configurar el agente adaptativo

## Desarrollo

### Agregar Nuevos Tipos de Niveles
1. Crear una clase que extienda `BaseProblemContext`
2. Implementar la lógica específica del dominio
3. Definir las acciones posibles en el bloque `Execute`
4. Crear configuraciones de ejemplo en JSON

### Personalizar el Agente Adaptativo
1. Modificar los factores de ajuste en las configuraciones
2. Implementar nuevas lógicas de adaptación
3. Ajustar los umbrales de rendimiento

### Extender el Sistema de Bloques
1. Crear nuevas subclases de `Block`
2. Implementar la lógica específica en el método `execute`
3. Asegurar que interactúen correctamente con el contexto del problema

## Configuración Estándar de Niveles

La estructura JSON estándar para configurar niveles incluye:
- `level_id` y `segment_id`: Identificadores del nivel
- `difficulty`: Nivel de dificultad (1-5)
- `problem_context`: Estado inicial y objetivo del problema
- `constraints`: Limitaciones como tiempo y bloques permitidos
- `adaptive_parameters`: Parámetros para la adaptación automática

## Contribuciones

Las contribuciones son bienvenidas. Si deseas contribuir:
1. Haz un fork del proyecto
2. Crea una rama para tu característica (`git checkout -b feature/NuevaCaracteristica`)
3. Haz commit de tus cambios (`git commit -m 'Agrega alguna característica'`)
4. Sube a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

## Documentación Adicional

- `docs/engine.md`: Explicación detallada del motor de ejecución
- `docs/adaptive_agent_implementation.md`: Guía de implementación del agente adaptativo
- Documentación de API en comentarios del código

## Licencia

[Incluye la información sobre la licencia aquí]

## Contacto

[Incluye información de contacto o colaboradores principales]