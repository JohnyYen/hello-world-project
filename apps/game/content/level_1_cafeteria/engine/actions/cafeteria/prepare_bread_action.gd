class_name PrepareBreadAction
extends Action

var bread_type := "pan"

func _init(type := "pan"):
	bread_type = type

func execute(context):
	var cafeteria_context = context as CafeteriaProblemContext

	# Verificar si hay pan en el inventario
	if not cafeteria_context.inventory.has(bread_type):
		print("[PrepareBreadAction] No hay pan en inventario. Estado actual:")
		print("- Inventario: ", cafeteria_context.inventory)
		print("- Expected outputs: ", cafeteria_context.expected_outputs)
		return
	
	#
	# ─── HAY PAN - PROCESAR ───────────────────────────────────────
	#
	
	print("1")
	# 1. Eliminar pan del inventario
	cafeteria_context.inventory.erase(bread_type)
	
	print("2")
	# 2. Eliminar pan de expected_outputs (si existe)
	var index_pan = cafeteria_context.outputs.find_custom(
		func(item):
			return item.has("inventory_contains") and bread_type in item["inventory_contains"]
	)

	if index_pan != -1:
		print("2.1")
		# Quitar pan de ese registro
		cafeteria_context.outputs[index_pan]["inventory_contains"].erase(bread_type)

		# Si quedó vacío, eliminar la entrada
		if cafeteria_context.outputs[index_pan]["inventory_contains"].is_empty():
			cafeteria_context.outputs.remove_at(index_pan)
			
	print("3")
	# 3. Añadir pan_preparado al inventario
	var processed = bread_type + "_preparado"
	cafeteria_context.inventory.append(processed)
	
	print("4")
	# 4. Añadir pan_preparado a expected_outputs
	var index_prepared = cafeteria_context.outputs.find_custom(
		func(item):
			return item.has("inventory_contains") and processed in item["inventory_contains"]
	)
	
	print("5")
	if index_prepared == -1:
		print("5.1")
		cafeteria_context.outputs.append({"inventory_contains": [processed]})
	else:
		print("5.2")
		cafeteria_context.outputs[index_prepared]["inventory_contains"].append(processed)

	# 5. Emitimos la señal normal
	cafeteria_context.prepare_bread.emit(processed)

	# Debug final
	print("[PrepareBreadAction] Pan procesado correctamente.")
	print("- Inventario: ", cafeteria_context.inventory)
	print("- Expected outputs: ", cafeteria_context.outputs)
