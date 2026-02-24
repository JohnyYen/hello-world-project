# Test script for the execution engine
extends Node

# Variables para los IDs de los bloques
var block_id_counter = 1

func create_block(block_type_id: int, description: String, name: String) -> Block:
    var block = Block.new(block_id_counter, block_type_id, description, name)
    block_id_counter += 1
    return block

func _ready():
    print("Iniciando prueba del motor de ejecución...")
    
    # Crear un contexto de cafetería
    var context = CafeteriaProblemContext.new()
    
    # Configurar el estado inicial de la cafetería
    context.student_queue = [
        {"nombre": "Ana", "pedido": "cafe"},
        {"nombre": "Luis", "pedido": "te"},
        {"nombre": "Carlos", "pedido": "cafe"}
    ]
    context.menu = {"cafe": 10, "te": 5}
    context.cash_register = 0
    context.expected_outputs = [ {"nombre": "Ana", "pedido": "cafe"}, {"nombre": "Luis", "pedido": "te"}, {"nombre": "Carlos", "pedido": "cafe"}]
    
    # Configurar objetivos del nivel
    context.level_goal = {"all_served": true}
    
    print("Contexto inicial creado:")
    print("  Cola de estudiantes: ", context.student_queue)
    print("  Menú: ", context.menu)
    print("  Caja registradora: ", context.cash_register)
    
    # Crear un programa simple: Inicio -> Ejecutar (atender) -> Ejecutar (atender) -> Ejecutar (atender) -> Fin
    var blocks = []
    
    # Crear bloques usando el constructor correcto
    var start_block = StartBlock.new();
    
    # Para los bloques especializados, necesitamos crear una instancia de Block
    # y luego añadir las propiedades específicas
    var execute_block1 = ExecutionBlock.new();
    execute_block1.stored_action = "atender_siguiente_cliente"
    
    var execute_block2 = ExecutionBlock.new();
    execute_block2.stored_action = "atender_siguiente_cliente"

    
    var execute_block3 = ExecutionBlock.new();
    execute_block3.stored_action = "atender_siguiente_cliente"
    
    var end_block = EndBlock.new();
    
    # Añadir bloques al programa
    blocks.append(start_block)
    blocks.append(execute_block1)
    blocks.append(execute_block2)
    blocks.append(execute_block3)
    blocks.append(end_block)
    
    print("\nPrograma creado con ", blocks.size(), " bloques")
    
    # Ejecutar el programa
    print("\nEjecutando el programa...")
    var final_context = ExecutionEngine.execute(blocks, context)
    
    # Imprimir resultados
    print("\nResultados después de la ejecución:")
    print("  Estudiantes atendidos: ", final_context.orders_served)
    print("  Caja registradora: ", final_context.cash_register)
    print("  Cola de estudiantes restante: ", final_context.student_queue)
    
    # Verificar la solución
    print("\nVerificando solución...")
    var is_correct = final_context.is_solution_correct()
    print("¿Solución correcta?: ", is_correct)
    
    if is_correct:
        print("¡Prueba pasada!")
    else:
        print("¡Prueba fallida!")
    
    # Salir de Godot después de la prueba
    print("\nFinalizando prueba.")