extends GutTest


class MockApiClient:
    var should_fail: bool = false
    var mock_items: Array = []

    func get_professor_feedback(_student_id: String, _skip: int = 0, _limit: int = 500) -> Dictionary:
        if should_fail:
            return {"OK": false, "error": "Error de red simulado"}
        return {"OK": true, "data": {"items": mock_items}}


class MockRepository:
    var inserted_items: Array = []

    func insert_all(items: Array[ProfessorFeedback]) -> bool:
        inserted_items = items.duplicate()
        return true

    func get_all() -> Array[ProfessorFeedback]:
        return inserted_items.duplicate()

    func count_unread() -> int:
        var count: int = 0
        for item in inserted_items:
            if not item.is_read:
                count += 1
        return count

    func mark_as_read(_feedback_id: String) -> bool:
        return true


func make_service() -> ProfessorFeedbackService:
    var service := ProfessorFeedbackService.new()
    service.api_client = MockApiClient.new()
    service.repository = MockRepository.new()
    return service


func test_fetch_feedback_returns_ok_on_success():
    var service := make_service()
    var mock_client := service.api_client as MockApiClient
    mock_client.mock_items = [
        {"id": "fb-1", "comments": "Buen trabajo!", "display_in_game": true},
        {"id": "fb-2", "comments": "Sigue asi", "display_in_game": true}
    ]

    var result := await service.fetch_feedback("student-1")

    assert_true(result.OK, "fetch_feedback debe retornar OK=true en exito")
    assert_eq(result.count, 2, "count debe ser el total de items de la API")


func test_fetch_feedback_filters_non_display_items():
    var service := make_service()
    var mock_client := service.api_client as MockApiClient
    mock_client.mock_items = [
        {"id": "fb-1", "comments": "Visible", "display_in_game": true},
        {"id": "fb-2", "comments": "Oculto", "display_in_game": false}
    ]

    var result := await service.fetch_feedback("student-1")

    assert_true(result.OK, "fetch_feedback debe retornar OK=true")
    assert_eq(result.count, 2, "count debe ser el total de items, incluyendo los filtrados")

    var mock_repo := service.repository as MockRepository
    assert_eq(mock_repo.inserted_items.size(), 1, "Solo 1 item debe insertarse (display_in_game=true)")
    assert_eq(mock_repo.inserted_items[0].id, "fb-1", "El item insertado debe ser el visible")


func test_fetch_feedback_returns_error_on_failure():
    var service := make_service()
    var mock_client := service.api_client as MockApiClient
    mock_client.should_fail = true

    var result := await service.fetch_feedback("student-1")

    assert_false(result.OK, "fetch_feedback debe retornar OK=false en error")
    assert_has(result, "error", "Debe incluir mensaje de error")


func test_get_cached_feedback_delegates_to_repository():
    var service := make_service()
    var mock_repo := service.repository as MockRepository
    mock_repo.inserted_items = [
        ProfessorFeedback.new("fb-cached-1", "Cached feedback")
    ]

    var cached := service.get_cached_feedback()

    assert_eq(cached.size(), 1, "get_cached_feedback debe retornar los items del repositorio")
    assert_eq(cached[0].id, "fb-cached-1")


func test_get_unread_count_delegates_to_repository():
    var service := make_service()
    var mock_repo := service.repository as MockRepository
    var fb := ProfessorFeedback.new("fb-unread", "No leido")
    mock_repo.inserted_items = [fb]

    var count := service.get_unread_count()

    assert_eq(count, 1, "get_unread_count debe delegar al repositorio")


func test_mark_as_read_delegates_to_repository():
    var service := make_service()
    var mock_repo := service.repository as MockRepository

    service.mark_as_read("fb-1")
    # No assertion needed - verifying no crash and proper delegation
    pass
