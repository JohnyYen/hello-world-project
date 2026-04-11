extends Node
class_name DialogueUIController


signal changed_background(path : String)
signal changed_character(side : String,path : String)
signal played_music(path : String)
signal played_sfx(path : String)
signal showed_cg(path : String)
signal showed_title(title: String, duration : float)
signal clean_character(duration : float)
signal set_flag(flag : String, value : bool)

func _ready() -> void:
	pass
	
