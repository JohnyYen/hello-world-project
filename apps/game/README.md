# Hello World Game 🎮

[![Godot Version](https://img.shields.io/badge/Godot-4.4-blue)](https://godotengine.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Mobile%2FDesktop-purple)](https://godotengine.org)
[![PRD](https://img.shields.io/badge/PRD-v0.1.0--draft-blue)](PRD.md)

**Hello World Game** es un videojuego educativo desarrollado en **Godot 4.4** diseñado para enseñar fundamentos de programación a través de una novela visual interactiva y puzzles de programación visual.

## 📖 Descripción del Proyecto

El juego funciona como una novela visual donde los estudiantes:
- Exploran una historia envolvente ambientada en una facultad de magia y tecnología
- Resuelven problemas del mundo real usando programación visual con bloques
- Reciben retroalimentación instantánea sobre su código
- Progresan a través de niveles que se adaptan automáticamente a su rendimiento

### Filosofía Educativa

El diseño del juego se fundamenta en tres pilares educativos definidos en el [PRD](PRD.md):

- **🏗️ Construccionismo (Papert)**: Los estudiantes construyen programas visuales para resolver problemas auténticos. Los bloques son "objetos para pensar" — representaciones tangibles de conceptos abstractos.
- **🎯 Aprendizaje por Maestría (Bloom)**: El agente adaptativo ajusta la dificultad dinámicamente para que cada estudiante progrese a su ritmo hacia el mismo estándar de dominio.
- **🔧 Aprender Haciendo (Dewey)**: No hay lecciones teóricas. Cada nivel presenta un problema, el estudiante construye una solución, la ejecuta, recibe feedback inmediato, itera y aprende.

### Características Principales

Las funcionalidades están priorizadas según el [PRD](PRD.md#3-catálogo-de-funcionalidades):

#### P0 — MVP / Lanzamiento
- 🎮 **Novela Visual** ([F-05](PRD.md#f-05-sistema-de-diálogos-y-narrativa)): Historia interactiva con diálogos y toma de decisiones
- 🧩 **Programación Visual** ([F-01](PRD.md#f-01-motor-de-programación-visual)): Bloques intuitivos para construir programas (Si, Mientras, Ejecutar)
- ⚙️ **Motor de Ejecución** ([F-03](PRD.md#f-03-motor-de-ejecución-execution-engine)): Intérprete que ejecuta y valida programas contra problemas del mundo real
- 📊 **Registro de Progreso** ([F-06](PRD.md#f-06-emisión-de-eventos-xapi)): Envía statements xAPI al backend para tracking de aprendizaje
- 💾 **Almacenamiento Local** ([F-04](PRD.md#f-04-almacenamiento-local-offline-sqlite)): SQLite offline-first con sincronización asíncrona
- 📖 **Sistema de Contexto** ([F-02](PRD.md#f-02-sistema-de-contexto-de-problemas-problem-context)): Problemas del mundo real con estado, reglas y condiciones de éxito

#### P1 — Post-MVP
- 🤖 **Agente Adaptativo** ([F-07](PRD.md#f-07-agente-adaptativo-adaptive-agent)): Ajusta la dificultad según el rendimiento del estudiante
- 🏗️ **Modo Sandbox** ([F-08](PRD.md#f-08-modo-sandbox)): Entorno abierto para experimentar sin objetivos fijos
- 📚 **Multi-Capítulo** ([F-09](PRD.md#f-09-soporte-multi-capítulo)): Progresión narrativa con capítulos desbloqueables

#### P2 — Futuro
- 🧩 **Bloques Personalizados** ([F-10](PRD.md#f-10-personalización-de-librería-de-bloques)): Profesores crean bloques de dominio específico
- 🏆 **Desafío entre Pares** ([F-11](PRD.md#f-11-modo-desafío-entre-pares)): Compartir soluciones y competir con restricciones

---

## 📋 Estado del Proyecto

| Funcionalidad | ID PRD | Prioridad | Estado |
|--------------|--------|-----------|--------|
| Motor de Programación Visual | [F-01](PRD.md#f-01-motor-de-programación-visual) | **P0** | ✅ Implementado |
| Sistema de Contexto de Problemas | [F-02](PRD.md#f-02-sistema-de-contexto-de-problemas-problem-context) | **P0** | ✅ Implementado |
| Motor de Ejecución | [F-03](PRD.md#f-03-motor-de-ejecución-execution-engine) | **P0** | ✅ Implementado |
| Almacenamiento Local SQLite | [F-04](PRD.md#f-04-almacenamiento-local-offline-sqlite) | **P0** | ✅ Implementado |
| Sistema de Diálogos y Narrativa | [F-05](PRD.md#f-05-sistema-de-diálogos-y-narrativa) | **P0** | ✅ Implementado |
| Emisión de Eventos xAPI | [F-06](PRD.md#f-06-emisión-de-eventos-xapi) | **P0** | ✅ Implementado |
| Agente Adaptativo | [F-07](PRD.md#f-07-agente-adaptativo-adaptive-agent) | **P1** | 🔄 En desarrollo |
| Modo Sandbox | [F-08](PRD.md#f-08-modo-sandbox) | **P1** | ⏳ Planificado |
| Soporte Multi-Capítulo | [F-09](PRD.md#f-09-soporte-multi-capítulo) | **P1** | ⏳ Planificado |
| Personalización de Bloques | [F-10](PRD.md#f-10-personalización-de-librería-de-bloques) | **P2** | 🔮 Futuro |
| Modo Desafío entre Pares | [F-11](PRD.md#f-11-modo-desafío-entre-pares) | **P2** | 🔮 Futuro |

> Para el detalle completo de requisitos, criterios de aceptación y dependencias, consultar el [PRD](PRD.md#3-catálogo-de-funcionalidades).

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
├── dialogue/               # Archivos de diálogo (.dialogue)
│   ├── C00/               # Capítulo 0
│   ├── C01/               # Capítulo 1
│   ├── Tutorial/          # Diálogos de tutorial
│   ├── Testing.dialogue   # Diálogos de testing
│   └── dialogue.dialogue  # Diálogos principales
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
│   ├── controllers/       # Controladores de lógica
│   ├── database/          # Repositorios SQLite
│   ├── engine/            # Motor de ejecución
│   ├── http/              # Clientes HTTP
│   ├── globals/           # Variables globales
│   ├── eventBus.gd        # Sistema de eventos globales
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
| `_GameConfig` | Configuración global del juego |
| `_GameState` | Estado del juego |
| `_GameController` | Controlador principal |
| `_FeedbackController` | Sistema de feedback |
| `_SaveController` | Persistencia de datos |
| `_DialogueUiController` | Controlador de UI de diálogos |
| `_Util` | Utilidades globales |

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
│  SaveController, DialogueUIController │
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
│          CLIENTE HTTP               │  scripts/http/
│     Comunicación con Backend        │
├─────────────────────────────────────┤
│        VARIABLES GLOBALES           │  scripts/globals/
│     GameConfig, GameState           │
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
| `/api/v1/sync/sessions` | POST | Crear sesión de sincronización |
| `/api/v1/sync/events` | POST | Registrar evento de sincronización |
| `/api/v1/sync/sessions/{id}/events` | GET | Obtener eventos de una sesión |
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
| [PRD.md](PRD.md) | Documento de Requisitos de Producto (autoritativo) |
| [docs/engine.md](docs/engine.md) | Motor de ejecución de código |
| [docs/adaptive_agent.md](docs/adaptive_agent.md) | Implementación del agente adaptativo |
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
