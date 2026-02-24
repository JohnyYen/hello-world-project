extends CodeBlockComponent

@export var color: Color = Color(0.9, 0.8, 0.3, 1.0)

func _ready():
	super() # llama al _ready() del bloque base
	self.block = EndBlock.new()
	block_type = BlockTypesEnum.BlockTypesEnum.END
	block_name = "Finalizar"
	description = "Bloque que marca el inicio de la ejecución"
	$TextureRect.self_modulate = color
