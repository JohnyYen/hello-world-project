extends Block
class_name ExecuteBlock

var sentence : String
# Called when the node enters the scene tree for the first time.
func _init(id:int, b_block_type_id:int, b_description: String, b_name: String, b_sentence : String):
	super(id, b_block_type_id, b_description, b_name)
	self.sentence = b_sentence


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
