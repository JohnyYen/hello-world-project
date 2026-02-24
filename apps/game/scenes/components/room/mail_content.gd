extends PanelContainer

signal mail_closed

@onready var subject_label: Label = $VBoxContainer/Subject
@onready var from_label: Label = $VBoxContainer/From
@onready var body_label: RichTextLabel = $VBoxContainer/Body
@onready var close_button: Button = $VBoxContainer/Close

func _ready():
	close_button.pressed.connect(_on_close_pressed)
	visible = false


#
# PUBLIC: Mostrar el contenido de un correo
#
# Espera un diccionario con esta estructura:
# {
#     "subject": "Título",
#     "from": "Remitente",
#     "body": "Contenido del correo"
# }
#
func show_mail(data: Dictionary) -> void:
	# Seguridad — evita errores si falta un campo
	subject_label.text = data.get("subject", "Sin asunto")
	from_label.text = data.get("from", "Desconocido")
	body_label.text = data.get("body", "")

	# Asegurar que el contenido haga wrap correctamente
	body_label.fit_content = true
	body_label.scroll_active = true
	
	visible = true


#
# PRIVATE: Evento del botón Back
#
func _on_close_pressed() -> void:
	hide_mail()
	emit_signal("mail_closed")


#
# PUBLIC: Ocultar el panel del correo
#
func hide_mail() -> void:
	visible = false
