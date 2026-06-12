class_name ProfessorFeedback

var id: String = ""
var student_id: String = ""
var professor_id: String = ""
var professor_name: String = ""
var comments: String = ""
var rating: int = 0
var feedback_type: String = ""
var course_id: String = ""
var game_id: String = ""
var level_id: String = ""
var display_in_game: bool = false
var acknowledged_at: String = ""
var is_read: bool = false
var created_at: String = ""
var updated_at: String = ""


func _init(p_id: String = "", p_comments: String = "") -> void:
    id = p_id
    comments = p_comments


func to_dict() -> Dictionary:
    return {
        "id": id,
        "student_id": student_id,
        "professor_id": professor_id,
        "professor_name": professor_name,
        "comments": comments,
        "rating": rating,
        "feedback_type": feedback_type,
        "course_id": course_id,
        "game_id": game_id,
        "level_id": level_id,
        "display_in_game": display_in_game,
        "acknowledged_at": acknowledged_at,
        "is_read": is_read,
        "created_at": created_at,
        "updated_at": updated_at
    }


static func from_api_dict(data: Dictionary) -> ProfessorFeedback:
    var fb := ProfessorFeedback.new()
    fb.id = str(data.get("id", ""))
    fb.student_id = str(data.get("student_id", ""))
    fb.professor_id = str(data.get("professor_id", ""))
    fb.professor_name = str(data.get("professor_name", ""))
    fb.comments = str(data.get("comments", ""))
    fb.rating = int(data.get("rating", 0))
    fb.feedback_type = str(data.get("feedback_type", ""))
    fb.course_id = str(data.get("course_id", ""))
    fb.game_id = str(data.get("game_id", ""))
    fb.level_id = str(data.get("level_id", ""))
    fb.display_in_game = bool(data.get("display_in_game", false))
    fb.acknowledged_at = str(data.get("acknowledged_at", ""))
    fb.is_read = false
    fb.created_at = str(data.get("created_at", ""))
    fb.updated_at = str(data.get("updated_at", ""))
    return fb
