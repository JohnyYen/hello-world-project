# Resource class that contains configuration for the feedback system
# This includes types of feedback, thresholds, display settings, and predefined messages
class_name FeedbackConfig

## Enum for feedback types to ensure consistency
enum FeedbackType {
	POSITIVE,     # For successful actions or good performance
	NEGATIVE,     # For errors or poor performance
	CORRECTIVE,   # For providing guidance on mistakes
	INFORMATIONAL,# For general information
	MOTIVATIONAL  # For encouragement and motivation
}

## Score threshold for positive feedback (0.0-1.0 scale)
const PERF_SCORE_THRESHOLD_HIGH := 0.8

## Score threshold for negative feedback (0.0-1.0 scale)
const PERF_SCORE_THRESHOLD_LOW := 0.4

## Error count threshold for corrective feedback
const ERROR_COUNT_THRESHOLD_HIGH := 3

## Time threshold in seconds for time-related feedback
const TIME_THRESHOLD_SLOW := 60.0

## How long to show feedback in seconds
const FEEDBACK_DISPLAY_DURATION := 5.0

## Minimum time between feedback messages in seconds
const FEEDBACK_MIN_INTERVAL := 2.0

## Maximum number of feedback messages to queue
const FEEDBACK_QUEUE_SIZE := 3

## Configuration for different levels of the game
const LEVEL_FEEDBACK_SETTINGS := {
	"cafeteria": {
		"display_duration": 4.0,
		"min_interval": 1.5,
		"motivational_frequency": 0.3
	},
	"library": {
		"display_duration": 6.0,
		"min_interval": 3.0,
		"motivational_frequency": 0.5
	}
}

## Predefined feedback messages organized by type
const FEEDBACK_MESSAGES := {
	FeedbackType.POSITIVE: [
		"¡Bien hecho! Estás progresando muy bien.",
		"Excelente trabajo, sigue así.",
		"Has resuelto este reto de forma muy efectiva."
	],
	FeedbackType.NEGATIVE: [
		"Tu solución tuvo algunos errores, inténtalo de nuevo.",
		"No te preocupes, todos cometemos errores. Aprende de esta experiencia.",
		"Parece que necesitas más práctica con este concepto."
	],
	FeedbackType.CORRECTIVE: [
		"Considera revisar la sintaxis de tu código aquí.",
		"Recuerda verificar las condiciones de tu bucle.",
		"¿Estás seguro de que esta variable está inicializada correctamente?"
	],
	FeedbackType.INFORMATIONAL: [
		"Recuerda que las variables deben declararse antes de usarse.",
		"Los bucles te permiten repetir acciones de forma eficiente.",
		"Las funciones ayudan a organizar tu código de forma modular."
	],
	FeedbackType.MOTIVATIONAL: [
		"¡No te rindas! Cada error es una oportunidad para aprender.",
		"Estás en el camino correcto, ¡continúa esforzándote!",
		"Tu dedicación está dando resultados, ¡bien hecho!"
	]
}

## Priority levels for different feedback types (higher number = higher priority)
const FEEDBACK_PRIORITY := {
	FeedbackType.NEGATIVE: 3,
	FeedbackType.CORRECTIVE: 4,
	FeedbackType.POSITIVE: 2,
	FeedbackType.MOTIVATIONAL: 1,
	FeedbackType.INFORMATIONAL: 2
}

## Accessibility settings for feedback display
const ACCESSIBILITY_SETTINGS := {
	"text_size_multiplier": 1.0,  # Multiplier for text size
	"high_contrast_mode": false,   # Whether to use high contrast colors
	"alt_text_enabled": true       # Whether to include alternative text descriptions
}
