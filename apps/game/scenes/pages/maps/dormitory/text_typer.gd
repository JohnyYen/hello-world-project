extends RichTextLabel

@export var speed := 50.0  # letras por segundo

func _ready() -> void:
	if is_visible_in_tree():
		type_text("Guardando...")

func type_text(text: String, duration : float = 1.0):
	self.text = text
	self.visible_characters = 0

	var total := text.length()
	
	while visible_characters < total:
		visible_characters += 1
		await get_tree().create_timer(duration / speed).timeout
		
	await get_tree().create_timer(0.5).timeout
	self.visible = 0


func _on_visibility_changed() -> void:
	if self.visible:
		type_text("Guardando...")
