class_name LevelStrategy

static func create_level(level) -> LevelController:

    match level:
        LevelEnum.Level.Level_One:
            return LevelOneController.new();
        _:
            push_error("LEVEL_CONTROLLER_NOT_SUPORTED")
    return null