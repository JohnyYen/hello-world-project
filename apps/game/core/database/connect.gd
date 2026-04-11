# Database
extends Node
class_name Connect

# Variable para la conexión a la base de datos
var db: SQLite = SQLite.new()

func _init() -> void:
	# 1. Especificar la ruta de la base de datos
	db.path = Env.DATABASE_URL  # Guarda la base de datos en la carpeta del usuario
	var first_execution = FileAccess.file_exists(Env.DATABASE_URL);
	# 2. Abrir la base de datos (se crea si no existe)
	if db.open_db() == true:
		print("Conexión a la base de datos establecida.")
		
		print(first_execution)
		if !first_execution:
			# 3. Crear las tablas
			print("Las tablas no existen")
			create_tables()
			run_seeds();
		else:
			print("Las tablas existen")
	else:
		print("Error al conectar a la base de datos.")

func run_seeds():
	var run_all_seeds_script = load("res://core/database/seed/run_all_seeds.gd")
	var seed_runner = run_all_seeds_script.new()
	seed_runner.run_all_seeds(db)



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
	"configuration" : {"data_type": "TEXT", "not_null": true}
	}
	
	db.create_table("Segments", segments_table)
	
func on_create_segment_block_table():
	var segment_blocks_table = {
	"segment_id": {"data_type": "INTEGER", "not_null": true, "foreign_key": {"table": "segments", "column": "segment_id"}},
	"block_id": {"data_type": "INTEGER", "not_null": true, "foreign_key": {"table": "blocks", "column": "block_id"}},
	"is_required": {"data_type": "INTEGER", "not_null": true}  # 0 para false, 1 para true
	}
	
	db.create_table("Segment_Blocks", segment_blocks_table)

	
	


	
