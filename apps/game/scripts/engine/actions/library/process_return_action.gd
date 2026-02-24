# Acción específica para procesar una devolución en la biblioteca
class_name ProcessReturnAction
extends Action
    
func execute(context: BaseProblemContext) -> void:
    var library_context = context as LibraryProblemContext
    if library_context != null:
        # Lógica para procesar una devolución
        context.log("Procesando devolución de libro...")
    else:
        context.log("Este contexto no soporta procesamiento de devoluciones.")