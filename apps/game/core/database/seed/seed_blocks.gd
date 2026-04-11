func create_blocks(db) -> void:
    # BLOQUES
    db.insert_row("Blocks", {"block_type_id": 1, "description": "Nodo que dicta el inicio de la sentencia", "name": "Iniciar"})
    db.insert_row("Blocks", {"block_type_id": 2, "description": "Nodo que dicta el fin de la sentencia", "name": "Finalizar"})
    db.insert_row("Blocks", {"block_type_id": 3, "description": "Nodo que para ejecutar una instrucción", "name": "Ejecutar"})