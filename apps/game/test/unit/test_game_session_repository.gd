# test_game_session_repository.gd
# Tests for GameSessionRepository - manages cached game_id and instance_id in local SQLite.
# Follows the same pattern as test_block_repository.gd: real DB integration tests.
extends GutTest


# ==================== Tests del comportamiento público ====================

func test_has_session_returns_false_when_empty():
	# Arrange
	assert_file_exists(Env.DATABASE_URL, "La DB real debe existir")
	var repo: GameSessionRepository = GameSessionRepository.new()
	repo.clear_session()  # Asegurar estado limpio

	# Act & Assert
	assert_false(repo.has_session(), "has_session debe ser false cuando no hay datos")


func test_save_session_persists_data():
	# Arrange
	var repo: GameSessionRepository = GameSessionRepository.new()
	repo.clear_session()  # Estado limpio

	# Act
	repo.save_session("game-uuid-123", "instance-uuid-456", "student-uuid-789")

	# Assert
	assert_true(repo.has_session(), "Debe haber sesión después de save")
	var session: GameSession = repo.get_session()
	assert_not_null(session, "La sesión debe existir")
	assert_eq(session.game_id, "game-uuid-123", "game_id debe coincidir")
	assert_eq(session.instance_id, "instance-uuid-456", "instance_id debe coincidir")
	assert_eq(session.student_id, "student-uuid-789", "student_id debe coincidir")

	# Cleanup
	repo.clear_session()


func test_get_session_returns_null_when_empty():
	# Arrange
	var repo: GameSessionRepository = GameSessionRepository.new()
	repo.clear_session()

	# Act
	var session: GameSession = repo.get_session()

	# Assert
	assert_null(session, "get_session debe devolver null cuando no hay datos")


func test_has_session_returns_true_when_data_exists():
	# Arrange
	var repo: GameSessionRepository = GameSessionRepository.new()
	repo.clear_session()
	repo.save_session("game-uuid", "instance-uuid", "student-uuid")

	# Act & Assert
	assert_true(repo.has_session(), "has_session debe ser true cuando hay datos")

	# Cleanup
	repo.clear_session()


func test_clear_session_removes_data():
	# Arrange
	var repo: GameSessionRepository = GameSessionRepository.new()
	repo.save_session("game-uuid", "instance-uuid", "student-uuid")
	assert_true(repo.has_session(), "Pre-condición: debe haber datos")

	# Act
	repo.clear_session()

	# Assert
	assert_false(repo.has_session(), "No debe haber datos después de clear")
	assert_null(repo.get_session(), "get_session debe devolver null después de clear")


func test_save_session_overwrites_previous_data():
	# Arrange
	var repo: GameSessionRepository = GameSessionRepository.new()
	repo.clear_session()
	repo.save_session("old-game", "old-instance", "old-student")

	# Act - save over the previous
	repo.save_session("new-game", "new-instance", "new-student")

	# Assert - should have only one session with new values
	var session: GameSession = repo.get_session()
	assert_eq(session.game_id, "new-game", "game_id debe estar actualizado")
	assert_eq(session.instance_id, "new-instance", "instance_id debe estar actualizado")

	# Cleanup
	repo.clear_session()


func test_get_all_sessions_returns_array_with_one_element():
	# Arrange
	var repo: GameSessionRepository = GameSessionRepository.new()
	repo.clear_session()
	repo.save_session("game-1", "instance-1", "student-1")

	# Act
	var sessions: Array = repo.get_all_sessions()

	# Assert
	assert_eq(sessions.size(), 1, "Debe haber 1 sesión (singleton)")
	var session: GameSession = sessions[0]
	assert_eq(session.game_id, "game-1")

	# Cleanup
	repo.clear_session()
