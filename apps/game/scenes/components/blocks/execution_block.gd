extends CodeBlockComponent
class_name ExecutionCodeBlock

@export var color: Color = Color(0.9, 0.8, 0.3, 1.0)
signal action_chosen(action_name: String)
signal block_spawned(block: ExecutionCodeBlock, spawn_position: Vector2)
signal block_deleted(block: ExecutionCodeBlock)

@export var action_slot: OptionButton
@export var popup_theme: Theme
@export var block_body: PanelContainer
@export var value_label: Label
@export var popup: PopupMenu
@export var delete_button: Button

var actions_list: Array = []
var action_selected: String = "atender_siguiente_cliente"

enum BlockState { IN_PALETTE, IN_WORKSPACE }
var current_state: BlockState = BlockState.IN_PALETTE

func _ready():
	super()
	_setup_visual_block()
	_setup_popup()
	_setup_delete_button()
	
	var popup_native := self.action_slot.get_popup()
	popup_native.theme = popup_theme
	
	self.block = ExecutionBlock.new(action_selected)
	self.block.name = "Ejecutar"
	self.block_type = BlockTypesEnum.BlockTypesEnum.ACTION
	self.block_name = "Ejecutar"
	self.description = "Bloque que marca el inicio de la ejecución"
	
	$TextureButton.self_modulate = color

func _setup_visual_block() -> void:
	if block_body:
		block_body.theme_type_variation = "BlockMotionBody"
	if value_label:
		value_label.theme_type_variation = "BlockMotionValue"
		value_label.text = "--"

func _setup_popup() -> void:
	if not popup:
		return
		
	popup.hide()
	popup.id_pressed.connect(_on_popup_item_selected)
	
	if popup_theme:
		popup.theme = popup_theme

func set_state(new_state: BlockState) -> void:
	current_state = new_state
	call_deferred("_apply_state_visuals")

func _apply_state_visuals() -> void:
	match current_state:
		BlockState.IN_PALETTE:
			if action_slot:
				action_slot.mouse_filter = Control.MOUSE_FILTER_IGNORE
			if popup:
				popup.hide()
			if delete_button:
				delete_button.visible = false
			if block_body:
				block_body.modulate = Color(1, 1, 1, 0.7)

		BlockState.IN_WORKSPACE:
			if action_slot:
				action_slot.mouse_filter = Control.MOUSE_FILTER_PASS
			if delete_button:
				delete_button.visible = true  # Forzar visible
				print("DELETE BUTTON VISIBLE: ", delete_button.visible)
			if block_body:
				block_body.modulate = Color(1, 1, 1, 1)
	#match current_state:
		#BlockState.IN_PALETTE:
			#if action_slot:
				#action_slot.mouse_filter = Control.MOUSE_FILTER_IGNORE
			#if popup:
				#popup.hide()
			## En lista: click envía a zona de solución
			#mouse_filter = Control.MOUSE_FILTER_STOP
				#
		#BlockState.IN_WORKSPACE:
			#if action_slot:
				#action_slot.mouse_filter = Control.MOUSE_FILTER_PASS
			## En zona: click abre popup
			#mouse_filter = Control.MOUSE_FILTER_STOP

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
	if self.block != null:
		(self.block as ExecutionBlock).stored_action = "null"
	_sync_popup_items()

func _sync_popup_items() -> void:
	if not popup:
		return
		
	popup.clear()
	popup.add_item("-- Seleccionar acción --")
	for action in actions_list:
		popup.add_item(action["name"])

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
	
	if value_label:
		value_label.text = slot

func _on_popup_item_selected(id: int) -> void:
	var item_text = popup.get_item_text(id)
	
	for i in range(action_slot.item_count):
		if action_slot.get_item_text(i) == item_text:
			action_slot.select(i)
			_on_option_button_item_selected(i)
			break

func _gui_input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.pressed:
		match current_state:
			BlockState.IN_PALETTE:
				if event.button_index == MOUSE_BUTTON_LEFT:
					# Click en lista: spawnear en zona de solución
					emit_signal("block_spawned", self, get_global_mouse_position())
					get_viewport().set_input_as_handled()
					
			BlockState.IN_WORKSPACE:
				if event.button_index == MOUSE_BUTTON_LEFT:
					# Click en zona: abrir popup
					if delete_button:
						delete_button.visible = true  
					
					mouse_filter = Control.MOUSE_FILTER_STOP
					
					if popup and popup.item_count > 0:
						popup.position = global_position + Vector2(0, size.y + 4)
						popup.popup()
					get_viewport().set_input_as_handled()
					
				elif event.button_index == MOUSE_BUTTON_RIGHT:
					# Right-click: eliminar
					emit_signal("block_deleted", self)
					get_viewport().set_input_as_handled()

func _setup_delete_button() -> void:
	if not delete_button:
		return
	# Ocultar por defecto (en palette)
	delete_button.visible = false

	# Conectar señal
	delete_button.pressed.connect(_on_delete_button_pressed)

func _on_delete_button_pressed() -> void:
	print("DELETE BUTTON PRESSED")
	self.queue_free()
	emit_signal("block_dropped", self)

func _on_label_gui_input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.pressed:
		pass
