class_name ServeBreadAction
extends Action

func execute(context):
	var cafeteria_context = context as CafeteriaProblemContext
	var student = cafeteria_context.current_student
	
	var bread_processed := "pan_preparado"

	#
	# ─── VALIDAR SI HAY PAN_PREPARADO EN INVENTARIO ───────────────
	#
	if not cafeteria_context.inventory.has(bread_processed):
		print("[ServeBreadAction] No hay pan preparado en el inventario.")
		return

	#
	# ─── QUITAR DE INVENTARIO ─────────────────────────────────────
	#
	cafeteria_context.inventory.erase(bread_processed)

	#
	# ─── QUITAR DE OUTPUTS (INVENTORY_CONTAINS) ───────────────────
	#
	var index_prepared = cafeteria_context.outputs.find_custom(
		func(item):
			return item.has("inventory_contains") and bread_processed in item["inventory_contains"]
	)

	if index_prepared != -1:
		print("Eliminar pan preparado")
		# Eliminar pan_preparado de la lista
		cafeteria_context.outputs[index_prepared]["inventory_contains"].erase(bread_processed)

		# Si quedó vacía eliminar la entrada completa
		if cafeteria_context.outputs[index_prepared]["inventory_contains"].is_empty():
			cafeteria_context.outputs.remove_at(index_prepared)

	#
	# ─── REGISTRAR EL SERVICIO DEL PAN ────────────────────────────
	#
	# pan_preparado → pan
	var original_item := bread_processed.replace("_preparado", "")

	var order_entry = {
		"nombre": student.nombre,
		"pedido": original_item
	}

	# Buscar si ya existe un registro "orders_served"
	var index_order_served = cafeteria_context.outputs.find_custom(
		func(item):
			return item.has("orders_served")
	)

	if index_order_served == -1:
		# Crear estructura nueva
		cafeteria_context.outputs.append({
			"orders_served": [order_entry]
		})
	else:
		# Añadir a la estructura existente
		cafeteria_context.outputs[index_order_served]["orders_served"].append(order_entry)

	#
	# ─── REGISTER LOGIC IN ENGINE LIST ────────────────────────────
	#
	cafeteria_context.orders_served.append(student)

	#
	# ─── EMIT SIGNAL ──────────────────────────────────────────────
	#
	cafeteria_context.serve_bread.emit(student)

	#
	# ─── DEBUG ────────────────────────────────────────────────────
	#
	print("[ServeBreadAction] Servicio de pan correcto.")
	print("- Inventario:", cafeteria_context.inventory)
	print("- Outputs:", cafeteria_context.outputs)
