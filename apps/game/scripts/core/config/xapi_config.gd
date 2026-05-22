# xAPI Configuration
class_name XAPIConfig
extends Node

const BATCH_SIZE: int = 50
const MAX_RETRIES: int = 5
const POLL_INTERVAL_SECONDS: float = 30.0
const BASE_RETRY_DELAY_SECONDS: float = 1.0
const MAX_RETRY_DELAY_SECONDS: float = 16.0

var base_url: String = ""
var health_endpoint: String = "/health"

func _init() -> void:
    base_url = Env.API_BASE_URL

func get_health_url() -> String:
    return base_url + health_endpoint

func get_sync_endpoint() -> String:
    return base_url + "/api/v1/sync/sync-events"

func calculate_retry_delay(retry_count: int) -> float:
    var delay := BASE_RETRY_DELAY_SECONDS * pow(2.0, retry_count)
    return minf(delay, MAX_RETRY_DELAY_SECONDS)
