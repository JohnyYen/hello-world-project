extends Node

const DATABASE_URL = "res://data/hello_world_database.db"
const SAVE_FILE_PATH = "res://data/savegame.json"
const API_BASE_URL = "http://localhost:8010"
const ENVIORMENT = "dev"
const GAME_TITLE = "Hello World"
const LEVEL_PROGRESS_PATH = "user://levels_progress.json"

## Global JWT token storage - accesible desde cualquier ApiClient
var jwt_token: String = ""
var current_user: Dictionary = {}
