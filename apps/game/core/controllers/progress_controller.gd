class_name ProgressController

var _repo : ProgressRepository

func _init() -> void:
	_repo = ProgressRepository.new()

func record_attempt(data : ProgressData) -> void:
	_repo.create_progress(data)

func get_progress_for_segment(segment_id : int):
	return _repo.get_progress_by_segment(segment_id)

func get_all_progress_user():
	return _repo.get_all_progress_by_user();


# Implementar una conexión con la señal cuando se termina el nivel
# Esta señal será utilizado también en el agente inteligente
