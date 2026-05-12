# UUID utilities
class_name UUID

## Genera un UUID v4 aleatorio
static func generate() -> String:
	var uuid := ""
	var hex_chars := "0123456789abcdef"
	
	for i in range(32):
		var random_index := randi() % 16
		uuid += hex_chars[random_index]
		if i == 7 or i == 11 or i == 15 or i == 19:
			uuid += "-"
	
	return uuid