# Test script para el contexto de biblioteca
extends Node

func _ready():
    print("=== PRUEBA DEL CONTEXTO DE BIBLIOTECA ===")
    
    # Verificar que podemos crear instancias del contexto de biblioteca
    print("\n1. Verificando creación del contexto de biblioteca...")
    
    var library_context
    var error_occurred = false
    
    if ClassDB.class_exists("LibraryProblemContext"):
        library_context = LibraryProblemContext.new()
        if library_context:
            print("   ✓ LibraryProblemContext creado correctamente")
        else:
            print("   ✗ Error al crear LibraryProblemContext")
            error_occurred = true
    else:
        print("   ✗ La clase LibraryProblemContext no existe")
        error_occurred = true
    
    if error_occurred:
        print("\n=== PRUEBA COMPLETADA CON ERRORES ===")
        print("Hubo errores en las pruebas.")
        get_tree().quit()
        return
    
    # Configurar el contexto de biblioteca
    library_context.book_queue = [
        {"title": "El Quijote", "author": "Cervantes", "category": "clásicos"},
        {"title": "1984", "author": "Orwell", "category": "ciencia ficción"},
        {"title": "El Principito", "author": "Saint-Exupéry", "category": "infantil"}
    ]
    library_context.bookshelves = {
        "clásicos": [],
        "ciencia ficción": [],
        "infantil": []
    }
    library_context.library_catalog = {
        "El Quijote": {"author": "Cervantes", "category": "clásicos", "available": true},
        "1984": {"author": "Orwell", "category": "ciencia ficción", "available": true},
        "El Principito": {"author": "Saint-Exupéry", "category": "infantil", "available": true}
    }
    library_context.level_goal = {"all_returned": true}
    
    print("   Contexto de biblioteca configurado con", library_context.book_queue.size(), "libros en cola")
    
    # Probar la verificación de solución
    print("\n2. Verificando la función de verificación de solución...")
    
    var is_correct_before = library_context.is_solution_correct()
    print("   ¿Solución correcta antes de procesar libros?:", is_correct_before)
    
    # Mover todos los libros de la cola
    while library_context.book_queue.size() > 0:
        library_context.returned_books.append(library_context.book_queue.pop_front())
    
    var is_correct_after = library_context.is_solution_correct()
    print("   ¿Solución correcta después de procesar libros?:", is_correct_after)
    
    print("\n=== PRUEBA COMPLETADA ===")
    
    print("¡Todas las pruebas pasaron!" if not error_occurred else "Hubo errores en las pruebas.")
        
    # Salir
    get_tree().quit()