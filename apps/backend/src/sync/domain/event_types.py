from enum import Enum


class SyncEventType(str, Enum):
    """
    Tipos de eventos de sincronización del pipeline de estadísticas.

    Clasificación:
    - Simple: Eventos que pueden procesarse de forma directa sin transformación compleja
    - Complex: Eventos que requieren procesamiento adicional, transformación o validación
    """

    # Simple events - direct processing
    LEVEL_TIME = "level_time"
    ATTEMPT = "attempt"
    SCORE = "score"
    LEVEL_COMPLETED = "level_completed"
    DIFFICULTY_CHANGED = "difficulty_changed"
    ADAPTATION = "adaptation"

    # Complex events - require additional processing
    ERROR = "error"
    INTERACTION = "interaction"
    HINT_USED = "hint_used"

    # Classification constants
    SIMPLE = "simple"
    COMPLEX = "complex"

    @classmethod
    def is_simple(cls, event_type: str) -> bool:
        """Verifica si un tipo de evento es simple."""
        simple_types = {
            cls.LEVEL_TIME,
            cls.ATTEMPT,
            cls.SCORE,
            cls.LEVEL_COMPLETED,
            cls.DIFFICULTY_CHANGED,
            cls.ADAPTATION,
        }
        return event_type in simple_types

    @classmethod
    def is_complex(cls, event_type: str) -> bool:
        """Verifica si un tipo de evento es complejo."""
        complex_types = {cls.ERROR, cls.INTERACTION, cls.HINT_USED}
        return event_type in complex_types

    @classmethod
    def classify(cls, event_type: str) -> str:
        """
        Clasifica un tipo de evento como simple o complex.

        Args:
            event_type: Tipo de evento a clasificar

        Returns:
            'simple' o 'complex'
        """
        if cls.is_simple(event_type):
            return cls.SIMPLE
        elif cls.is_complex(event_type):
            return cls.COMPLEX
        else:
            raise ValueError(f"Tipo de evento desconocido: {event_type}")

    @classmethod
    def get_all_simple(cls) -> list[str]:
        """Retorna todos los tipos de eventos simples."""
        return [e.value for e in cls if cls.is_simple(e.value)]

    @classmethod
    def get_all_complex(cls) -> list[str]:
        """Retorna todos los tipos de eventos complejos."""
        return [e.value for e in cls if cls.is_complex(e.value)]
