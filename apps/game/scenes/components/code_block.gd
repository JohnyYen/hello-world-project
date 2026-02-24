# Bloque.gd
extends TextureButton
class_name CodeBlock

#@onready var icono: TextureRect = $icon
@onready var nombre: Label = $nombre
@onready var descripcion: Label = $description
var in_zone = false;

signal block_clicked(block: Block)
signal block_dragged(block: Block)
signal block_dropped(block: Block)

# Variables to store block data
var bloque_icono: Texture = load("res://icon.svg")
var bloque_nombre: String
var bloque_descripcion: String
var init_parent: Control;
@onready var block: Block

# Variables for drag and drop functionality
var _drag_offset: Vector2
var _is_dragging: bool = false


func _ready() -> void:
	# Connect signals for mouse hover
	connect("mouse_entered", Callable(self, "_on_mouse_entered"))
	connect("mouse_exited", Callable(self, "_on_mouse_exited"))
	connect("pressed", Callable(self, "_on_block_pressed"))  # Changed from gui_input to pressed signal
	
	# Update the UI with block data
	update_ui()


func _on_block_pressed() -> void:
	# Only trigger if not already in zone (meaning it's in the execution area)
	if !in_zone:  # This means it's in the palette area
		# Emit signal to create a copy in execution area
		emit_signal("block_clicked", block)
		# Set in_zone to true so this instance won't create additional copies
		in_zone = true
	else:
		# If it's already in execution area, start dragging
		_start_drag()


func _start_drag() -> void:
	# Store initial position and parent
	_drag_offset = get_global_mouse_position() - self.global_position
	init_parent = get_parent()
	
	# Remove from parent temporarily and add to top level for dragging
	if init_parent:
		init_parent.remove_child(self)
	
	# Add to parent's parent (or directly to the scene root) to make it appear on top
	var top_parent = find_top_parent(get_parent())
	if top_parent:
		top_parent.add_child(self)
	
	self.global_position = get_global_mouse_position() - _drag_offset
	_is_dragging = true
	self.z_index = 999  # Bring to front during drag


func _stop_drag() -> void:
	if _is_dragging:
		_is_dragging = false
		self.z_index = 0  # Reset z-index
		
		# Emit signal that block was dropped
		emit_signal("block_dropped", block)
		
		# For now, we'll leave the block where it was dropped
		# The parent will decide what to do with it based on position


# Find the topmost parent to add the dragged element to
func find_top_parent(node):
	if node.get_parent() == null:
		return node
	return find_top_parent(node.get_parent())


# Signal: When the mouse enters the block
func _on_mouse_entered() -> void:
	descripcion.visible = true


# Signal: When the mouse exits the block
func _on_mouse_exited() -> void:
	descripcion.visible = false


# Process function to handle dragging
func _process(_delta) -> void:
	if _is_dragging:
		self.global_position = get_global_mouse_position() - _drag_offset


# Function to update the UI with block data
func update_ui() -> void:
	#icono.texture = bloque_icono
	nombre.text = bloque_nombre
	descripcion.text = bloque_descripcion


# Function to configure the block with data
func configure(block_data: Block) -> void:
	self.block = block_data
	bloque_icono = load("res://icon.svg")
	bloque_nombre = block_data.name
	bloque_descripcion = block_data.description
	update_ui()


# Function to get the associated block
func get_block() -> Block:
	return block
