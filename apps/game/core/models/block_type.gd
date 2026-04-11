# BlockType.gd
class_name BlockType


var tipo_bloque_id: int  # Clave primaria (PK)
var tipo_bloque: String

# Relación con Blocks (uno a muchos)
var blocks: Array = []  # Lista de bloques de este tipo
