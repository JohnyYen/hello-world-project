# Database
extends Node
class_name Connect

# Variable para la conexión a la base de datos
var db: SQLite = SQLite.new()

func _init() -> void:
	# 1. Especificar la ruta de la base de datos
	db.path = Env.DATABASE_URL  # Guarda la base de datos en la carpeta del usuario
	var is_first_run = !FileAccess.file_exists(Env.DATABASE_URL);
	# 2. Abrir la base de datos (se crea si no existe)
	if db.open_db() == true:
		print("Conexion a la base de datos establecida.")
		
		# 3. Siempre crear/actualizar tablas (CREATE TABLE IF NOT EXISTS es seguro)
		create_tables()
		
		# 4. Migration: agregar adaptation_state column a Segments existentes
		_migrate_adaptation_state()

		# 5. Fixup: agregar segment_type faltante en segmentos existentes
		_fixup_segment_types()
		
		# 6. Insertar feedback de introduccion si la tabla esta vacia
		_seed_intro_feedback_if_empty()
		
		if is_first_run:
			# 7. Seeds solo en primera ejecucion
			print("Primera ejecucion: insertando datos iniciales.")
			run_seeds();
		else:
			print("Base de datos existente, tablas actualizadas.")
	else:
		print("Error al conectar a la base de datos.")

func run_seeds():
	var run_all_seeds_script = load("res://scripts/database/seed/run_all_seeds.gd")
	var seed_runner = run_all_seeds_script.new()
	seed_runner.run_all_seeds(db)


func _seed_intro_feedback_if_empty() -> void:
	var rows = db.select_rows("professor_feedback", "", ["id"], "1")
	if rows.is_empty():
		var data = {
			"id": "intro-feedback-001",
			"student_id": "",
			"professor_id": "system",
			"professor_name": "Sistema",
			"comments": "Fortalezas: Este es tu primer feedback! Aca vas a ver los comentarios que tu profesor te deja sobre tu desempeno.\nAreas de mejora: Revisa esta seccion para identificar en que podes mejorar.\nComentarios adicionales: Presta atencion a las recomendaciones de tu profesor para aprovechar al maximo cada nivel.",
			"rating": 0,
			"feedback_type": "message",
			"course_id": "",
			"game_id": "",
			"level_id": "",
			"display_in_game": 1,
			"acknowledged_at": "",
			"is_read": 0,
			"created_at": "2026-01-01T00:00:00",
			"updated_at": "2026-01-01T00:00:00"
		}
		db.insert_row("professor_feedback", data)
		print("Seed: Feedback de introduccion insertado.")


# Migration: agrega adaptation_state column a la tabla Segments si no existe
# Es idempotente: usa sqlite_master para verificar si la columna ya esta presente
func _migrate_adaptation_state() -> void:
	var create_sql_rows := db.select_rows("sqlite_master", "type = 'table' AND name = 'Segments'", ["sql"])
	if create_sql_rows.is_empty():
		return

	var create_sql: String = create_sql_rows[0].get("sql", "")
	if "adaptation_state" in create_sql:
		return

	var alter_sql := "ALTER TABLE Segments ADD COLUMN adaptation_state TEXT"
	if db.query(alter_sql):
		print("Migration: Columna 'adaptation_state' agregada a la tabla Segments")
	else:
		push_error("Migration: No se pudo agregar la columna 'adaptation_state' a Segments")


# Fixup: agrega segment_type faltante en segmentos existentes
# Corre siempre (no solo en primera ejecución) y es idempotente
func _fixup_segment_types() -> void:
	var SeedScript = load("res://scripts/database/seed/seed_segments.gd")
	var seed = SeedScript.new()
	seed.fixup_segment_types(db)


# Función para crear las tablas
func create_tables() -> void:
	# Tabla: Players
	on_create_player_table();
	
	# Tabla: Level
	on_create_level_table();

	# Tabla: Segments
	on_create_segment_table()
	
	# Tabla: Progress
	on_create_progress_table();

	# Tabla: Block_types
	on_create_block_types_table();
	
	
	# Tabla: Blocks
	on_create_block_table();

	# Tabla: Segment_Blocks
	on_create_segment_block_table();

	# Tabla: xAPI
	on_create_xapi_tables();

	# Tabla: Game Session Cache
	on_create_game_session_table();

	# Tabla: Professor Feedback
	on_create_professor_feedback_table();

	print("Tablas creadas correctamente.")
	
	

func on_create_player_table():
	var table = {
		"user_id" : {"data_type": "text", "primary_key": true, "not_null":true},
		"username": {"data_type": "text"},
		"password": {"data_type": "text"}
	}
	
	db.create_table("Players", table)
	
func on_create_block_types_table():
	var block_types_table = {
		"block_type_id": {"data_type": "INTEGER", "primary_key": true, "not_null": true},
		"block_type": {"data_type": "TEXT", "not_null": true}
	}
	
	db.create_table("Block_Types", block_types_table)
	
func on_create_block_table():
	var blocks_table = {
	"block_id": {"data_type": "INTEGER", "primary_key": true, "not_null": true},
	"block_type_id": {"data_type": "INTEGER", "not_null": true, "foreign_key": {"table": "block_types", "column": "tipo_bloque_id"}},
	"description": {"data_type": "TEXT"},
	"name": {"data_type": "TEXT", "not_null": true}
	}
	
	db.create_table("Blocks", blocks_table)
	
func on_create_level_table():
	var levels_table = {
	"level_id": {"data_type": "INTEGER", "primary_key": true, "not_null": true},
	"real_problem": {"data_type": "TEXT", "not_null": true},
	"title": {"data_type": "TEXT", "not_null": true},
	"goal": {"data_type": "TEXT", "not_null": true}
	}
	
	db.create_table("Levels", levels_table)
	
	
func on_create_progress_table():
	var progress_table = {
	"progress_id": {"data_type": "INTEGER", "primary_key": true, "not_null": true},
	"user_id": {"data_type": "TEXT", "not_null": true, "foreign_key": {"table": "players", "column": "user_id"}},
	"segment_id": {"data_type": "INTEGER", "not_null": true, "foreign_key": {"table": "segments", "column": "segment_id"}},
	"attemptat": {"data_type": "INTEGER", "not_null": true},
	"time_in_complete": {"data_type": "REAL", "not_null": true},
	"complete": {"data_type": "INTEGER", "not_null": true},  # 0 para false, 1 para true
	"last_try": {"data_type": "TEXT", "not_null": true}  # Fecha como texto
	}
	
	db.create_table("Progress", progress_table)
	
func on_create_segment_table():
	var segments_table = {
	"segment_id": {"data_type": "INTEGER", "primary_key": true, "not_null": true},
	"level_id": {"data_type": "INTEGER", "not_null": true},
	"problem": {"data_type": "TEXT", "not_null": true},
	"goal": {"data_type": "TEXT", "not_null": true},
	"position": {"data_type": "INTEGER", "not_null": true},
	"difficulty": {"data_type": "TEXT", "not_null": true},
	"configuration" : {"data_type": "TEXT", "not_null": true},
	"adaptation_state": {"data_type": "TEXT"}
	}
	
	db.create_table("Segments", segments_table)
	
func on_create_segment_block_table():
	var segment_blocks_table = {
	"segment_id": {"data_type": "INTEGER", "not_null": true, "foreign_key": {"table": "segments", "column": "segment_id"}},
	"block_id": {"data_type": "INTEGER", "not_null": true, "foreign_key": {"table": "blocks", "column": "block_id"}},
	"is_required": {"data_type": "INTEGER", "not_null": true}
	}

	db.create_table("Segment_Blocks", segment_blocks_table)

func on_create_game_session_table() -> void:
	# Tabla singleton para cachear game_id e instance_id del backend
	# Usa id=1 como fila única (patrón singleton)
	var game_session_table = {
		"id": {"data_type": "INTEGER", "primary_key": true, "not_null": true},
		"game_id": {"data_type": "TEXT", "not_null": true},
		"instance_id": {"data_type": "TEXT", "not_null": true},
		"student_id": {"data_type": "TEXT"},
		"created_at": {"data_type": "TEXT", "not_null": true},
		"updated_at": {"data_type": "TEXT", "not_null": true}
	}

	db.create_table("game_session", game_session_table)

func on_create_xapi_tables() -> void:
	var migration_script := load("res://scripts/database/migrations/001_create_xapi_tables.gd")
	var migration = migration_script.new()
	migration.run(db)
	
	# Tabla: Raw Stats (for offline-first stats tracking)
	on_create_raw_stats_table()

func on_create_raw_stats_table() -> void:
	var migration_script := load("res://scripts/database/migrations/002_create_raw_stats_table.gd")
	var migration = migration_script.new()
	migration.run(db)


func on_create_professor_feedback_table() -> void:
	var table = {
		"id": {"data_type": "text", "primary_key": true, "not_null": true},
		"student_id": {"data_type": "text"},
		"professor_id": {"data_type": "text"},
		"professor_name": {"data_type": "text"},
		"comments": {"data_type": "text", "not_null": true},
		"rating": {"data_type": "integer"},
		"feedback_type": {"data_type": "text"},
		"course_id": {"data_type": "text"},
		"game_id": {"data_type": "text"},
		"level_id": {"data_type": "text"},
		"display_in_game": {"data_type": "integer"},
		"acknowledged_at": {"data_type": "text"},
		"is_read": {"data_type": "integer", "not_null": true, "default": 0},
		"created_at": {"data_type": "text"},
		"updated_at": {"data_type": "text"}
	}

	db.create_table("professor_feedback", table)
	
