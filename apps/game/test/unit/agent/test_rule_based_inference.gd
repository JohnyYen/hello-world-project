# Test file for Rule-based Inference Engine
# Validates that the inference engine correctly decides actions based on performance data

extends "res://addons/gut/test.gd"

var RuleBasedInference = load("res://core/agent/inference/rule_inference.gd")
var inference_engine

func setup():
    print("DEBUG: Iniciando setup de test_rule_based_inference")
    # Create an instance of the Rule-based Inference Engine for testing
    inference_engine = RuleBasedInference.new()
    print("DEBUG: RuleBasedInference creado en setup")

func _init() -> void:
    print("DEBUG: TestRuleBasedInference initialized")
    setup()
    
    print("DEBUG: Iniciando test_inference_engine_initialization")
    test_inference_engine_initialization()
    print("DEBUG: Finalizado test_inference_engine_initialization")
    
    print("DEBUG: Iniciando test_inference_decreases_difficulty_for_low_performance")
    test_inference_decreases_difficulty_for_low_performance()
    print("DEBUG: Finalizado test_inference_decreases_difficulty_for_low_performance")
    
    print("DEBUG: Iniciando test_inference_increases_difficulty_for_high_performance")
    test_inference_increases_difficulty_for_high_performance()
    print("DEBUG: Finalizado test_inference_increases_difficulty_for_high_performance")
    
    print("DEBUG: Iniciando test_inference_keeps_difficulty_for_moderate_performance")
    test_inference_keeps_difficulty_for_moderate_performance()
    print("DEBUG: Finalizado test_inference_keeps_difficulty_for_moderate_performance")
    
    print("DEBUG: Iniciando test_inference_handles_boundary_values")
    test_inference_handles_boundary_values()
    print("DEBUG: Finalizado test_inference_handles_boundary_values")
    
    print("DEBUG: Iniciando test_inference_handles_edge_cases")
    test_inference_handles_edge_cases()
    print("DEBUG: Finalizado test_inference_handles_edge_cases")
    
    print("DEBUG: Iniciando test_inference_returns_default_keep")
    test_inference_returns_default_keep()
    print("DEBUG: Finalizado test_inference_returns_default_keep")
    
    teardown()

func test_inference_engine_initialization():
    print("DEBUG: Ejecutando test_inference_engine_initialization")
    var test_passed = true
    # Validate that the inference engine initializes with correct default values
    if inference_engine == null:
        print("ERROR: inference_engine is null")
        test_passed = false
    if inference_engine.rules.size() <= 0:  # Should have rules loaded
        print("ERROR: inference_engine has no rules loaded. Count: ", inference_engine.rules.size())
        test_passed = false

    if test_passed:
        print("SUCCESS: test_inference_engine_initialization passed")
    else:
        print("FAILURE: test_inference_engine_initialization failed")

func test_inference_decreases_difficulty_for_low_performance():
    print("DEBUG: Ejecutando test_inference_decreases_difficulty_for_low_performance")
    var test_passed = true
    # Test that the engine returns "decrease" for low performance scores
    var performance_data_low = {"avg_score": 0.3, "score": 0.3, "errors": 8}
    var action = inference_engine.decide_action(performance_data_low)
    
    if action != "decrease":
        print("ERROR: Expected action 'decrease' for low performance, got: ", action)
        test_passed = false

    if test_passed:
        print("SUCCESS: test_inference_decreases_difficulty_for_low_performance passed")
    else:
        print("FAILURE: test_inference_decreases_difficulty_for_low_performance failed")

func test_inference_increases_difficulty_for_high_performance():
    print("DEBUG: Ejecutando test_inference_increases_difficulty_for_high_performance")
    var test_passed = true
    # Test that the engine returns "increase" for high performance scores
    var performance_data_high = {"avg_score": 0.9, "score": 0.9, "errors": 1}
    var action = inference_engine.decide_action(performance_data_high)
    
    if action != "increase":
        print("ERROR: Expected action 'increase' for high performance, got: ", action)
        test_passed = false

    if test_passed:
        print("SUCCESS: test_inference_increases_difficulty_for_high_performance passed")
    else:
        print("FAILURE: test_inference_increases_difficulty_for_high_performance failed")

func test_inference_keeps_difficulty_for_moderate_performance():
    print("DEBUG: Ejecutando test_inference_keeps_difficulty_for_moderate_performance")
    var test_passed = true
    # Test that the engine returns "keep" for moderate performance scores
    var performance_data_moderate = {"avg_score": 0.65, "score": 0.65, "errors": 3}
    var action = inference_engine.decide_action(performance_data_moderate)
    
    if action != "keep":
        print("ERROR: Expected action 'keep' for moderate performance, got: ", action)
        test_passed = false

    if test_passed:
        print("SUCCESS: test_inference_keeps_difficulty_for_moderate_performance passed")
    else:
        print("FAILURE: test_inference_keeps_difficulty_for_moderate_performance failed")

func test_inference_handles_boundary_values():
    print("DEBUG: Ejecutando test_inference_handles_boundary_values")
    var test_passed = true
    # Test that the engine correctly handles boundary values
    # Value just below 0.5 should trigger decrease
    var performance_data_just_below = {"avg_score": 0.49, "score": 0.49, "errors": 4}
    var action1 = inference_engine.decide_action(performance_data_just_below)
    if action1 != "decrease":
        print("ERROR: Expected action 'decrease' for value below 0.5, got: ", action1)
        test_passed = false
    
    # Value just above 0.5 should trigger keep (since rule is >= 0.5)
    var performance_data_just_above_threshold = {"avg_score": 0.51, "score": 0.51, "errors": 3}
    var action2 = inference_engine.decide_action(performance_data_just_above_threshold)
    if action2 != "keep":
        print("ERROR: Expected action 'keep' for value above 0.5, got: ", action2)
        test_passed = false
    
    # Value just above 0.8 should trigger increase
    var performance_data_just_above = {"avg_score": 0.81, "score": 0.81, "errors": 1}
    var action3 = inference_engine.decide_action(performance_data_just_above)
    if action3 != "increase":
        print("ERROR: Expected action 'increase' for value above 0.8, got: ", action3)
        test_passed = false

    if test_passed:
        print("SUCCESS: test_inference_handles_boundary_values passed")
    else:
        print("FAILURE: test_inference_handles_boundary_values failed")

func test_inference_handles_edge_cases():
    print("DEBUG: Ejecutando test_inference_handles_edge_cases")
    var test_passed = true
    # Test edge cases like minimum and maximum scores
    var performance_data_min = {"avg_score": 0.0, "score": 0.0, "errors": 10}
    var action_min = inference_engine.decide_action(performance_data_min)
    if action_min != "decrease":
        print("ERROR: Expected action 'decrease' for minimum score, got: ", action_min)
        test_passed = false
    
    var performance_data_max = {"avg_score": 1.0, "score": 1.0, "errors": 0}
    var action_max = inference_engine.decide_action(performance_data_max)
    if action_max != "increase":
        print("ERROR: Expected action 'increase' for maximum score, got: ", action_max)
        test_passed = false

    if test_passed:
        print("SUCCESS: test_inference_handles_edge_cases passed")
    else:
        print("FAILURE: test_inference_handles_edge_cases failed")

func test_inference_returns_default_keep():
    print("DEBUG: Ejecutando test_inference_returns_default_keep")
    var test_passed = true
    # Test that the engine returns "keep" when no rules match
    # This shouldn't happen with the current rule set, but let's test the fallback
    # With the current rules, all values between 0 and 1 will match at least one rule
    # So we'll create an empty rules array to test the fallback behavior
    var original_rules = inference_engine.rules
    inference_engine.rules = []
    
    var performance_data = {"avg_score": 0.7, "score": 0.7, "errors": 2}
    var action = inference_engine.decide_action(performance_data)
    
    if action != "keep":
        print("ERROR: Expected action 'keep' when no rules match, got: ", action)
        test_passed = false
    
    # Restore original rules
    inference_engine.rules = original_rules

    if test_passed:
        print("SUCCESS: test_inference_returns_default_keep passed")
    else:
        print("FAILURE: test_inference_returns_default_keep failed")

func teardown():
    # Clean up after tests if needed
    inference_engine = null