class_name LevelOneController
extends LevelController

func _init():
	self.context = CafeteriaProblemContext.new()
	self.block_repository = BlockRepository.new();
	self.modifier = LevelOneModifier.new()
	
	_GameController.agent.action_decided.connect(Callable(self.modifier, 'modify_level'))


func get_avaible_blocks() -> Array[Block]:
	# For level one, we might want to return specific blocks
	# For now, returning all blocks as an example

	print("DEBUG [Level One Controller]: Fetching available blocks for Level One")

	var blocks : Array[Block] = self.block_repository.get_all_blocks()
	# You can filter blocks based on level requirements here
	# For example, only blocks with block_id <= 5 for the first level
	var filtered_blocks : Array[Block] = []

	print("DEBUG [Level One Controller]: Total blocks fetched: ", blocks.size())

	for block in blocks:
		if block.block_id <= 10: # Adjust this condition based on your level requirements
			filtered_blocks.append(block);

	print("DEBUG [Level One Controller]: Filtered blocks for Level One: ", filtered_blocks.size())
	return filtered_blocks
	
func get_level_configuration(segment_id : int) -> LevelOneConfiguration:
	self.level_configuration = LevelOneConfiguration.new(segment_id).load_data()
	return self.level_configuration

func _update_context_with_config() -> CafeteriaProblemContext:
	self.context.expected_outputs = self.level_configuration.expected_outputs
	(self.context as CafeteriaProblemContext).student_queue = (self.level_configuration as LevelOneConfiguration).get_student_queue()
	(self.context as CafeteriaProblemContext).menu = (self.level_configuration as LevelOneConfiguration).initial_state["menu"]
	(self.context as CafeteriaProblemContext).inventory = (self.level_configuration as LevelOneConfiguration).initial_state["inventory"]
	(self.context as CafeteriaProblemContext).cash_register = (self.level_configuration as LevelOneConfiguration).initial_state["cash_register"]
	#(self.context as CafeteriaProblemContext).level_goal = (self.level_configuration as LevelOneConfiguration).goals
	(self.context as CafeteriaProblemContext).expected_outputs = (self.level_configuration as LevelOneConfiguration).expected_outputs
	print("DEBUG [Level One Controller]: Setup Context")
	return context

func get_problem_context() -> CafeteriaProblemContext:
	return _update_context_with_config();
