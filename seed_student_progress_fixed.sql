-- ============================================================================
-- Script de Seed para Rellenar Datos de Progreso de Estudiante (VERSIÓN CORREGIDA)
-- ============================================================================

-- Usar el student_id correcto: e985f329-b760-49ca-a819-2c2e47ac09d2
-- Este estudiante tiene user_id: 45db5077-378d-4c0d-baf4-431a8eb2dc84

-- PASO 1: Verificar que el estudiante existe
SELECT id FROM students WHERE id = 'e985f329-b760-49ca-a819-2c2e47ac09d2' LIMIT 1;

-- PASO 2: Obtener algunos segment_levels disponibles para usar
SELECT id FROM segment_levels LIMIT 10;

-- PASO 3: Insertar registros de progreso (8 registros con datos realistas)
INSERT INTO progresses (
    id,
    created_at,
    updated_at,
    attempt_count,
    error_count,
    hints_used_count,
    errors_details,
    objectives_completed,
    efficiency_rating,
    student_id,
    segment_level_id,
    is_deleted
) VALUES
-- Progreso 1: Nivel básico con múltiples intentos
(
    gen_random_uuid(),
    NOW() - INTERVAL '25 days',
    NOW() - INTERVAL '25 days',
    2,
    1,
    1,
    '{"errors": [{"type": "logic_error", "line": 5}]}'::json,
    3,
    78,
    'e985f329-b760-49ca-a819-2c2e47ac09d2'::uuid,
    (SELECT id FROM segment_levels ORDER BY RANDOM() LIMIT 1),
    false
),
-- Progreso 2: Nivel intermedio bien completado
(
    gen_random_uuid(),
    NOW() - INTERVAL '22 days',
    NOW() - INTERVAL '22 days',
    1,
    0,
    0,
    '{"errors": []}'::json,
    5,
    95,
    'e985f329-b760-49ca-a819-2c2e47ac09d2'::uuid,
    (SELECT id FROM segment_levels ORDER BY RANDOM() LIMIT 1),
    false
),
-- Progreso 3: Nivel con dificultad media
(
    gen_random_uuid(),
    NOW() - INTERVAL '20 days',
    NOW() - INTERVAL '20 days',
    3,
    2,
    2,
    '{"errors": [{"type": "syntax_error", "line": 8}, {"type": "runtime_error", "line": 12}]}'::json,
    4,
    82,
    'e985f329-b760-49ca-a819-2c2e47ac09d2'::uuid,
    (SELECT id FROM segment_levels ORDER BY RANDOM() LIMIT 1),
    false
),
-- Progreso 4: Nivel desafiante con varios intentos
(
    gen_random_uuid(),
    NOW() - INTERVAL '18 days',
    NOW() - INTERVAL '18 days',
    4,
    3,
    3,
    '{"errors": [{"type": "logic_error", "line": 3}, {"type": "logic_error", "line": 7}, {"type": "syntax_error", "line": 15}]}'::json,
    3,
    71,
    'e985f329-b760-49ca-a819-2c2e47ac09d2'::uuid,
    (SELECT id FROM segment_levels ORDER BY RANDOM() LIMIT 1),
    false
),
-- Progreso 5: Nivel completado con excelente rendimiento
(
    gen_random_uuid(),
    NOW() - INTERVAL '15 days',
    NOW() - INTERVAL '15 days',
    1,
    0,
    0,
    '{"errors": []}'::json,
    5,
    98,
    'e985f329-b760-49ca-a819-2c2e47ac09d2'::uuid,
    (SELECT id FROM segment_levels ORDER BY RANDOM() LIMIT 1),
    false
),
-- Progreso 6: Nivel con progreso intermedio
(
    gen_random_uuid(),
    NOW() - INTERVAL '12 days',
    NOW() - INTERVAL '12 days',
    2,
    1,
    1,
    '{"errors": [{"type": "logic_error", "line": 6}]}'::json,
    4,
    85,
    'e985f329-b760-49ca-a819-2c2e47ac09d2'::uuid,
    (SELECT id FROM segment_levels ORDER BY RANDOM() LIMIT 1),
    false
),
-- Progreso 7: Nivel reciente con buen desempeño
(
    gen_random_uuid(),
    NOW() - INTERVAL '8 days',
    NOW() - INTERVAL '8 days',
    1,
    0,
    0,
    '{"errors": []}'::json,
    5,
    92,
    'e985f329-b760-49ca-a819-2c2e47ac09d2'::uuid,
    (SELECT id FROM segment_levels ORDER BY RANDOM() LIMIT 1),
    false
),
-- Progreso 8: Nivel muy reciente (actividad actual)
(
    gen_random_uuid(),
    NOW() - INTERVAL '3 days',
    NOW() - INTERVAL '2 days',
    2,
    1,
    2,
    '{"errors": [{"type": "runtime_error", "line": 10}]}'::json,
    4,
    88,
    'e985f329-b760-49ca-a819-2c2e47ac09d2'::uuid,
    (SELECT id FROM segment_levels ORDER BY RANDOM() LIMIT 1),
    false
);

-- PASO 4: Verificar los datos insertados
SELECT 
    p.id,
    p.created_at,
    p.attempt_count,
    p.error_count,
    p.hints_used_count,
    p.objectives_completed,
    p.efficiency_rating
FROM progresses p
WHERE p.student_id = 'e985f329-b760-49ca-a819-2c2e47ac09d2'
ORDER BY p.created_at DESC;

-- PASO 5: Ver estadísticas del estudiante
SELECT 
    COUNT(*) as total_progress_records,
    COUNT(CASE WHEN p.objectives_completed > 0 THEN 1 END) as completed_levels,
    AVG(p.efficiency_rating) as average_score,
    SUM(p.attempt_count * 5) as total_play_time_minutes,
    MAX(p.updated_at) as last_activity
FROM progresses p
WHERE p.student_id = 'e985f329-b760-49ca-a819-2c2e47ac09d2';
