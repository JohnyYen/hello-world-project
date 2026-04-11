class_name LibraryExecutionBlock
extends Block

# Esta propiedad almacena la acción específica del dominio de la biblioteca.
# Ej: "procesar_siguiente_libro", "ordenar_libro_en_estanteria", "prestar_libro"
var stored_action: String

func execute(context: BaseProblemContext):
    # La lógica aquí depende del nivel y de la acción.
    # Necesitamos una forma de mapear acciones a funciones.
    # Por ahora, usamos un `match`. Una "ActionFactory" sera más elegante a largo plazo.
    
    # Verificar si el contexto es del tipo LibraryProblemContext
    var library_context = context as LibraryProblemContext
    if library_context == null:
        context.log("Error: Este bloque solo puede ejecutarse en un contexto de biblioteca")
        return
    
    match stored_action:
        "procesar_siguiente_libro":
            if library_context.book_queue.size() > 0:
                var book = library_context.book_queue.pop_front()
                # Simular el procesamiento: añadir a la lista de libros devueltos
                library_context.returned_books.append(book)
                context.log("Procesando libro: " + str(book["title"]))
            else:
                context.log("No hay más libros en la cola para procesar.")
        
        "prestar_libro":
            # Lógica simplificada: tomar el primer libro disponible de una estantería
            var book_prestado = false
            for shelf_name in library_context.bookshelves.keys():
                if library_context.bookshelves[shelf_name].size() > 0:
                    var book = library_context.bookshelves[shelf_name].pop_front()
                    library_context.borrowed_books.append(book)
                    context.log("Prestado libro: " + str(book["title"]) + " de la estantería " + shelf_name)
                    book_prestado = true
                    break
            
            if not book_prestado:
                context.log("¡No hay libros disponibles para prestar!")
        
        "ordenar_libro_en_estanteria":
            # Lógica para ordenar libros devueltos en estanterías
            if library_context.returned_books.size() > 0:
                var book = library_context.returned_books.pop_front()
                var shelf_name = book.get("category", "general")
                
                # Crear la estantería si no existe
                if not library_context.bookshelves.has(shelf_name):
                    library_context.bookshelves[shelf_name] = []
                
                library_context.bookshelves[shelf_name].append(book)
                context.log("Ordenado libro: " + str(book["title"]) + " en la estantería " + shelf_name)
            else:
                context.log("¡No hay libros devueltos para ordenar!")
        
        _:
            context.log("Acción no reconocida o no implementada: " + stored_action)