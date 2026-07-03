class_name ProfessorFeedbackService
extends Node

var api_client: ApiClient
var repository: ProfessorFeedbackRepository


func _init() -> void:
	api_client = ApiClient.new()
	repository = ProfessorFeedbackRepository.new()


func _ready() -> void:
	add_child(api_client)


func fetch_feedback(student_id: String) -> Dictionary:
	print("DEBUG [ProfessorFeedbackService] fetch_feedback: inicio para student_id=", student_id)
	var api_result := await api_client.get_professor_feedback(student_id)

	if not api_result.OK:
		print("DEBUG [ProfessorFeedbackService] fetch_feedback: FALLO - ", api_result.get("error", "Error desconocido"))
		return {"OK": false, "error": str(api_result.get("error", "Error desconocido"))}

	var items_raw = api_result.get("data", {})
	var items = items_raw.get("items", []) if items_raw is Dictionary else []
	var total_count: int = items.size()
	print("DEBUG [ProfessorFeedbackService] fetch_feedback: API devolvio ", total_count, " items totales")

	var feedback_list: Array[ProfessorFeedback] = []
	for item in items:
		var fb := ProfessorFeedback.from_api_dict(item)
		feedback_list.append(fb)

	print("DEBUG [ProfessorFeedbackService] fetch_feedback: ", feedback_list.size(), " items recibidos, guardando en repositorio")
	repository.insert_all(feedback_list)
	print("DEBUG [ProfessorFeedbackService] fetch_feedback: COMPLETADO, ", total_count, " recibidos, ", feedback_list.size(), " almacenados")

	return {"OK": true, "count": total_count}


func get_cached_feedback() -> Array[ProfessorFeedback]:
	return repository.get_all()


func get_unread_count() -> int:
	return repository.count_unread()


func mark_as_read(feedback_id: String) -> void:
	repository.mark_as_read(feedback_id)
