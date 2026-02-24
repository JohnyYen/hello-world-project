class_name ActionFactory

static func create_action(action : String) -> Action:
	match action:
		"attend_next_student":
			return AttendStudentAction.new();
		"prepare_drink":
			return PrepareDrinkAction.new();
		"get_bread":
			return GetBreadAction.new()
		"serve_bread":
			return ServeBreadAction.new()
		"serve_drink":
			return ServeDrinkAction.new()
		"prepare_bread":
			return PrepareBreadAction.new()
		_:
			push_error("ACTION_NOT_EXIST");
	
	return NullAction.new();

# Acción nula para casos donde no se encuentra una acción específica
class NullAction:
	extends Action
	
	func execute(context: BaseProblemContext) -> void:
		context.log("Acción no reconocida o no implementada.")
