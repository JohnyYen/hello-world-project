class_name CodeBlockFactory


func create_code_block(block_type):
	var code_block;
	print("DEBUG [CodeBlockFactory]: Create Block in Factory with block_type: %s" % block_type)
	match block_type:
		BlockTypesEnum.BlockTypesEnum.START, "START":
			print("DEBUG [CodeBlockFactory]: Create Block in Factory : Start")
			
			code_block =  preload("res://scenes/components/blocks/start_block.tscn")
		BlockTypesEnum.BlockTypesEnum.END, "END":
			print("DEBUG [CodeBlockFactory]: Create Block in Factory : Finish")
			
			code_block =  preload("res://scenes/components/blocks/finish_block.tscn")
		BlockTypesEnum.BlockTypesEnum.ACTION, "ACTION":
			print("DEBUG [CodeBlockFactory]: Create Block in Factory : Execution")
			
			code_block =  preload("res://scenes/components/blocks/execution_block.tscn")
		_:
			print_debug("DEBUG [CodeBlockFactory]: BLOCK_TYPE_NOT_SUPPORTED")
			push_error("BLOCK_TYPE_NOT_SUPPORTED")
			code_block = null

	print("DEBUG [CodeBlockFactory]: Return Block Component %s" % code_block)
	return code_block.instantiate()
