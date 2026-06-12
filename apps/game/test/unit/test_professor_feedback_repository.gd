extends GutTest


func build_sample_feedback(id: String, comments: String, is_read: bool = false, display_in_game: bool = true) -> ProfessorFeedback:
    var fb := ProfessorFeedback.new(id, comments)
    fb.student_id = "student-1"
    fb.professor_id = "prof-1"
    fb.professor_name = "Prof. Test"
    fb.rating = 4
    fb.feedback_type = "advice"
    fb.display_in_game = display_in_game
    fb.is_read = is_read
    fb.created_at = Time.get_datetime_string_from_system(true)
    fb.updated_at = fb.created_at
    return fb


func test_insert_all_inserts_items():
    assert_file_exists(Env.DATABASE_URL)
    var repo := ProfessorFeedbackRepository.new()
    repo.clear_all()

    var items := [
        build_sample_feedback("fb-test-1", "Primer feedback"),
        build_sample_feedback("fb-test-2", "Segundo feedback")
    ]
    var result := repo.insert_all(items)

    assert_true(result, "insert_all debe retornar true")
    var all := repo.get_all()
    assert_true(all.size() >= 2, "Debe haber al menos 2 elementos insertados")

    repo.clear_all()


func test_insert_all_empty_returns_true():
    var repo := ProfessorFeedbackRepository.new()
    var result := repo.insert_all([])
    assert_true(result, "insert_all con array vacío debe retornar true")


func test_get_unread_returns_only_unread():
    assert_file_exists(Env.DATABASE_URL)
    var repo := ProfessorFeedbackRepository.new()
    repo.clear_all()

    repo.insert_all([
        build_sample_feedback("fb-unread-1", "No leido", false),
        build_sample_feedback("fb-read-1", "Leido", true)
    ])

    var unread := repo.get_unread()
    assert_true(unread.size() > 0, "Debe haber al menos 1 no leido")
    for fb in unread:
        assert_false(fb.is_read, "Todos los items de get_unread deben tener is_read=false")

    repo.clear_all()


func test_mark_as_read_updates_item():
    assert_file_exists(Env.DATABASE_URL)
    var repo := ProfessorFeedbackRepository.new()
    repo.clear_all()

    repo.insert_all([build_sample_feedback("fb-mark-1", "Para marcar", false)])
    assert_eq(repo.count_unread(), 1, "Debe haber 1 no leido antes de marcar")

    var marked := repo.mark_as_read("fb-mark-1")
    assert_true(marked, "mark_as_read debe retornar true")

    assert_eq(repo.count_unread(), 0, "No debe haber no leidos despues de marcar")

    repo.clear_all()


func test_mark_all_as_read_updates_all():
    assert_file_exists(Env.DATABASE_URL)
    var repo := ProfessorFeedbackRepository.new()
    repo.clear_all()

    repo.insert_all([
        build_sample_feedback("fb-all-1", "Uno", false),
        build_sample_feedback("fb-all-2", "Dos", false),
        build_sample_feedback("fb-all-3", "Tres", true)
    ])

    var marked := repo.mark_all_as_read()
    assert_true(marked, "mark_all_as_read debe retornar true")
    assert_eq(repo.count_unread(), 0, "No debe haber no leidos despues de mark_all")

    repo.clear_all()


func test_count_unread_returns_correct_count():
    assert_file_exists(Env.DATABASE_URL)
    var repo := ProfessorFeedbackRepository.new()
    repo.clear_all()

    assert_eq(repo.count_unread(), 0, "Debe haber 0 no leidos al inicio")

    repo.insert_all([
        build_sample_feedback("fb-cnt-1", "Uno", false),
        build_sample_feedback("fb-cnt-2", "Dos", true)
    ])
    assert_eq(repo.count_unread(), 1, "Debe haber 1 no leido")

    repo.clear_all()


func test_delete_by_id_removes_item():
    assert_file_exists(Env.DATABASE_URL)
    var repo := ProfessorFeedbackRepository.new()
    repo.clear_all()

    repo.insert_all([build_sample_feedback("fb-del-1", "Para borrar")])
    assert_eq(repo.get_all().size(), 1, "Debe haber 1 elemento")

    var deleted := repo.delete_by_id("fb-del-1")
    assert_true(deleted, "delete_by_id debe retornar true")
    assert_eq(repo.get_all().size(), 0, "No debe haber elementos despues de borrar")

    repo.clear_all()


func test_clear_all_removes_everything():
    assert_file_exists(Env.DATABASE_URL)
    var repo := ProfessorFeedbackRepository.new()
    repo.clear_all()

    repo.insert_all([
        build_sample_feedback("fb-clr-1", "Uno"),
        build_sample_feedback("fb-clr-2", "Dos")
    ])
    assert_true(repo.get_all().size() >= 2, "Debe haber elementos antes de clear")

    repo.clear_all()
    assert_eq(repo.get_all().size(), 0, "No debe haber elementos despues de clear")
