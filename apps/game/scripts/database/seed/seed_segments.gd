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
			"segment_type": "bread-only",
			"required_actions": ["get_bread"],
			"difficulty_bounds": {"min_students": 0, "max_students": 0, "min_blocks": 3, "max_blocks": 8},
			"templates": {
				"decrease_major": {
					"title": "Nivel 1 - Aprende a tomar pan",
					"description": "Usa un bloque Ejecutar con la accion get_bread para tomar pan del dispensador",
					"learning_objective": "Introduccion a la secuencia de instrucciones"
				},
				"decrease_minor": {
					"title": "Nivel 1 - Toma pan del dispensador",
					"description": "Usa un bloque Ejecutar con get_bread",
					"learning_objective": "Ejecutar una accion simple"
				},
				"keep": {
					"title": "Nivel 1 - Segmento 1",
					"description": "Aprende a tomar un pan del dispensador",
					"learning_objective": "Introduccion a la secuencia de instrucciones"
				},
				"increase_minor": {
					"title": "Nivel 1 - Toma pan del dispensador",
					"description": "Usa la accion get_bread para tomar pan",
					"learning_objective": "Ejecutar una accion basica"
				},
				"increase_major": {
					"title": "Nivel 1 - Toma pan del dispensador",
					"description": "Identifica y usa get_bread para completar la tarea",
					"learning_objective": "Reconocer y ejecutar la accion correcta"
				}
			},
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
			"environment_data": {
				"bread_station": true,
				"drink_machine": false,
				"cash_register": false
			},
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
			"segment_type": "bread-only",
			"required_actions": ["get_bread", "prepare_bread"],
			"difficulty_bounds": {"min_students": 0, "max_students": 0, "min_blocks": 3, "max_blocks": 10},
			"templates": {
				"decrease_major": {
					"title": "Nivel 1 - Prepara pan paso a paso",
					"description": "Primero get_bread, luego prepare_bread. {student_count} estudiante{student_plural}",
					"learning_objective": "Secuencia de dos acciones"
				},
				"decrease_minor": {
					"title": "Nivel 1 - Prepara pan",
					"description": "Toma y prepara el pan con get_bread y prepare_bread",
					"learning_objective": "Secuencia de {student_count} accion{student_plural}"
				},
				"keep": {
					"title": "Nivel 1 - Segmento 2",
					"description": "Preparar pan despues de tomarlo",
					"learning_objective": "Secuencia de multiples acciones simples"
				},
				"increase_minor": {
					"title": "Nivel 1 - Prepara pan eficientemente",
					"description": "Combina get_bread y prepare_bread en el orden correcto",
					"learning_objective": "Secuencia de dos acciones en orden"
				},
				"increase_major": {
					"title": "Nivel 1 - Prepara pan sin ayuda",
					"description": "Descubre la secuencia correcta para preparar pan",
					"learning_objective": "Resolver secuencia de dos pasos"
				}
			},
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
			"environment_data": {
				"bread_station": true,
				"drink_machine": false,
				"cash_register": false
			},
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
			"segment_type": "bread-only",
			"required_actions": ["get_bread", "prepare_bread", "serve_bread"],
			"difficulty_bounds": {"min_students": 1, "max_students": 5, "min_blocks": 3, "max_blocks": 12},
			"templates": {
				"decrease_major": {
					"title": "Sirve pan a {student_count} estudiante{student_plural}",
					"description": "Prepara y sirve pan a {student_count} estudiante{student_plural}. Estudiantes: {student_names}",
					"learning_objective": "Atender a {student_count} cliente{student_plural}"
				},
				"decrease_minor": {
					"title": "Sirve pan a {student_count} estudiante{student_plural}",
					"description": "Toma, prepara y sirve pan a {student_count} estudiante{student_plural}",
					"learning_objective": "Atender a {student_count} cliente{student_plural}"
				},
				"keep": {
					"title": "Nivel 1 - Segmento 3",
					"description": "Servir pan preparado a un estudiante",
					"learning_objective": "Atender al primer cliente"
				},
				"increase_minor": {
					"title": "Sirve pan a {student_count} estudiantes",
					"description": "Atiende a {student_count} estudiantes con pedidos de pan",
					"learning_objective": "Atender multiples clientes"
				},
				"increase_major": {
					"title": "Sirve pan a {student_count} estudiantes",
					"description": "Organiza las acciones para servir a {student_names}",
					"learning_objective": "Gestionar multiples pedidos de pan"
				}
			},
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
			"environment_data": {
				"bread_station": true,
				"drink_machine": false,
				"cash_register": true
			},
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
			"segment_type": "drink-only",
			"required_actions": ["prepare_drink", "serve_drink"],
			"difficulty_bounds": {"min_students": 1, "max_students": 5, "min_blocks": 3, "max_blocks": 12},
			"templates": {
				"decrease_major": {
					"title": "Sirve bebida a {student_count} estudiante{student_plural}",
					"description": "Prepara y sirve {drink_item} a {student_count} estudiante{student_plural}",
					"learning_objective": "Atender a {student_count} cliente{student_plural} con bebidas"
				},
				"decrease_minor": {
					"title": "Sirve bebida a {student_count} estudiante{student_plural}",
					"description": "Prepara y sirve una bebida a {student_count} estudiante{student_plural}",
					"learning_objective": "Servir bebidas a {student_count} cliente{student_plural}"
				},
				"keep": {
					"title": "Nivel 1 - Segmento 4",
					"description": "Atender a un estudiante que pide bebida",
					"learning_objective": "Introduccion a acciones con bebidas"
				},
				"increase_minor": {
					"title": "Sirve bebidas a {student_count} estudiantes",
					"description": "Prepara y sirve {drink_item} a {student_count} estudiantes",
					"learning_objective": "Atender multiples pedidos de bebida"
				},
				"increase_major": {
					"title": "Sirve bebidas a {student_count} estudiantes",
					"description": "Organiza las acciones para servir bebidas a {student_count} estudiantes",
					"learning_objective": "Gestionar multiples pedidos de bebida"
				}
			},
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
			"environment_data": {
				"bread_station": false,
				"drink_machine": true,
				"cash_register": true
			},
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
			"segment_type": "mixed",
			"required_actions": ["get_bread", "prepare_bread", "serve_bread", "prepare_drink", "serve_drink"],
			"difficulty_bounds": {"min_students": 2, "max_students": 6, "min_blocks": 4, "max_blocks": 15},
			"templates": {
				"decrease_major": {
					"title": "Atiende a {student_count} estudiante{student_plural}",
					"description": "Los estudiantes tienen distintos pedidos. Atiende a {student_count} estudiante{student_plural}: {student_names}",
					"learning_objective": "Atender pedidos mixtos de {student_count} cliente{student_plural}"
				},
				"decrease_minor": {
					"title": "Atiende a {student_count} estudiante{student_plural}",
					"description": "Cada estudiante tiene un pedido especifico. Sirve a {student_count} estudiante{student_plural}",
					"learning_objective": "Atender {student_count} cliente{student_plural} correctamente"
				},
				"keep": {
					"title": "Nivel 1 - Segmento 5",
					"description": "Atender a dos clientes en orden con pedidos distintos",
					"learning_objective": "Secuencias mas complejas con multiples clientes"
				},
				"increase_minor": {
					"title": "Atiende a {student_count} estudiantes",
					"description": "{student_count} estudiantes esperan. Identifica cada pedido y sirve correctamente",
					"learning_objective": "Gestionar multiples pedidos variados"
				},
				"increase_major": {
					"title": "Atiende a {student_count} estudiantes",
					"description": "{student_count} estudiantes con pedidos variados. Usa las acciones correctas para cada uno",
					"learning_objective": "Resolver secuencia compleja de {student_count} pasos"
				}
			},
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
			"environment_data": {
				"bread_station": true,
				"drink_machine": true,
				"cash_register": true
			},
			"execution_rules": {
				"max_blocks": 8
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
