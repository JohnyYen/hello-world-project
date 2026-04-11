func seed_level_1(_db: SQLite) -> void:
	var level_id := 1 # ID del nivel correspondiente

	# =======================
	# JSON DEL NIVEL 1
	# =======================
	var segments_data = [
		{
			"title": "Nivel 1 - Segmento 1",
			"description": "Aprende a tomar un pan del dispensador",
			"version": "1.0",
			"segment_id": 1,
			"initial_state": {
				"student_queue": [],
				"menu": {"pan": 1},
				"cash_register": 0,
				"inventory": [],
				"stations": {
					"bread_dispenser": ["pan"]
				}
			},
			"expected_outputs": [
				{"inventory_contains": ["pan"]}
			],
			"available_blocks": ["Start", "Execute", "End"],
			"learning_objective": "Introducción a la secuencia de instrucciones",
			"environment_data": {},
			"execution_rules": {
				"max_blocks": 5
			},
			"validation_criteria": [
				{
					"condition": "inventory contains pan",
					"description": "El jugador debe tomar el pan correctamente"
				}
			],
			"feedback_messages": {
				"success": "¡Perfecto! Has tomado pan del dispensador.",
				"failure": "No se ha colocado pan en el inventario.",
				"hints": [
					"Recuerda usar un bloque Ejecutar.",
					"La acción correcta es get_bread()."
				]
			},
			"ui_config": {
				"code_editor": {
					"syntax_highlighting": true,
					"line_numbers": true
				},
				"visualization": {
					"show_state": true,
					"animation_speed": 1
				}
			},
			"defined_actions": [
				{"name": "Tomar pan", "value": "get_bread"}
			]
		},
		{
			"title": "Nivel 1 - Segmento 2",
			"description": "Preparar pan después de tomarlo",
			"version": "1.0",
			"segment_id": 2,
			"initial_state": {
				"student_queue": [],
				"menu": {"pan": 1},
				"cash_register": 0,
				"inventory": [],
				"stations": {
					"bread_dispenser": ["pan"]
				}
			},
			"expected_outputs": [
				{"inventory_contains": ["pan_preparado"]}
			],
			"available_blocks": ["Start", "Execute", "End"],
			"learning_objective": "Secuencia de múltiples acciones simples",
			"environment_data": {},
			"execution_rules": {
				"max_blocks": 6
			},
			"validation_criteria": [
				{
					"condition": "inventory contains pan_preparado",
					"description": "El jugador debe tomar y preparar el pan"
				}
			],
			"feedback_messages": {
				"success": "¡Muy bien! Has preparado el pan.",
				"failure": "Falta preparar el pan después de tomarlo.",
				"hints": [
					"Primero get_bread(), luego prepare_bread()."
				]
			},
			"ui_config": {
				"code_editor": {
					"syntax_highlighting": true,
					"line_numbers": true
				},
				"visualization": {
					"show_state": true,
					"animation_speed": 1
				}
			},
			"defined_actions": [
				{"name": "Atender estudiante", "value": "attend_next_student"},
				{"name": "Tomar pan", "value": "get_bread"},
				{"name": "Preparar pan", "value": "prepare_bread"}
			]
		},
		{
			"title": "Nivel 1 - Segmento 3",
			"description": "Servir pan preparado a un estudiante",
			"version": "1.0",
			"segment_id": 3,
			"initial_state": {
				"student_queue": [
					{"nombre": "Ana", "pedido": "pan"}
				],
				"menu": {"pan": 1},
				"cash_register": 0,
				"inventory": [],
				"stations": {
					"bread_dispenser": ["pan"]
				}
			},
			"expected_outputs": [
				{"orders_served": [ {"nombre": "Ana", "pedido": "pan"}]}
			],
			"available_blocks": ["Start", "Execute", "End"],
			"learning_objective": "Atender al primer cliente",
			"environment_data": {},
			"execution_rules": {
				"max_blocks": 8
			},
			"validation_criteria": [
				{
					"condition": "Ana served",
					"description": "El jugador debe entregar el pan preparado"
				}
			],
			"feedback_messages": {
				"success": "¡Excelente! Ana recibió su pan.",
				"failure": "El pan no fue entregado correctamente.",
				"hints": [
					"Primero prepara el pan.",
					"Luego sirve usando serve_bread(student)."
				]
			},
			"ui_config": {
				"code_editor": {
					"syntax_highlighting": true,
					"line_numbers": true
				},
				"visualization": {
					"show_state": true,
					"animation_speed": 1
				}
			},
			"defined_actions": [
				{"name": "Atender estudiante", "value": "attend_next_student"},
				{"name": "Tomar pan", "value": "get_bread"},
				{"name": "Preparar pan", "value": "prepare_bread"},
				{"name": "Servir pan", "value": "serve_bread"}
			]
		},
		{
			"title": "Nivel 1 - Segmento 4",
			"description": "Atender a un estudiante que pide bebida",
			"version": "1.0",
			"segment_id": 4,
			"initial_state": {
				"student_queue": [
					{"nombre": "Luis", "pedido": "cafe"}
				],
				"menu": {"cafe": 1},
				"cash_register": 0,
				"inventory": [],
				"stations": {
					"drink_dispenser": ["cafe"]
				}
			},
			"expected_outputs": [
				{"orders_served": [ {"nombre": "Luis", "pedido": "cafe"}]}
			],
			"available_blocks": ["Start", "Execute", "End"],
			"learning_objective": "Introducción a acciones con bebidas",
			"environment_data": {},
			"execution_rules": {
				"max_blocks": 8
			},
			"validation_criteria": [
				{
					"condition": "Luis served",
					"description": "El jugador debe preparar y entregar la bebida"
				}
			],
			"feedback_messages": {
				"success": "¡Muy bien! Luis recibió su café.",
				"failure": "El café no fue entregado.",
				"hints": [
					"Usa prepare_drink('cafe')",
					"Luego serve_drink(student)"
				]
			},
			"ui_config": {
				"code_editor": {
					"syntax_highlighting": true,
					"line_numbers": true
				},
				"visualization": {
					"show_state": true,
					"animation_speed": 1
				}
			},
			"defined_actions": [
				{"name": "Atender estudiante", "value": "attend_next_student"},
				{"name": "Preparar bebida", "value": "prepare_drink"},
				{"name": "Servir bebida", "value": "serve_drink"}
			]
		},
		{
			"title": "Nivel 1 - Segmento 5",
			"description": "Atender a dos clientes en orden con pedidos distintos",
			"version": "1.0",
			"segment_id": 5,
			"initial_state": {
				"student_queue": [
					{"nombre": "Ana", "pedido": "pan"},
					{"nombre": "Carlos", "pedido": "cafe"}
				],
				"menu": {"pan": 1, "cafe": 1},
				"cash_register": 0,
				"inventory": [],
				"stations": {
					"bread_dispenser": ["pan"],
					"drink_dispenser": ["cafe"]
				}
			},
			"expected_outputs": [
				{"orders_served": [
					{"nombre": "Ana", "pedido": "pan"},
					{"nombre": "Carlos", "pedido": "cafe"}
				]}
			],
			"available_blocks": ["Start", "Execute", "End"],
			"learning_objective": "Secuencias más complejas con múltiples clientes",
			"environment_data": {},
			"execution_rules": {
				"max_blocks": 12
			},
			"validation_criteria": [
				{
					"condition": "All students served",
					"description": "Los dos pedidos deben completarse en orden"
				}
			],
			"feedback_messages": {
				"success": "¡Excelente! Todos los clientes fueron atendidos correctamente.",
				"failure": "No todos los pedidos fueron entregados.",
				"hints": [
					"Atiende siempre al primer estudiante en la fila.",
					"Cada pedido requiere una secuencia correcta de acciones."
				]
			},
			"ui_config": {
				"code_editor": {
					"syntax_highlighting": true,
					"line_numbers": true
				},
				"visualization": {
					"show_state": true,
					"animation_speed": 1
				}
			},
			"defined_actions": [
				{"name": "Atender estudiante", "value": "attend_next_student"},
				{"name": "Tomar pan", "value": "get_bread"},
				{"name": "Preparar pan", "value": "prepare_bread"},
				{"name": "Servir pan", "value": "serve_bread"},
				{"name": "Preparar bebida", "value": "prepare_drink"},
				{"name": "Servir bebida", "value": "serve_drink"}
			]
		}
	]
	var i : int = 1
	# Inserta cada segmento
	for seg_data in segments_data:
		var config_str := JSON.stringify(seg_data)
		
		_db.insert_row("Segments", {
			"segment_id": seg_data.get("segment_id", 1),
			"level_id": level_id,
			"problem": seg_data.get("description", ""),
			"goal": seg_data.get("learning_objective", ""),
			"position": i,
			"difficulty": "easy",
			"configuration": config_str
		})

	print("Se han insertado todos los segmentos del Nivel 1.")
