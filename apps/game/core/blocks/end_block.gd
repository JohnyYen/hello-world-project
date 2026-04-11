class_name EndBlock
extends BaseBlock

# Bloque de fin - marca el final de una sección de código
func execute(context: BaseProblemContext):
	# Este bloque no necesita hacer nada especial en su ejecución
	# El motor de ejecución maneja el flujo, especialmente para estructuras de control
	context.log("Fin")
	return context;
