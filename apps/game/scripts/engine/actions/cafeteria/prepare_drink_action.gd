# Acción específica para preparar una bebida en la cafetería
class_name PrepareDrinkAction
extends Action
	
func execute(context: BaseProblemContext) -> void:
	var cafeteria_context = context as CafeteriaProblemContext
	if cafeteria_context != null:
		# Lógica para preparar una bebida
		var drink_name = "cafe"  # Ejemplo de bebida
		cafeteria_context.prepare_drink.emit(drink_name)
		cafeteria_context.inventory.append(drink_name)
		context.log("Preparando bebida...")
	else:
		context.log("Este contexto no soporta preparación de bebidas.")
