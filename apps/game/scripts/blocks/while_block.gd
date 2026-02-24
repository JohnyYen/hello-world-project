class_name WhileBlock
extends BaseBlock

# Reutilizamos las mismas propiedades que `If`
var variable_name: String
var operator: String
var value_to_compare

# La evaluación se delega a la misma función que `If`
func evaluate_condition(context: BaseProblemContext) -> bool:
    # Podríamos copiar el código de `block_if.gd` o crear una clase base
    # `ConditionalBlock` de la que hereden `If` y `While`.
    # Por ahora, copiamos para simplificar.
    var var_value = context.get_variable(variable_name)

    match operator:
        "==": return var_value == value_to_compare
        "!=": return var_value != value_to_compare
        ">": return var_value > value_to_compare
        "<": return var_value < value_to_compare
        ">=": return var_value >= value_to_compare
        "<=": return var_value <= value_to_compare
        _:
            context.log("Operador no soportado: " + operator)
            return false