extends GutTest


func test_init_sets_defaults():
    var fb := ProfessorFeedback.new()

    assert_eq(fb.id, "", "id debe ser vacío por defecto")
    assert_eq(fb.student_id, "", "student_id debe ser vacío por defecto")
    assert_eq(fb.professor_name, "", "professor_name debe ser vacío por defecto")
    assert_eq(fb.comments, "", "comments debe ser vacío por defecto")
    assert_eq(fb.rating, 0, "rating debe ser 0 por defecto")
    assert_eq(fb.feedback_type, "", "feedback_type debe ser vacío por defecto")
    assert_eq(fb.display_in_game, false, "display_in_game debe ser false por defecto")
    assert_eq(fb.is_read, false, "is_read debe ser false por defecto")


func test_init_with_params():
    var fb := ProfessorFeedback.new("uuid-123", "Buen trabajo!")

    assert_eq(fb.id, "uuid-123", "id debe coincidir con el constructor")
    assert_eq(fb.comments, "Buen trabajo!", "comments debe coincidir con el constructor")


func test_to_dict_returns_all_fields():
    var fb := ProfessorFeedback.new("fb-1", "Great work!")
    fb.student_id = "student-1"
    fb.professor_id = "prof-1"
    fb.professor_name = "Dr. Smith"
    fb.rating = 4
    fb.feedback_type = "advice"
    fb.course_id = "course-1"
    fb.game_id = "game-1"
    fb.level_id = "level-1"
    fb.display_in_game = true
    fb.is_read = false
    fb.created_at = "2025-01-01T00:00:00"
    fb.updated_at = "2025-01-02T00:00:00"

    var dict := fb.to_dict()

    assert_eq(dict["id"], "fb-1")
    assert_eq(dict["comments"], "Great work!")
    assert_eq(dict["rating"], 4)
    assert_eq(dict["display_in_game"], true)
    assert_eq(dict["professor_name"], "Dr. Smith")


func test_from_api_dict_creates_instance():
    var data := {
        "id": "api-uuid-1",
        "student_id": "stu-1",
        "professor_id": "prof-1",
        "professor_name": "Prof. Garcia",
        "comments": "Excelente trabajo!",
        "rating": 5,
        "feedback_type": "hint",
        "course_id": "course-x",
        "game_id": "game-y",
        "level_id": "level-z",
        "display_in_game": true,
        "acknowledged_at": "",
        "created_at": "2025-06-10T10:00:00",
        "updated_at": "2025-06-10T10:00:00"
    }

    var fb := ProfessorFeedback.from_api_dict(data)

    assert_eq(fb.id, "api-uuid-1")
    assert_eq(fb.student_id, "stu-1")
    assert_eq(fb.professor_name, "Prof. Garcia")
    assert_eq(fb.comments, "Excelente trabajo!")
    assert_eq(fb.rating, 5)
    assert_eq(fb.feedback_type, "hint")
    assert_eq(fb.display_in_game, true)
    assert_eq(fb.is_read, false, "is_read siempre debe ser false en from_api_dict")


func test_from_api_dict_handles_empty_dict():
    var fb := ProfessorFeedback.from_api_dict({})

    assert_eq(fb.id, "")
    assert_eq(fb.comments, "")
    assert_eq(fb.rating, 0)
    assert_eq(fb.display_in_game, false)
    assert_eq(fb.is_read, false)
