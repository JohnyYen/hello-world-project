class_name CafeteriaProblemContext
extends BaseProblemContext

# --- Señales específicas del problema de la Cafetería ---
signal attend_student(student)
signal prepare_drink(drink_name)
signal serve_drink(student)
signal no_students_left()
signal player_move_to(position)
signal money_added(amount)

signal get_bread()
signal prepare_bread()
signal serve_bread(student)

# --- Datos específicos del problema de la Cafetería ---
var student_queue: Array = []      # Estudiantes esperando ser atendidos
var current_student = null         # El estudiante actualmente atendido
var menu: Dictionary = {}          # Productos disponibles
var cash_register: int = 0         # Dinero acumulado
var orders_served: Array = []      # Auditoría de pedidos completados
var inventory : Array = []         # Posesion de los objetos en posesion del jugador 

# --- Objetivo del nivel ---
var level_goal: Dictionary = {}

func _init():
	student_queue = []
	current_student = null
	menu = {}
	cash_register = 0
	orders_served = []
	level_goal = {}


func is_solution_correct() -> bool:
	print("Verificando si la solución del nivel es correcta...", level_goal)
	if level_goal.is_empty():
		print(outputs)
		print(expected_outputs)
		print("No hay objetivos definidos para este nivel, se usara uno por defecto, ",  outputs == expected_outputs)
		return outputs == expected_outputs

	for goal_key in level_goal.keys():
		print("Verificando objetivo: " + goal_key)
		match goal_key:
			"all_served":
				if level_goal[goal_key] and student_queue.size() > 0:
					print("No se han atendido a todos los estudiantes.")
					return false

			"min_money":
				if cash_register < level_goal[goal_key]:
					print(
						"No se ha alcanzado el dinero mínimo. Actual: " +
						str(cash_register) +
						", Requerido: " +
						str(level_goal[goal_key])
					)
					return false

			_:
				print("Condición de objetivo desconocida: " + str(goal_key))
				return false

	print("¡Todos los objetivos del nivel cumplidos!")
	return true
