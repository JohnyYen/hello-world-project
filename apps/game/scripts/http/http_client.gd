## HTTP Client class using HTTPClient (Godot 4)
class_name HttpClient

var client := HTTPClient.new()
var base_url: String = Env.API_BASE_URL

# Makes an HTTP request to the specified endpoint
# method: HTTP method (GET, POST, PUT, etc.)
# body: dictionary to send as JSON
# headers: array of additional headers
# Returns: dictionary { OK, status, data, error }
func request(endpoint: String, method: int = HTTPClient.METHOD_GET, body: Dictionary = {}, headers: Array = []) -> Dictionary:
	var full_url = base_url.rstrip("/") + "/" + endpoint.lstrip("/")
	
	# Parse básico de host, puerto y path
	var is_https := full_url.begins_with("https://")
	var stripped := full_url.replace("https://", "").replace("http://", "")
	var slash_index := stripped.find("/")
	var host := stripped.substr(0, slash_index)
	var path := stripped.substr(slash_index, stripped.length())
	var port = is_https if 443 else 80

	
	# Connect to host
	var err = client.connect_to_host(host, port)
	if err != OK:
		return { "OK": false, "error": "Error al conectar al host: %s" % err }

	# Esperar a la conexión
	while client.get_status() in [HTTPClient.STATUS_CONNECTING, HTTPClient.STATUS_RESOLVING]:
		client.poll()

	if client.get_status() != HTTPClient.STATUS_CONNECTED:
		return { "OK": false, "error": "No se pudo establecer la conexión" }

	# Preparar body JSON si aplica
	var json_body := ""
	if body.size() > 0:
		json_body = JSON.stringify(body)
		headers.append("Content-Type: application/json")

	# Iniciar la petición
	err = client.request(method, full_url, headers, json_body)
	if err != OK:
		return { "OK": false, "error": "Error al iniciar la solicitud HTTP: %s" % err }

	# Esperar a que la petición se complete
	while client.get_status() in [HTTPClient.STATUS_REQUESTING, HTTPClient.STATUS_BODY]:
		client.poll()

	if client.get_status() != HTTPClient.STATUS_BODY and client.get_status() != HTTPClient.STATUS_CONNECTED:
		return { "OK": false, "error": "Error en la solicitud HTTP" }

	# Leer body completo
	var response_body := ""
	while client.get_status() == HTTPClient.STATUS_BODY:
		client.poll()
		var chunk = client.read_response_body_chunk()
		response_body += chunk.get_string_from_utf8()

	# Parse JSON
	var json_result = {}
	if response_body != "":
		var parsed = JSON.parse_string(response_body)
		if parsed.error != OK:
			return { "OK": false, "error": "Error parseando JSON: %s" % parsed.error }
		json_result = parsed.result

	var status_code = client.get_response_code()

	if status_code >= 200 and status_code < 300:
		return { "OK": true, "status": status_code, "data": json_result }
	else:
		return { "OK": false, "status": status_code, "error": json_result }
