## Loads level definitions from JSON configuration files.
## Reduces hardcoded GDScript for level data by reading from external JSON.
class_name LevelJSONConfig

## Base path for level JSON configs
const LEVELS_DIR := "res://data/levels/"


## Load a level configuration from a JSON file.
## @param level_id: The level identifier (e.g., "cafeteria_level")
## @return: Dictionary with level data, or empty dict if not found
func load_level(level_id: String) -> Dictionary:
	var file_path := LEVELS_DIR + level_id + "_config.json"

	if not FileAccess.file_exists(file_path):
		push_warning("Level JSON config not found: " + file_path)
		return {}

	var file := FileAccess.open(file_path, FileAccess.READ)
	if file == null:
		push_error("Cannot open level JSON: " + file_path)
		return {}

	var json_text := file.get_as_text()
	file.close()

	var json = JSON.new()
	var parse_error := json.parse(json_text)
	if parse_error != OK:
		push_error("JSON parse error in %s at line %d: %s" % [file_path, json.get_error_line(), json.get_error_message()])
		return {}

	var data = json.data
	return data


## Load all segments for a level from JSON config.
## @param level_id: The level identifier
## @return: Array of segment dictionaries
func load_segments(level_id: String) -> Array:
	var level_data := load_level(level_id)

	if level_data.has("segments"):
		return level_data["segments"]

	return []


## Load a specific segment by ID from a level JSON config.
## @param level_id: The level identifier
## @param segment_id: The segment ID to find
## @return: Segment dictionary, or empty dict if not found
func load_segment(level_id: String, segment_id: int) -> Dictionary:
	var segments := load_segments(level_id)

	for segment in segments:
		if segment.get("segment_id") == segment_id:
			return segment

	push_warning("Segment %d not found in level %s" % [segment_id, level_id])
	return {}


## Check if a level JSON config exists.
func exists(level_id: String) -> bool:
	var file_path := LEVELS_DIR + level_id + "_config.json"
	return FileAccess.file_exists(file_path)


## List all available level config files.
func list_available_levels() -> Array:
	var levels: Array = []
	var dir := DirAccess.open(LEVELS_DIR)

	if dir == null:
		return levels

	dir.list_dir_begin()
	var file_name := dir.get_next()

	while file_name != "":
		if file_name.ends_with("_config.json"):
			var level_id = file_name.replace("_config.json", "")
			levels.append(level_id)
		file_name = dir.get_next()

	dir.list_dir_end()
	return levels
