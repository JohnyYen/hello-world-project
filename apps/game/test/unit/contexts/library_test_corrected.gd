# Unit test for LibraryProblemContext
extends Node

func test_library_problem_context():
    print("Iniciando prueba de LibraryProblemContext...")
    
    var error_occurred = false
    
    # Intentar crear una instancia de LibraryProblemContext
    var library_context
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
    
    # Si no hubo errores, hacer más pruebas
    if not error_occurred and library_context:
        # Probar propiedades heredadas
        print("   Probando propiedades heredadas...")
        library_context.set_variable("test_var", 42)
        var retrieved_value = library_context.get_variable("test_var")
        if retrieved_value == 42:
            print("   ✓ Propiedades heredadas funcionan correctamente")
        else:
            print("   ✗ Error en propiedades heredadas")
            error_occurred = true
            
        # Probar propiedades específicas de la biblioteca
        print("   Probando propiedades específicas de biblioteca...")
        library_context.books_to_return = ["Libro A", "Libro B"]
        if library_context.books_to_return.size() == 2:
            print("   ✓ Propiedades específicas de biblioteca funcionan")
        else:
            print("   ✗ Error en propiedades específicas de biblioteca")
            error_occurred = true

    # Resultado final
    if error_occurred:
        print("\n✗ Algunas pruebas fallaron")
        return false
    else:
        print("\n✓ Todas las pruebas pasaron exitosamente")
        return true

func _ready():
    var result = test_library_problem_context()
    if result:
        print("\n✓ Prueba de LibraryProblemContext completada exitosamente")
    else:
        print("\n✗ Prueba de LibraryProblemContext falló")