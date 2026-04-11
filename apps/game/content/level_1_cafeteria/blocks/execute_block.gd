class_name ExecutionBlock
extends BaseBlock

# Esta propiedad almacena la acción específica del dominio del nivel.
# Ej: "atender_siguiente_cliente", "preparar_bebida:cafe", "cobrar_pedido"
var stored_action: String

func _init(action : String = "NOT_PASSED") -> void:
	self.stored_action = action

func execute(context: BaseProblemContext):
	# La lógica aquí depende del nivel y de la acción.
	# Necesitamos una forma de mapear acciones a funciones.
	# Por ahora, usamos un `match`. Una "ActionFactory" sera más elegante a largo plazo.
	

	# Verificar si el contexto es del tipo CafeteriaProblemContext
	# TODO: Mover valdiación a las acciones correspondientes según el contexto
	var cafeteria_context = context as CafeteriaProblemContext
	if cafeteria_context == null:
		context.log("Error: Este bloque solo puede ejecutarse en un contexto de cafetería")
		return

	var action : Action = ActionFactory.create_action(self.stored_action);

	action.execute(context);
   
