## Abstract base class for player interaction mechanisms.
## Defines HOW players express their solutions to problems.
##
## Subclasses MUST implement get_player_solution().
## Examples of concrete implementations:
##   - BlockInteraction: Visual programming blocks (current game)
##   - DragDropInteraction: Dragging objects in a scene
##   - TextInputInteraction: Writing code or text answers
##   - SelectionInteraction: Choosing from multiple options
##   - TimelineInteraction: Ordering events on a timeline
class_name InteractionMechanism

## Emitted when the player submits their solution
signal solution_submitted(solution: SolutionData)

## Emitted when the player starts interacting
signal interaction_started()

## Emitted when the player resets their solution
signal solution_reset()


## Returns the player's current solution.
## MUST be overridden by subclasses.
func get_player_solution() -> SolutionData:
	push_error("InteractionMechanism.get_player_solution() is abstract. Subclasses MUST implement this method.")
	return null


## Resets the interaction state.
## MAY be overridden by subclasses.
func reset() -> void:
	push_warning("InteractionMechanism.reset() not implemented by subclass.")


## Checks if the player has provided a valid solution.
## MAY be overridden by subclasses.
func has_valid_solution() -> bool:
	push_warning("InteractionMechanism.has_valid_solution() not implemented by subclass.")
	return false


## Gets available options/elements for the player.
## MAY be overridden by subclasses.
func get_available_elements() -> Array:
	push_warning("InteractionMechanism.get_available_elements() not implemented by subclass.")
	return []


## Converts this interaction's data to SolutionData format.
## Utility method for subclasses.
func _create_solution(data: Dictionary) -> SolutionData:
	var solution := SolutionData.new()
	solution.timestamp = Time.get_unix_time_from_system()
	for key in data:
		solution.set_data(key, data[key])
	return solution
