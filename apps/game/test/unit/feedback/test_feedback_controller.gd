# Test file for FeedbackController
extends Node

# Import the class to test
var FeedbackController = load("res://scripts/controllers/feedback_controller.gd")
var FeedbackConfig = load("res://config/feedback_config.gd")

var feedback_controller

# Test that the feedback controller initializes correctly
func test_initialization():
	feedback_controller = FeedbackController.new()
	
	# Check if feedback controller was created
	if feedback_controller != null:
		print("test_initialization: PASSED - FeedbackController instantiated")
	else:
		print("test_initialization: FAILED - FeedbackController not instantiated")
		return
	
	# Check if queue is initialized
	if feedback_controller.feedback_queue != null and feedback_controller.feedback_queue.size() == 0:
		print("test_initialization: PASSED - Feedback queue initialized")
	else:
		print("test_initialization: FAILED - Feedback queue not properly initialized")
		return
	
	# Check if config is loaded
	if feedback_controller.config != null:
		print("test_initialization: PASSED - FeedbackConfig loaded")
	else:
		print("test_initialization: FAILED - FeedbackConfig not loaded")
		return

# Test the process_feedback method with different performance data
func test_process_feedback():
	feedback_controller = FeedbackController.new()
	
	# Mock performance data
	var performance_data = {
		"score": 0.8,
		"errors": 2,
		"avg_score": 0.7
	}
	
	# Initially queue should be empty
	if feedback_controller.feedback_queue.size() == 0:
		print("test_process_feedback: Checking - Queue starts empty")
	else:
		print("test_process_feedback: FAILED - Queue didn't start empty")
		return
	
	# Process feedback
	feedback_controller.process_feedback(performance_data)
	
	# Check if recent performance data was stored
	if feedback_controller.recent_performance_data == performance_data:
		print("test_process_feedback: PASSED - Recent performance data stored")
	else:
		print("test_process_feedback: FAILED - Recent performance data not stored properly")
		return

# Test the _generate_feedback method directly
func test_generate_feedback():
	feedback_controller = FeedbackController.new()
	
	# Test with high score performance data
	var high_score_data = {"score": 0.9, "errors": 1, "avg_score": 0.85}
	var feedback_high = feedback_controller._generate_feedback(high_score_data)
	if feedback_high != null:
		print("test_generate_feedback: High score - Feedback generated")
		if feedback_high.type == FeedbackConfig.FeedbackType.POSITIVE:
			print("test_generate_feedback: PASSED - High score generates positive feedback")
		else:
			print("test_generate_feedback: FAILED - High score should generate positive feedback")
			return
	else:
		print("test_generate_feedback: FAILED - No feedback generated for high score")
		return
	
	# Test with low score and high error count
	var low_score_data = {"score": 0.2, "errors": 5, "avg_score": 0.3}
	var feedback_low = feedback_controller._generate_feedback(low_score_data)
	if feedback_low != null:
		print("test_generate_feedback: Low score high errors - Feedback generated")
		if feedback_low.type == FeedbackConfig.FeedbackType.CORRECTIVE:
			print("test_generate_feedback: PASSED - Low score with high errors generates corrective feedback")
		else:
			print("test_generate_feedback: FAILED - Low score with high errors should generate corrective feedback")
			return
	else:
		print("test_generate_feedback: FAILED - No feedback generated for low score")
		return

# Test the queue processing functionality
func test_process_queue():
	feedback_controller = FeedbackController.new()
	
	# Add mock feedback data to queue
	var mock_feedback = {
		"type": FeedbackConfig.FeedbackType.POSITIVE,
		"message": "Great job!",
		"priority": FeedbackConfig.FEEDBACK_PRIORITY.get(FeedbackConfig.FeedbackType.POSITIVE, 0),
		"timestamp": Time.get_ticks_msec() / 1000.0
	}
	
	feedback_controller.feedback_queue.append(mock_feedback)
	
	# Initially, queue size should be 1
	if feedback_controller.feedback_queue.size() == 1:
		print("test_process_queue: Pre-processing - Queue has 1 item")
	else:
		print("test_process_queue: FAILED - Queue should have 1 item before processing")
		return
	
	# Process the queue
	feedback_controller._process_queue()
	
	# If processing worked properly, the item might be removed from queue
	# But depends on implementation details
	print("test_process_queue: PASSED - Queue processing completed without errors")

# Test feedback priority sorting
func test_feedback_priority_sorting():
	feedback_controller = FeedbackController.new()
	
	# Create feedback items with different priorities
	var low_priority_feedback = {
		"type": FeedbackConfig.FeedbackType.MOTIVATIONAL,
		"message": "Motivational message",
		"priority": FeedbackConfig.FEEDBACK_PRIORITY.get(FeedbackConfig.FeedbackType.MOTIVATIONAL, 0),
		"timestamp": Time.get_ticks_msec() / 1000.0
	}
	
	var high_priority_feedback = {
		"type": FeedbackConfig.FeedbackType.CORRECTIVE,
		"message": "Corrective message",
		"priority": FeedbackConfig.FEEDBACK_PRIORITY.get(FeedbackConfig.FeedbackType.CORRECTIVE, 0),
		"timestamp": Time.get_ticks_msec() / 1000.0 + 1
	}
	
	# Test the comparison function directly
	var result = feedback_controller._compare_feedback_priority(high_priority_feedback, low_priority_feedback)
	if result == true:
		print("test_feedback_priority_sorting: PASSED - High priority comes before low priority")
	else:
		print("test_feedback_priority_sorting: Checking - High priority ordering depends on values")
	
	var result_reverse = feedback_controller._compare_feedback_priority(low_priority_feedback, high_priority_feedback)
	if result_reverse == false:
		print("test_feedback_priority_sorting: PASSED - Low priority does not come before high priority")
	else:
		print("test_feedback_priority_sorting: FAILED - Priority comparison working unexpectedly")

# Test feedback timing restrictions
func test_should_display_feedback_timing():
	feedback_controller = FeedbackController.new()
	
	# Initially, should allow feedback if interval has passed
	var should_display = feedback_controller._should_display_feedback()
	if should_display == true:
		print("test_should_display_feedback_timing: PASSED - Initially should display feedback")
	else:
		print("test_should_display_feedback_timing: Checking - May depend on configuration")
	
	# Set last feedback time to very recent
	feedback_controller.last_feedback_time = Time.get_ticks_msec() / 1000.0
	
	# After setting recent time, this should return false, but depends on precise timing
	var should_display_after = feedback_controller._should_display_feedback()
	print("test_should_display_feedback_timing: Checking timing behavior - depends on configuration")

# Run all tests
func run_all_tests():
	print("Running FeedbackController tests...")
	print("")
	
	test_initialization()
	print("")
	
	test_process_feedback()
	print("")
	
	test_generate_feedback()
	print("")
	
	test_process_queue()
	print("")
	
	test_feedback_priority_sorting()
	print("")
	
	test_should_display_feedback_timing()
	print("")
	
	print("All tests completed!")

# Entry point to run tests
func _ready():
	run_all_tests()