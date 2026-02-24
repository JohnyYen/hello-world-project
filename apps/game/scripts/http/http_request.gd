## HTTP Request class for making HTTP requests
## Provides a simplified interface for making HTTP requests using Godot's HTTPRequest node
class_name HttpRequest
extends Node
# HTTP request instance to handle network operations
var http := HTTPRequest.new()

## Makes an HTTP request to the specified URL
## @param url: The URL to make the request to
## @param method: The HTTP method (0 for GET, 1 for POST, 2 for PUT, etc.)
## @param body: The request body as a dictionary (will be converted to JSON)
## @param headers: An array of additional headers to include in the request
## @return: A dictionary containing the request result with keys:
##          - "OK": Boolean indicating if the request was successful
##          - "status": HTTP response code if successful
##          - "data": The parsed JSON response data if successful
##          - "error": Error message if the request failed
func request(endpoint: String, method: int = HTTPClient.METHOD_GET, body : Dictionary = {}, headers: Array = []) -> Dictionary:
    # Prepare the request body as JSON string if provided
    var json_body := ""

    print("DEBUG: Format Body JSON")
    if body:
        json_body = JSON.stringify(body)
        headers.append("Content-Type: application/json")

    print("DEBUG: Construct full URL")
    # Construct the full URL by combining API base URL with the endpoint
    var url = Env.API_BASE_URL + endpoint 
    
    print("DEBUG: Do Request")
    # Make the HTTP request with provided parameters
    var err = http.request(url, headers, method, json_body)

    # Check if the request failed to initiate
    if err != OK:
       return { "OK": false, "error": "Error al iniciar la solicitud HTTP: %s" % err}

    print("DEBUG: Get the response of request")

    # Wait for the request to complete and get the response
    var response = await http.request_completed

    print("DEBUG: Get Data")
    # Extract response components
    var status = response[0]              # Network status
    var response_code = response[1]       # HTTP response code
    var _headers = response[2]            # Response headers
    var body_bytes = response[3]          # Raw response body as bytes

    print("DEBUG: Check the error network")
    # Check for network errors
    if status != OK:
        return { "OK": false, "error": "Error de red: %s" % status }
    
    # Convert response body from bytes to string
    var body_text = body_bytes.get_string_from_utf8()

    # Parse the JSON response
    var json = JSON.parse_string(body_text)

    print("DEBUG: Send Response")
    # Check HTTP response code to determine success or failure
    if response_code >= 200 and response_code < 300:
        # Successful response
        return { "OK": true, "status": response_code, "data": json }
    else:
        # Error response
        return { "OK": false, "status": response_code, "error": json }
    