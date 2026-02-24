extends Control
class_name CodeBlockComponent

@export var block_type = BlockTypesEnum.BlockTypesEnum.ACTION
@export var block_name: String = "Bloque genérico"
@export var description: String = "Bloque base para construir código"
@export var block_color: Color = Color(0.8, 0.8, 0.8, 1.0)
@onready var block: BaseBlock
@onready var btn : TextureButton = $TextureButton


signal block_selected(block_data: Dictionary)

func _ready():
	print("BTN:", btn)
	# Configurar el texto y el tooltip
	$Label.text = block_name
	tooltip_text = description

	# Aplicar color al TextureRect como fondo del bloque
	if $TextureRect.texture:
		$TextureRect.self_modulate = block_color

	# Permitir que capture eventos de ratón
	#mouse_filter = Control.MOUSE_FILTER_STOP


func _on_gui_input(event: InputEvent):
	print("ghfhfgh")
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
		print("SDDSDD")
		emit_signal("block_selected", {
			"type": block_type,
			"name": block_name,
			"description": description
		})

func get_block() -> BaseBlock:
	return block

func _on_texture_button_pressed() -> void:
	print("Me tocaron uwu")
	var data = {
		"type": block_type,
		"name": block_name,
		"description": description
	}
	print(data)
	emit_signal("block_selected", data)
