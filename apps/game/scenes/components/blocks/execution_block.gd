extends CodeBlockComponent
class_name ExecutionCodeBlock

@export var color: Color = Color(0.9, 0.8, 0.3, 1.0)
signal action_chosen(action_name: String)

@onready var action_slot: OptionButton = $TextureButton/OptionButton
var actions_list : Array = []
var action_selected : String = "atender_siguiente_cliente"

func _ready():
	super() # llama al _ready() del bloque base
	
	var rect = self.btn.get_global_rect()
	#action_slot.global_position = rect.position
	#action_slot.size = rect.size
	
	self.block = ExecutionBlock.new(action_selected)
	self.block_type = BlockTypesEnum.BlockTypesEnum.ACTION
	self.block_name = "Ejecutar"
	self.description = "Bloque que marca el inicio de la ejecución"
	$TextureButton.self_modulate = color

# Este método puede ser llamado desde fuera, por ejemplo, cuando el nivel emite las acciones disponibles
func set_actions(actions: Array) -> void:
	self.actions_list = actions
	print(actions)
	action_slot.clear()
	action_slot.add_item("-- Seleccionar acción --")
	actions.shuffle()
	for action in actions:
		action_slot.add_item(action["name"])
	
	action_slot.select(0)
	action_selected = ""

# Maneja la selección del jugador
func _on_action_selected(index: int) -> void:
	
	var action_name = action_slot.get_item_text(index)
	emit_signal("action_chosen", action_name)

func _on_option_button_item_selected(index: int) -> void:
	if index == 0:
		action_selected = "null"
		(self.block as ExecutionBlock).stored_action = "null"
		print("Ninguna acción seleccionada.")
		return
	var slot := action_slot.get_item_text(index)
	action_selected = actions_list.filter(func(e):
		return e["name"] == slot
	)[0]["value"]
	print(action_selected)
	(self.block as ExecutionBlock).stored_action = action_selected
