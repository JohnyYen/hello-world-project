class_name StartBlock
extends BaseBlock

# Bloque de inicio - marca el comienzo del programa
func execute(context: BaseProblemContext):
    # Este bloque no necesita hacer nada especial en su ejecución
    # El motor de ejecución maneja el flujo
    context.log("Inicio")
    return context;