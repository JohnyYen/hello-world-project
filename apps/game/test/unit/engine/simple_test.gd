# Test simple del motor de ejecución
extends Node

func _ready():
    print("=== PRUEBA DEL MOTOR DE EJECUCIÓN ===")
    
    # Verificar que podemos crear instancias de las clases
    print("\n1. Verificando creación de clases...")
    
    # Intentar crear un contexto de cafetería
    var context
    var error_occurred = false
    
    context = CafeteriaProblemContext.new()
    if context != null:
        print("   ✓ CafeteriaProblemContext creado correctamente")
    else:
        print("   ✗ Error al crear CafeteriaProblemContext")
        error_occurred = true
        return

    # Configurar el contexto
    context.student_queue = [
        {"nombre": "Ana", "pedido": "cafe"},
        {"nombre": "Luis", "pedido": "te"}
    ]
    context.menu = {"cafe": 5, "te": 3}
    context.cash_register = 0
    context.level_goal = {"all_served": true}
    
    print("   Contexto configurado con", context.student_queue.size(), "estudiantes")
    
    # Intentar crear bloques
    print("\n2. Verificando creación de bloques...")
    
    var blocks = []
    
    # Crear un bloque básico usando el constructor correcto
    var base_block = StartBlock.new()
    if base_block != null:
        print("   ✓ Block base creado correctamente")
        blocks.append(base_block)
    else:
        print("   ✗ Error al crear Block base")
        error_occurred = true
        return
    
    # Probar el motor de ejecución con bloques vacíos
    print("\n3. Verificando motor de ejecución...")
    
    var result_context = ExecutionEngine.execute(blocks, context)
    if result_context != null:
        print("   ✓ ExecutionEngine ejecutado correctamente")
        print("   Estudiantes restantes:", result_context.student_queue.size())
    else:
        print("   ✗ Error al ejecutar ExecutionEngine")
        error_occurred = true
        return
    
    print("\n=== PRUEBA COMPLETADA ===")
    
    if not error_occurred:
        print("¡Todas las pruebas pasaron!")
    else:
        print("Hubo errores en las pruebas.")
        