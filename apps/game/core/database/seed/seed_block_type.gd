

func create_block_types(db) -> void:
    for bt in BlockTypesEnum.BlockTypesEnum.keys():
        db.insert_row("Block_Types", {"block_type": bt})