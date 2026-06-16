class_name LevelOneController
extends LevelController

func _init():
	self.context = CafeteriaProblemContext.new()
	self.block_repository = BlockRepository.new();
	self.modifier = LevelOneModifier.new()
	
	_GameController.agent.action_decided.connect(Callable(self.modifier, 'modify_level'))


func get_avaible_blocks() -> Array[Block]:
	var blocks : Array[Block] = self.block_repository.get_all_blocks()
	
	# If level_configuration has available_blocks from the config, filter by block type
	var config_allowed := level_configuration.access_blocks if level_configuration != null else []
	if not config_allowed.is_empty():
		var name_to_type := {
			"Start": "START",
			"Execute": "ACTION",
			"End": "END",
			"Condition": "CONDITION",
			"Loop": "LOOP"
		}
		var allowed_types := []
		for name in config_allowed:
			if name in name_to_type:
				allowed_types.append(name_to_type[name])
		
		var filtered: Array[Block] = []
		for block in blocks:
			if block.block_type in allowed_types:
				filtered.append(block)
		return filtered
	
	# Fallback: filter by block_id (legacy behavior)
	var filtered_blocks : Array[Block] = []
	for block in blocks:
		if block.block_id <= 10:
			filtered_blocks.append(block)
	return filtered_blocks
	
func get_level_configuration(segment_id : int) -> LevelOneConfiguration:
	self.level_configuration = LevelOneConfiguration.new(segment_id).load_data()
	return self.level_configuration

func _update_context_with_config() -> CafeteriaProblemContext:
	self.context.expected_outputs = self.level_configuration.expected_outputs
	(self.context as CafeteriaProblemContext).student_queue = (self.level_configuration as LevelOneConfiguration).get_student_queue()
	(self.context as CafeteriaProblemContext).menu = (self.level_configuration as LevelOneConfiguration).initial_state.get("menu", {})
	(self.context as CafeteriaProblemContext).inventory = (self.level_configuration as LevelOneConfiguration).initial_state.get("inventory", [])
	(self.context as CafeteriaProblemContext).cash_register = (self.level_configuration as LevelOneConfiguration).initial_state.get("cash_register", 0)
	#(self.context as CafeteriaProblemContext).level_goal = (self.level_configuration as LevelOneConfiguration).goals
	(self.context as CafeteriaProblemContext).expected_outputs = (self.level_configuration as LevelOneConfiguration).expected_outputs
	#print("DEBUG [Level One Controller]: Setup Context")
	return context

func get_problem_context() -> CafeteriaProblemContext:
	return _update_context_with_config();
