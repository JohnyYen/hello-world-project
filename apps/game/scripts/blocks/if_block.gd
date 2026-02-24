class_name IfBlock
extends BaseBlock

# Propiedades para definir la condición
var variable_name: String
var operator: String # "==", "!=", ">", "<", etc.
var value_to_compare

func evaluate_condition(context: BaseProblemContext) -> bool:
    var var_value = context.get_variable(variable_name)
    
    match operator:
        "==":
            return var_value == value_to_compare
        "!=":
            return var_value != value_to_compare
        ">":
            return var_value > value_to_compare
        "<":
            return var_value < value_to_compare
        ">=":
            return var_value >= value_to_compare
        "<=":
            return var_value <= value_to_compare
        _:
            context.log("Operador no soportado: " + operator)
            return false