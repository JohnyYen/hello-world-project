# Videojuego

## Hello World Game

**Hello World Game** es un videojuego educativo diseñado para enseñar fundamentos de programación a través de una novela visual y puzzles interactivos. El juego adapta su dificultad al rendimiento del estudiante mediante un agente inteligente que modifica dinámicamente los niveles, proporciona retroalimentación automática y registra el progreso en una base de datos.

### Características Principales

- **Aprendizaje Basado en Juegos**: Enseñanza de conceptos de programación a través de mecánicas de juego atractivas
- **Adaptación Inteligente**: Dificultad que se ajusta automáticamente según el rendimiento del estudiante
- **Novela Visual**: Historia envolvente que contextualiza los problemas de programación
- **Puzzles Interactivos**: Problemas del mundo real que se resuelven con programación visual
- **Registro de Progreso**: Seguimiento detallado del avance del estudiante
- **Sistema de Feedback Automático**: Respuestas inmediatas al código del estudiante

### Tecnología

- **Motor**: Godot Engine 4.x
- **Lenguaje**: GDScript
- **Base de datos**: SQLite (local)
- **Arquitectura**: MVC (Model-View-Controller)

---

## Estructura de carpetas

```
hello-world!!/
├── addons/           # Plugins de Godot
├── assets/           # Recursos: imágenes, sprites, sonidos
│   ├── background/
│   ├── character/
│   ├── music/
│   └── ui/
├── config/           # Configuraciones del juego
├── data/             # Base de datos local y configuraciones de niveles
│   └── levels/
├── dialogue/         # Diálogos de la novela visual
├── docs/             # Documentación del proyecto
├── models/           # Capa Models - Clases que se mapean en la base de datos
│   └── dto/
├── scenes/           # Capa View - Escenas y componentes de UI
│   ├── components/
│   └── pages/
├── scripts/          # Capa Controller - Lógica del juego
│   ├── agent/        # Agente inteligente adaptativo
│   ├── blocks/       # Implementaciones de bloques de programación
│   ├── controllers/  # Controladores de escenas
│   ├── database/     # Acceso a la base de datos
│   ├── engine/       # Motor de ejecución y contextos de problemas
│   ├── globals/      # Variables y estados globales
│   └── http/         # Cliente HTTP para sincronización
└── test/             # Pruebas del proyecto
    ├── integrations/
    └── unit/
```

---

## Convención de nombres

### Archivos

- **Scripts GDScript**: `snake_case.gd`
  - Ejemplos: `adaptive_agent.gd`, `execution_engine.gd`, `feedback_controller.gd`
  
- **Escenas Godot**: `snake_case.tscn`
  - Ejemplos: `main.tscn`, `root.tscn`, `dialogue_responses.tscn`

- **Clases (class_name)**: `PascalCase`
  - Ejemplos: `AdaptiveAgent`, `ExecutionEngine`, `CafeteriaProblemContext`

### Variables y Funciones

- **Variables**: `snake_case`
  - Ejemplos: `student_queue`, `cash_register`, `db`
  
- **Funciones**: `snake_case`
  - Ejemplos: `execute()`, `is_solution_correct()`, `create_tables()`

- **Constantes**: `SCREAMING_SNAKE_CASE`
  - Definidas en `env.gd` como `DATABASE_URL`, `API_BASE_URL`

### Jerarquía de Clases

- **Prefijos por tipo**:
  - Acciones: `XxxAction` (ej: `ServeDrinkAction`, `AttendStudentAction`)
  - Controladores: `XxxController` (ej: `FeedbackController`, `GameController`)
  - Bloques: `XxxBlock` (ej: `ExecutionBlock`, `IfBlock`, `WhileBlock`)
  - Repositorios: `XxxRepository` (ej: `BlockRepository`, `LevelRepository`)
  - Contextos: `XxxProblemContext` (ej: `CafeteriaProblemContext`)

---

## Linting, identación, formateo

### GDScript

- **Identación**: Tabs (estándar de Godot)
- **Comillas**: Dobles comillas para strings
- **Espacios alrededor de operadores**: 
  ```gdscript
  var result = a + b
  if x == y:
  ```
- **Espacios después de comas**:
  ```gdscript
  func my_func(a, b, c):
  ```

### Comentarios

- Comentarios en español para el código de negocio
- Comentarios TODO para tareas pendientes:
  ```gdscript
  extends Block # TODO: Revisar esta herencia a detalle
  ```

### Formato de Clases

```gdscript
class_name MiClase
extends Node

# Variables primero
var variable_publica
var _variable_privada

# Funciones de inicialización
func _init():
    pass

# Funciones públicas
func funcion_publica():
    pass

# Funciones privadas (prefijo _)
func _funcion_privada():
    pass
```

### Notas

- No se encontraron archivos de configuración de ESLint, Prettier ni herramientas similares
- El proyecto utiliza el formateo por defecto de Godot 4.x

---

## Manejo de errores

### Retorno de Diccionarios con Estado

El proyecto utiliza un patrón de retorno de diccionarios con campos `OK`, `error`, `status`:

```gdscript
# Ejemplo de HttpClient
def request(endpoint: String, ...) -> Dictionary:
    var err = client.connect_to_host(host, port)
    if err != OK:
        return { "OK": false, "error": "Error al conectar al host: %s" % err }
    
    if status_code >= 200 and status_code < 300:
        return { "OK": true, "status": status_code, "data": json_result }
    else:
        return { "OK": false, "status": status_code, "error": json_result }
```

### Manejo de Base de Datos

```gdscript
# Verificación de conexión
if db.open_db() == true:
    print("Conexión a la base de datos establecida.")
else:
    print("Error al conectar a la base de datos.")
```

### Valores por Defecto

```gdscript
# Manejo de campos faltantes en PerformanceAnalyzer
if !data.has("score"):
    data["score"] = 0.0
if !data.has("errors"):
    data["errors"] = 0
if !data.has("time"):
    data["time"] = 0.0
```

### Prints para Debugging

El proyecto utiliza extensivamente `print()` para logging durante desarrollo:
- Estado de conexiones
- Existencia de archivos
- Creación de tablas

### Validación de Archivos

```gdscript
var first_execution = FileAccess.file_exists(Env.DATABASE_URL)
if !first_execution:
    print("Las tablas no existen")
    create_tables()
```

---

## Pruebas

### Framework

- **GUT (Godot Unit Test)**: Framework de pruebas específico para Godot

### Estructura de Tests

```
test/
├── unit/                    # Tests unitarios
│   ├── agent/              # Tests del agente adaptativo
│   ├── blocks/             # Tests de bloques
│   ├── contexts/           # Tests de contextos (cafetería, biblioteca)
│   ├── engine/             # Tests del motor de ejecución
│   └── feedback/           # Tests del sistema de feedback
├── integrations/           # Tests de integración
│   ├── scenarios/          # Escenarios específicos
│   └── workflows/          # Flujos completos
├── fixtures/               # Datos de prueba
└── helpers/                # Utilidades de test
```

### Tipos de Tests Implementados

#### 1. Tests del Agente Adaptativo
- `test_adaptive_agent.gd`: Inicialización, ajuste de dificultad, límites
- `test_performance_analyzer.gd`: Normalización, promedios móviles
- `test_rule_based_inference.gd`: Motor de inferencia y reglas

#### 2. Tests del Motor de Ejecución
- `engine_test.gd`: Flujo completo de ejecución
- `simple_test.gd`: Funcionalidad básica

#### 3. Tests de Contextos
- `library_test.gd` y `library_test_corrected.gd`: Contexto de biblioteca

#### 4. Tests de Feedback
- `test_feedback_controller.gd`: Procesamiento y generación
- `test_feedback_controller_visual.gd`: Aspectos visuales y señales

#### 5. Tests de Repositorios
- `test_block_repository.gd`: Acceso a base de datos

#### 6. Tests de Controladores
- `test_dialogue_controller.gd`: Carga de diálogos JSON
- `test_http_client.gd`: Comunicación HTTP

#### 7. Tests de Integración
- `test_code_space.gd`: Espacio de código (UI + lógica)

### Ejemplo de Test

```gdscript
extends GutTest

func test_agent_adjusts_difficulty_up():
    var agent = AdaptiveAgent.new()
    var data = {
        "score": 0.9,
        "errors": 1,
        "time": 60.0,
        "avg_score": 0.85
    }
    var initial_difficulty = agent.difficulty
    agent.adjust_difficulty(data)
    assert_gt(agent.difficulty, initial_difficulty)
```

### Ejecución de Tests

Los tests se ejecutan desde el editor de Godot utilizando el plugin GUT.

### Cobertura

El proyecto cuenta con:
- **12 suites de tests** documentadas
- Tests para todos los componentes críticos (agente, motor, feedback)
- Tests de integración para flujos completos
- Mocks para aislar componentes (MockSQLite)
