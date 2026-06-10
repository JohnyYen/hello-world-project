# test_verbs.gd
extends GutTest

# =============================================================================
# Verbs.is_valid tests
# =============================================================================

func test_is_valid_returns_true_for_known_verbs() -> void:
    assert_eq(Verbs.is_valid(Verbs.ATTEMPTED), true)
    assert_eq(Verbs.is_valid(Verbs.COMPLETED), true)
    assert_eq(Verbs.is_valid(Verbs.ANSWERED), true)
    assert_eq(Verbs.is_valid(Verbs.INITIALIZED), true)
    assert_eq(Verbs.is_valid(Verbs.TERMINATED), true)
    assert_eq(Verbs.is_valid(Verbs.PASSED), true)
    assert_eq(Verbs.is_valid(Verbs.FAILED), true)

func test_is_valid_returns_false_for_unknown_verb() -> void:
    assert_eq(Verbs.is_valid("nonexistent"), false)
    assert_eq(Verbs.is_valid(""), false)

# =============================================================================
# Verbs.INTERACTED tests (Ciclo 2)
# =============================================================================

func test_interacted_is_valid() -> void:
    assert_eq(Verbs.is_valid("interacted"), true,
        "INTERACTED debe ser un verbo válido")

func test_interacted_has_id() -> void:
    var verb_id := Verbs.get_id("interacted")
    assert_has(verb_id, "adlnet.gov",
        "INTERACTED debe usar IRI de ADLNET")

func test_interacted_has_spanish_display() -> void:
    var display := Verbs.get_display("interacted")
    assert_eq(display, "interactuó",
        "get_display debe retornar 'interactuó' para español")

func test_interacted_has_english_display() -> void:
    var display := Verbs.get_display("interacted", "en-US")
    assert_eq(display, "interacted",
        "get_display('en-US') debe retornar 'interacted'")

func test_interacted_in_get_all_keys() -> void:
    var keys := Verbs.get_all_keys()
    assert_has(keys, "interacted",
        "INTERACTED debe estar en get_all_keys()")

# =============================================================================
# Verbs.get_verb tests
# =============================================================================

func test_get_verb_returns_dictionary() -> void:
    var verb := Verbs.get_verb(Verbs.ATTEMPTED)
    assert_eq(typeof(verb), TYPE_DICTIONARY)

func test_get_verb_has_expected_keys() -> void:
    var verb := Verbs.get_verb(Verbs.COMPLETED)
    assert_has(verb, "id")
    assert_has(verb, "display")

func test_get_verb_returns_empty_for_unknown() -> void:
    var verb := Verbs.get_verb("unknown")
    assert_eq(verb, {})
