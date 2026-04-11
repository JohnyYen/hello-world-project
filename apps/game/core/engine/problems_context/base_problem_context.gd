class_name BaseProblemContext

# --- Estado de la Ejecución del Programa ---
var program_counter: int = 0
var variables: Dictionary = {}  # Almacena variables del programa (ej: var_contador = 0)
var call_stack: Array = []     # Pila para manejar funciones (pares de índices de inicio/fin)
var is_running: bool = true      # Indica si el programa sigue ejecutándose

# --- Datos del Problema del Nivel Actual ---
# Estos deben ser definidos y gestionados por las subclases específicas del problema.
# Ejemplos genéricos que pueden ser utilizados:
var inputs: Array = []          # Datos de entrada para el nivel
var outputs: Array = []         # Resultados producidos por el programa

# --- Salida esperada para verificar la solución ---
# Debe ser definida por la subclase.
var expected_outputs: Array = []

func _init():
	pass

# --- Funciones para que los bloques interactúen con el contexto ---
func advance_pc():
	program_counter += 1

func jump_to(index: int):
	program_counter = index

func set_variable(name: String, value):
	variables[name] = value

func get_variable(name: String):
	return variables.get(name, null)

func push_call(start_index: int, end_index: int):
	call_stack.append({"start": start_index, "end": end_index})

func pop_call():
	return call_stack.pop_back() if !call_stack.is_empty() else null

# --- Función para verificar si el objetivo del nivel se ha cumplido ---
# Esta función debe ser sobrescrita por las subclases para implementar
# la lógica específica de verificación del nivel.
func is_solution_correct() -> bool:
	# Implementación por defecto, puede ser sobrescrita.
	return outputs == expected_outputs

# --- Función para registrar logs de ejecución ---
func log(message: String):
	print("[LOG]: ", message)
