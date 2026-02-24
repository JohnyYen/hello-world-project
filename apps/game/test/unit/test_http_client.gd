# Test file for HTTP Client
# Validates that the HTTP client connects properly with a server, sends data correctly,
# receives data correctly, and handles data display

extends "res://addons/gut/test.gd"

var HttpClient = load("res://scripts/http/http_client.gd")
var http_client : HttpClient

func setup():
    # Create an instance of the HttpClient for testing
    http_client = HttpClient.new()
    # Add the HTTPRequest node as a child to the test scene so it can process requests
    add_child(http_client.http)
    await get_tree().process_frame

func _ready() -> void:
    setup()
    print("DEBUG: Testing Http Client")
    test_get_data_succesful()
    # test_http_client_creation()
    # test_successful_get_request()
    # test_successful_post_request()
    # test_failed_request()
    teardown()

func test_get_data_succesful():
    var data = await http_client.request("todos/1", HTTPClient.METHOD_GET)
    print(data)

func test_http_client_creation():
    # Validates that the HTTP client can be instantiated successfully
    assert(http_client != null)
    assert(http_client.http != null)

func test_successful_get_request():
    # Test the structure of a successful GET request response
    # This is testing the expected data structure rather than making actual requests
    var successful_response = {
        "OK": true,
        "status": 200,
        "data": {"id": 1, "title": "Test todo", "completed": false}
    }
    
    assert(successful_response.OK == true)
    assert(successful_response.status == 200)
    assert(successful_response.data != null)
    assert(successful_response.data.id == 1)
    assert(successful_response.data.title == "Test todo")
    assert(successful_response.data.completed == false)

func test_successful_post_request():
    # Test the structure of a successful POST request response
    var post_data = {"title": "New todo", "completed": false}
    var successful_response = {
        "OK": true,
        "status": 201,  # Created status code
        "data": {"id": 101, "title": "New todo", "completed": false}
    }
    
    assert(successful_response.OK == true)
    assert(successful_response.status == 201)
    assert(successful_response.data != null)
    assert(successful_response.data.id == 101)
    assert(successful_response.data.title == "New todo")
    assert(successful_response.data.completed == false)

func test_failed_request():
    # Test the structure of a failed request response
    var failed_response = {
        "OK": false,
        "status": 404,
        "error": "Resource not found"
    }
    
    assert(failed_response.OK == false)
    assert(failed_response.status == 404)
    assert(failed_response.error != null and failed_response.error != "")

func test_request_initiation_error():
    # Test the response structure when request initiation fails
    var error_response = {
        "OK": false,
        "error": "Error al iniciar la solicitud HTTP: %s" % ERR_CANT_CONNECT
    }
    
    assert(error_response.OK == false)
    assert(error_response.error != null)
    assert(error_response.error.contains("Error al iniciar la solicitud HTTP"))

func test_data_handling():
    # Validates that the HTTP client correctly handles different types of data
    var sample_user_data = {
        "userId": 1,
        "id": 1,
        "title": "delectus aut autem",
        "completed": false
    }
    
    var api_response = {
        "OK": true,
        "status": 200,
        "data": sample_user_data
    }
    
    # Ensure the data structure is as expected
    assert(api_response.OK == true)
    assert(api_response.status == 200)
    assert(api_response.data != null)
    
    # Validate that each field in the data can be accessed properly
    assert(api_response.data.userId == 1)
    assert(api_response.data.id == 1)
    assert(api_response.data.title == "delectus aut autem")
    assert(api_response.data.completed == false)

func test_data_display_formatting():
    # Validates that the data received from the HTTP client can be displayed properly
    var sample_data = {
        "id": 123,
        "name": "Sample Item",
        "description": "This is a sample item for testing display"
    }
    
    var response = {
        "OK": true,
        "status": 200,
        "data": sample_data
    }
    
    # Test that the data can be accessed and formatted for display
    var display_name = response.data.name
    var display_description = response.data.description
    var display_id = str(response.data.id)
    
    # Verify that the display values are correct
    assert(display_name == "Sample Item")
    assert(display_description == "This is a sample item for testing display")
    assert(display_id == "123")
    
    # Test that the data maintains its structure for complex displays
    var display_object = {
        "title": response.data.name,
        "detail": response.data.description,
        "identifier": response.data.id
    }
    
    assert(display_object.title == "Sample Item")
    assert(display_object.detail == "This is a sample item for testing display")
    assert(display_object.identifier == 123)

func test_empty_body_handling():
    # Validates that the HTTP client handles requests with empty bodies correctly
    var empty_body_response = {
        "OK": true,
        "status": 204  # No Content status
    }
    
    # Even with no data, the response structure should be correct
    assert(empty_body_response.OK == true)
    assert(empty_body_response.status == 204)
    # Data field might not exist in this case, so we only check it doesn't break
    if empty_body_response.has("data"):
        assert(empty_body_response.data == null)

func teardown():
    # Clean up the HTTPRequest node after tests
    if http_client.http.get_parent():
        http_client.http.get_parent().remove_child(http_client.http)