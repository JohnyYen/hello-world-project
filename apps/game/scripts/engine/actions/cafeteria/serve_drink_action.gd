class_name ServeDrinkAction
extends Action

func execute(context):
	var cafeteria_context = context as CafeteriaProblemContext
	var student = cafeteria_context.current_student
	
	var item := "cafe"

	#
	# ─── VALIDAR INVENTARIO ──────────────────────────────────────
	#
	if not cafeteria_context.inventory.has(item):
		print("[ServeDrinkAction] No hay café en inventario.")
		print("- Inventario:", cafeteria_context.inventory)
		print("- Outputs:", cafeteria_context.outputs)
		return

	#
	# ─── QUITAR DEL INVENTARIO ───────────────────────────────────
	#
	cafeteria_context.inventory.erase(item)


	#
	# ─── QUITAR DE OUTPUTS (INVENTORY_CONTAINS) ──────────────────
	#
	var index_inventory = cafeteria_context.outputs.find_custom(
		func(entry):
			return entry.has("inventory_contains") and item in entry["inventory_contains"]
	)

	if index_inventory != -1:
		# Eliminar el café de la lista
		cafeteria_context.outputs[index_inventory]["inventory_contains"].erase(item)

		# Si la lista quedó vacía, eliminar el registro completo
		if cafeteria_context.outputs[index_inventory]["inventory_contains"].is_empty():
			cafeteria_context.outputs.remove_at(index_inventory)


	#
	# ─── REGISTRAR EL SERVICIO ───────────────────────────────────
	#
	var served_entry := {
		"nombre": student.nombre,
		"pedido": item
	}

	# Buscar si ya existe orders_served
	var index_orders = cafeteria_context.outputs.find_custom(
		func(entry):
			return entry.has("orders_served")
	)

	if index_orders == -1:
		cafeteria_context.outputs.append({
			"orders_served": [served_entry]
		})
	else:
		cafeteria_context.outputs[index_orders]["orders_served"].append(served_entry)


	#
	# ─── GUARDAR TAMBIÉN EN LA LISTA DEL CONTEXTO ────────────────
	#
	cafeteria_context.orders_served.append(student)


	#
	# ─── EMITIR SEÑAL ────────────────────────────────────────────
	#
	cafeteria_context.serve_drink.emit(student)


	#
	# ─── DEBUG ───────────────────────────────────────────────────
	#
	print("[ServeDrinkAction] Café servido correctamente.")
	print("- Inventario:", cafeteria_context.inventory)
	print("- Outputs:", cafeteria_context.outputs)
