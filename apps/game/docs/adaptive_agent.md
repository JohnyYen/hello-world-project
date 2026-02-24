# 🧠 Documento de Diseño del Agente Inteligente de Ajuste de Dificultad

## 1. Descripción general

**Nombre del agente:**  
**Propósito principal:**  
**Tipo de enfoque actual:** Regla basada / Híbrido / Aprendizaje por refuerzo (futuro)  
**Versión del prototipo:**  

---

## 2. Objetivo general del agente

Explica brevemente qué busca lograr el agente dentro del sistema educativo o del videojuego.  
Ejemplo: “El agente ajusta dinámicamente la dificultad de los niveles en función del rendimiento del estudiante, buscando mantenerlo en un estado de flujo óptimo que favorezca el aprendizaje.”

---

## 3. Parámetros de rendimiento y estado

### 3.1. Métricas que el agente utiliza
| Métrica | Descripción | Fuente de datos | Tipo (Local / Histórico) |
|----------|--------------|-----------------|---------------------------|
| `score` | Puntuación o porcentaje de aciertos | Sistema de evaluación | Local |
| `errors` | Cantidad de errores cometidos | Motor de juego | Local |
| `time` | Tiempo total del nivel | Timer del nivel | Local |
| `avg_score` | Promedio suavizado de puntuaciones | Agente | Histórico |
| `fatigue_index` | (Opcional) Fatiga o número de repeticiones consecutivas | Juego / Analizador | Histórico |

---

### 3.2. Estado del jugador
Define qué datos representan el estado del jugador o estudiante.
```

Ejemplo:
{
"avg_score": 0.72,
"error_rate": 0.18,
"time_factor": 0.65
}

```

---

## 4. Objetivos de ajuste

### 4.1. Criterios de ajuste
- **Aumentar dificultad:**  
  Cuando `avg_score > 0.85` y `errors < 2`.

- **Reducir dificultad:**  
  Cuando `avg_score < 0.55` o `errors > 5`.

- **Mantener dificultad:**  
  Cuando el rendimiento esté entre 0.55 y 0.85.

### 4.2. Zona de flujo (Flow Zone)
| Límite inferior | Límite superior | Descripción |
|------------------|------------------|--------------|
| 0.55 | 0.85 | Rango óptimo de rendimiento donde el jugador se siente desafiado pero no frustrado. |

---

## 5. Estrategia de inferencia

### 5.1. Tipo de inferencia actual
- [x] Basada en reglas (JSON)
- [ ] Probabilística
- [ ] Q-Learning (planeado)
- [ ] Híbrida

### 5.2. Descripción técnica
Explica cómo el agente toma decisiones:
```

1. Analiza los datos de rendimiento del nivel actual.
2. Actualiza el promedio histórico usando un suavizado exponencial.
3. Evalúa las reglas del archivo JSON.
4. Emite una señal al modificador de nivel con la acción correspondiente.

````

### 5.3. Formato de reglas
```json
{
  "rules": [
    { "condition": "avg_score > 0.85 and errors < 2", "action": "increase_difficulty" },
    { "condition": "avg_score < 0.55 or errors > 5", "action": "decrease_difficulty" },
    { "condition": "true", "action": "keep" }
  ]
}
````

---

## 6. Mecanismo de aprendizaje y memoria

### 6.1. Método de suavizado

```
new_avg = (0.3 * last_score) + (0.7 * previous_avg)
```

### 6.2. Variables persistentes

| Variable           | Descripción                      | Persistencia               |
| ------------------ | -------------------------------- | -------------------------- |
| `avg_score`        | Promedio histórico de puntuación | Por sesión / Base de datos |
| `avg_time`         | Tiempo promedio de resolución    | Por sesión                 |
| `adaptation_count` | Número de ajustes aplicados      | Por sesión                 |

---

## 7. Frecuencia de decisión

| Evento                 | ¿El agente actúa? | Acción                      |
| ---------------------- | ----------------- | --------------------------- |
| Fin de nivel           | ✅                 | Analiza y ajusta dificultad |
| Durante nivel          | ❌ (por ahora)     | —                           |
| Al completar un módulo | 🔄 (opcional)     | Recalibra tendencia global  |

---

## 8. Integración del agente

### 8.1. Comunicación con otros sistemas

| Componente      | Tipo de interacción                     | Método / Señal           |
| --------------- | --------------------------------------- | ------------------------ |
| `LevelModifier` | Receptor                                | `action_decided(action)` |
| `GameManager`   | Fuente de datos                         | `performance_data`       |
| `Backend`       | (opcional) Sincroniza métricas globales | API REST o WebSocket     |

### 8.2. Ciclo de funcionamiento

```
[Jugador termina nivel]
      ↓
[Se envían métricas al agente]
      ↓
[Agente decide acción]
      ↓
[Se emite señal al modificador]
      ↓
[Se ajusta dificultad del siguiente nivel]
```

---

## 9. Escalabilidad y evolución

| Fase   | Descripción                                              | Estado |
| ------ | -------------------------------------------------------- | ------ |
| Fase 1 | Prototipo basado en reglas (actual)                      | ✅      |
| Fase 2 | Introducir ponderaciones dinámicas (adaptabilidad suave) | 🟡     |
| Fase 3 | Implementar Q-Learning o SARSA                           | ⏳      |
| Fase 4 | Integrar feedback emocional o fisiológico (opcional)     | ⏳      |

---

## 10. Validación del agente

### 10.1. Indicadores de éxito

| Indicador                | Descripción                               | Método de medición      |
| ------------------------ | ----------------------------------------- | ----------------------- |
| Estabilidad del flujo    | El jugador se mantiene en el rango óptimo | Promedio de rendimiento |
| Progresión sostenida     | Mejora gradual del aprendizaje            | Evolución del puntaje   |
| Reducción de frustración | Menor tasa de abandono                    | Encuestas o registros   |

### 10.2. Métodos de prueba

* Simulación con datos artificiales de rendimiento.
* Test con jugadores reales.
* Comparación entre ajustes automáticos vs manuales.

---

## 11. Preguntas abiertas o pendientes

* ¿Qué frecuencia de decisión mantiene mejor el flujo?
* ¿Debería el agente considerar factores emocionales o de fatiga?
* ¿Cómo manejar casos extremos (jugadores que fallan o aciertan siempre)?

---

**Autor:**
**Fecha de creación:**
**Última actualización:**

