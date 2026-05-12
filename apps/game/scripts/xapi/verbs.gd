# xAPI Verbs Registry
class_name Verbs

const ATTEMPTED: String = "attempted"
const COMPLETED: String = "completed"
const ANSWERED: String = "answered"
const INITIALIZED: String = "initialized"
const TERMINATED: String = "terminated"
const PASSED: String = "passed"
const FAILED: String = "failed"

const VERBS := {
    ATTEMPTED: {
        "id": "http://adlnet.gov/expapi/verbs/attempted",
        "display": {
            "en-US": "attempted",
            "es-ES": "intentó"
        }
    },
    COMPLETED: {
        "id": "http://adlnet.gov/expapi/verbs/completed",
        "display": {
            "en-US": "completed",
            "es-ES": "completó"
        }
    },
    ANSWERED: {
        "id": "http://adlnet.gov/expapi/verbs/answered",
        "display": {
            "en-US": "answered",
            "es-ES": "respondió"
        }
    },
    INITIALIZED: {
        "id": "http://adlnet.gov/expapi/verbs/initialized",
        "display": {
            "en-US": "initialized",
            "es-ES": "inició"
        }
    },
    TERMINATED: {
        "id": "http://adlnet.gov/expapi/verbs/terminated",
        "display": {
            "en-US": "terminated",
            "es-ES": "terminó"
        }
    },
    PASSED: {
        "id": "http://adlnet.gov/expapi/verbs/passed",
        "display": {
            "en-US": "passed",
            "es-ES": "aprobó"
        }
    },
    FAILED: {
        "id": "http://adlnet.gov/expapi/verbs/failed",
        "display": {
            "en-US": "failed",
            "es-ES": "reprobó"
        }
    }
}

static func get(verb_key: String) -> Dictionary:
    if VERBS.has(verb_key):
        return VERBS[verb_key]
    return {}

static func get_id(verb_key: String) -> String:
    var verb := get(verb_key)
    if verb.is_empty():
        return ""
    return verb.get("id", "")

static func get_display(verb_key: String, lang: String = "es-ES") -> String:
    var verb := get(verb_key)
    if verb.is_empty():
        return ""
    var display := verb.get("display", {})
    return display.get(lang, display.get("en-US", ""))

static func is_valid(verb_key: String) -> bool:
    return VERBS.has(verb_key)

static func get_all_keys() -> Array[String]:
    return VERBS.keys()
