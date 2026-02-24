extends ScrollContainer

@onready var list_container: VBoxContainer = $VBoxContainer
@onready var mail_content = $"../MailContent"


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
	render_emails()


#
# Renderiza todos los correos en la interfaz
#
func render_emails():
	queue_free_children(list_container)
	#list_container.queue_free_children()

	for email in emails:
		var item = create_mail_item(email)
		list_container.add_child(item)


#
# Crea un item visual para un correo
#
func create_mail_item(email: Dictionary) -> Control:
	var item = HBoxContainer.new()
	item.custom_minimum_size = Vector2(0, 40)
	item.mouse_filter = MOUSE_FILTER_PASS

	var subject_label := Label.new()
	subject_label.text = email.get("subject", "Sin asunto")
	subject_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL

	var from_label := Label.new()
	from_label.text = email.get("from", "Desconocido")
	from_label.modulate = Color(0.7, 0.7, 0.7)

	item.add_child(subject_label)
	item.add_child(from_label)

	# convertimos el item entero en un botón clickeable
	item.gui_input.connect(func(event):
		if event is InputEventMouseButton and event.pressed:
			mail_content.show_mail(email)
	)

	# Estilos simples tipo Ubuntu
	item.add_theme_constant_override("separation", 10)

	return item


#
# Utilidad: limpia hijos del contenedor
#
func queue_free_children(container : Container):
	for c in container.get_children():
		c.queue_free()
#func VBoxContainer.queue_free_children(self):
	#for c in self.get_children():
		#c.queue_free()
