# ConnectionDetector.gd
# Detecta conectividad a internet mediante polling del backend
class_name ConnectionDetector
extends Node

## Señales
signal connection_status_changed(is_connected: bool)
signal connection_lost()
signal connection_restored()

## Estado
var _is_connected: bool = false
var _poll_timer: Timer
var _config: XAPIConfig
var _http_request: HTTPRequest

func _init() -> void:
	_config = XAPIConfig.new()

func _ready() -> void:
	# Crear timer para polling
	_poll_timer = Timer.new()
	add_child(_poll_timer)
	_poll_timer.timeout.connect(_on_poll_timeout)
	
	# Crear HTTPRequest para verificar conexión
	_http_request = HTTPRequest.new()
	add_child(_http_request)
	_http_request.request_completed.connect(_on_request_completed)
	
	# Iniciar polling
	_start_polling()
	
	print("DEBUG [ConnectionDetector]: Inicializado")

## Inicia el polling de conexión
func _start_polling() -> void:
	_poll_timer.start(_config.POLL_INTERVAL_SECONDS)
	# Verificar inmediatamente
	_check_connection()

## Detiene el polling
func stop() -> void:
	_poll_timer.stop()

## Verifica si hay conexión
func is_online() -> bool:
	return _is_connected

## Fuerza una verificación de conexión
func check_now() -> void:
	_check_connection()

## Handler del timer
func _on_poll_timeout() -> void:
	_check_connection()

## Realiza la verificación de conexión
func _check_connection() -> void:
	var url := _config.get_health_url()
	print("DEBUG [ConnectionDetector]: Verificando conexión a %s" % url)
	
	var err := _http_request.request(url, [], HTTPClient.METHOD_GET)
	if err != OK:
		_update_connection_status(false)
		push_error("ConnectionDetector: Error al iniciar request: %s" % err)

## Callback del request HTTP
func _on_request_completed(result: int, response_code: int, _headers: PackedStringArray, _body: PackedByteArray) -> void:
	if result == OK and response_code >= 200 and response_code < 300:
		_update_connection_status(true)
	else:
		_update_connection_status(false)

## Actualiza el estado de conexión y emite señales
func _update_connection_status(connected: bool) -> void:
	var was_connected := _is_connected
	if _is_connected != connected:
		_is_connected = connected
		connection_status_changed.emit(connected)
		
		if connected:
			print("DEBUG [ConnectionDetector]: Conexión restaurada")
			connection_restored.emit()
		else:
			print("DEBUG [ConnectionDetector]: Conexión perdida")
			connection_lost.emit()
	else:
		print("DEBUG [ConnectionDetector]: Estado de conexión: %s" % str(connected))