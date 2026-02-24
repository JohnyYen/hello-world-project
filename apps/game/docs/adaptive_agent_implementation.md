# Implementación del Agente Inteligente Adaptativo

## Introducción

Este documento describe cómo implementar un agente inteligente adaptativo que puede modificar las configuraciones de niveles de programación basándose en el rendimiento del estudiante. El agente está diseñado para ser flexible y reutilizable en cualquier nivel de programación dentro del juego.

## Arquitectura General

El agente adaptativo consiste en una clase principal (`AdaptiveAgent`) que interacciona con el sistema de niveles y las bases de datos del juego. La arquitectura se divide en:

1. **AdaptiveAgent**: El corazón del sistema, responsable de tomar decisiones de adaptación
2. **Sistema de Niveles**: Componentes que gestionan la configuración de niveles
3. **Sistema de Persistencia**: Componentes que almacenan la configuración en la base de datos

## Paso 1: Crear el Agente Adaptativo

Primero, crea la clase base del agente en `scripts/agent/adaptive_agent.gd`:

```gdscript
class_name AdaptiveAgent

# Esta clase se encarga de ajustar la dificultad de los niveles basándose en el rendimiento del estudiante

# Método para ajustar la configuración basándose en el rendimiento
func adjust_difficulty(current_config: Dictionary, student_performance: Dictionary) -> Dictionary:
    pass

# Método para calcular el puntaje de rendimiento
func calculate_performance_score(performance: Dictionary) -> float:
    pass

# Método para aumentar la dificultad
func increase_difficulty(config: Dictionary) -> Dictionary:
    pass

# Método para disminuir la dificultad
func decrease_difficulty(config: Dictionary) -> Dictionary:
    pass

# Método para guardar la nueva configuración en la base de datos
func update_level_config_in_db(level_id: int, segment_id: int, new_config: Dictionary):
    pass
```

## Paso 2: Estructura de Configuración Estándar

Define una estructura JSON estándar para representar la configuración de cualquier nivel:

```json
{
  "level_id": 1,
  "segment_id": 1,
  "difficulty": 1,
  "problem_context": {
    "initial_state": {
      "queue_size": 5,
      "available_resources": {
        "resource1": 10,
        "resource2": 5
      },
      "target_values": {
        "money_earned": 50,
        "items_processed": 10
      }
    },
    "constraints": {
      "max_blocks_allowed": 20,
      "time_limit": 120,
      "available_block_types": ["inicio", "fin", "if", "while", "execute"]
    }
  },
  "learning_objectives": [
    "understand_sequence",
    "use_conditionals",
    "implement_loops"
  ],
  "adaptive_parameters": {
    "success_threshold": 0.8,
    "time_adjustment_factor": 1.2,
    "resource_adjustment_factor": 1.1
  }
}
```

## Paso 3: Integrar el Agente en un Controlador de Nivel

En tu controlador de nivel, instancia el agente y úsalo para gestionar la configuración del nivel:

```gdscript
extends Node

var adaptive_agent: AdaptiveAgent

func _ready():
    adaptive_agent = AdaptiveAgent.new()
    
    # Cargar la configuración del nivel actual
    var current_config = load_level_config_from_db(level_id, segment_id)
    
    # Aplicar configuración al contexto del problema
    apply_config_to_problem_context(current_config)

# Función que se llama cuando el jugador completa un nivel
func on_level_completed(performance_data: Dictionary):
    # Cargar la configuración actual
    var current_config = load_level_config_from_db(level_id, segment_id)
    
    # Permitir que el agente ajuste la dificultad
    var new_config = adaptive_agent.adjust_difficulty(current_config, performance_data)
    
    # Guardar la nueva configuración en la base de datos
    adaptive_agent.update_level_config_in_db(level_id, segment_id + 1, new_config)
```

## Paso 4: Implementar la Lógica de Adaptación

Implementa las funciones del agente con la lógica específica:

### Calcular el Puntaje de Rendimiento

```gdscript
func calculate_performance_score(performance: Dictionary) -> float:
    var success_count = performance.get("success_count", 0)
    var total_attempts = performance.get("total_attempts", 1)
    var avg_time = performance.get("avg_time", 0)
    var optimal_time = performance.get("optimal_time", 100)
    
    var success_rate = float(success_count) / total_attempts
    var time_efficiency = min(optimal_time / max(1, avg_time), 1.0)
    
    # Se pondera más el éxito que la eficiencia de tiempo
    var performance_score = (success_rate * 0.7) + (time_efficiency * 0.3)
    
    return performance_score
```

### Aumentar Dificultad

```gdscript
func increase_difficulty(config: Dictionary) -> Dictionary:
    # Incrementa la dificultad basándose en los parámetros actuales
    if config.problem_context.initial_state.has("queue_size"):
        config.problem_context.initial_state.queue_size = int(
            config.problem_context.initial_state.queue_size * 
            config.adaptive_parameters.resource_adjustment_factor
        )
    
    # Aplica otros ajustes según sea necesario
    # ...
    
    return config
```

### Disminuir Dificultad

```gdscript
func decrease_difficulty(config: Dictionary) -> Dictionary:
    # Disminuye la dificultad basándose en los parámetros actuales
    if config.problem_context.initial_state.has("queue_size") and config.problem_context.initial_state.queue_size > 1:
        config.problem_context.initial_state.queue_size = max(1, int(
            config.problem_context.initial_state.queue_size / 
            config.adaptive_parameters.resource_adjustment_factor
        ))
    
    # Aplica otros ajustes según sea necesario
    # ...
    
    return config
```

### Ajustar Configuración Basándose en Rendimiento

```gdscript
func adjust_difficulty(current_config: Dictionary, student_performance: Dictionary) -> Dictionary:
    var new_config = current_config.duplicate(true)  # Hacer una copia profunda
    
    var performance_score = calculate_performance_score(student_performance)
    
    if performance_score >= current_config.adaptive_parameters.success_threshold:
        new_config = increase_difficulty(new_config)
    elif performance_score <= (current_config.adaptive_parameters.success_threshold - 0.2):
        new_config = decrease_difficulty(new_config)
    
    # Ajustar el nivel de dificultad general
    if performance_score >= 0.9:
        new_config.difficulty = min(new_config.difficulty + 1, 5)
    elif performance_score <= 0.6:
        new_config.difficulty = max(new_config.difficulty - 1, 1)
    
    return new_config
```

## Paso 5: Aplicar Configuración al Contexto del Problema

Crea una función que aplique la configuración a un contexto de problema específico:

```gdscript
func apply_config_to_problem_context(config: Dictionary):
    # Aplicar tamaño de cola
    if config.problem_context.initial_state.has("queue_size"):
        # Aplicar al contexto específico (cafetería, biblioteca, etc.)
        problem_context.set_queue_size(config.problem_context.initial_state.queue_size)
    
    # Aplicar recursos disponibles
    if config.problem_context.initial_state.has("available_resources"):
        problem_context.set_resources(config.problem_context.initial_state.available_resources)
    
    # Aplicar limitaciones
    if config.problem_context.constraints.has("time_limit"):
        problem_context.set_time_limit(config.problem_context.constraints.time_limit)
    
    # Aplicar otros parámetros según el contexto
    # ...
```

## Paso 6: Persistencia de Configuración

Implementa funciones para guardar y cargar configuraciones desde la base de datos:

```gdscript
func load_level_config_from_db(level_id: int, segment_id: int) -> Dictionary:
    # Lógica para cargar la configuración desde la base de datos
    # ...
    return config_dictionary

func save_level_config_to_db(level_id: int, segment_id: int, config: Dictionary):
    # Lógica para guardar la configuración en la base de datos
    # ...
```

## Consideraciones para la Flexibilidad

1. **Estructura Genérica**: La estructura JSON permite adaptar diferentes tipos de niveles manteniendo una base común.

2. **Parámetros Configurables**: Los parámetros de adaptación se pueden ajustar por nivel o globalmente para diferentes tipos de problemas.

3. **Extensibilidad**: Puedes añadir nuevos campos a la estructura de configuración según las necesidades específicas de cada tipo de nivel.

4. **Desacoplamiento**: El agente no necesita conocer la lógica interna de cada tipo de nivel, solo trabaja con la configuración estándar.

## Conclusión

Este sistema de agente adaptativo proporciona una forma flexible y escalable de personalizar la experiencia de aprendizaje en tu juego educativo. Al seguir esta arquitectura, puedes aplicar el mismo agente a diferentes tipos de niveles de programación, ajustando automáticamente la dificultad según el rendimiento del estudiante.