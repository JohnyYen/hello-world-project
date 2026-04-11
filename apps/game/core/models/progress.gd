# Progress
class_name Progress


var progress_id: int  # Clave primaria (PK)
var user_id: String  # Clave foránea (FK) a Players
var segment_id: int  # Clave foránea (FK) a Segments
var attemptat: int
var time_in_complete: float
var complete: bool
var last_try: String  # Usar String para fechas (puedes convertirlo a Date si es necesario)

# Relación con Player (muchos a uno)
var player: Player = null

# Relación con Segment (muchos a uno)
var segment: Segment = null
