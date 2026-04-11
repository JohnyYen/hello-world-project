# Interfaz para los bloques
class_name BaseBlock
extends Block # TODO: Revisar esta herencia a detalle

func _init():
	pass

func execute(context: BaseProblemContext):
	return context;
