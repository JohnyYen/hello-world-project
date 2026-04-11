class_name GetBreadAction
extends Action

func execute(context):
	var cafeteria_context = context as CafeteriaProblemContext
	print("Emitir señal de obtener pan")
	cafeteria_context.inventory.append("pan")
	var index_bread_inventory = cafeteria_context.outputs.find_custom(func(item):return item.has("inventory_contains") and "pan" in item["inventory_contains"])
	if index_bread_inventory == -1:
		print("Es nuevo el pan en el inventario")
		cafeteria_context.outputs.append({"inventory_contains": ["pan"]})
	else:
		print("Es viejo el pan en el inventorio")
		cafeteria_context.outputs[index_bread_inventory]["inventory_contains"].append("pan")
	cafeteria_context.get_bread.emit()
