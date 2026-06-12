extends ScrollContainer

@onready var list_container: VBoxContainer = $VBoxContainer
@onready var mail_content = $"../MailContent"

var _feedback_repo: ProfessorFeedbackRepository
var _feedback_service: ProfessorFeedbackService


#
# DATA DE PRUEBA
#
var emails := [
	{
		"subject": "Bienvenido al Campus Virtual",
		"from": "administracion@universidad.edu",
		"body": "¡Hola! Bienvenido oficialmente al campus virtual.\n\nAquí podrás acceder a tus cursos, materiales y notificaciones importantes.\n\nQue tengas un excelente inicio de semestre."
	},
	{
		"subject": "Actualización del Sistema",
		"from": "it@soporte.edu",
		"body": "Estimado usuario:\n\nHemos realizado una actualización de mantenimiento en los servidores.\nTodo debería funcionar correctamente.\n\nSaludos,\nEquipo de IT."
	},
	{
		"subject": "Tu Horario Académico",
		"from": "secretaria@universidad.edu",
		"body": "Adjuntamos tu horario completo para este semestre.\nRecuerda revisar constantemente por si hay modificaciones de última hora."
	}
]

func _ready():
	_feedback_repo = ProfessorFeedbackRepository.new()
	_feedback_service = ProfessorFeedbackService.new()
	add_child(_feedback_service)
	_fetch_and_render()


func _fetch_and_render():
	print("DEBUG [mail_list] _fetch_and_render: obteniendo feedback del backend...")
	var result = await _feedback_service.fetch_feedback("023436ff-0b9a-4aa7-b10c-77287c2fc943")
	print("DEBUG [mail_list] _fetch_and_render: resultado -> ", result)
	render_emails()


#
# Convierte un ProfessorFeedback del repositorio a un dict tipo email
#
func _feedback_to_email(fb: ProfessorFeedback) -> Dictionary:
	var subject = _feedback_subject(fb.feedback_type)
	var from = fb.professor_name if fb.professor_name != "" else "Profesor"
	var body = fb.comments

	return {
		"subject": subject,
		"from": from,
		"body": body,
		"_feedback_id": fb.id,
		"_is_feedback": true,
		"_is_read": fb.is_read
	}


#
# Retorna el asunto segun el tipo de feedback
#
func _feedback_subject(feedback_type: String) -> String:
	match feedback_type:
		"advice":
			return "Consejo del Profesor"
		"hint":
			return "Pista del Profesor"
		"tip":
			return "Tip del Profesor"
		"message":
			return "Mensaje del Profesor"
		_:
			return "Feedback del Profesor"


#
# Renderiza todos los correos y feedbacks en la interfaz
#
func render_emails():
	queue_free_children(list_container)

	var all_items = _build_mail_list()
	for item in all_items:
		var ui_item = create_mail_item(item)
		list_container.add_child(ui_item)


#
# Arma la lista combinada: feedback del profesor (no leidos primero) + emails de prueba
#
func _build_mail_list() -> Array:
	var result: Array = []

	# Feedback del profesor desde el repositorio local (leídos y no leídos)
	var feedback_list = _feedback_repo.get_all()
	for fb in feedback_list:
		result.append(_feedback_to_email(fb))

	# Emails de prueba
	for email in emails:
		result.append(email.duplicate())

	return result


#
# Crea un item visual para un correo/feedback
#
func create_mail_item(email: Dictionary) -> Control:
	var item = HBoxContainer.new()
	item.custom_minimum_size = Vector2(0, 40)
	item.mouse_filter = MOUSE_FILTER_PASS

	var subject_label := Label.new()
	subject_label.text = email.get("subject", "Sin asunto")
	subject_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL

	# Feedback no leido: se destaca con color claro
	# Feedback leido: se atenúa para indicar que ya fue visto
	if email.get("_is_feedback", false):
		if email.get("_is_read", false):
			subject_label.modulate = Color(0.6, 0.6, 0.6)  # gris atenuado
		else:
			subject_label.modulate = Color(1, 1, 0.9)  # claro destacado
	else:
		# Emails de prueba (no feedback)
		subject_label.modulate = Color(1, 1, 1)

	var from_label := Label.new()
	from_label.text = email.get("from", "Desconocido")
	from_label.modulate = Color(0.7, 0.7, 0.7)

	item.add_child(subject_label)
	item.add_child(from_label)

	# Click: mostrar contenido, marcar como leido si es feedback y refrescar UI
	item.gui_input.connect(func(event):
		if event is InputEventMouseButton and event.pressed:
			if email.get("_is_feedback", false):
				var fb_id: String = email.get("_feedback_id", "")
				if fb_id != "":
					_feedback_repo.mark_as_read(fb_id)
					render_emails()  # refrescar lista para mostrar cambio visual
			mail_content.show_mail(email)
	)

	item.add_theme_constant_override("separation", 10)

	return item


#
# Utilidad: limpia hijos del contenedor
#
func queue_free_children(container: Container):
	for c in container.get_children():
		c.queue_free()
