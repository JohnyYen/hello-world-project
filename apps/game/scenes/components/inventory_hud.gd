class_name InventoryHUD
extends Node

@export var inventory_container: HBoxContainer

func add_inventory_item(item_name: String, quantity: int = 1):
	# Busca si el item ya existe para actualizar cantidad
	for child in inventory_container.get_children():
		if child.get_meta("item_name") == item_name:
			var qty_label = child.get_node("Quantity")
			qty_label.text = "x" + str(int(qty_label.text.substr(1)) + quantity)
			return

	# Si no existe, crea uno nuevo
	var item_box = PanelContainer.new()
	item_box.set_meta("item_name", item_name)

	var hbox = HBoxContainer.new()
	item_box.add_child(hbox)

	var name_label = Label.new()
	name_label.text = item_name

	var qty_label = Label.new()
	qty_label.name = "Quantity"
	qty_label.text = "x" + str(quantity)

	hbox.add_child(name_label)
	hbox.add_child(qty_label)
	inventory_container.add_child(item_box)

func remove_inventory_item(item_name: String):
	for child in inventory_container.get_children():
		if child.get_meta("item_name") == item_name:
			child.queue_free()
			return

func clear_inventory():
	for child in inventory_container.get_children():
		child.queue_free()

func set_inventory(items: Array):
	clear_inventory()
	for item in items:
		# item puede ser un String o un Dictionary {"name": "pan", "qty": 2}
		if item is String:
			add_inventory_item(item)
		elif item is Dictionary:
			add_inventory_item(item["name"], item.get("qty", 1))
