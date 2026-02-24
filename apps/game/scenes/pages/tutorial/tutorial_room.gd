extends Control

@onready var pc_btn = $"PC Btn"
@onready var bed_btn = $"Bedroom Btn"

enum TutorialStep { CLICK_PC, CLICK_BED, FINISHED }
var current_step = TutorialStep.CLICK_PC

# Referencia al DialogueManager (asegúrate de tenerlo en tu escena o singleton)


func _ready():
	# Desactivar highlights al inicio
	pc_btn.disable_tutorial_highlight()
	bed_btn.disable_tutorial_highlight()

	# Conectar señales de los botones
	pc_btn.pressed.connect(_on_pc_pressed)
	bed_btn.pressed.connect(_on_bed_pressed)

	# Conectar señal del DialogueManager cuando termina un diálogo
	DialogueManager.dialogue_ended.connect(_on_dialogue_finished)
	# Iniciar tutorial
	start_tutorial()


func start_tutorial():
	current_step = TutorialStep.CLICK_PC
	# Cargar diálogo de la PC
	DialogueManager.show_dialogue_balloon(load("res://dialogue/Tutorial/Tutorial_PC.dialogue"), "start")
	pc_btn.enable_tutorial_highlight()


func _on_pc_pressed():
	print('adasdasd')
	if current_step != TutorialStep.CLICK_PC:
		return

	pc_btn.disable_tutorial_highlight()
	current_step = TutorialStep.CLICK_BED
	
	print('ggfhfgh')
	# Cargar diálogo de la cama
	DialogueManager.show_dialogue_balloon(load("res://dialogue/Tutorial/Tutorial_Bed.dialogue"), "start")
	bed_btn.enable_tutorial_highlight()


func _on_bed_pressed():
	print('qeqweqwe')
	if current_step != TutorialStep.CLICK_BED:
		return

	bed_btn.disable_tutorial_highlight()
	current_step = TutorialStep.FINISHED
	print('oppopo')
	# Guardado automático
	if Engine.has_singleton("_SaveController"):
		_on_bedroom_btn_pressed()
	
	print('dgdf')
	# Cargar diálogo final del tutorial
	var ballon = DialogueManager.show_dialogue_balloon(load("res://dialogue/Tutorial/Tutorial_Room_Finish.dialogue"), "start")
	await DialogueManager.dialogue_ended
	_on_dialogue_finished()


func _on_dialogue_finished():
	print("dadasdas")
	# Cuando el último diálogo termina, pasar a la habitación real
	if current_step == TutorialStep.FINISHED:
		go_to_real_room()

func go_to_real_room():
	var real_room = "res://scenes/pages/maps/dormitory/player_room.tscn"
	print("Holaaaaaa")
	get_tree().change_scene_to_file(real_room)


func _on_bedroom_btn_pressed() -> void:
	_SaveController.save_game()
	$MessageLabel.visible = true
