class_name GameConfig
extends Node

# var config_path : String = "user://config/settings.cfg"
var config_path : String = "res://config/settings.cfg"

signal art_style_changed(new_style)
signal language_changed(new_language)
signal volume_changed(type, value)
signal fullscreen_toogled(enabled)


var art_style := "anime"
var language:= "es"
var music_volume := 1.0
var sfx_volume := 1.0
var fullscreen := false

func _ready() -> void:
	load_settings()

func set_art_style(new_style : String):
	if art_style != new_style:
		art_style = new_style
		emit_signal("art_style_changed", art_style)
		save_settings()

func set_volume(type : String, new_volume : float):
	var value = clamp(new_volume, 0.0, 1.0)
	match type:
		"music":
			music_volume = value
			emit_signal("volume_changed",type, value)
			AudioServer.set_bus_volume_db(AudioServer.get_bus_index("Music"), linear_to_db(value))
			save_settings()
		"sfx":
			sfx_volume = value
			emit_signal("volume_changed",type, value)
			AudioServer.set_bus_volume_db(AudioServer.get_bus_index("SFX"), linear_to_db(value))
			save_settings()
		_:
			push_error("TYPE_NOT_SUPPORTED")

func set_language(new_language : String):
	if language != new_language:
		language = new_language
		TranslationServer.set_locale(new_language)
		emit_signal("language", new_language)
		save_settings()

func set_screen(toogle : bool):
	fullscreen = toogle
	DisplayServer.window_set_mode(toogle if DisplayServer.WINDOW_MODE_FULLSCREEN else DisplayServer.WINDOW_MODE_WINDOWED)
	emit_signal("fullscreen_toogled", toogle)
	save_settings()

func load_settings():
	var config = ConfigFile.new()
	if config.load(config_path) == OK:
		art_style = config.get_value("graphics", "art_style", "anime")
		music_volume = config.get_value("audio", "music_volume", 1.0)
		sfx_volume = config.get_value("audio", "sfx_volume", 1.0)
		language = config.get_value("system", "language", "en")
		fullscreen = config.get_value("system", "fullscreen", false)

		# Aplicar inmediatamente
		set_language(language)
		set_volume("music", music_volume)
		set_volume("sfx", sfx_volume)
		set_screen(fullscreen)

func save_settings():
	var config = ConfigFile.new()
	config.set_value("graphics", "art_style", art_style)
	config.set_value("audio", "sfx_volume", sfx_volume)
	config.set_value("audio", "music_volume", music_volume)
	config.set_value("system", "language", language)
	config.set_value("system", "fullscreen", fullscreen)

	config.save(config_path)
