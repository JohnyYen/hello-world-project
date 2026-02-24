extends SubViewport

@onready var player_zone = $PlayerZone

func _ready():
	update_player_zone()

# func _notification(what):
# 	if what == NOTIFICATION_RESIZED:
# 		update_player_zone()

func update_player_zone():
	var viewport_height = size.y
	player_zone.position.y = viewport_height - 150  # margen inferior fijo
