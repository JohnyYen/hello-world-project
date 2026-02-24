extends Panel

@onready var music_slider = $Music_Slider
@onready var sfx_slider = $SFX_Slider
@onready var toogle_fullscreen = $"Toogle Fullscreen"
@onready var art_options = $"Art Options"
@onready var lang_options = $"Lang Options"

func _ready() -> void:
	music_slider.value = _GameConfig.music_volume
	sfx_slider.value = _GameConfig.sfx_volume
	select_by_text(_GameConfig.language, lang_options)
	select_by_text(_GameConfig.art_style, art_options)
	toogle_fullscreen.button_pressed = _GameConfig.fullscreen
	
func select_by_text(text : String, button : OptionButton):
	for i in range(button.item_count):
		print(button.get_item_text(i), text)
		if button.get_item_text(i).to_lower() == text.to_lower():
			print("Hecho")
			button.select(i)
			break
