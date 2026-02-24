# Acción específica para prestar un libro en la biblioteca
class_name LendBookAction
extends Action

func execute(context: BaseProblemContext) -> void:
    var library_context = context as LibraryProblemContext
    if library_context != null:
        # Lógica para prestar un libro
        context.log("Prestando un libro...")
    else:
        context.log("Este contexto no soporta préstamos de libros.") 