## API Client para Godot - Maneja requests HTTP al backend
## Incluye login con JWT y sincronización completa de datos
## Usa HTTPRequest node para operaciones asíncronas
class_name ApiClient
extends Node

# HTTP request node para hacer peticiones
var http_request := HTTPRequest.new()

# JWT token para requests autenticados
var jwt_token: String = ""

# URL base para las peticiones API
# IMPORTANTE: Usar el nombre del autoload (Env), NO instanciar
var base_url: String = "http://localhost:8010"

# Datos del usuario autenticado
var current_user: Dictionary = {}

# Señales para notificar resultados
signal login_success(token: String, user_data: Dictionary)
signal login_failed(error: String)
signal sync_completed(result: Dictionary)
signal sync_failed(error: String)

func _ready() -> void:
	add_child(http_request)
	# En Godot 4, usamos await http_request.request_completed
	# NO necesitamos conectar la señal manualmente
	
	# Cargar token desde el store global si existe
	if Env.jwt_token != "":
		jwt_token = Env.jwt_token
		current_user = Env.current_user
		print("DEBUG [ApiClient]: Token cargado desde Env")

## Hace una petición HTTP al endpoint especificado
## @param endpoint: Ruta del API (ej: "/auth/login")
## @param method: Método HTTP (usar constantes HTTPClient.METHOD_*)
## @param body: Dictionary para enviar como JSON (opcional)
## @param auth_required: Si se debe incluir el token JWT en el header
## @return: Dictionary con keys "OK", "status", "data", "error"
func _make_request(endpoint: String, method: int, body: Dictionary = {}, auth_required: bool = true) -> Dictionary:
	var headers := ["Content-Type: application/json"]
	
	if auth_required and jwt_token != "":
		headers.append("Authorization: Bearer %s" % jwt_token)
	
	var json_body := ""
	if not body.is_empty():
		json_body = JSON.stringify(body)
	
	var url = base_url.rstrip("/") + "/" + endpoint.lstrip("/")
	
	var err = http_request.request(url, headers, method, json_body)
	if err != OK:
		var error_msg = "Error al iniciar request: %s" % err
		return {"OK": false, "error": error_msg}
	
	# Esperar a que se complete la petición
	var response = await http_request.request_completed
	
	var status = response[0]
	var response_code = response[1]
	var _headers = response[2]
	var body_bytes = response[3]
	
	if status != OK:
		var error_msg = "Error de red: %s" % status
		return {"OK": false, "error": error_msg}
	
	var body_text = body_bytes.get_string_from_utf8()
	var json = JSON.parse_string(body_text)
	
	if response_code >= 200 and response_code < 300:
		return {"OK": true, "status": response_code, "data": json}
	else:
		return {"OK": false, "status": response_code, "error": json}

## Inicia sesión y guarda el JWT token
## @param username: Nombre de usuario (opcional si se provee email)
## @param email: Email del usuario (opcional si se provee username)
## @param password: Contraseña (requerido)
## @return: Dictionary con el resultado del login
func login(username: String = "", email: String = "", password: String = "") -> Dictionary:
	var body = {"password": password}
	
	if username != "":
		body["username"] = username
	elif email != "":
		body["email"] = email
	else:
		return {"OK": false, "error": "Debe proporcionar username o email"}
	
	var result = await _make_request("api/v1/auth/login", HTTPClient.METHOD_POST, body, false)
	
	if result.OK:
		jwt_token = result.data.access_token
		current_user = result.data.user if result.data.has("user") else {}
		
		# Guardar en el store global
		Env.jwt_token = jwt_token
		Env.current_user = current_user
		print("DEBUG [ApiClient]: Token guardado en Env")
		
		login_success.emit(jwt_token, current_user)
		return {"OK": true, "status": result.status, "data": result.data}
	else:
		login_failed.emit(result.get("error", "Error desconocido"))
		return result

## Inicia una sesión de sincronización
## @param instance_id: ID de la instancia del juego (UUID string)
## @return: Dictionary con los datos de la sesión
func start_sync_session(instance_id: String) -> Dictionary:
	print("DEBUG [ApiClient]:start_sync_session() instance_id=%s" % instance_id)
	var body = {"instance_id": instance_id}
	print("DEBUG [ApiClient]:start_sync_session() body=%s" % str(body))
	var result = await _make_request("api/v1/sync/sync-sessions", HTTPClient.METHOD_POST, body)
	print("DEBUG [ApiClient]:start_sync_session() _make_request result.OK=%s" % result.OK)
	
	if result.OK:
		var session_id = result.data.id if result.data.has("id") else ""
		print("DEBUG [ApiClient]:start_sync_session() - SUCCESS session_id=%s" % session_id)
		return {"OK": true, "session_id": session_id, "data": result.data}
	else:
		var error_msg = result.get("error", "Error")
		var status_code = result.get("status", 0)
		print("DEBUG [ApiClient]:start_sync_session() - FALLO status=%d error=%s" % [status_code, str(error_msg)])
		return {"OK": false, "error": error_msg, "status": status_code}

## Registra un evento de sincronización
## @param session_id: ID de la sesión de sync (UUID string)
## @param event_type: Tipo de evento (ej: "level_completed")
## @param payload: Datos del evento (Dictionary)
## @return: Dictionary con el resultado
func register_sync_event(session_id: String, event_type: String, payload: Dictionary) -> Dictionary:
	print("DEBUG [ApiClient]:register_sync_event() session_id=%s event_type=%s" % [session_id, event_type])
	var body = {
		"sync_session_id": session_id,
		"event_type": event_type,
		"payload": payload
	}
	var result = await _make_request("api/v1/sync/sync-events", HTTPClient.METHOD_POST, body)
	print("DEBUG [ApiClient]:register_sync_event() result.OK=%s" % result.OK)
	
	if result.OK:
		return {"OK": true, "data": result.data}
	else:
		var error_msg = result.get("error", "Error")
		var status_code = result.get("status", 0)
		print("DEBUG [ApiClient]:register_sync_event() - FALLO status=%d" % status_code)
		return {"OK": false, "error": error_msg, "status": status_code}

## Finaliza una sesión de sincronización
## @param session_id: ID de la sesión de sync (UUID string)
## @return: Dictionary con el resultado
func end_sync_session(session_id: String) -> Dictionary:
	print("DEBUG [ApiClient]:end_sync_session() session_id=%s" % session_id)
	var endpoint = "api/v1/sync/sync-sessions/" + session_id + "/end"
	var result = await _make_request(endpoint, HTTPClient.METHOD_PUT, {})
	print("DEBUG [ApiClient]:end_sync_session() result.OK=%s" % result.OK)
	
	if result.OK:
		return {"OK": true, "data": result.data}
	else:
		return {"OK": false, "error": result.get("error", "Error"), "status": result.get("status", 0)}

## Ejecuta la sincronización completa
## @param instance_id: ID de la instancia del juego (UUID string)
## @param events: Array de eventos, cada uno con "event_type" y "payload"
## @return: Dictionary con el resultado de la sincronización
func sync_all(instance_id: String, events: Array) -> Dictionary:
	print("DEBUG [ApiClient]:sync_all() instance_id=%s, events.count=%d" % [instance_id, events.size()])
	
	# Iniciar sesión de sync
	print("DEBUG [ApiClient]:sync_all() - Llamando start_sync_session()...")
	var session_result = await start_sync_session(instance_id)
	print("DEBUG [ApiClient]:sync_all() - start_sync_session() retornó: %s" % str(session_result))
	
	if not session_result.OK:
		var error_detail = session_result.get("error", "Desconocido")
		var error_msg = "Error al iniciar sesión de sync: %s" % error_detail
		print("DEBUG [ApiClient]:sync_all() - ERROR en start: %s" % error_msg)
		sync_failed.emit(error_msg)
		return {"OK": false, "error": error_msg}
	
	var session_id = session_result.session_id
	print("DEBUG [ApiClient]:sync_all() - session_id=%s" % session_id)
	
	# Registrar todos los eventos
	var event_index = 0
	for event in events:
		event_index += 1
		var event_type = event.get("event_type", "")
		var payload = event.get("payload", {})
		print("DEBUG [ApiClient]:sync_all() - Registrando evento %d/%d: %s" % [event_index, events.size(), event_type])
		
		var event_result = await register_sync_event(session_id, event_type, payload)
		print("DEBUG [ApiClient]:sync_all() - Evento %d result: %s" % [event_index, str(event_result)])
		
		if not event_result.OK:
			# Intentar cerrar la sesión de todos modos
			await end_sync_session(session_id)
			var error_detail = event_result.get("error", "Desconocido")
			var error_msg = "Error al registrar evento: %s" % error_detail
			print("DEBUG [ApiClient]:sync_all() - ERROR en evento %d: %s" % [event_index, error_msg])
			sync_failed.emit(error_msg)
			return {"OK": false, "error": error_msg, "session_id": session_id}
	
	# Cerrar sesión de sync
	print("DEBUG [ApiClient]:sync_all() - Llamando end_sync_session()...")
	var end_result = await end_sync_session(session_id)
	print("DEBUG [ApiClient]:sync_all() - end_sync_session() retornó: %s" % str(end_result))
	
	if not end_result.OK:
		var error_detail = end_result.get("error", "Desconocido")
		var error_msg = "Error al cerrar sesión de sync: %s" % error_detail
		print("DEBUG [ApiClient]:sync_all() - ERROR en end: %s" % error_msg)
		sync_failed.emit(error_msg)
		return {"OK": false, "error": error_msg, "session_id": session_id}
	
	var events_count = events.size()
	var success_msg = "Sincronización completada: %s eventos enviados" % events_count
	print("DEBUG [ApiClient]:sync_all() - ÉXITO! events_count=%d" % events_count)
	sync_completed.emit({"session": end_result.data, "events_count": events_count})
	return {"OK": true, "message": success_msg, "session": end_result.data, "events_count": events_count}

## Verifica si hay un token JWT válido guardado
## @return: true si hay un token, false si no
func is_authenticated() -> bool:
	return jwt_token != ""

## Cierra la sesión eliminando el token
func logout() -> void:
	jwt_token = ""
	current_user = {}
