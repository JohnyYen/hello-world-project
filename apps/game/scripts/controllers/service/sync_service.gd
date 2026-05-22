## Servicio de sincronización que usa el ApiClient
## Maneja el login y sincronización de datos del juego
class_name SyncService
extends Node

var api_client := ApiClient.new()

# Datos locales que se sincronizarán
var pending_events: Array = []

func _ready() -> void:
	add_child(api_client)
	# Conectar señales
	api_client.login_success.connect(_on_login_success)
	api_client.login_failed.connect(_on_login_failed)
	api_client.sync_completed.connect(_on_sync_completed)
	api_client.sync_failed.connect(_on_sync_failed)
	print("DEBUG [SyncService]: Inicializado")

## Configura las credenciales y hace login
## @param username: Usuario (opcional)
## @param email: Email (opcional)
## @param password: Contraseña
func login(username: String = "", email: String = "", password: String = "") -> void:
	print("DEBUG [SyncService]:/login() llamado con username=%s" % username)
	# El login es asíncrono, pero usamos señales para el resultado
	api_client.login(username, email, password)

## Agrega un evento a la cola de sincronización pending
## @param event_type: Tipo de evento (ej: "level_completed")
## @param payload: Datos del evento
func add_event(event_type: String, payload: Dictionary) -> void:
	pending_events.append({
		"event_type": event_type,
		"payload": payload
	})
	print("DEBUG [SyncService]:add_event() - event_type=%s, Total=%d" % [event_type, pending_events.size()])

## Ejecuta la sincronización de todos los eventos pendientes
## @param instance_id: ID de la instancia del juego (UUID string)
func sync_all_pending(instance_id: String) -> void:
	print("DEBUG [SyncService]:sync_all_pending() instance_id=%s" % instance_id)
	print("DEBUG [SyncService]:sync_all_pending() pending_events.size()=%d" % pending_events.size())
	print("DEBUG [SyncService]:sync_all_pending() is_authenticated()=%s" % api_client.is_authenticated())
	
	if pending_events.is_empty():
		print("DEBUG [SyncService]:sync_all_pending() - No hay eventos pendientes")
		return
	
	if not api_client.is_authenticated():
		print("ERROR [SyncService]: No hay sesión activa. Haga login primero.")
		return
	
	# La sincronización es asíncrona, el resultado llega por señales
	print("DEBUG [SyncService]:sync_all_pending() - Llamando api_client.sync_all()...")
	api_client.sync_all(instance_id, pending_events)
	print("DEBUG [SyncService]:sync_all_pending() - api_client.sync_all() retornar")

## Callback: Login exitoso
func _on_login_success(token: String, user_data: Dictionary) -> void:
	print("DEBUG [SyncService]:_on_login_success() - token=%s, user=%s" % [token.substr(0, 20), user_data.get("username", "unknown")])
	# Aquí podrías guardar el token localmente si quieres persistencia

## Callback: Login fallido
func _on_login_failed(error: String) -> void:
	push_error("ERROR [SyncService]: Login fallido: %s" % error)
	print("DEBUG [SyncService]:_on_login_failed() error=%s" % error)

## Callback: Sincronización completada
func _on_sync_completed(result: Dictionary) -> void:
	print("DEBUG [SyncService]:_on_sync_completed() result=%s" % str(result))
	# Limpiar eventos pendientes después del sync exitoso
	pending_events.clear()
	print("DEBUG [SyncService]: Sincronización completada - Eventos limpiados")

## Callback: Sincronización fallida
func _on_sync_failed(error: String) -> void:
	push_error("ERROR [SyncService]: Sincronización fallida: %s" % error)
	print("DEBUG [SyncService]:_on_sync_failed() error=%s" % error)

## EJEMPLO de cómo usar este servicio desde otro script:
## 
## # En tu escena de juego (ej: cafeteria_gameplay.gd):
## var sync_service := SyncService.new()
## add_child(sync_service)
## 
## # 1. Hacer login (los resultados vienen por señales)
## sync_service.login("estudiante1", "", "password123")
## 
## # 2. Agregar eventos mientras juega
## sync_service.add_event("level_started", {"level_id": 1, "timestamp": Time.get_time_string_from_system()})
## sync_service.add_event("level_completed", {"level_id": 1, "score": 0.95, "errors": 2, "time": 125.5})
## 
## # 3. Cuando haya conexión, sincronizar todo
## sync_service.sync_all_pending(1)  # 1 es el instance_id
## 
## # Nota: Los eventos se limpian automáticamente después de un sync exitoso