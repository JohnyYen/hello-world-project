# Acción específica para atender a un estudiante en la cafetería
class_name AttendStudentAction
extends Action
	
func execute(context: BaseProblemContext) -> void:
	var cafeteria_context = context as CafeteriaProblemContext
	if cafeteria_context != null and cafeteria_context.student_queue.size() > 0:
		if context.student_queue.size() == 0:
			context.emit_signal("no_students_left")
			return
	
		var student = cafeteria_context.student_queue.pop_front()
		cafeteria_context.current_student = student
		cafeteria_context.attend_student.emit(student)
		context.log("Atendiendo a: " + str(student["nombre"]))
	elif cafeteria_context != null:
		context.log("No hay más clientes en la cola.")
