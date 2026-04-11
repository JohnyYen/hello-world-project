## Abstract base class for all problem contexts.
## Manages execution state, variables, and solution validation.
## Subclasses MUST override is_solution_correct() for domain-specific validation.
class_name BaseProblemContext

# --- Estado de la Ejecución del Programa ---
var program_counter: int = 0
var variables: Dictionary = {}  # Almacena variables del programa (ej: var_contador = 0)
var call_stack: Array = []     # Pila para manejar funciones (pares de índices de inicio/fin)
var is_running: bool = true      # Indica si el programa sigue ejecutándose

# --- Datos del Problema del Nivel Actual ---
# Estos deben ser definidos y gestionados por las subclases específicas del problema.
var inputs: Array = []          # Datos de entrada para el nivel
var outputs: Array = []         # Resultados producidos por el programa

# --- Salida esperada para verificar la solución ---
var expected_outputs: Array = []

# --- Last solution data (for metrics and validation) ---
var last_solution: SolutionData = null
var last_execution_context: ExecutionContext = null


func _init():
	pass


# --- Functions for blocks to interact with the context ---
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


# --- SolutionData integration ---
## Store the last submitted solution for metrics collection.
func set_solution(solution: SolutionData) -> void:
	last_solution = solution


## Store the last execution context for metrics and validation.
func set_execution_context(ctx: ExecutionContext) -> void:
	last_execution_context = ctx


## Apply solution data to the context (for backward compatibility).
## Converts SolutionData blocks into internal representation.
func apply_solution(solution: SolutionData) -> void:
	last_solution = solution
	if solution.has("blocks"):
		pass  # Blocks are executed by the executor, not stored here


# --- Validation ---
## Check if the level objective has been met.
## MUST be overridden by subclasses for domain-specific validation.
func is_solution_correct() -> bool:
	# Default implementation: compare outputs to expected
	return outputs == expected_outputs


# --- Logging ---
func log(message: String):
	print("[LOG]: ", message)
