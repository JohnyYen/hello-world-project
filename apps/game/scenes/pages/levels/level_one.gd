extends Node2D

var level_id: int = 1;
var level_repository: LevelRepository;
var segments_repository: SegmentRepository;
var segments : Array
var level: Level;
var is_complete_level_one = false
@onready var title : RichTextLabel
@onready var button_list : VBoxContainer = $CanvasLayer/VBoxContainer
@onready var result;
func _ready():
	
	
	
	level_repository = LevelRepository.new();
	segments_repository = SegmentRepository.new()
	title = $CanvasLayer/RichTextLabel;
	level = level_repository.get_level_by_id(level_id);
	segments = segments_repository.get_all_segments_by_level(level_id)
	
	title.text = level.title;
	
	
	var index_button : int = 1;
	
	for hbox in button_list.get_children():
		if hbox == Control:
			continue;
		
		for btn in hbox.get_children():
			if btn is TextureButton:	
				btn.pressed.connect(Callable(self._on_pressed_load_level).bind(index_button))
				index_button += 1
			
		
	

func _on_pressed_load_level(index : int):
	var segment_scene = preload("res://scenes/pages/levels/level_one_segment.tscn")
	var fade = preload("res://scenes/transition/fade.tscn").instantiate()
	if index == 1:
		var introduction_class = preload("res://scenes/pages/levels/init_class.tscn").instantiate()
		is_complete_level_one = true
		introduction_class.dialog_dir =  "res://assets/dialogues/introduction_class_one.json"
		introduction_class.previous_scene_path = "res://scenes/pages/levels/level_one.tscn"
		get_tree().root.add_child(introduction_class)
		get_tree().current_scene.queue_free()
		get_tree().current_scene = introduction_class
		
	elif index > 1 and index <= 6:
		add_child(fade);
		await fade.fade_in()
		
		var instantiate = segment_scene.instantiate()
		instantiate.segment = segments[index-2]
		
		get_tree().root.add_child(instantiate)
		get_tree().current_scene.queue_free()
		get_tree().current_scene = instantiate
		
		await fade.fade_out()
		fade.queue_free()
	

	
