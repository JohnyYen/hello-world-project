class_name AddMoneyAction
extends Action

var amount := 10

func _init(value: int = 10):
    amount = value

func execute(context):
    var cafeteria_context = context as CafeteriaProblemContext
    cafeteria_context.cash_register += amount
    cafeteria_context.money_added.emit(amount)
