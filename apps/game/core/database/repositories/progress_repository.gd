class_name ProgressRepository

## A repository to handle database operations for progress tracking.

# Conexión a la base de datos SQLite
var _db: SQLite

# Inicializar la conexión a la base de datos
func _init() -> void:
	_db = SQLite.new()
	_db.path = Env.DATABASE_URL
	if !_db.open_db():
		push_error("No se pudo abrir la base de datos.")

## Creates a new progress entry in the database.
## @param progress_data: ProgressData object containing user_id, segment_id, attemptat, time_in_complete, complete, and last_try
## @return: The ID of the inserted row or -1 if the insert failed
func create_progress(progress_data : ProgressData) -> int:
	var query = """INSERT INTO Progress (user_id, segment_id, attemptat, time_in_complete, complete, last_try) VALUES (?, ?, ?, ?, ?, ?)"""
	var values = [
		progress_data.user_id,
		progress_data.segment_id,
		progress_data.attemptat,
		progress_data.time_in_complete,
		progress_data.complete,
		progress_data.last_try
	]
	
	var result = _db.query_with_values(query, values)
	if result:
		return _db.get_last_insert_rowid()
	else:
		push_error("Error inserting progress: " + _db.get_error_message())
		return -1

## Retrieves progress data for a specific user and segment.
## @param user_id: ID of the user whose progress is being retrieved
## @param segment_id: ID of the segment whose progress is being retrieved
## @return: ProgressData object containing the progress data or null if not found
func get_progress_by_segment(segment_id) -> ProgressData:
	var query = """SELECT * FROM Progress WHERE segment_id = ?"""
	var values = [segment_id]
	var result = _db.query_with_values(query, values)
	if result:
		if _db.fetch_row():
			var progress = ProgressData.new()
			progress.progress_id = _db.get_data("progress_id")
			progress.user_id = _db.get_data("user_id")
			progress.segment_id = _db.get_data("segment_id")
			progress.attemptat = _db.get_data("attemptat")
			progress.time_in_complete = _db.get_data("time_in_complete")
			progress.complete = _db.get_data("complete")
			progress.last_try = _db.get_data("last_try")
			return progress
		else:
			return null
	else:
		push_error("Error retrieving progress: " + _db.get_error_message())
		return null

## Updates an existing progress entry in the database.
## @param progress_data: ProgressData object containing progress_id and fields to update
## @return: True if update was successful, false otherwise
func update_progress(progress_data : ProgressData) -> bool:
	var query = """UPDATE Progress SET user_id = ?, segment_id = ?, attemptat = ?, time_in_complete = ?, complete = ?, last_try = ? WHERE progress_id = ?"""
	var values = [
		progress_data.user_id,
		progress_data.segment_id,
		progress_data.attemptat,
		progress_data.time_in_complete,
		progress_data.complete,
		progress_data.last_try,
		progress_data.progress_id
	]
	
	var result = _db.query_with_values(query, values)
	if result:
		return true
	else:
		push_error("Error updating progress: " + _db.get_error_message())
		return false

## Retrieves all progress entries for a specific user.
## @param user_id: ID of the user whose progress is being retrieved
## @return: Array of ProgressData objects containing the progress data
func get_all_progress_by_user():
	var query = """SELECT * FROM Progress"""
	
	var result = _db.query_with_values(query)
	var progress_list = []
	
	if result:
		while _db.fetch_row():
			var progress = ProgressData.new()
			progress.progress_id = _db.get_data("progress_id")
			progress.user_id = _db.get_data("user_id")
			progress.segment_id = _db.get_data("segment_id")
			progress.attemptat = _db.get_data("attemptat")
			progress.time_in_complete = _db.get_data("time_in_complete")
			progress.complete = _db.get_data("complete")
			progress.last_try = _db.get_data("last_try")
			progress_list.append(progress)
		return progress_list
	else:
		push_error("Error retrieving progress: " + _db.get_error_message())
		return []