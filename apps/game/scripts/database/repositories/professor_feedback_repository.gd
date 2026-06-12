class_name ProfessorFeedbackRepository

const TABLE_NAME: String = "professor_feedback"

var _db: SQLite


func _init() -> void:
	_db = SQLite.new()
	_db.path = Env.DATABASE_URL
	if !_db.open_db():
		push_error("No se pudo abrir la base de datos.")


func insert_all(items: Array[ProfessorFeedback]) -> bool:
	if items.is_empty():
		return true

	_db.query("BEGIN TRANSACTION")
	for item in items:
		var query := """INSERT OR IGNORE INTO %s (
			id, student_id, professor_id, professor_name, comments, rating,
			feedback_type, course_id, game_id, level_id, display_in_game,
			acknowledged_at, is_read, created_at, updated_at
		) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""" % TABLE_NAME
		var values := [
			item.id,
			item.student_id,
			item.professor_id,
			item.professor_name,
			item.comments,
			item.rating,
			item.feedback_type,
			item.course_id,
			item.game_id,
			item.level_id,
			1 if item.display_in_game else 0,
			item.acknowledged_at,
			1 if item.is_read else 0,
			item.created_at,
			item.updated_at
		]
		if not _db.query_with_bindings(query, values):
			_db.query("ROLLBACK")
			return false
	_db.query("COMMIT")
	return true


func get_unread() -> Array[ProfessorFeedback]:
	var rows: Array = _db.select_rows(
		TABLE_NAME,
		"is_read = 0",
		[
			"id", "student_id", "professor_id", "professor_name", "comments",
			"rating", "feedback_type", "course_id", "game_id", "level_id",
			"display_in_game", "acknowledged_at", "is_read", "created_at", "updated_at"
		]
	)
	return _rows_to_feedback_list(rows)


func get_all() -> Array[ProfessorFeedback]:
	var rows: Array = _db.select_rows(
		TABLE_NAME,
		"",
		[
			"id", "student_id", "professor_id", "professor_name", "comments",
			"rating", "feedback_type", "course_id", "game_id", "level_id",
			"display_in_game", "acknowledged_at", "is_read", "created_at", "updated_at"
		]
	)
	return _rows_to_feedback_list(rows)


func mark_as_read(feedback_id: String) -> bool:
	var query := "UPDATE %s SET is_read = 1 WHERE id = ?" % TABLE_NAME
	return _db.query_with_bindings(query, [feedback_id])


func mark_all_as_read() -> bool:
	var query := "UPDATE %s SET is_read = 1 WHERE is_read = 0" % TABLE_NAME
	return _db.query(query)


func count_unread() -> int:
	var query := "SELECT COUNT(*) AS cnt FROM %s WHERE is_read = 0" % TABLE_NAME
	var result = _db.query_with_bindings(query, [])
	if result and _db.fetch_row():
		return int(_db.get_data("cnt"))
	return 0


func delete_by_id(feedback_id: String) -> bool:
	var query := "DELETE FROM %s WHERE id = ?" % TABLE_NAME
	return _db.query_with_bindings(query, [feedback_id])


func clear_all() -> bool:
	var query := "DELETE FROM %s" % TABLE_NAME
	return _db.query(query)


func _rows_to_feedback_list(rows: Array) -> Array[ProfessorFeedback]:
	var result: Array[ProfessorFeedback] = []
	for row in rows:
		result.append(_row_to_feedback(row))
	return result


func _row_to_feedback(row: Dictionary) -> ProfessorFeedback:
	var fb := ProfessorFeedback.new()
	fb.id = str(row.get("id", ""))
	fb.student_id = str(row.get("student_id", ""))
	fb.professor_id = str(row.get("professor_id", ""))
	fb.professor_name = str(row.get("professor_name", ""))
	fb.comments = str(row.get("comments", ""))
	fb.rating = int(row.get("rating", 0))
	fb.feedback_type = str(row.get("feedback_type", ""))
	fb.course_id = str(row.get("course_id", ""))
	fb.game_id = str(row.get("game_id", ""))
	fb.level_id = str(row.get("level_id", ""))
	fb.display_in_game = row.get("display_in_game", 0) == 1
	fb.acknowledged_at = str(row.get("acknowledged_at", ""))
	fb.is_read = row.get("is_read", 0) == 1
	fb.created_at = str(row.get("created_at", ""))
	fb.updated_at = str(row.get("updated_at", ""))
	return fb
