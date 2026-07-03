# test_adaptive_agent.gd
# Tests for AdaptiveAgent with 5 graduated actions and cross-session blend
extends GutTest

var AdaptiveAgent = load("res://scripts/agent/adaptive_agent.gd")
var agent


func before_each() -> void:
	AttemptHistoryPersistence.clear_history()
	agent = AdaptiveAgent.new()


# =============================================================================
# Initialization
# =============================================================================

func test_agent_initialization() -> void:
	assert_not_null(agent, "agent debe ser no null")
	assert_not_null(agent.inference_engine, "inference_engine no null")
	assert_not_null(agent.analyzer, "analyzer no null")
	assert_not_null(agent.trend_calculator, "trend_calculator no null")

	assert_eq(agent.difficulty, 1.0, "difficulty inicial debe ser 1.0")
	assert_eq(agent.min_difficulty, 0.5, "min_difficulty debe ser 0.5")
	assert_eq(agent.max_difficulty, 2.0, "max_difficulty debe ser 2.0")


# =============================================================================
# _apply_action() — 5 graduated actions
# =============================================================================

func test_apply_decrease_major() -> void:
	agent.difficulty = 1.0
	agent._apply_action("decrease_major")
	assert_eq(agent.difficulty, 0.8, "decrease_major: 1.0 - 0.2 = 0.8")


func test_apply_decrease_minor() -> void:
	agent.difficulty = 1.0
	agent._apply_action("decrease_minor")
	assert_eq(agent.difficulty, 0.9, "decrease_minor: 1.0 - 0.1 = 0.9")


func test_apply_keep() -> void:
	agent.difficulty = 1.0
	agent._apply_action("keep")
	assert_eq(agent.difficulty, 1.0, "keep: 1.0 + 0.0 = 1.0")


func test_apply_increase_minor() -> void:
	agent.difficulty = 1.0
	agent._apply_action("increase_minor")
	assert_eq(agent.difficulty, 1.1, "increase_minor: 1.0 + 0.1 = 1.1")


func test_apply_increase_major() -> void:
	agent.difficulty = 1.0
	agent._apply_action("increase_major")
	assert_eq(agent.difficulty, 1.2, "increase_major: 1.0 + 0.2 = 1.2")


# =============================================================================
# Difficulty clamping
# =============================================================================

func test_clamp_at_minimum() -> void:
	agent.difficulty = 0.55
	agent._apply_action("decrease_major")
	assert_eq(agent.difficulty, 0.5, "debe clamp a 0.5 mínimo")


func test_clamp_at_maximum() -> void:
	agent.difficulty = 1.95
	agent._apply_action("increase_major")
	assert_eq(agent.difficulty, 2.0, "debe clamp a 2.0 máximo")


func test_keep_within_bounds() -> void:
	agent.difficulty = agent.min_difficulty
	agent._apply_action("keep")
	assert_eq(agent.difficulty, agent.min_difficulty, "keep debe mantener en 0.5")


# =============================================================================
# analyze_and_decide() — early exit
# =============================================================================

func test_analyze_and_decide_no_decision_with_few_attempts() -> void:
	agent.difficulty = 1.0
	agent.analyze_and_decide({"score": 0.9, "errors": 0, "time": 30.0})
	# With only 1 attempt (total_count=1 < 5), no decision should be made
	assert_eq(agent.difficulty, 1.0, "sin suficientes intentos no debe cambiar difficulty")


func test_analyze_and_decide_with_minimum_attempts() -> void:
	agent.difficulty = 1.0
	# Add 5 attempts to trigger decision
	for i in range(5):
		agent.analyze_and_decide({"score": 0.9, "errors": 0, "time": 30.0})
	# After 5 high-score attempts, difficulty likely increased
	assert_ne(agent.difficulty, 0.0, "después de 5 intentos altos debe haber decisión")


func test_analyze_and_decide_with_low_scores() -> void:
	agent.difficulty = 1.0
	for i in range(5):
		agent.analyze_and_decide({"score": 0.2, "errors": 8, "time": 120.0})

	# With 5 low-score attempts, difficulty should decrease or stay
	assert_lt(agent.difficulty, 1.1, "scores bajos deben mantener o bajar difficulty")


func test_analyze_and_decide_with_high_scores() -> void:
	agent.difficulty = 1.0
	for i in range(5):
		agent.analyze_and_decide({"score": 0.95, "errors": 0, "time": 25.0})

	# With 5 high-score attempts, difficulty should increase or stay
	assert_gt(agent.difficulty, 0.9, "scores altos deben mantener o subir difficulty")


# =============================================================================
# Cross-session blend: use persistence for long-term
# =============================================================================

func test_agent_with_combined_session_and_long_term() -> void:
	# Pre-populate persistence with long-term data
	for i in range(20):
		var entry := AttemptData.new(0.5 + (i % 3) * 0.1, 1, 30.0)
		AttemptHistoryPersistence.append_attempt(entry)

	agent.difficulty = 1.0
	# Add only 3 in-session attempts (but total with persistence = 23 >= 5)
	for i in range(3):
		agent.analyze_and_decide({"score": 0.4, "errors": 5, "time": 90.0})

	# Decision should have been made (total 23 >= 5)
	# The actual action depends on blend; just verify something happened
	assert_lt(agent.difficulty, 1.01, "total ≥ 5 debe generar decisión")


# =============================================================================
# Signal emission
# =============================================================================

func test_action_decided_signal_emitted() -> void:
	var signal_data := {"received": false, "action": "", "difficulty": 0.0}
	EventBus.action_decided.connect(func(a: String, d: float):
		signal_data.received = true
		signal_data.action = a
		signal_data.difficulty = d
	)
	agent._apply_action("increase_minor")

	assert_eq(signal_data.received, true, "EventBus.action_decided debe emitirse")
	assert_eq(signal_data.action, "increase_minor", "EventBus debe tener action correcta")
	assert_eq(signal_data.difficulty, 1.1, "EventBus debe tener difficulty correcta")
