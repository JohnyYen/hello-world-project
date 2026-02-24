extends Control

@onready var dorm_btn = $"Dormitory Btn"
@onready var faculty_btn = $"Faculty Btn"
@onready var park_btn = $"Park Btn"

enum MapTutorialStep { DORM, FACULTY, PARK, FINISHED }
var current_step = MapTutorialStep.DORM

func _ready():
	# Desactivar highlights iniciales
	dorm_btn.stop_pulse()
	faculty_btn.stop_pulse()
	park_btn.stop_pulse()

	# Conectar señales
	dorm_btn.pressed.connect(_on_dorm_pressed)
	faculty_btn.pressed.connect(_on_faculty_pressed)
	park_btn.pressed.connect(_on_park_pressed)

	DialogueManager.dialogue_ended.connect(_on_dialogue_finished)

	# Iniciar tutorial
	start_tutorial()


func start_tutorial():
	current_step = MapTutorialStep.DORM
	dorm_btn.start_pulse()
	dorm_btn.z_index = 10000
	DialogueManager.show_dialogue_balloon(load("res://dialogue/Tutorial/Tutorial_Map_Dorm.dialogue"))


func _on_dorm_pressed():
	if current_step != MapTutorialStep.DORM:
		return
	dorm_btn.stop_pulse()
	current_step = MapTutorialStep.FACULTY
	faculty_btn.start_pulse()
	DialogueManager.show_dialogue_balloon(load("res://dialogue/Tutorial/Tutorial_Map_Faculty.dialogue"))



func _on_faculty_pressed():
	if current_step != MapTutorialStep.FACULTY:
		return
	faculty_btn.stop_pulse()
	current_step = MapTutorialStep.PARK
	park_btn.start_pulse()
	DialogueManager.show_dialogue_balloon(load("res://dialogue/Tutorial/Tutorial_Map_Park.dialogue"))



func _on_park_pressed():
	if current_step != MapTutorialStep.PARK:
		return
	park_btn.stop_pulse()
	current_step = MapTutorialStep.FINISHED
	DialogueManager.show_dialogue_balloon(load("res://dialogue/Tutorial/Tutorial_Map_Finish.dialogue"))



func _on_dialogue_finished():
	print("DEBUG [Tutorial Global Map]: No se ha terminado tutorial aun")
	if current_step == MapTutorialStep.FINISHED:
		print("DEBUG [Tutorial Global Map]: Se termino tutorial final")
		# Tutorial finalizado, habilitar navegación libre
		#dorm_btn.start_pulse()
		#faculty_btn.start_pulse()
		#park_btn.start_pulse()
		get_tree().change_scene_to_file("res://scenes/pages/tutorial/tutorial_gameplay.tscn")
