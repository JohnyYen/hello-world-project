# Script de prueba básico para Godot 3
# Uso sintaxis compatiple con Godot 3 (no await, no features de Godot 4)

extends SceneTree

func _init():
	print("===========")
	print("PRUEBA DE SYNCRONIZACIÓN")
	print("===========")
	
	# Test 1: Verificar conexión
	print("Test 1: Verificando conexión al backend...")
	var http = HTTPRequest.new()
	get_root().add_child(http)
	
	# Esperar un frame
	yield(get_tree(), "idle_frame")
	
	# Hacer request simple
	var err = http.request("http://127.0.0.1:8000/api/v1/health", [], HTTPClient.METHOD_GET, "")
	
	if err != OK:
		print("ERROR: No se pudo conectar al backend")
		print("Asegúrese que el backend esté en 127.0.0.1:8000")
	else:
		print("Request enviado, esperando respuesta...")
	
	# Esperar respuesta
	yield(http, "request_completed")
	
	print("Test completado.")
	print("===========")
	
	# Salir
	get_tree().quit()

func _ready():
	pass
