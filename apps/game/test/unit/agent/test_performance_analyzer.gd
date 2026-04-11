# Test file for Performance Analyzer
# Validates that the performance analyzer correctly normalizes and tracks performance data

extends "res://addons/gut/test.gd"

var PerformanceAnalyzer = load("res://core/agent/analizer/performance_analizer.gd")
var performance_analyzer

func setup():
    # Create an instance of the Performance Analyzer for testing
    performance_analyzer = PerformanceAnalyzer.new()

func _init() -> void:
    print("DEBUG: TestPerformanceAnalyzer initialized")
    setup()
    print("DEBUG: Iniciando test_performance_analyzer_initialization")
    test_performance_analyzer_initialization()
    print("DEBUG: Finalizado test_performance_analyzer_initialization")
    
    print("DEBUG: Iniciando test_normalize_clamps_scores")
    test_normalize_clamps_scores()
    print("DEBUG: Finalizado test_normalize_clamps_scores")
    
    print("DEBUG: Iniciando test_normalize_tracks_history")
    test_normalize_tracks_history()
    print("DEBUG: Finalizado test_normalize_tracks_history")
    
    print("DEBUG: Iniciando test_history_size_limit")
    test_history_size_limit()
    print("DEBUG: Finalizado test_history_size_limit")
    
    print("DEBUG: Iniciando test_normalize_calculates_moving_average")
    test_normalize_calculates_moving_average()
    print("DEBUG: Finalizado test_normalize_calculates_moving_average")
    
    print("DEBUG: Iniciando test_normalize_returns_correct_structure")
    test_normalize_returns_correct_structure()
    print("DEBUG: Finalizado test_normalize_returns_correct_structure")
    
    print("DEBUG: Iniciando test_normalize_handles_missing_fields")
    test_normalize_handles_missing_fields()
    print("DEBUG: Finalizado test_normalize_handles_missing_fields")
    
    teardown()

func test_performance_analyzer_initialization():
    print("DEBUG: Ejecutando test_performance_analyzer_initialization")
    var test_passed = true
    # Validate that the performance analyzer initializes with correct default values
    if performance_analyzer == null:
        print("ERROR: performance_analyzer is null")
        test_passed = false
    if performance_analyzer.avg_score != 0.7:
        print("ERROR: performance_analyzer.avg_score is ", performance_analyzer.avg_score, " expected 0.7")
        test_passed = false
    if performance_analyzer.history_size != 5:
        print("ERROR: performance_analyzer.history_size is ", performance_analyzer.history_size, " expected 5")
        test_passed = false
    if performance_analyzer.scores.size() != 0:
        print("ERROR: performance_analyzer.scores.size() is ", performance_analyzer.scores.size(), " expected 0")
        test_passed = false
    if performance_analyzer.smooth_alpha != 0.3:
        print("ERROR: performance_analyzer.smooth_alpha is ", performance_analyzer.smooth_alpha, " expected 0.3")
        test_passed = false

    if test_passed:
        print("SUCCESS: test_performance_analyzer_initialization passed")
    else:
        print("FAILURE: test_performance_analyzer_initialization failed")

func test_normalize_clamps_scores():
    print("DEBUG: Ejecutando test_normalize_clamps_scores")
    var test_passed = true
    # Test that the normalize function clamps scores between 0.0 and 1.0
    var raw_data_high = {"score": 1.5, "errors": 0}  # Above 1.0
    var result_high = performance_analyzer.normalize(raw_data_high)
    if result_high.score != 1.0:
        print("ERROR: High score was not clamped. Expected: 1.0, Got: ", result_high.score)
        test_passed = false
    
    var raw_data_low = {"score": -0.5, "errors": 5}  # Below 0.0
    var result_low = performance_analyzer.normalize(raw_data_low)
    if result_low.score != 0.0:
        print("ERROR: Low score was not clamped. Expected: 0.0, Got: ", result_low.score)
        test_passed = false
    
    var raw_data_valid = {"score": 0.7, "errors": 2}
    var result_valid = performance_analyzer.normalize(raw_data_valid)
    if result_valid.score != 0.7:
        print("ERROR: Valid score was changed. Expected: 0.7, Got: ", result_valid.score)
        test_passed = false

    if test_passed:
        print("SUCCESS: test_normalize_clamps_scores passed")
    else:
        print("FAILURE: test_normalize_clamps_scores failed")

func test_normalize_tracks_history():
    print("DEBUG: Ejecutando test_normalize_tracks_history")
    var test_passed = true
    # Test that the analyzer correctly tracks score history
    var initial_size = performance_analyzer.scores.size()
    
    # Add several scores
    performance_analyzer.normalize({"score": 0.6, "errors": 3})
    performance_analyzer.normalize({"score": 0.8, "errors": 1})
    performance_analyzer.normalize({"score": 0.4, "errors": 5})
    
    if performance_analyzer.scores.size() != initial_size + 3:
        print("ERROR: Scores were not added correctly. Expected size: ", initial_size + 3, ", Got: ", performance_analyzer.scores.size())
        test_passed = false
    # Verify the scores were added in the right order
    if performance_analyzer.scores[-1] != 0.4:  # Last added
        print("ERROR: Last added score not at end of array. Expected: 0.4, Got: ", performance_analyzer.scores[-1])
        test_passed = false
    if performance_analyzer.scores[-2] != 0.8:  # Second to last
        print("ERROR: Second to last score is incorrect. Expected: 0.8, Got: ", performance_analyzer.scores[-2])
        test_passed = false
    if performance_analyzer.scores[-3] != 0.6:  # Third to last
        print("ERROR: Third to last score is incorrect. Expected: 0.6, Got: ", performance_analyzer.scores[-3])
        test_passed = false

    if test_passed:
        print("SUCCESS: test_normalize_tracks_history passed")
    else:
        print("FAILURE: test_normalize_tracks_history failed")

func test_history_size_limit():
    print("DEBUG: Ejecutando test_history_size_limit")
    var test_passed = true
    # Test that the analyzer maintains only the specified history size
    # Set a small history size for testing
    performance_analyzer.history_size = 3
    
    # Add more scores than the history limit
    performance_analyzer.normalize({"score": 0.6, "errors": 3})
    performance_analyzer.normalize({"score": 0.8, "errors": 1})
    performance_analyzer.normalize({"score": 0.4, "errors": 5})
    performance_analyzer.normalize({"score": 0.9, "errors": 0})
    performance_analyzer.normalize({"score": 0.3, "errors": 7})
    
    # History should be limited to the size specified
    if performance_analyzer.scores.size() != 3:
        print("ERROR: History exceeded size limit. Expected: 3, Got: ", performance_analyzer.scores.size())
        test_passed = false
    # The oldest scores should be removed, keeping only the most recent
    if performance_analyzer.scores[0] != 0.4:  # The third score added
        print("ERROR: Oldest score not properly removed. Expected: 0.4, Got: ", performance_analyzer.scores[0])
        test_passed = false
    if performance_analyzer.scores[1] != 0.9:  # The fourth score added
        print("ERROR: Middle score is incorrect. Expected: 0.9, Got: ", performance_analyzer.scores[1])
        test_passed = false
    if performance_analyzer.scores[2] != 0.3:  # The fifth (most recent) score added
        print("ERROR: Newest score is incorrect. Expected: 0.3, Got: ", performance_analyzer.scores[2])
        test_passed = false

    if test_passed:
        print("SUCCESS: test_history_size_limit passed")
    else:
        print("FAILURE: test_history_size_limit failed")

func test_normalize_calculates_moving_average():
    print("DEBUG: Ejecutando test_normalize_calculates_moving_average")
    var test_passed = true
    # Test that the analyzer correctly calculates the exponentially weighted average
    var initial_avg = performance_analyzer.avg_score
    
    # With exponential smoothing, new average = alpha * new_score + (1-alpha) * old_avg
    var raw_data = {"score": 0.8, "errors": 2}
    var result = performance_analyzer.normalize(raw_data)
    
    var expected_avg = (performance_analyzer.smooth_alpha * 0.8) + ((1 - performance_analyzer.smooth_alpha) * initial_avg)
    if abs(result.avg_score - expected_avg) >= 0.0001:  # Allow for floating point precision errors
        print("ERROR: Moving average not calculated correctly. Expected: ", expected_avg, ", Got: ", result.avg_score)
        test_passed = false

    if test_passed:
        print("SUCCESS: test_normalize_calculates_moving_average passed")
    else:
        print("FAILURE: test_normalize_calculates_moving_average failed")

func test_normalize_returns_correct_structure():
    print("DEBUG: Ejecutando test_normalize_returns_correct_structure")
    var test_passed = true
    # Test that the normalize function returns data in the correct structure
    var raw_data = {"score": 0.75, "errors": 3, "time": 45.5}
    var result = performance_analyzer.normalize(raw_data)
    
    # Verify the structure of the returned data
    if not result.has("score"):
        print("ERROR: Result does not have 'score' key")
        test_passed = false
    if not result.has("errors"):
        print("ERROR: Result does not have 'errors' key")
        test_passed = false
    if not result.has("avg_score"):
        print("ERROR: Result does not have 'avg_score' key")
        test_passed = false
    if not result.has("time"):
        print("ERROR: Result does not have 'time' key")
        test_passed = false
    
    # Verify the values match what was provided
    if result.score != 0.75:
        print("ERROR: Score value mismatch. Expected: 0.75, Got: ", result.score)
        test_passed = false
    if result.errors != 3:
        print("ERROR: Errors value mismatch. Expected: 3, Got: ", result.errors)
        test_passed = false
    if result.time != 45.5:
        print("ERROR: Time value mismatch. Expected: 45.5, Got: ", result.time)
        test_passed = false
    # avg_score should be calculated based on the new score and previous average

    if test_passed:
        print("SUCCESS: test_normalize_returns_correct_structure passed")
    else:
        print("FAILURE: test_normalize_returns_correct_structure failed")

func test_normalize_handles_missing_fields():
    print("DEBUG: Ejecutando test_normalize_handles_missing_fields")
    var test_passed = true
    # Test that the normalize function handles missing fields gracefully
    var raw_data_missing_score = {"errors": 5}
    var result1 = performance_analyzer.normalize(raw_data_missing_score)
    if result1.score != 0.0:  # Should default to 0.0
        print("ERROR: Score with missing value was not defaulted to 0.0. Got: ", result1.score)
        test_passed = false
    
    var raw_data_missing_errors = {"score": 0.9}
    var result2 = performance_analyzer.normalize(raw_data_missing_errors)
    if result2.errors != 0:  # Should default to 0
        print("ERROR: Errors with missing value was not defaulted to 0. Got: ", result2.errors)
        test_passed = false
    
    var raw_data_missing_time = {"score": 0.8, "errors": 2}
    var result3 = performance_analyzer.normalize(raw_data_missing_time)
    if result3.time != 0.0:  # Should default to 0.0
        print("ERROR: Time with missing value was not defaulted to 0.0. Got: ", result3.time)
        test_passed = false

    if test_passed:
        print("SUCCESS: test_normalize_handles_missing_fields passed")
    else:
        print("FAILURE: test_normalize_handles_missing_fields failed")

func teardown():
    # Clean up after tests if needed
    performance_analyzer = null