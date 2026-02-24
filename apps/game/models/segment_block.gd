# SegmentBlock

class_name SegmentBlock

var segment_id: int  # Clave foránea (FK) a Segments
var block_id: int  # Clave foránea (FK) a Blocks
var is_required: bool

# Relación con Segment (muchos a uno)
var segment: Segment = null

# Relación con Block (muchos a uno)
var block: Block = null
