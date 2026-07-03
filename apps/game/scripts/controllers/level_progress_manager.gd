extends Node
class_name LevelProgressManager

## Singleton que gestiona la progresión de niveles con persistencia en JSON.
## Se registra como _LevelProgressManager en project.godot (autoload).
##
## Responsabilidades:
## - Persistencia local del progreso de niveles (user://levels_progress.json)
## - Lógica de desbloqueo: niveles 0 y 1 siempre unlocked, N requiere N-1 completado
## - Auto-guardado al completar un nivel
## - Nivel 0 (tutorial) se marca completado automáticamente en la primera carga

var _data: Dictionary = {}

func _ready() -> void:
	load_progress()


# =============================================================================
#                         API PÚBLICA
# =============================================================================

## Carga el progreso desde disco. Si no existe archivo, crea estado inicial.
func load_progress() -> void:
	if not FileAccess.file_exists(Env.LEVEL_PROGRESS_PATH):
		_init_default_progress()
		save_progress()
		print("[LevelProgressManager] Progreso inicial creado")
		return

	var file := FileAccess.open(Env.LEVEL_PROGRESS_PATH, FileAccess.READ)
	if not file:
		push_error("[LevelProgressManager] No se pudo leer el archivo de progreso")
		_init_default_progress()
		return

	var content := file.get_as_text()
	if content.is_empty():
		push_error("[LevelProgressManager] Archivo de progreso vacío — reiniciando")
		_init_default_progress()
		save_progress()
		return

	var parsed = JSON.parse_string(content)
	if typeof(parsed) != TYPE_DICTIONARY or not parsed.has("levels"):
		push_error("[LevelProgressManager] Archivo de progreso corrupto — reiniciando")
		_init_default_progress()
		save_progress()
		return

	_data = parsed
	print("[LevelProgressManager] Progreso cargado exitosamente")


## Persiste el estado actual a disco.
func save_progress() -> void:
	var json := JSON.stringify(_data, "\t")
	var file := FileAccess.open(Env.LEVEL_PROGRESS_PATH, FileAccess.WRITE)
	if file:
		file.store_string(json)
	else:
		push_error("[LevelProgressManager] No se pudo guardar el progreso")


## Indica si un nivel (identificado por segment_id) está desbloqueado.
## Regla: niveles 0 y 1 siempre desbloqueados.
##        Nivel N desbloqueado si N-1 está completado.
func is_level_unlocked(segment_id: int) -> bool:
	if segment_id <= 1:
		return true

	var prev_key := str(segment_id - 1)
	var prev_level = _data.get("levels", {}).get(prev_key, {})
	return prev_level.get("completed", false)


## Indica si un nivel ya fue completado.
func is_level_completed(segment_id: int) -> bool:
	var key := str(segment_id)
	var level = _data.get("levels", {}).get(key, {})
	return level.get("completed", false)


## Devuelve la cantidad de estrellas obtenidas en un nivel (0 si no completado).
func get_level_stars(segment_id: int) -> int:
	var key := str(segment_id)
	var level = _data.get("levels", {}).get(key, {})
	return level.get("stars", 0)


## Marca un nivel como completado. Auto-guarda a disco.
## stars: cantidad de estrellas (1-3). Por defecto 3.
func complete_level(segment_id: int, stars: int = 3) -> void:
	var key := str(segment_id)
	var levels: Dictionary = _data.get("levels", {})

	if not levels.has(key):
		push_warning("[LevelProgressManager] Nivel %d no existe en los datos — se creará" % segment_id)
		levels[key] = {}

	levels[key]["completed"] = true
	levels[key]["stars"] = stars

	# Si se completó el nivel 0, aseguramos que el segment 1 está accesible
	print("[LevelProgressManager] Nivel %d completado con %d estrella(s)" % [segment_id, stars])
	save_progress()


## Reinicia todo el progreso. Útil para testing.
func reset_progress() -> void:
	if FileAccess.file_exists(Env.LEVEL_PROGRESS_PATH):
		DirAccess.remove_absolute(Env.LEVEL_PROGRESS_PATH)
	_init_default_progress()
	save_progress()
	print("[LevelProgressManager] Progreso reiniciado")


# =============================================================================
#                         MÉTODOS INTERNOS
# =============================================================================

func _init_default_progress() -> void:
	_data = {
		"levels": {}
	}

	# Inicializar niveles 0 a 5
	for i in range(6):
		_data["levels"][str(i)] = {
			"completed": false,
			"stars": 0
		}

	# Nivel 0 (tutorial) siempre completado por defecto
	_data["levels"]["0"]["completed"] = true
	_data["levels"]["0"]["stars"] = 3
