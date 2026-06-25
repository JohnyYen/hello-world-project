extends Node

signal execute_block(block: Block)
signal level_loaded(segment_id: int, level_number: int, actor_id: String)
signal action_decided(action: String, new_difficulty: float)
signal execution_finished(context: BaseProblemContext)
