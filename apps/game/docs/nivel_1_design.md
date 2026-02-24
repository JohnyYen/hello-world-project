# Diseño del Nivel 1 - Cafetería Universitaria

## Layout General del Nivel

```
┌─────────────────────────────────────────────────────────┐
│  Barra de herramientas                                  │
├────────────────────┬────────────────────────────────────┤
│                    │  ┌─────────────────────────────┐   │
│                    │  │                             │   │
│                    │  │     C O D E S P A C E     │   │
│                    │  │                             │   │
│                    │  │                             │   │
│                    │  │                             │   │
│                    │  │        (Área para          │   │
│    ÁREA DEL        │  │    arrastrar bloques)      │   │
│   PROBLEMA         │  │                             │   │
│                    │  └─────────────────────────────┘   │
│                    │                                    │
│                    │                                    │
│                    │                                    │
│                    │                                    │
│                    │                                    │
│                    │                                    │
│                    │                                    │
└────────────────────┴────────────────────────────────────┘
```

## Elementos del Nivel 1

### 1. Área del Problema (Izquierda)
- **Representación visual de la cafetería**
  - Cola de clientes con sus pedidos
  - Dispensadores de ingredientes (pan, queso, café, té)
  - Área de preparación
  - Caja registradora
- **Descripción del problema**
  - Texto que explica qué debe hacer el jugador
  - Objetivo del segmento actual
- **Botones de control**
  - "Ejecutar": Para correr el programa construido
  - "Reiniciar": Para limpiar el CodeSpace
  - "Siguiente": Para avanzar al siguiente segmento

### 2. CodeSpace (Derecha)
- **Área de trabajo** donde se construyen los programas visuales
- **Contiene** los bloques arrastrados por el jugador
- **Muestra** visualmente la secuencia de instrucciones

### 3. Paleta de Bloques
- **Ubicación**: Generalmente en la parte superior o lateral izquierdo
- **Contiene** los bloques disponibles para el nivel:
  - Bloque "Inicio"
  - Bloque "Fin"
  - Bloques "Ejecutar" con diferentes acciones:
    * "Tomar pan"
    * "Tomar queso"
    * "Hacer sándwich"
    * "Tomar café"
    * "Entregar producto"
    * "Cobrar cliente"

## Flujo de Interacción

### Inicialización del Nivel
1. El `LevelOneController` carga el segmento actual
2. Inicializa el `CafeteriaProblemContext` con los valores específicos del segmento
3. Muestra la representación visual de la cafetería con los elementos iniciales
4. Presenta la descripción del problema al jugador

### Interacción del Jugador
1. El jugador arrastra bloques desde la paleta al CodeSpace
2. Organiza los bloques en el orden que considera correcto
3. Presiona "Ejecutar" para correr el programa

### Procesamiento del Programa
1. El `ExecutionEngine` toma los bloques del CodeSpace
2. Ejecuta el programa y actualiza el `CafeteriaProblemContext`
3. Se actualiza la representación visual de la cafetería
4. Se verifica si se cumplió el objetivo del segmento

### Validación y Feedback
1. Si se cumple el objetivo → Avanzar al siguiente segmento
2. Si no se cumple → Mostrar feedback y permitir otro intento
3. El `AdaptiveAgent` puede ajustar la dificultad para el próximo intento

## Implementación Sugerida

### Estructura de Escena
- `LevelOne.tscn` como escena principal
  - `CafeteriaArea` como nodo para el área del problema
  - `CodeSpace` como nodo para la sección de código
  - `BlockPalette` como nodo para la paleta de bloques
  - `LevelController` como nodo controlador del nivel

### Código del Controlador
```gdscript
class_name LevelOneController
extends Node

var current_segment: int = 1
var problem_context: CafeteriaProblemContext
var execution_engine: ExecutionEngine

func _ready():
    load_segment(current_segment)

func load_segment(segment_number: int):
    # Inicializa el contexto del problema
    problem_context = CafeteriaProblemContext.new()
    configure_segment(segment_number)
    
    # Actualiza la representación visual
    update_visual_representation()
    
    # Inicializa el CodeSpace
    initialize_codespace()

func execute_program():
    var blocks = get_blocks_from_codespace()
    var result_context = execution_engine.execute(blocks, problem_context)
    
    if result_context.is_solution_correct():
        handle_success()
    else:
        handle_failure()

func handle_success():
    if current_segment < 6:
        current_segment += 1
        load_segment(current_segment)
    else:
        # Nivel completado
        emit_signal("level_completed")

func handle_failure():
    # Proporcionar feedback al jugador
    show_feedback_message("Tu programa no resolvió el problema. Intenta otra vez.")
```

## Consideraciones de Diseño

1. **Visualización clara**: La representación de la cafetería debe ser intuitiva y reflejar el estado actual
2. **Retroalimentación inmediata**: Mostrar claramente qué está sucediendo cuando se ejecuta el código
3. **Gradualidad**: Cada segmento debe introducir un concepto nuevo sin abrumar al jugador
4. **Adaptabilidad**: El nivel debe poder ajustarse a diferentes niveles de habilidad
5. **Accesibilidad**: Asegurar que todos los elementos sean fáciles de usar y entender