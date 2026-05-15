# test_full_integration.gd
# Test de integracion completo: 3 tiraderas de nivel → agente adaptativo → xAPI → login → sync
extends Node

# Variables globales compartidas entre fases
var _test_instance_id: String = ""
var _jwt_token: String = ""
var _user_data: Dictionary = {}
var _has_token: bool = false
var _batch_ids: Array = []

# =============================================================================
# _ready() — Entry point principal
# =============================================================================
func _ready() -> void:
	print("\n========================================")
	print("=== FULL INTEGRATION TEST ===")
	print("========================================")
	print("Inicio: %s" % Time.get_datetime_string_from_system())

	_test_instance_id = "integration-test-%d" % Time.get_ticks_msec()
	print("Instance ID: %s" % _test_instance_id)

	# Fase 1: Login
	print("\n--- FASE 1: Login ---")
	var login_data := await _login()
	_has_token = login_data.get("OK", false)
	_jwt_token = login_data.get("token", "")
	_user_data = login_data.get("user_data", {})
	if _has_token:
		print("Token obtenido: %s..." % _jwt_token.substr(0, 20))
		print("User data: %s" % str(_user_data))
	else:
		print("Modo offline - continuando sin token")

	# Fase 2: Run 1 — Nivel completado alto rendimiento
	print("\n--- FASE 2: Run 1 - Nivel Completado Alto Rendimiento ---")
	var r1 := await _run_single_level(
		"Run 1 - Alto Rendimiento",
		0.85, 2, 90.0, true, "increase"
	)
	print("Resultado: %s" % ("PASS" if r1.get("test_passed", false) else "FAIL"))

	# Fase 3: Run 2 — Nivel fallido bajo rendimiento
	print("\n--- FASE 3: Run 2 - Nivel Fallido Bajo Rendimiento ---")
	var r2 := await _run_single_level(
		"Run 2 - Bajo Rendimiento",
		0.20, 15, 200.0, false, "decrease"
	)
	print("Resultado: %s" % ("PASS" if r2.get("test_passed", false) else "FAIL"))

	# Fase 4: Run 3 — Nivel completado con mucho tiempo
	print("\n--- FASE 4: Run 3 - Nivel Lento ---")
	var r3 := await _run_single_level(
		"Run 3 - Lento",
		0.70, 3, 300.0, true, "keep"
	)
	print("Resultado: %s" % ("PASS" if r3.get("test_passed", false) else "FAIL"))

	# Fase 5: Sync al backend
	print("\n--- FASE 5: Sync ---")
	var sync_data := await _sync_flow()
	if sync_data.get("OK", false):
		print("Sync completado: %s" % str(sync_data.get("results", {})))
	else:
		print("Sync skip: %s" % sync_data.get("reason", "desconocido"))

	# Resumen final
	_print_summary([r1, r2, r3], sync_data)

	print("\n========================================")
	print("=== FIN DEL TEST ===")
	print("========================================")


# =============================================================================
# _login() — Autenticacion contra el backend
# =============================================================================
func _login() -> Dictionary:
	print("\n--- Login ---")
	var api := ApiClient.new()
	add_child(api)
	await get_tree().process_frame

	print("Autenticando con estudiante1 / password123...")
	var result := await api.login("estudiante1", "", "password123")

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
# _run_single_level() — Una tiradera de nivel completa
# =============================================================================
func _run_single_level(
	label: String,
	score: float,
	errors: int,
	time: float,
	success: bool,
	expected_action: String
) -> Dictionary:
	print("\n========== %s ==========" % label)
	print("Score: %.2f, Errors: %d, Time: %.0fs, Success: %s" % [score, errors, time, str(success)])
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
		xapi.track_level_started("level_1", label, "estudiante1")
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

	# 4. Agente adaptativo
	print("\n[4/7] Analizando con AdaptiveAgent...")
	var agent := AdaptiveAgent.new()
	var initial_diff := agent.difficulty

	agent.analyze_and_decide({"score": score, "errors": errors, "time": time})

	# Detectar accion comparando dificultad antes/despues
	var action: String
	if agent.difficulty > initial_diff:
		action = "increase"
	elif agent.difficulty < initial_diff:
		action = "decrease"
	else:
		action = "keep"

	print("Dificultad: %.1f → %.1f (delta=%.1f)" % [initial_diff, agent.difficulty, agent.difficulty - initial_diff])
	print("Accion del agente: %s (esperada: %s)" % [action, expected_action])

	var test_passed := (action == expected_action)
	if test_passed:
		print(">>> PASS: La accion coincide con la esperada (%s) <<<" % expected_action)
	else:
		print(">>> FAIL: Se esperaba '%s' pero se obtuvo '%s' <<<" % [expected_action, action])

	# 5. LevelOneModifier
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

	modifier.modify_level(action, agent.difficulty)
	print("Modificador aplicado")

	# 6. xAPI tracking (nivel completado)
	print("\n[6/7] Trackeando resultado en xAPI...")
	if _has_token:
		var duration_str := _format_duration(time)
		xapi.track_level_completed(
			"level_1", label, "estudiante1",
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
			"level_1", label, "estudiante1",
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
		"action": action,
		"expected_action": expected_action,
		"initial_difficulty": initial_diff,
		"final_difficulty": agent.difficulty,
		"test_passed": test_passed,
		"batch_id": batch_id
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
