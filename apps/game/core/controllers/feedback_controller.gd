# Controller class that manages the feedback system
# Handles receiving performance data, determining appropriate feedback,
# and displaying it to the player at appropriate times
class_name FeedbackController
extends Node

## Reference to the feedback configuration
var config := FeedbackConfig.new()

## Queue to store pending feedback messages
var feedback_queue := []

## Track the last time feedback was displayed to respect minimum intervals
var last_feedback_time := 0.0

## Track player context (current level, recent metrics)
var current_level: String = "cafeteria"
var recent_performance_data: Dictionary = {}

@export var feedback_panel_scene: PackedScene = preload("res://scenes/components/feedback/feedback_ballon.tscn")
@export var hud_node: HUD  # un control o canvaslayer del juego


## Signal emitted when feedback is generated, containing the feedback data
signal feedback_generated(feedback_data: Dictionary)

## Initialize the controller and connect to event bus
func _ready():
	print("DEBUG: FeedbackController ready")

	# Connect to event bus for relevant events
	# EventBus.connect("player_action_performed", _on_player_action)
	# EventBus.connect("performance_updated", _on_performance_updated)
	# EventBus.connect("level_changed", _on_level_changed)

## Process performance data and potentially generate feedback
## @param raw_data Dictionary containing performance metrics
func process_feedback(raw_data: Dictionary):
	print("DEBUG: FeedbackController.process_feedback called with: ", raw_data)

	# Store the most recent performance data
	recent_performance_data = raw_data

	# Determine if we should display feedback based on timing
	if not _should_display_feedback():
		print("DEBUG: Skipping feedback due to timing constraints")
		return

	# Generate the feedback message
	var feedback_data = _generate_feedback(raw_data)
	if feedback_data:
		feedback_queue.append(feedback_data)
		_process_queue()

## Determine if feedback should be displayed based on configuration
## @return bool indicating whether feedback should be displayed
func _should_display_feedback() -> bool:
	var current_time = Time.get_ticks_msec() / 1000.0
	var time_since_last = current_time - last_feedback_time

	# Get the minimum interval for the current level
	var min_interval = config.LEVEL_FEEDBACK_SETTINGS.get(current_level, {}).get("min_interval", config.FEEDBACK_MIN_INTERVAL)

	return time_since_last >= min_interval

## Generate appropriate feedback based on performance data
## @param raw_data Dictionary containing performance metrics
## @return Dictionary containing feedback data or null if no feedback should be generated
func _generate_feedback(raw_data: Dictionary) -> Dictionary:
	print("DEBUG: Generating feedback from raw data: ", raw_data)

	var score = raw_data.get("score", 0.5)
	var errors = raw_data.get("errors", 0)
	var avg_score = raw_data.get("avg_score", 0.5)

	# Determine feedback type based on performance metrics
	var feedback_type = FeedbackConfig.FeedbackType.POSITIVE
	var message = ""

	# Logic to determine feedback type
	if score >= config.PERF_SCORE_THRESHOLD_HIGH:
		feedback_type = FeedbackConfig.FeedbackType.POSITIVE
	elif score <= config.PERF_SCORE_THRESHOLD_LOW:
		if errors >= config.ERROR_COUNT_THRESHOLD_HIGH:
			feedback_type = FeedbackConfig.FeedbackType.CORRECTIVE
		else:
			feedback_type = FeedbackConfig.FeedbackType.NEGATIVE
	elif errors >= config.ERROR_COUNT_THRESHOLD_HIGH:
		feedback_type = FeedbackConfig.FeedbackType.CORRECTIVE
	else:
		# For scores in the middle range, randomly select motivational or informational
		if randf() < 0.5:
			feedback_type = FeedbackConfig.FeedbackType.MOTIVATIONAL
		else:
			feedback_type = FeedbackConfig.FeedbackType.INFORMATIONAL

	# Select a random message of the determined type
	var messages = config.FEEDBACK_MESSAGES.get(feedback_type, [])
	if messages.size() > 0:
		message = messages[randi() % messages.size()]

	print("DEBUG: Determined feedback type: ", feedback_type, " with message: ", message)

	return {
		"type": feedback_type,
		"message": message,
		"priority": config.FEEDBACK_PRIORITY.get(feedback_type, 0),
		"timestamp": Time.get_ticks_msec() / 1000.0
	}

## Process the feedback queue and show feedback if appropriate
func _process_queue():
	if feedback_queue.size() == 0:
		return

	# Sort queue by priority (highest first) and then by timestamp (oldest first)
	feedback_queue.sort_custom(Callable(self, "_compare_feedback_priority"))

	# Limit the queue size based on configuration
	if feedback_queue.size() > config.FEEDBACK_QUEUE_SIZE:
		feedback_queue.resize(config.FEEDBACK_QUEUE_SIZE)

	# Show the highest priority feedback
	var feedback_data = feedback_queue[0]

	# Update the last feedback time before showing
	last_feedback_time = Time.get_ticks_msec() / 1000.0

	print("DEBUG: Showing feedback: ", feedback_data.message)
	show_feedback(feedback_data)

	# Remove the shown feedback from the queue
	feedback_queue.remove_at(0)

## Compare function for sorting feedback by priority and timestamp
## @param a First feedback dictionary to compare
## @param b Second feedback dictionary to compare
## @return bool indicating whether a should come before b
func _compare_feedback_priority(a: Dictionary, b: Dictionary) -> bool:
	if a.priority != b.priority:
		return a.priority > b.priority  # Higher priority first
	return a.timestamp < b.timestamp  # Older first among same priority

## Display feedback to the player
## @param feedback_data Dictionary containing feedback information to display
func show_feedback(feedback_data: Dictionary):
	print("DEBUG: Displaying feedback in UI")

	var panel = feedback_panel_scene.instantiate()

	# Set the text inside the panel
	panel.show_feedback(feedback_data.message)

	# Add it to the HUD
	hud_node.add_child(panel)

	# Emit the signal for other systems if needed
	emit_signal("feedback_generated", feedback_data)


## Convert the feedback type enum to the corresponding string for the balloon
## @param feedback_type_enum The enum value to convert
## @return String representation of the feedback type
func _convert_enum_to_string(feedback_type_enum) -> String:
	match feedback_type_enum:
		FeedbackConfig.FeedbackType.POSITIVE:
			return "positive"
		FeedbackConfig.FeedbackType.NEGATIVE:
			return "negative"
		FeedbackConfig.FeedbackType.CORRECTIVE:
			return "negative"  # Using negative style for corrective feedback
		FeedbackConfig.FeedbackType.INFORMATIONAL:
			return "info"
		FeedbackConfig.FeedbackType.MOTIVATIONAL:
			return "positive"  # Using positive style for motivational feedback
		_:
			return "neutral"  # Default to neutral

## Update the current level context
## @param level The new level identifier
func set_current_level(level: String):
	current_level = level

## Clear the feedback queue
func clear_queue():
	feedback_queue.clear()

## Event handler for when player performs an action
## @param action_data Dictionary containing information about the player action
func _on_player_action(action_data: Dictionary):
	print("DEBUG: Received player action: ", action_data)
	# Process action to see if feedback is needed
	# In a real implementation, this would depend on the specific action

## Event handler for when performance data is updated
## @param performance_data Dictionary containing updated performance metrics
func _on_performance_updated(performance_data: Dictionary):
	process_feedback(performance_data)

## Event handler for when level changes
## @param new_level String identifier for the new level
func _on_level_changed(new_level: String):
	set_current_level(new_level)
