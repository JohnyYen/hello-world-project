extends CodeBlockComponent

@export var start_color: Color = Color(0.2, 0.7, 0.3, 1.0)

func _ready():
	super() # llama al _ready() del bloque base
	self.block_type = BlockTypesEnum.BlockTypesEnum.START
	self.block = StartBlock.new()
	self.block_name = "Inicio"
	self.description = "Bloque que marca el inicio de la ejecución"
	$TextureRect.self_modulate = start_color
