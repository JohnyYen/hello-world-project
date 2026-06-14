# test_full_integration.gd
# Test de integracion completo: 3 tiraderas de nivel → agente adaptativo → xAPI → login → sync
# Incluye datos enriquecidos (hints_used, efficiency_rating, objectives_completed) en el pipeline.
extends Node

# UUID canónico de fixture para actor_id (REQ-P2-R4).
# Reemplaza el literal hardcodeado que vivía en este archivo y que era
# rechazado por los guards de XAPIService/GameController (no representaba
# un usuario autenticado real). El UUID fixture es reutilizable.
const FIXTURE_USER_UUID: String = "00000000-0000-0000-0000-000000000001"

# Variables globales compartidas entre fases
var _test_instance_id: String = ""
var _jwt_token: String = ""
var _user_data: Dictionary = {}
var _has_token: bool = false
var _batch_ids: Array = []

# Agente compartido entre runs para acumular historial de intentos
var _agent: AdaptiveAgent = null

# =============================================================================
# _ready() — Entry point principal
# =============================================================================
func _ready() -> void:
	# Limpiar historial persistente y crear agente compartido
	AttemptHistoryPersistence.clear_history()
	_agent = AdaptiveAgent.new()

	# Datos enriquecidos: score, errors, time, hints_used, efficiency, objectives, blocks
	var runs: Array = []

	# Run 1: High score - la dificultad debe aumentar
	runs.append(_run_single_level("Paso 1 - Alto", 0.9, 1, 30.0, true,
		1, 90.0, 5, 12, "increase"))

	# Run 2: Low score - la dificultad debe disminuir
	runs.append(_run_single_level("Paso 2 - Bajo", 0.2, 10, 120.0, true,
		5, 30.0, 1, 8, "decrease"))

	# Run 3: Medium score - la dificultad debe mantenerse
	runs.append(_run_single_level("Paso 3 - Medio", 0.65, 3, 90.0, true,
		2, 65.0, 3, 10, "keep"))

	# Sync flow
	var sync_data := _sync_flow()

	# Resumen
	_print_summary(runs, sync_data)

	get_tree().change_scene_to_file("res://scenes/pages/menu.tscn")


# =============================================================================
# _login() — Autenticacion contra el backend
# =============================================================================
func _login() -> Dictionary:
	print("\n--- Login ---")
	var api := ApiClient.new()
	add_child(api)
	await get_tree().process_frame

	print("Autenticando con estudiante1 / password123...")
	var result := await api.login("", "student.game@example.com", "Studentpass123!")

	if result.get("OK", false):
		var token := api.jwt_token
		var truncated := token.substr(0, 20) + "..."
		print(">>> Login EXITOSO <<<")
		print("Token: %s" % truncated)
		print("User: %s" % str(api.current_user))

		var user_data := api.current_user.duplicate()
		remove_child(api)
		api.queue_free()
		return {"OK": true, "token": token, "user_data": user_data}
	else:
		var error_msg = result.get("error", "unknown")
		print(">>> Login FALLIDO (backend offline?) <<<")
		print("Error: %s" % str(error_msg))
		print("Continuando con test offline...")
		remove_child(api)
		api.queue_free()
		return {"OK": false, "token": "", "user_data": {}}


# =============================================================================
# _build_enriched_data() — Construye data enriquecida para el agente
# =============================================================================
func _build_enriched_data(
	score: float,
	errors: int,
	time: float,
	hints_used: int,
	efficiency_rating: float,
	objectives_completed: int,
	blocks_count: int
) -> Dictionary:
	return {
		"score": score,
		"errors": errors,
		"time": time,
		"hints_used": hints_used,
		"efficiency_rating": efficiency_rating,
		"objectives_completed": objectives_completed,
		"blocks_count": blocks_count,
		"error_details": {},
		"custom_events": []
	}


# =============================================================================
# _run_single_level() — Una tiradera de nivel completa con datos enriquecidos
# =============================================================================
func _run_single_level(
	label: String,
	score: float,
	errors: int,
	time: float,
	success: bool,
	hints_used: int,
	efficiency_rating: float,
	objectives_completed: int,
	blocks_count: int,
	expected_action: String
) -> Dictionary:
	print("\n========== %s ==========" % label)
	print("Score: %.2f, Errors: %d, Time: %.0fs, Success: %s" % [score, errors, time, str(success)])
	print("Hints: %d, Efficiency: %.1f, Objetivos: %d, Bloques: %d" % [hints_used, efficiency_rating, objectives_completed, blocks_count])
	print("Accion esperada: %s" % expected_action)

	# 1. Crear contexto de cafeteria
	print("\n[1/7] Creando contexto...")
	var context := CafeteriaProblemContext.new()
	context.student_queue = [
		{"nombre": "Ana", "pedido": "cafe"},
		{"nombre": "Luis", "pedido": "te"},
		{"nombre": "Maria", "pedido": "pan"}
	]
	context.menu = {"cafe": 5, "te": 3, "pan": 2}
	context.cash_register = 0
	context.level_goal = {"all_served": true}
	print("Contexto creado con %d estudiantes" % context.student_queue.size())

	# 2. XAPIService
	print("\n[2/7] Inicializando XAPIService...")
	var xapi := XAPIService.new()
	add_child(xapi)
	await get_tree().process_frame

	if _has_token:
		xapi.track_level_started("level_1", label, FIXTURE_USER_UUID)
		print("Statement 'started' creado")
	else:
		print("Modo offline: xAPI tracking local (no se envia al backend)")

	# 3. ExecutionEngine
	print("\n[3/7] Ejecutando motor...")
	var blocks: Array = []
	var start_block := StartBlock.new()
	var end_block := EndBlock.new()
	blocks.append(start_block)
	blocks.append(end_block)

	var result_context := ExecutionEngine.execute(blocks, context)
	if result_context != null:
		print("Ejecucion completada: %d outputs" % result_context.outputs.size())
	else:
		print("Ejecucion retorno NULL")

	# 4. Agente adaptativo (compartido entre runs para acumular historial)
	print("\n[4/7] Analizando con AdaptiveAgent...")
	var initial_diff := _agent.difficulty

	# Pasar datos enriquecidos: score, errors, time + hints_used, efficiency_rating, etc.
	var enriched_data := _build_enriched_data(
		score, errors, time,
		hints_used, efficiency_rating, objectives_completed, blocks_count
	)

	# Capturar la accion exacta del agente via signal
	var captured_action := ""
	var signal_connected := _agent.action_decided.connect(func(a: String, d: float):
		captured_action = a
	)

	_agent.analyze_and_decide(enriched_data)

	# Detectar accion comparando dificultad antes/despues (direccion)
	var direction: String
	if _agent.difficulty > initial_diff:
		direction = "increase"
	elif _agent.difficulty < initial_diff:
		direction = "decrease"
	else:
		direction = "keep"

	print("Dificultad: %.1f → %.1f (delta=%.1f)" % [initial_diff, _agent.difficulty, _agent.difficulty - initial_diff])
	print("Accion exacta del agente: %s" % captured_action)
	print("Direccion detectada: %s (esperada: %s)" % [direction, expected_action])

	var test_passed := (direction == expected_action)
	if test_passed:
		print(">>> PASS: La direccion coincide con la esperada (%s) <<<" % expected_action)
	else:
		print(">>> FAIL: Se esperaba '%s' pero se obtuvo '%s' <<<" % [expected_action, direction])

	# 5. LevelOneModifier (usa la accion exacta del agente)
	print("\n[5/7] Aplicando modificador de nivel...")
	var modifier := LevelOneModifier.new()

	# Necesita un segment con configuracion
	modifier.set_level_segment({
		"segment_id": 0,
		"configuration": {
			"execution_rules": {"max_blocks": 10},
			"initial_state": {
				"student_queue": [
					{"nombre": "Ana", "pedido": "cafe"},
					{"nombre": "Luis", "pedido": "te"},
					{"nombre": "Maria", "pedido": "pan"}
				],
				"inventory": [],
				"stations": {
					"bread_dispenser": ["pan"],
					"drink_dispenser": ["cafe"]
				}
			},
			"feedback_messages": {"hints": ["Pista inicial"]},
			"version": "1.0"
		}
	})

	if captured_action != "":
		modifier.modify_level(captured_action, _agent.difficulty)
		print("Modificador aplicado con accion: %s" % captured_action)
	else:
		print("Sin accion (historial insuficiente) - no se aplica modificador")

	# 6. xAPI tracking (nivel completado)
	print("\n[6/7] Trackeando resultado en xAPI...")
	if _has_token:
		var duration_str := _format_duration(time)
		xapi.track_level_completed(
			"level_1", label, FIXTURE_USER_UUID,
			score * 100.0, score, success, duration_str
		)
		print("Statement 'completed' creado")

		# Mostrar statements pendientes
		var pending := xapi.get_pending_statements(50)
		print("Statements pendientes en SQLite: %d" % pending.size())
		for stmt in pending:
			print("  - %s: %s (%s)" % [stmt.get("id", "?"), stmt.get("verb_display", "?"), stmt.get("object_type", "?")])
	else:
		xapi.track_level_completed(
			"level_1", label, FIXTURE_USER_UUID,
			score * 100.0, score, success, _format_duration(time)
		)
		var pending := xapi.get_pending_statements(50)
		print("Statements guardados localmente: %d" % pending.size())

	# 7. Crear batch para sync
	print("\n[7/7] Creando batch de sync...")
	var batch_id := xapi.create_batch()
	if batch_id != "":
		_batch_ids.append(batch_id)
		print("Batch creado: %s" % batch_id)
	else:
		print("Batch no creado (sin statements pendientes)")

	# Cleanup
	remove_child(xapi)
	xapi.queue_free()

	print("\n--- Fin %s: %s ---" % [label, "PASS" if test_passed else "FAIL"])

	return {
		"OK": true,
		"label": label,
		"action": captured_action,
		"direction": direction,
		"expected_action": expected_action,
		"initial_difficulty": initial_diff,
		"final_difficulty": _agent.difficulty,
		"test_passed": test_passed,
		"batch_id": batch_id,
		"total_attempts": _agent.analyzer.get_attempt_count()
	}


# =============================================================================
# _sync_flow() — Sincronizar batches al backend
# =============================================================================
func _sync_flow() -> Dictionary:
	print("\n========== SYNC FLOW ==========")

	if not _has_token:
		print("SKIP: No hay JWT token (backend estaba offline)")
		return {"OK": false, "reason": "no_token"}

	var results := {}

	# Inicializar XAPIService para sync
	print("\n[1/4] Inicializando XAPIService para sync...")
	var xapi := XAPIService.new()
	add_child(xapi)
	await get_tree().process_frame

	# Sincronizar batches pendientes
	print("\n[2/4] Enviando batches xAPI...")
	for i in range(_batch_ids.size()):
		var bid = _batch_ids[i]
		print("  Enviando batch %d/%d: %s" % [i + 1, _batch_ids.size(), bid])
		var batch_result := await xapi.process_batch(bid)
		print("  Resultado batch %s: %s" % [bid, str(batch_result)])
		results["batch_%d" % i] = batch_result

	remove_child(xapi)
	xapi.queue_free()

	# Legacy sync
	print("\n[3/4] Sincronizando eventos legacy...")
	var sync_svc := SyncService.new()
	add_child(sync_svc)
	await get_tree().process_frame

	# Agregar un evento legacy de prueba
	sync_svc.add_event("test_integration", {
		"runs": _batch_ids.size(),
		"instance_id": _test_instance_id,
		"timestamp": Time.get_datetime_string_from_system()
	})

	sync_svc.sync_all_pending(_test_instance_id)
	print("Sync legacy disparado (eventos pendientes seran enviados)")

	remove_child(sync_svc)
	sync_svc.queue_free()

	# Mostrar stats finales
	print("\n[4/4] Stats del sistema xAPI:")
	var stats := xapi.get_stats() if xapi != null else {}
	print("  Stats: %s" % str(stats))

	print("\n--- Sync completo ---")
	return {"OK": true, "results": results}


# =============================================================================
# _print_summary() — Resumen final del test
# =============================================================================
func _print_summary(runs: Array, sync_data: Dictionary) -> void:
	print("\n========================================")
	print("=== RESUMEN DEL TEST ===")
	print("========================================")

	var passed := 0
	var failed := 0

	for run in runs:
		var label = run.get("label", "?")
		var test_passed = run.get("test_passed", false)
		var action = run.get("action", "?")
		var expected = run.get("expected_action", "?")

		if test_passed:
			passed += 1
			print("  PASS | %s | accion=%s (esperada=%s)" % [label, action, expected])
		else:
			failed += 1
			print("  FAIL | %s | accion=%s (esperada=%s)" % [label, action, expected])

	print("----------------------------------------")
	print("  Resultado: %d/%d tests pasaron" % [passed, passed + failed])
	print("  Sync: %s" % ("OK" if sync_data.get("OK", false) else "SKIP"))
	print("  Token: %s" % ("obtenido" if _has_token else "no disponible"))
	print("  Batches creados: %d" % _batch_ids.size())
	print("========================================")


# =============================================================================
# _format_duration() — Convierte segundos a ISO 8601
# =============================================================================
func _format_duration(total_seconds: float) -> String:
	var hours := int(total_seconds) / 3600
	var minutes := (int(total_seconds) % 3600) / 60
	var secs := int(total_seconds) % 60

	var result := "PT"
	if hours > 0:
		result += "%dH" % hours
	if minutes > 0:
		result += "%dM" % minutes
	result += "%dS" % secs
	return result
