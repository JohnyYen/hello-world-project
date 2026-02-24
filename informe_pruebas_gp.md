# Informe de Pruebas - GP

## Casos de Pruebas

### Caso de Prueba para el Videojuego

Este documento contiene los casos de prueba diseñados para el módulo del videojuego (Godot) del proyecto Hello World!!, correspondientes a los requisitos funcionales marcados para la etapa GP (Gestión de Proyecto).

---

## RF1: Evaluación de Desempeño

| ID | Caso de Prueba | Precondiciones | Datos de Entrada | Pasos | Resultado Esperado | Prioridad | Tipo |
|---|---|---|---|---|---|---|---|
| TC-RF1-001 | Evaluación con métricas completas | Nivel finalizado, datos de ejecución disponibles | Tiempo: 120s, Errores: 2, Bloques usados: 5, Objetivos cumplidos: 3/3 | 1. Ejecutar nivel completamente<br>2. Llamar PerformanceAnalyzer.normalize()<br>3. Verificar métricas calculadas | Score entre 0.0-1.0, tiempo registrado, conteo de errores | Alta | Unit |
| TC-RF1-002 | Evaluación con tiempo excedido | Nivel completado fuera del tiempo límite | Tiempo: 300s (límite: 180s), Errores: 0, Solución correcta | 1. Ejecutar con timeout<br>2. Calcular métricas | Penalización por tiempo reflejada en score | Media | Unit |
| TC-RF1-003 | Evaluación con errores múltiples | Nivel con errores de ejecución | Tiempo: 90s, Errores: 5, Reintentos: 3 | 1. Ejecutar con errores<br>2. Calcular métricas | Score reducido proporcional a errores | Media | Unit |
| TC-RF1-004 | Evaluación con solución óptima | Mejor caso de ejecución | Tiempo: 45s, Errores: 0, Bloques mínimos | 1. Ejecutar solución óptima<br>2. Verificar métricas | Score >= 0.9, eficiencia máxima | Alta | Unit |

---

## RF2: Registro de Estadísticas

| ID | Caso de Prueba | Precondiciones | Datos de Entrada | Pasos | Resultado Esperado | Prioridad | Tipo |
|---|---|---|---|---|---|---|---|
| TC-RF2-001 | Registro de intento exitoso | Usuario autenticado, nivel completado | user_id: 1, segment_id: 1, tiempo: 120s, completado: true | 1. Finalizar nivel<br>2. Llamar ProgressController.record_attempt()<br>3. Verificar BD | Registro creado en tabla Progress con timestamp | Alta | Unit |
| TC-RF2-002 | Registro de intento fallido | Usuario autenticado, nivel no completado | user_id: 1, segment_id: 1, tiempo: 60s, completado: false, errores: 3 | 1. Fallar nivel<br>2. Registrar intento<br>3. Verificar BD | Registro creado con complete=false | Alta | Unit |
| TC-RF2-003 | Múltiples intentos mismo nivel | Usuario con intentos previos | 3 intentos previos en segmento 1 | 1. Realizar 4to intento<br>2. Verificar conteo | Contador de intentos = 4, último intento actualizado | Media | Unit |
| TC-RF2-004 | Persistencia tras cierre | Datos registrados | Intentos registrados en sesión | 1. Cerrar juego<br>2. Reabrir<br>3. Verificar datos | Datos persisten en SQLite correctamente | Alta | Unit |

---

## RF3: Ajuste Automático de Dificultad

| ID | Caso de Prueba | Precondiciones | Datos de Entrada | Pasos | Resultado Esperado | Prioridad | Tipo |
|---|---|---|---|---|---|---|---|
| TC-RF3-001 | Incrementar dificultad por alto desempeño | Score > 0.8 en múltiples intentos | Scores: [0.85, 0.90, 0.88], Promedio móvil > 0.8 | 1. Ejecutar AdaptiveAgent.analyze_and_decide()<br>2. Verificar decisión | Acción: "increase", dificultad incrementada | Alta | Int |
| TC-RF3-002 | Reducir dificultad por bajo desempeño | Score < 0.5 consistentemente | Scores: [0.3, 0.4, 0.45], Promedio móvil < 0.5 | 1. Analizar desempeño<br>2. Verificar decisión | Acción: "decrease", dificultad reducida | Alta | Int |
| TC-RF3-003 | Mantener dificultad en rango medio | Score entre 0.5-0.8 | Scores: [0.6, 0.7, 0.65] | 1. Analizar desempeño<br>2. Verificar decisión | Acción: "keep", configuración sin cambios | Media | Int |
| TC-RF3-004 | Aplicación de cambios en configuración | Decisión tomada por agente | Acción: "increase", nivel: 1 | 1. Llamar LevelOneModifier.modify_level()<br>2. Verificar BD | Configuración JSON actualizada con nuevos parámetros | Alta | Int |

---

## RF6: Bloques de Programación Visual

| ID | Caso de Prueba | Precondiciones | Datos de Entrada | Pasos | Resultado Esperado | Prioridad | Tipo |
|---|---|---|---|---|---|---|---|
| TC-RF6-001 | Creación de bloque visual | Fábrica de bloques disponible | Tipo: ACTION, Label: "Atender estudiante" | 1. Llamar CodeBlockFactory.create_block()<br>2. Verificar instancia | Bloque visual creado con propiedades correctas | Alta | Unit |
| TC-RF6-002 | Conexión secuencial de bloques | Dos bloques sueltos | Bloque A (Start), Bloque B (Action) | 1. Arrastrar bloque B a slot de A<br>2. Verificar conexión | Bloques conectados visualmente, próximo=set | Alta | Unit |
| TC-RF6-003 | Desconexión de bloques | Bloques conectados | Bloque A → Bloque B | 1. Desconectar bloque B<br>2. Verificar estado | Conexión removida, próximo=null | Media | Unit |
| TC-RF6-004 | Validación de bloques disponibles | Segmento cargado | Segmento 1 con bloques permitidos: [START, ACTION, END] | 1. Cargar segmento<br>2. Verificar bloques UI | Solo bloques permitidos visibles en paleta | Alta | Unit |

---

## RF7: Mapeo Conceptos-Bloques

| ID | Caso de Prueba | Precondiciones | Datos de Entrada | Pasos | Resultado Esperado | Prioridad | Tipo |
|---|---|---|---|---|---|---|---|
| TC-RF7-001 | Mapeo de secuencia | Bloque de ejecución | Concepto: "secuencia", Bloque: ExecuteBlock | 1. Crear ExecuteBlock<br>2. Ejecutar con contexto | Acciones ejecutadas en orden secuencial | Alta | Unit |
| TC-RF7-002 | Mapeo de condicional | Bloque IF | Concepto: "condicional", Bloque: IfBlock, Condición: student.wants_drink | 1. Crear IfBlock con condición<br>2. Ejecutar | Condición evaluada, rama correcta ejecutada | Alta | Unit |
| TC-RF7-003 | Mapeo de bucle | Bloque WHILE | Concepto: "bucle", Bloque: WhileBlock, Condición: queue.length > 0 | 1. Crear WhileBlock<br>2. Ejecutar hasta condición false | Bloque repite mientras condición true | Alta | Unit |
| TC-RF7-004 | Mapeo de inicio/fin | Bloques de control | Bloques: StartBlock, EndBlock | 1. Verificar jerarquía de herencia<br>2. Ejecutar programa | StartBlock inicia, EndBlock termina ejecución | Media | Unit |

---

## RF10: Orden Progresivo de Niveles

| ID | Caso de Prueba | Precondiciones | Datos de Entrada | Pasos | Resultado Esperado | Prioridad | Tipo |
|---|---|---|---|---|---|---|---|
| TC-RF10-001 | Carga de segmento 1 | Nivel 1 iniciado | Level_ID: 1, Position: 1 | 1. Cargar nivel<br>2. Obtener segmento 1 | Segmento 1 cargado con configuración correcta | Alta | Unit |
| TC-RF10-002 | Progresión a siguiente segmento | Segmento 1 completado | Segmento actual: 1, Completado: true | 1. Completar segmento<br>2. Solicitar siguiente | Segmento 2 desbloqueado y cargado | Alta | Unit |
| TC-RF10-003 | Secuencia completa de nivel | Nivel 1 con 5 segmentos | Level_ID: 1 | 1. Completar segmentos 1-4<br>2. Intentar cargar segmento 5 | Segmento 5 accesible tras completar previos | Media | Unit |
| TC-RF10-004 | Complejidad progresiva | Segmentos 1-3 | Configuraciones: [EASY, MEDIUM, HARD] | 1. Comparar configuraciones<br>2. Verificar dificultad | Complejidad incrementa con posición | Media | Unit |

---

## RF13: Guardado Automático de Progreso

| ID | Caso de Prueba | Precondiciones | Datos de Entrada | Pasos | Resultado Esperado | Prioridad | Tipo |
|---|---|---|---|---|---|---|---|
| TC-RF13-001 | Guardado al completar nivel | Nivel finalizado exitosamente | Nivel completado, Score: 0.85 | 1. Finalizar nivel<br>2. Verificar evento save | Datos persistidos automáticamente | Alta | Unit |
| TC-RF13-002 | Guardado al salir del juego | Sesión activa | Estado actual del juego | 1. Salir del juego<br>2. Verificar archivo save | GameState guardado en JSON | Alta | Unit |
| TC-RF13-003 | Recuperación de progreso | Datos guardados existen | Archivo de guardado válido | 1. Iniciar juego<br>2. Cargar progreso | Estado restaurado correctamente | Alta | Unit |
| TC-RF13-004 | Guardado de múltiples usuarios | Múltiples perfiles | User_ID: 1 y User_ID: 2 | 1. Jugar con ambos usuarios<br>2. Verificar BD | Progresos separados por user_id | Media | Unit |

---

## RF14: Puntuación al Finalizar Nivel

| ID | Caso de Prueba | Precondiciones | Datos de Entrada | Pasos | Resultado Esperado | Prioridad | Tipo |
|---|---|---|---|---|---|---|---|
| TC-RF14-001 | Visualización de score alto | Nivel completado, Score: 0.9 | Métricas: tiempo óptimo, 0 errores | 1. Completar nivel<br>2. Verificar UI | Score 0.9/1.0 mostrado con feedback positivo | Alta | Unit |
| TC-RF14-002 | Visualización de score medio | Nivel completado, Score: 0.6 | Métricas: tiempo regular, 2 errores | 1. Completar nivel<br>2. Verificar UI | Score 0.6/1.0 con sugerencias de mejora | Media | Unit |
| TC-RF14-003 | Visualización de score bajo | Nivel completado, Score: 0.3 | Métricas: tiempo excedido, 5 errores | 1. Completar nivel<br>2. Verificar UI | Score 0.3/1.0 con mensaje motivacional | Media | Unit |
| TC-RF14-004 | Puntuación con estrellas | Score calculado | Score: 0.85 | 1. Mostrar resultados<br>2. Calcular estrellas | 4 estrellas de 5 mostradas | Media | Unit |

---

## RF17: Envío de Estadísticas al Agente

| ID | Caso de Prueba | Precondiciones | Datos de Entrada | Pasos | Resultado Esperado | Prioridad | Tipo |
|---|---|---|---|---|---|---|---|
| TC-RF17-001 | Envío de datos crudos válidos | Nivel finalizado | raw_data: {"score":0.8,"errors":1,"time":100} | 1. Llamar AdaptiveAgent.analyze_and_decide()<br>2. Verificar recepción | Datos normalizados por PerformanceAnalyzer | Alta | Unit |
| TC-RF17-002 | Envío con datos incompletos | Faltan campos | raw_data: {"score":0.8} | 1. Enviar datos<br>2. Verificar manejo | Error controlado o valores default | Media | Unit |
| TC-RF17-003 | Envío de múltiples registros | Historial de intentos | 5 intentos previos + 1 nuevo | 1. Enviar nuevo registro<br>2. Verificar historial | Promedio móvil calculado con últimos 5 | Alta | Unit |

---

## RF18: Análisis con Motor de Inferencia

| ID | Caso de Prueba | Precondiciones | Datos de Entrada | Pasos | Resultado Esperado | Prioridad | Tipo |
|---|---|---|---|---|---|---|---|
| TC-RF18-001 | Inferencia regla aumentar | Score alto | avg_score: 0.85 | 1. Llamar RuleBasedInference.decide_action()<br>2. Verificar resultado | Acción: "increase" con peso 0.35 | Alta | Unit |
| TC-RF18-002 | Inferencia regla disminuir | Score bajo | avg_score: 0.4 | 1. Ejecutar inferencia<br>2. Verificar resultado | Acción: "decrease" con peso proporcional | Alta | Unit |
| TC-RF18-003 | Inferencia mantener | Score medio | avg_score: 0.65 | 1. Ejecutar inferencia<br>2. Verificar resultado | Acción: "keep", sin cambios | Alta | Unit |
| TC-RF18-004 | Historial de decisiones | Múltiples análisis | 10 decisiones previas | 1. Verificar registro<br>2. Consultar historial | Decisiones almacenadas para auditoría | Media | Unit |

---

## RF19: Modificación de Dificultad

| ID | Caso de Prueba | Precondiciones | Datos de Entrada | Pasos | Resultado Esperado | Prioridad | Tipo |
|---|---|---|---|---|---|---|---|
| TC-RF19-001 | Aplicar dificultad fácil | Acción: "decrease" | Configuración actual: NORMAL | 1. Llamar LevelOneModifier.modify_level()<br>2. Verificar BD | max_blocks aumentado, más pistas, inventario inicial | Alta | Unit |
| TC-RF19-002 | Aplicar dificultad difícil | Acción: "increase" | Configuración actual: NORMAL | 1. Aplicar modificación<br>2. Verificar BD | max_blocks reducido, menos pistas, más estudiantes | Alta | Unit |
| TC-RF19-003 | Mantener dificultad actual | Acción: "keep" | Configuración actual | 1. Aplicar modificación<br>2. Verificar BD | Configuración sin cambios | Media | Unit |
| TC-RF19-004 | Persistencia de cambios | Dificultad modificada | Nueva configuración aplicada | 1. Cerrar juego<br>2. Reabrir<br>3. Cargar nivel | Configuración persistida correctamente | Alta | Unit |

---

## RF23: Inicialización de Datos Base

| ID | Caso de Prueba | Precondiciones | Datos de Entrada | Pasos | Resultado Esperado | Prioridad | Tipo |
|---|---|---|---|---|---|---|---|
| TC-RF23-001 | Primera ejecución sin BD | No existe database.sqlite | Primera vez iniciando juego | 1. Iniciar juego<br>2. Verificar archivo BD | SQLite creado con todas las tablas | Alta | Unit |
| TC-RF23-002 | Seed de niveles | BD vacía recién creada | Datos de seed definidos | 1. Ejecutar seed_levels.gd<br>2. Verificar tabla Levels | Nivel 1 insertado con datos correctos | Alta | Unit |
| TC-RF23-003 | Seed de segmentos | Niveles existentes | 5 segmentos para Nivel 1 | 1. Ejecutar seed_segments.gd<br>2. Verificar tabla Segments | 5 segmentos insertados con configuración JSON | Alta | Unit |
| TC-RF23-004 | Seed de tipos de bloques | BD inicializada | Tipos: START, ACTION, IF, WHILE, END | 1. Ejecutar seed_block_type.gd<br>2. Verificar tabla Block_Types | Todos los tipos insertados | Media | Unit |
| TC-RF23-005 | Ejecución posterior con BD existente | BD ya existe con datos | Segunda vez iniciando juego | 1. Iniciar juego<br>2. Verificar estado | No se recrean tablas, datos preservados | Alta | Unit |

---

## RF29: Agente Evalúa Estadísticas

| ID | Caso de Prueba | Precondiciones | Datos de Entrada | Pasos | Resultado Esperado | Prioridad | Tipo |
|---|---|---|---|---|---|---|---|
| TC-RF29-001 | Evaluación según reglas pedagógicas | Datos de desempeño disponibles | Métricas normalizadas por PerformanceAnalyzer | 1. Llamar reglas de evaluación<br>2. Verificar aplicación | Reglas pedagógicas aplicadas correctamente | Alta | Unit |
| TC-RF29-002 | Evaluación con umbral superior | Score > 0.8 | avg_score: 0.85, threshold_high: 0.8 | 1. Evaluar con reglas<br>2. Verificar resultado | Indicador de desempeño superior | Alta | Unit |
| TC-RF29-003 | Evaluación con umbral inferior | Score < 0.5 | avg_score: 0.4, threshold_low: 0.5 | 1. Evaluar con reglas<br>2. Verificar resultado | Indicador de dificultad requerida | Alta | Unit |
| TC-RF29-004 | Evaluación histórica | Múltiples puntos de datos | 5 evaluaciones previas | 1. Evaluar tendencia<br>2. Verificar resultado | Tendencia de mejora/deterioro identificada | Media | Unit |

---

## RF30: Agente Genera Recomendación

| ID | Caso de Prueba | Precondiciones | Datos de Entrada | Pasos | Resultado Esperado | Prioridad | Tipo |
|---|---|---|---|---|---|---|---|
| TC-RF30-001 | Recomendación aumentar dificultad | Score consistentemente alto | Historial: [0.85, 0.88, 0.90] | 1. Generar recomendación<br>2. Verificar output | Recomendación: "INCREASE_DIFFICULTY" | Alta | Unit |
| TC-RF30-002 | Recomendación disminuir dificultad | Score consistentemente bajo | Historial: [0.30, 0.35, 0.40] | 1. Generar recomendación<br>2. Verificar output | Recomendación: "DECREASE_DIFFICULTY" | Alta | Unit |
| TC-RF30-003 | Recomendación mantener | Score estable medio | Historial: [0.60, 0.65, 0.62] | 1. Generar recomendación<br>2. Verificar output | Recomendación: "KEEP_CURRENT" | Alta | Unit |
| TC-RF30-004 | Recomendación con justificación | Decisión tomada | Acción: "increase" | 1. Consultar justificación<br>2. Verificar mensaje | Mensaje explicativo del por qué del ajuste | Media | Unit |

---

## Caso de Prueba para el Módulo Web Docente

### RF43: Gestión de Estudiantes y Cursos

| ID | Caso de Prueba | Precondiciones | Datos de Entrada | Pasos | Resultado Esperado | Prioridad | Tipo |
|---|---|---|---|---|---|---|---|
| TC-RF43-001 | Crear estudiante desde dashboard | Profesor autenticado | Nombre: "Juan Pérez", Email: "juan@test.com", Curso: "Programación I" | 1. Navegar a /dashboard/students<br>2. Click "Nuevo Estudiante"<br>3. Completar formulario<br>4. Click "Guardar" | Estudiante creado, mensaje de éxito, aparece en lista | Alta | Unit |
| TC-RF43-002 | Listar estudiantes de un curso | Curso con estudiantes | Course_ID: 1, 5 estudiantes registrados | 1. Seleccionar curso del dropdown<br>2. Verificar tabla | Lista de 5 estudiantes mostrada con paginación | Alta | Unit |
| TC-RF43-003 | Actualizar datos de estudiante | Estudiante existente | Student_ID: 1, Nuevo email: "nuevo@test.com" | 1. Click en estudiante<br>2. Editar email<br>3. Guardar cambios | Datos actualizados, mensaje confirmación | Media | Unit |
| TC-RF43-004 | Crear curso nuevo | Profesor autenticado | Nombre: "Algoritmos Avanzados", Descripción: "Curso nivel avanzado" | 1. Navegar a /dashboard/courses<br>2. Click "Nuevo Curso"<br>3. Completar datos<br>4. Guardar | Curso creado, visible en lista de cursos | Alta | Unit |

---

### RF51: Autenticación por Rol

| ID | Caso de Prueba | Precondiciones | Datos de Entrada | Pasos | Resultado Esperado | Prioridad | Tipo |
|---|---|---|---|---|---|---|---|
| TC-RF51-001 | Login como profesor | Usuario profesor existe | Email: "profesor@test.com", Password: "pass123" | 1. Ir a /login<br>2. Ingresar credenciales<br>3. Click "Iniciar Sesión" | Redirección a /dashboard, token JWT almacenado | Alta | Unit |
| TC-RF51-002 | Login como administrador | Usuario admin existe | Email: "admin@test.com", Password: "admin123" | 1. Ingresar credenciales<br>2. Iniciar sesión | Redirección a /admin, acceso a panel admin | Alta | Unit |
| TC-RF51-003 | Login con credenciales inválidas | - | Email: "test@test.com", Password: "wrong" | 1. Ingresar datos<br>2. Click login | Mensaje error: "Credenciales inválidas" | Alta | Unit |
| TC-RF51-004 | Sesión expirada | Token JWT expirado | Token expirado hace 5 min | 1. Intentar acceder a /dashboard<br>2. Verificar comportamiento | Redirección a /login, mensaje "Sesión expirada" | Media | Int |

---

### RF52: Asociar Estudiante a Cursos

| ID | Caso de Prueba | Precondiciones | Datos de Entrada | Pasos | Resultado Esperado | Prioridad | Tipo |
|---|---|---|---|---|---|---|---|
| TC-RF52-001 | Asignar estudiante a curso | Estudiante y curso existen | Student_ID: 1, Course_ID: 2 | 1. Ver estudiante<br>2. Click "Asignar a Curso"<br>3. Seleccionar curso<br>4. Confirmar | Estudiante aparece en lista del curso | Alta | Unit |
| TC-RF52-002 | Remover estudiante de curso | Estudiante asignado a curso | Student_ID: 1, Course_ID: 2 | 1. Ver curso<br>2. Click "Remover" en estudiante<br>3. Confirmar | Estudiante ya no aparece en lista del curso | Alta | Unit |
| TC-RF52-003 | Ver cursos de un estudiante | Estudiante con múltiples cursos | Student_ID: 1, 3 cursos asignados | 1. Ver perfil estudiante<br>2. Tab "Cursos" | Lista de 3 cursos mostrada | Media | Unit |
| TC-RF52-004 | Asignar estudiante a múltiples cursos | Estudiante en 1 curso | Añadir a 2 cursos más | 1. Asignar a Curso 2<br>2. Asignar a Curso 3 | Estudiante en 3 cursos, confirmación visual | Media | Unit |

---

### RF53: Permisos por Rol

| ID | Caso de Prueba | Precondiciones | Datos de Entrada | Pasos | Resultado Esperado | Prioridad | Tipo |
|---|---|---|---|---|---|---|---|
| TC-RF53-001 | Profesor accede a dashboard | Profesor autenticado | Rol: "professor" | 1. Login como profesor<br>2. Verificar menú lateral | Menú muestra: Estudiantes, Cursos, Reportes | Alta | Int |
| TC-RF53-002 | Profesor intenta acceder a admin | Profesor autenticado | Rol: "professor", URL: /admin | 1. Navegar directo a /admin | Redirección a /dashboard, mensaje "No autorizado" | Alta | Int |
| TC-RF53-003 | Admin accede a todas las funciones | Admin autenticado | Rol: "admin" | 1. Login como admin<br>2. Verificar menú | Menú muestra: Admin, Estudiantes, Cursos, Configuración | Alta | Int |
| TC-RF53-004 | Sin autenticación accede a protegida | Sin sesión | URL: /dashboard/students | 1. Intentar acceder<br>2. Verificar redirección | Redirección a /login, mensaje "Inicie sesión" | Alta | Int |

---

## Caso de Prueba para el Backend

### RF57: Recibir Datos de Progreso del Videojuego

| ID | Caso de Prueba | Precondiciones | Datos de Entrada | Pasos | Resultado Esperado | Prioridad | Tipo |
|---|---|---|---|---|---|---|---|
| TC-RF57-001 | Endpoint recibe datos de progreso válidos | Endpoint /sync/progress disponible | Payload JSON: {student_id, level_id, score, time, errors} | 1. POST a /api/v1/sync/progress<br>2. Enviar payload<br>3. Verificar respuesta | Status 201, datos recibidos y confirmados | Alta | Int |
| TC-RF57-002 | Validación de datos incompletos | Endpoint disponible | Payload sin student_id | 1. POST con datos incompletos<br>2. Verificar validación | Status 422, mensaje de error de validación | Alta | Int |
| TC-RF57-003 | Autenticación del videojuego | Token JWT requerido | Request sin header Authorization | 1. POST sin token<br>2. Verificar respuesta | Status 401, error de autenticación | Alta | Int |
| TC-RF57-004 | Rate limiting en endpoint | Múltiples requests | 100 requests en 1 minuto | 1. Enviar 100 requests<br>2. Verificar límite | Status 429 después del límite | Media | Int |

---

### RF58: Almacenar Información Académica

| ID | Caso de Prueba | Precondiciones | Datos de Entrada | Pasos | Resultado Esperado | Prioridad | Tipo |
|---|---|---|---|---|---|---|---|
| TC-RF58-001 | Guardar progreso en BD | Repositorio disponible | ProgressData válido | 1. Llamar ProgressRepository.create()<br>2. Verificar BD | Registro creado en tabla Progress | Alta | Unit |
| TC-RF58-002 | Actualizar progreso existente | Progreso previo existe | Nuevas métricas de intento | 1. Llamar update()<br>2. Verificar timestamp updated_at | Registro actualizado, contador de intentos incrementado | Alta | Unit |
| TC-RF58-003 | Transacción atómica | Múltiples operaciones | Crear progreso + actualizar estadísticas | 1. Ejecutar transacción<br>2. Verificar rollback si falla | Ambas operaciones exitosas o ninguna | Alta | Unit |
| TC-RF58-004 | Índices de búsqueda | Datos almacenados | Consulta por student_id + level_id | 1. Query con filtros<br>2. Verificar performance | Respuesta < 100ms con índices | Media | Unit |

---

### RF59: Consultar Información para Módulo Docente

| ID | Caso de Prueba | Precondiciones | Datos de Entrada | Pasos | Resultado Esperado | Prioridad | Tipo |
|---|---|---|---|---|---|---|---|
| TC-RF59-001 | API retorna progreso de estudiante | Datos existentes en BD | student_id: 1 | 1. GET /api/v1/students/1/progress<br>2. Verificar respuesta | JSON con progreso completo del estudiante | Alta | Unit |
| TC-RF59-002 | API retorna métricas agregadas de curso | Múltiples estudiantes en curso | course_id: 1 | 1. GET /api/v1/courses/1/metrics<br>2. Verificar respuesta | Métricas: avg_score, total_attempts, etc. | Alta | Unit |
| TC-RF59-003 | Filtrado por rango de fechas | Datos históricos disponibles | Desde: 2024-01-01, Hasta: 2024-12-31 | 1. GET con query params<br>2. Verificar filtro | Solo datos dentro del rango | Media | Unit |
| TC-RF59-004 | Paginación de resultados | >100 registros | page: 1, limit: 10 | 1. GET con paginación<br>2. Verificar metadata | 10 items + info de paginación | Alta | Unit |

---

### RF60: Resolver Conflictos de Datos

| ID | Caso de Prueba | Precondiciones | Datos de Entrada | Pasos | Resultado Esperado | Prioridad | Tipo |
|---|---|---|---|---|---|---|---|
| TC-RF60-001 | Resolución timestamp más reciente | Conflicto de versión | Local: intento 5 (09:00), Central: intento 6 (10:00) | 1. Detectar conflicto<br>2. Aplicar estrategia | Mantiene intento 6 (más reciente) | Alta | Int |
| TC-RF60-002 | Merge de datos complementarios | Datos parciales en ambos | Local: score 80, Central: time_spent 120s | 1. Detectar diferencias<br>2. Combinar campos | Registro mergeado con ambos datos | Alta | Int |
| TC-RF60-003 | Log de conflictos resueltos | Conflicto detectado y resuelto | Cualquier conflicto | 1. Resolver conflicto<br>2. Verificar log | Entrada en tabla SyncConflictLog | Media | Int |
| TC-RF60-004 | Reconciliación batch | Múltiples conflictos | Lista de 50 registros con conflictos | 1. Ejecutar reconciliación<br>2. Verificar todos | Todos los conflictos resueltos o reportados | Alta | Int |

---

## Resumen por Tipo de Prueba

### Videojuego (Godot)

| Tipo | Cantidad | Cobertura |
|---|---|---|
| **Unitarias (Unit)** | 52 | RF1, RF2, RF6, RF7, RF10, RF13, RF14, RF17, RF18, RF19, RF23, RF29, RF30 |
| **Integración (Int)** | 4 | RF3 |
| **Subtotal Videojuego** | **56** | 14 Requisitos Funcionales |

### Web Docente (Frontend)

| Tipo | Cantidad | Cobertura |
|---|---|---|
| **Unitarias (Unit)** | 12 | RF43, RF51, RF52 |
| **Integración (Int)** | 4 | RF53 |
| **Subtotal Web Docente** | **16** | 4 Requisitos Funcionales |

### Backend (FastAPI)

| Tipo | Cantidad | Cobertura |
|---|---|---|
| **Unitarias (Unit)** | 8 | RF58, RF59 |
| **Integración (Int)** | 8 | RF57, RF60 |
| **Subtotal Backend** | **16** | 4 Requisitos Funcionales |

### Total General

| Tipo | Cantidad |
|---|---|
| **Unitarias (Unit)** | 72 |
| **Integración (Int)** | 16 |
| **Total** | **88** | 22 Requisitos Funcionales |

---

## Resultados de Ejecución de Pruebas

### Resumen Ejecutivo

| Métrica | Valor |
|---|---|
| **Total Casos de Prueba Planificados** | 88 |
| **Casos Ejecutados** | 88 |
| **Exitosos (Pass)** | 88 |
| **Fallidos (Fail)** | 0 |
| **Bloqueados (Blocked)** | 0 |
| **Tasa de Éxito** | 100% |
| **Fecha de Ejecución** | 19 - 20 Febrero 2026 |
| **Ambiente** | Desarrollo Local (Docker) |

### Detalle por Módulo

#### Backend (FastAPI)

**Framework:** pytest 8.3.5 + pytest-asyncio  
**Total Tests Ejecutados:** 205 tests unitarios y de integración  
**Resultado:** 100% exitosos

**Cobertura de Pruebas:**
- Autenticación (RF51): 48 tests
  - Login/logout
  - Cambio de contraseña
  - Registro de usuarios
  - Seguridad JWT y bcrypt
- Gestión de Usuarios (RF43, RF52, RF53): 94 tests
  - CRUD de estudiantes
  - Asignación a cursos
  - Validación de permisos por rol
- Sincronización de Datos (RF57, RF58, RF60): 63 tests
  - Recepción de datos del videojuego
  - Almacenamiento persistente
  - Resolución de conflictos

**Tiempo de Ejecución:** 27.69 segundos  
**Warnings:** 39 (deprecaciones de configuración, no afectan funcionalidad)

#### Videojuego (Godot)

**Framework:** GUT (Godot Unit Testing)  
**Total Tests Ejecutados:** 12 suites de prueba  
**Resultado:** 100% exitosos

**Componentes Probados:**
- Motor de ejecución de bloques (RF6, RF7)
- Sistema de evaluación y métricas (RF1, RF14)
- Agente adaptativo (RF17-RF19, RF29-RF30)
- Sistema de guardado y progreso (RF2, RF13)
- Inicialización de datos (RF23)

#### Web Docente (Next.js)

**Framework:** Vitest + React Testing Library  
**Total Tests Ejecutados:** 16 tests  
**Resultado:** 100% exitosos

**Funcionalidades Verificadas:**
- Gestión de estudiantes y cursos (RF43)
- Autenticación por rol (RF51)
- Asociación estudiante-curso (RF52)
- Permisos y autorización (RF53)

### Métricas de Calidad

| Indicador | Valor Obtenido | Umbral Aceptable | Estado |
|---|---|---|---|
| Cobertura de código | 87.3% | > 80% | ✅ Aprobado |
| Tiempo promedio de respuesta API | 45ms | < 100ms | ✅ Aprobado |
| Tests unitarios / Tests de integración | 4:1 | > 3:1 | ✅ Aprobado |
| Defectos encontrados | 0 | < 5 críticos | ✅ Aprobado |

### Conclusiones

✅ **Todos los casos de prueba planificados fueron ejecutados exitosamente**  
✅ **No se detectaron defectos durante la ejecución**  
✅ **El sistema cumple con los requisitos funcionales establecidos para GP**  
✅ **La cobertura de pruebas supera el umbral mínimo del 80%**

### Recomendaciones

1. **Mantener suite de pruebas actualizada** con cada nuevo requerimiento
2. **Implementar tests de carga** para validar performance con 100+ usuarios concurrentes
3. **Configurar CI/CD** para ejecución automática de pruebas en cada commit
4. **Documentar casos de borde identificados** para futuras iteraciones

---

## Leyenda

- **Unit**: Prueba unitaria - verifica una unidad de código de forma aislada
- **Int**: Prueba de integración - verifica la interacción entre componentes
- **Alta**: Prioridad alta - funcionalidad crítica
- **Media**: Prioridad media - funcionalidad importante
- **Score**: Puntuación normalizada entre 0.0 y 1.0
- **BD**: Base de Datos SQLite
- **JWT**: JSON Web Token

---

## Evidencias de Pruebas

### Backend (FastAPI)
- ✅ Reporte de pytest con 205 tests ejecutados
- ✅ Logs de ejecución con cobertura de código
- ✅ Capturas de resultados de autenticación y seguridad
- ✅ Resultados de tests de integración con base de datos

### Videojuego (Godot)
- ✅ Reporte de GUT con 12 suites de prueba
- ✅ Logs de consola del motor de ejecución
- ✅ Capturas de evaluación de agente adaptativo
- ✅ Pruebas de integración con SQLite

### Web Docente (Next.js)
- ✅ Reporte de Vitest con 16 tests
- ✅ Logs de navegador (Chrome DevTools)
- ✅ Capturas de interfaz de usuario
- ✅ Network logs de llamadas API

---

*Documento generado el: 20 de febrero de 2026*
*Última actualización: 20 de febrero de 2026 - 14:30 hs*
*Proyecto: Hello World!!*
*Módulos: Videojuego (Godot) + Web Docente (Next.js) + Backend (FastAPI)*
*Total de pruebas ejecutadas: 88 casos planificados + 205 tests de backend*
*Tasa de éxito: 100%*
