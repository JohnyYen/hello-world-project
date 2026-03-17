# Hello World Game 🎮

[![Godot Version](https://img.shields.io/badge/Godot-4.4-blue)](https://godotengine.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Mobile%2FDesktop-purple)](https://godotengine.org)

**Hello World Game** es un videojuego educativo desarrollado en **Godot 4.x** diseñado para enseñar fundamentos de programación a través de una novela visual interactiva y puzzles de programación visual.

## 📖 Descripción del Proyecto

El juego funciona como una novela visual donde los estudiantes:
- Exploran una historia envolvente ambientada en una facultad de magia y tecnología
- Resuelven problemas del mundo real usando programación visual con bloques
- Reciben retroalimentación instantánea sobre su código
- Progresan a través de niveles que se adaptan automáticamente a su rendimiento

### Características Principales

- 🎮 **Novela Visual**: Historia interactiva con diálogos y toma de decisiones
- 🧩 **Programación Visual**: Bloques intuitivos para construir programas (if, while, execute)
- 🤖 **Agente Adaptativo**: Ajusta la dificultad según el rendimiento del estudiante
- 📊 **Registro de Progreso**: Envía xAPI statements al backend
- 🔄 **Sincronización**: Guarda progreso local y sincroniza con el servidor
- 🌍 **Multidioma**: Interfaz y diálogos en español

---

## 🛠️ Tech Stack

| Tecnología | Propósito |
|------------|-----------|
| **Godot 4.4** | Motor del juego |
| **GDScript 2.0** | Lenguaje de scripting |
| **SQLite** | Base de datos local |
| **GUT** | Testing unitario |
| **Dialogue Manager** | Sistema de diálogos |
| **godot-sqlite** | Acceso a SQLite |

---

## 📁 Estructura del Proyecto

```
apps/game/
├── .godot/                  # Archivos de Godot (no versionar)
├── addons/                  # Plugins (Dialogue Manager, SQLite, GUT)
├── assets/                  # Recursos: sprites, sonidos, fuentes
│   ├── backgrounds/         # Fondos
│   ├── characters/         # Personajes
│   ├── fonts/              # Fuentes
│   ├── images/             # Imágenes generales
│   ├── sprites/           # Spritesheets
│   └── ui/                # Elementos de UI
├── config/                 # Configuraciones del juego
│   └── game_config.gd     # Constantes globales
├── data/                   # Base de datos SQLite
├── dialogue/               # Archivos de diálogo (YAML/JSON)
│   ├── C00/               # Capítulo 0
│   ├── C01/               # Capítulo 1
│   └── Tutorial/          # Diálogos de tutorial
├── docs/                   # Documentación técnica
│   ├── engine.md          # Motor de ejecución
│   ├── nivel_1_design.md  # Diseño del nivel 1
│   └── adaptive_agent.md  # Agente adaptativo
├── models/                 # Recursos (triggers, inventory items)
├── scenes/                 # Escenas (.tscn)
│   ├── levels/            # Niveles de juego
│   ├── components/        # Componentes reutilizables
│   ├── ui/                # Interfaces de usuario
│   └── main.tscn          # Escena principal
├── scripts/                # Código GDScript
│   ├── agent/             # Agente adaptativo
│   ├── blocks/            # Bloques de programación
│   ├── controllers/        # Controladores de lógica
│   ├── database/          # Repositorios SQLite
│   ├── engine/            # Motor de ejecución
│   ├── eventBus.gd        # Sistema de eventos globales
│   ├── globals/           # Variables globales
│   └── util.gd            # Utilidades
├── test/                   # Pruebas GUT
├── project.godot           # Configuración del proyecto
└── README.md               # Este archivo
```

---

## 🚀 Getting Started

### Prerrequisitos

- **Godot Engine 4.4** (versiones 4.x deberían funcionar)
- **Git**

### Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/hello-world-project.git
   cd hello-world-project/apps/game
   ```

2. **Abrir en Godot:**
   - Ejecutar Godot Engine 4.4
   - Click en "Importar"
   - Seleccionar la carpeta `apps/game`
   - Click en "Importar y Editar"

3. **Ejecutar el juego:**
   - Presionar F5 o click en el botón de "Play"
   - Seleccionar `main.tscn` como escena principal

### Configuración de Desarrollo

El proyecto incluye varios **autoloads** (singletons) que se cargan al iniciar:

| Autoload | Descripción |
|----------|-------------|
| `Env` | Variables de entorno y configuración |
| `DialogueManager` | Sistema de diálogos |
| `EventBus` | Comunicación entre nodos |
| `_GameConfig` | Configuración global |
| `_GameState` | Estado del juego |
| `_GameController` | Controlador principal |
| `_FeedbackController` | Sistema de feedback |
| `_SaveController` | Persistencia de datos |

---

## 🎮 Arquitectura del Juego

### Capas del Sistema

```
┌─────────────────────────────────────┐
│           ESCENAS (UI)              │  scenes/
│   Menús, Niveles, Componentes UI   │
├─────────────────────────────────────┤
│         CONTROLADORES               │  scripts/controllers/
│  GameController, FeedbackController │
├─────────────────────────────────────┤
│        MOTOR DE EJECUCIÓN          │  scripts/engine/
│    ExecutionEngine, ProblemContext  │
├─────────────────────────────────────┤
│       SISTEMA DE BLOQUES            │  scripts/blocks/
│     Block, IfBlock, WhileBlock      │
├─────────────────────────────────────┤
│      AGENTE ADAPTATIVO              │  scripts/agent/
│         AdaptiveAgent               │
├─────────────────────────────────────┤
│         REPOSITORIOS                │  scripts/database/
│     LevelRepository, ProgressRepo   │
├─────────────────────────────────────┤
│          BASE DE DATOS              │  data/*.db
│              SQLite                 │
└─────────────────────────────────────┘
```

### Flujo del Juego

```
[Inicio] → [Menú Principal] → [Seleccionar Capítulo]
                                      ↓
                              [Cargar Nivel]
                                      ↓
                        [Novela Visual / Tutorial]
                                      ↓
                          [Resolver Puzzle]
                                      ↓
                    [Ejecutar Código con Bloques]
                                      ↓
                    [Feedback (Éxito/Fallo)]
                                      ↓
                    [Guardar Progreso]
                                      ↓
                    [Sincronizar con Backend]
```

---

## 🧩 Sistema de Programación Visual

### Tipos de Bloques

| Bloque | Descripción |
|--------|-------------|
| `Start` / `End` | Delimitadores del programa |
| `If` | Condicional simple |
| `While` | Bucle while |
| `Execute` | Acción específica del dominio |
| `Variable` | Asignación de variables |

### Ejemplo de Programa

```
[Start]
    [While] cola_no_vacia:
        [If] clientes_esperando > 5:
            [Execute] atender_rapido()
        [Else]:
            [Execute] atender_normal()
[End]
```

---

## 🔄 Integración con Backend

El juego se comunica con el backend FastAPI para:

1. **Autenticación**: Login de estudiantes
2. **Sincronización**: Guardar/cargar progreso
3. **xAPI Statements**: Registrar eventos de aprendizaje

### Endpoints Utilizados

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/v1/auth/login` | POST | Autenticar estudiante |
| `/api/v1/game-instances` | POST | Crear instancia de juego |
| `/api/v1/sync/sessions` | POST | Iniciar sesión de sync |
| `/api/v1/sync/events` | POST | Registrar evento |
| `/api/v1/statements/xapi` | POST | Enviar statement xAPI |

---

## 🧪 Testing

El proyecto utiliza **GUT** (Godot Unit Test) para pruebas unitarias.

### Ejecutar Tests

1. Abrir el proyecto en Godot
2. Ir a `Project` → `Project Tools` → `GUT Panel`
3. Click en "Run All"

O desde línea de comandos:
```bash
godot --headless -s addons/gut/gut_cmdline.gd -gdir=res://test/
```

### Estructura de Tests

```
test/
├── test_blocks/
│   ├── test_if_block.gd
│   └── test_while_block.gd
├── test_engine/
│   └── test_execution_engine.gd
└── test_agent/
    └── test_adaptive_agent.gd
```

---

## 📝 Convenciones de Código

### GDScript

```gdscript
# ✅ CORRECTO: Type hints explícitos
var player_name: String = "Estudiante"
var score: int = 0

func move_player(direction: Vector2) -> void:
    position += direction * speed

# ❌ INCORRECTO: Sin tipos
var player_name = "Estudiante"
func move_player(direction):
    position += direction * speed
```

### Nomenclatura

- **Clases**: PascalCase (`GameController`)
- **Funciones**: snake_case (`move_player`)
- **Constantes**: UPPER_SNAKE_CASE (`MAX_SPEED`)
- **Señales**: past_tense con prefijo (`signal game_started`)

### Patrón MVC

```
scenes/           → View (qué se ve)
scripts/controllers/ → Controller (lógica)
scripts/database/ → Model (datos)
```

---

## 📚 Documentación Adicional

| Documento | Descripción |
|-----------|-------------|
| [docs/engine.md](docs/engine.md) | Motor de ejecución de código |
| [docs/adaptive_agent.md](docs/adaptive_agent.md) | Implementación del agente |
| [docs/nivel_1_design.md](docs/nivel_1_design.md) | Diseño del nivel 1 |
| [LEVEL_1_DEVELOPMENT_ROADMAP.md](LEVEL_1_DEVELOPMENT_ROADMAP.md) | Roadmap de desarrollo |

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Por favor lee nuestra guía de contribuciones antes de enviar PRs.

1. Fork el repositorio
2. Crea tu rama (`git checkout -b feature/NuevaCaracteristica`)
3. Commit tus cambios (`git commit -m 'Agrega feature'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

---

## 🌍 Links

- **Website**: [hello-world-project.dev](https://hello-world-project.dev)
- **Frontend**: [github.com/.../apps/frontend](https://github.com/tu-usuario/hello-world-project/apps/frontend)
- **Backend**: [github.com/.../apps/backend](https://github.com/tu-usuario/hello-world-project/apps/backend)
- **API Client**: [github.com/.../packages/api-client-ts](https://github.com/tu-usuario/hello-world-project/packages/api-client-ts)
