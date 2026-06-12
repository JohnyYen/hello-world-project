func seed_intro_feedback(db) -> void:
	var data = {
		"id": "intro-feedback-001",
		"student_id": "",
		"professor_id": "system",
		"professor_name": "Sistema",
		"comments": "Fortalezas: Este es tu primer feedback! Aca vas a ver los comentarios que tu profesor te deja sobre tu desempeño.\nAreas de mejora: Revisa esta seccion para identificar en que podes mejorar.\nComentarios adicionales: Presta atencion a las recomendaciones de tu profesor para aprovechar al maximo cada nivel.",
		"rating": 0,
		"feedback_type": "message",
		"course_id": "",
		"game_id": "",
		"level_id": "",
		"display_in_game": 1,
		"acknowledged_at": "",
		"is_read": 0,
		"created_at": "2026-01-01T00:00:00",
		"updated_at": "2026-01-01T00:00:00"
	}

	db.insert_row("professor_feedback", data)
	print("Seed: Feedback de introduccion insertado.")
