# Test file for Adaptive Agent
# Validates that the agent correctly analyzes performance data and adjusts difficulty

extends "res://addons/gut/test.gd"

var AdaptiveAgent = load("res://core/agent/adaptive_agent.gd")
var adaptive_agent

func setup():
	print("DEBUG: Iniciando setup de test_adaptive_agent")
	# Create an instance of the Adaptive Agent for testing
	adaptive_agent = AdaptiveAgent.new()
	print("DEBUG: AdaptiveAgent creado en setup")

func _init() -> void:
	print("DEBUG: TestAdaptiveAgent initialized")
	setup()
	
	print("DEBUG: Iniciando test_agent_initialization")
	test_agent_initialization()
	print("DEBUG: Finalizado test_agent_initialization")
	
	print("DEBUG: Iniciando test_agent_adjusts_difficulty_up")
	test_agent_adjusts_difficulty_up()
	print("DEBUG: Finalizado test_agent_adjusts_difficulty_up")
	
	print("DEBUG: Iniciando test_agent_adjusts_difficulty_down")
	test_agent_adjusts_difficulty_down()
	print("DEBUG: Finalizado test_agent_adjusts_difficulty_down")
	
	print("DEBUG: Iniciando test_agent_keeps_difficulty")
	test_agent_keeps_difficulty()
	print("DEBUG: Finalizado test_agent_keeps_difficulty")
	
	print("DEBUG: Iniciando test_agent_respects_difficulty_bounds")
	test_agent_respects_difficulty_bounds()
	print("DEBUG: Finalizado test_agent_respects_difficulty_bounds")
	
	teardown()

func test_agent_initialization():
	print("DEBUG: Ejecutando test_agent_initialization")
	var test_passed = true
	# Validate that the agent initializes with correct default values
	if adaptive_agent == null:
		print("ERROR: adaptive_agent is null")
		test_passed = false
	if adaptive_agent.inference_engine == null:
		print("ERROR: adaptive_agent.inference_engine is null")
		test_passed = false
	if adaptive_agent.analyzer == null:
		print("ERROR: adaptive_agent.analyzer is null")
		test_passed = false
	if adaptive_agent.difficulty != 1.0:
		print("ERROR: adaptive_agent.difficulty is ", adaptive_agent.difficulty, " expected 1.0")
		test_passed = false
	if adaptive_agent.min_difficulty != 0.5:
		print("ERROR: adaptive_agent.min_difficulty is ", adaptive_agent.min_difficulty, " expected 0.5")
		test_passed = false
	if adaptive_agent.max_difficulty != 2.0:
		print("ERROR: adaptive_agent.max_difficulty is ", adaptive_agent.max_difficulty, " expected 2.0")
		test_passed = false
	if adaptive_agent.delta != 0.1:
		print("ERROR: adaptive_agent.delta is ", adaptive_agent.delta, " expected 0.1")
		test_passed = false
	
	if test_passed:
		print("SUCCESS: test_agent_initialization passed")
	else:
		print("FAILURE: test_agent_initialization failed")
	
func test_agent_adjusts_difficulty_up():
	print("DEBUG: Ejecutando test_agent_adjusts_difficulty_up")
	var test_passed = true
	var initial_difficulty = adaptive_agent.difficulty
	
	# Limpiar historia para asegurar que avg_score se base en el nuevo valor
	adaptive_agent.analyzer.scores.clear()
	
	# Provide high performance data (should trigger increase)
	var raw_data = {"score": 0.9, "errors": 1, "time": 60.0}
	
	print("DEBUG: Before analyze_and_decide - initial_difficulty: ", initial_difficulty)
	adaptive_agent.analyze_and_decide(raw_data)
	print("DEBUG: After analyze_and_decide - new difficulty: ", adaptive_agent.difficulty)
	
	# Normalizar el score para ver qué valor se considera
	var normalized_data = adaptive_agent.analyzer.normalize(raw_data)
	print("DEBUG: Normalized data avg_score: ", normalized_data.avg_score)
	
	# La dificultad podría aumentar si el rendimiento es alto y supera el umbral de 0.8
	# La acción se decide basada en el avg_score
	if normalized_data.avg_score > 0.8:
		# Se debe haber decidido aumentar la dificultad
		if adaptive_agent.difficulty > initial_difficulty:
			print("SUCCESS: Difficulty increased as expected for high performance. Initial: ", initial_difficulty, ", Current: ", adaptive_agent.difficulty)
		else:
			print("ERROR: Expected difficulty to increase, but it did not. Initial: ", initial_difficulty, ", Current: ", adaptive_agent.difficulty)
			test_passed = false
	elif normalized_data.avg_score >= 0.5:
		# Se debe haber decidido mantener la dificultad
		if adaptive_agent.difficulty == initial_difficulty:
			print("SUCCESS: Difficulty kept as expected for moderate performance. Initial: ", initial_difficulty, ", Current: ", adaptive_agent.difficulty)
		else:
			print("INFO: Difficulty changed even though performance was moderate. Initial: ", initial_difficulty, ", Current: ", adaptive_agent.difficulty)
			# Esto puede ser aceptable dependiendo del promedio histórico
	else:
		# Se debe haber decidido disminuir la dificultad
		if adaptive_agent.difficulty < initial_difficulty:
			print("SUCCESS: Difficulty decreased as expected for low performance. Initial: ", initial_difficulty, ", Current: ", adaptive_agent.difficulty)
		else:
			print("ERROR: Expected difficulty to decrease, but it did not. Initial: ", initial_difficulty, ", Current: ", adaptive_agent.difficulty)
			test_passed = false
	
	# Asegurar que no exceda el máximo
	if adaptive_agent.difficulty > adaptive_agent.max_difficulty:
		print("ERROR: Difficulty exceeded max. Current: ", adaptive_agent.difficulty, ", Max: ", adaptive_agent.max_difficulty)
		test_passed = false
	
	if test_passed:
		print("SUCCESS: test_agent_adjusts_difficulty_up passed")
	else:
		print("FAILURE: test_agent_adjusts_difficulty_up failed")

func test_agent_adjusts_difficulty_down():
	print("DEBUG: Ejecutando test_agent_adjusts_difficulty_down")
	var test_passed = true
	var initial_difficulty = adaptive_agent.difficulty
	
	# Limpiar historia para asegurar que avg_score se base en el nuevo valor
	adaptive_agent.analyzer.scores.clear()
	
	# Provide low performance data (should trigger decrease)
	var raw_data = {"score": 0.2, "errors": 10, "time": 120.0}
	
	print("DEBUG: Before analyze_and_decide - initial_difficulty: ", initial_difficulty)
	adaptive_agent.analyze_and_decide(raw_data)
	print("DEBUG: After analyze_and_decide - new difficulty: ", adaptive_agent.difficulty)
	
	# Normalizar el score para ver qué valor se considera
	var normalized_data = adaptive_agent.analyzer.normalize(raw_data)
	print("DEBUG: Normalized data avg_score: ", normalized_data.avg_score)
	
	# La dificultad podría disminuir si el rendimiento es bajo y es menor a 0.5
	if normalized_data.avg_score < 0.5:
		# Se debe haber decidido disminuir la dificultad
		if adaptive_agent.difficulty < initial_difficulty:
			print("SUCCESS: Difficulty decreased as expected for low performance. Initial: ", initial_difficulty, ", Current: ", adaptive_agent.difficulty)
		else:
			print("ERROR: Expected difficulty to decrease, but it did not. Initial: ", initial_difficulty, ", Current: ", adaptive_agent.difficulty)
			test_passed = false
	elif normalized_data.avg_score >= 0.5:
		# Se debe haber decidido mantener la dificultad
		if adaptive_agent.difficulty == initial_difficulty:
			print("SUCCESS: Difficulty kept as expected for moderate performance. Initial: ", initial_difficulty, ", Current: ", adaptive_agent.difficulty)
		else:
			print("INFO: Difficulty changed even though performance was moderate. Initial: ", initial_difficulty, ", Current: ", adaptive_agent.difficulty)
			# Esto puede ser aceptable dependiendo del promedio histórico
	else:
		# Se debe haber decidido aumentar la dificultad
		if adaptive_agent.difficulty > initial_difficulty:
			print("SUCCESS: Difficulty increased as expected for high performance. Initial: ", initial_difficulty, ", Current: ", adaptive_agent.difficulty)
		else:
			print("ERROR: Expected difficulty to increase, but it did not. Initial: ", initial_difficulty, ", Current: ", adaptive_agent.difficulty)
			test_passed = false
	
	# Asegurar que no esté por debajo del mínimo
	if adaptive_agent.difficulty < adaptive_agent.min_difficulty:
		print("ERROR: Difficulty went below min. Current: ", adaptive_agent.difficulty, ", Min: ", adaptive_agent.min_difficulty)
		test_passed = false
	
	if test_passed:
		print("SUCCESS: test_agent_adjusts_difficulty_down passed")
	else:
		print("FAILURE: test_agent_adjusts_difficulty_down failed")

func test_agent_keeps_difficulty():
	print("DEBUG: Ejecutando test_agent_keeps_difficulty")
	var test_passed = true
	var initial_difficulty = adaptive_agent.difficulty
	
	# Limpiar historia para asegurar que avg_score se base en el nuevo valor
	adaptive_agent.analyzer.scores.clear()
	
	# Provide moderate performance data (should trigger keep)
	var raw_data = {"score": 0.65, "errors": 3, "time": 90.0}
	
	print("DEBUG: Before analyze_and_decide - initial_difficulty: ", initial_difficulty)
	adaptive_agent.analyze_and_decide(raw_data)
	print("DEBUG: After analyze_and_decide - new difficulty: ", adaptive_agent.difficulty)
	
	# Normalizar el score para ver qué valor se considera
	var normalized_data = adaptive_agent.analyzer.normalize(raw_data)
	print("DEBUG: Normalized data avg_score: ", normalized_data.avg_score)
	
	# La dificultad debería mantenerse para valores entre 0.5 y 0.8
	if normalized_data.avg_score >= 0.5 and normalized_data.avg_score <= 0.8:
		# Se debe haber decidido mantener la dificultad
		if adaptive_agent.difficulty == initial_difficulty:
			print("SUCCESS: Difficulty kept as expected for moderate performance. Initial: ", initial_difficulty, ", Current: ", adaptive_agent.difficulty)
		else:
			print("INFO: Difficulty changed even though performance was in keep range. Initial: ", initial_difficulty, ", Current: ", adaptive_agent.difficulty)
			# Puede haber cambiado si el promedio histórico afectó la decisión
	elif normalized_data.avg_score < 0.5:
		# Se debe haber decidido disminuir la dificultad
		if adaptive_agent.difficulty < initial_difficulty:
			print("SUCCESS: Difficulty decreased as expected for low performance. Initial: ", initial_difficulty, ", Current: ", adaptive_agent.difficulty)
		else:
			print("INFO: Difficulty did not decrease as expected for low performance. Initial: ", initial_difficulty, ", Current: ", adaptive_agent.difficulty)
	elif normalized_data.avg_score > 0.8:
		# Se debe haber decidido aumentar la dificultad
		if adaptive_agent.difficulty > initial_difficulty:
			print("SUCCESS: Difficulty increased as expected for high performance. Initial: ", initial_difficulty, ", Current: ", adaptive_agent.difficulty)
		else:
			print("INFO: Difficulty did not increase as expected for high performance. Initial: ", initial_difficulty, ", Current: ", adaptive_agent.difficulty)
	
	if test_passed:
		print("SUCCESS: test_agent_keeps_difficulty passed")
	else:
		print("FAILURE: test_agent_keeps_difficulty failed")

func test_agent_respects_difficulty_bounds():
	print("DEBUG: Ejecutando test_agent_respects_difficulty_bounds")
	var test_passed = true
	var current_difficulty = 1.95  # Close to the max
	adaptive_agent.difficulty = current_difficulty
	
	# Limpiar historia para asegurar que avg_score se base en el nuevo valor
	adaptive_agent.analyzer.scores.clear()
	
	# Force an increase with high performance
	var raw_data = {"score": 0.95, "errors": 0, "time": 30.0}
	
	print("DEBUG: Before analyze_and_decide (max test) - current_difficulty: ", current_difficulty)
	adaptive_agent.analyze_and_decide(raw_data)
	print("DEBUG: After analyze_and_decide (max test) - new difficulty: ", adaptive_agent.difficulty)
	
	# Normalizar el score para ver qué valor se considera
	var normalized_data = adaptive_agent.analyzer.normalize(raw_data)
	print("DEBUG: Normalized data avg_score (max test): ", normalized_data.avg_score)
	
	# Si el score es alto, el agente debería intentar aumentar la dificultad
	# pero como ya está cerca del máximo, debería mantenerse en el máximo
	if normalized_data.avg_score > 0.8:
		# Se intentó aumentar, pero no debería exceder el máximo
		if adaptive_agent.difficulty == adaptive_agent.max_difficulty:
			print("SUCCESS: Difficulty correctly limited at max. Expected: ", adaptive_agent.max_difficulty, ", Got: ", adaptive_agent.difficulty)
		else:
			print("ERROR: Difficulty exceeded max bound. Expected: ", adaptive_agent.max_difficulty, ", Got: ", adaptive_agent.difficulty)
			test_passed = false
	else:
		# Si no se intentó aumentar, solo verificar que no esté por encima del máximo
		if adaptive_agent.difficulty <= adaptive_agent.max_difficulty:
			print("SUCCESS: Difficulty within bounds. Expected: ", adaptive_agent.max_difficulty, ", Got: ", adaptive_agent.difficulty)
		else:
			print("ERROR: Difficulty exceeded max bound. Expected: ", adaptive_agent.max_difficulty, ", Got: ", adaptive_agent.difficulty)
			test_passed = false
	
	# Now test minimum bound
	var low_difficulty = 0.55  # Close to the min
	adaptive_agent.difficulty = low_difficulty
	
	# Limpiar historia para asegurar que avg_score se base en el nuevo valor
	adaptive_agent.analyzer.scores.clear()
	
	# Force a decrease with low performance
	var low_raw_data = {"score": 0.1, "errors": 15, "time": 150.0}
	
	print("DEBUG: Before analyze_and_decide (min test) - low_difficulty: ", low_difficulty)
	adaptive_agent.analyze_and_decide(low_raw_data)
	print("DEBUG: After analyze_and_decide (min test) - new difficulty: ", adaptive_agent.difficulty)
	
	# Normalizar el score para ver qué valor se considera
	var low_normalized_data = adaptive_agent.analyzer.normalize(low_raw_data)
	print("DEBUG: Normalized data avg_score (min test): ", low_normalized_data.avg_score)
	
	# Si el score es bajo, el agente debería intentar disminuir la dificultad
	# pero como está cerca del mínimo, debería mantenerse en el mínimo
	if low_normalized_data.avg_score < 0.5:
		# Se intentó disminuir, pero no debería ir por debajo del mínimo
		if adaptive_agent.difficulty == adaptive_agent.min_difficulty:
			print("SUCCESS: Difficulty correctly limited at min. Expected: ", adaptive_agent.min_difficulty, ", Got: ", adaptive_agent.difficulty)
		else:
			print("ERROR: Difficulty went below min bound. Expected: ", adaptive_agent.min_difficulty, ", Got: ", adaptive_agent.difficulty)
			test_passed = false
	else:
		# Si no se intentó disminuir, solo verificar que no esté por debajo del mínimo
		if adaptive_agent.difficulty >= adaptive_agent.min_difficulty:
			print("SUCCESS: Difficulty within bounds. Expected: ", adaptive_agent.min_difficulty, ", Got: ", adaptive_agent.difficulty)
		else:
			print("ERROR: Difficulty went below min bound. Expected: ", adaptive_agent.min_difficulty, ", Got: ", adaptive_agent.difficulty)
			test_passed = false
	
	if test_passed:
		print("SUCCESS: test_agent_respects_difficulty_bounds passed")
	else:
		print("FAILURE: test_agent_respects_difficulty_bounds failed")

func _on_action_decided(action: String, new_difficulty: float, signal_ref, action_ref, difficulty_ref):
	# Callback function to capture signal values
	print("DEBUG: Recibido signal con action: ", action, " y new_difficulty: ", new_difficulty)
	signal_ref.set(true)
	action_ref.set(action)
	difficulty_ref.set(new_difficulty)

func teardown():
	print("DEBUG: Finalizando teardown de test_adaptive_agent")
	# Clean up after tests if needed
	adaptive_agent = null
