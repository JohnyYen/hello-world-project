# test_block_repository.gd
extends GutTest

# Mock de la base de datos simplificado
class MockSQLite:
	var open_db_result = true
	var select_rows_result
	var query_result = []

	func open_db(): return open_db_result
	func select_rows(table, where, columns): return select_rows_result
	func query(query): pass
	func fetch_row(): return !query_result.empty()
	func get_data(col): return query_result.pop_front()

# Datos de prueba
var blocks_data = [{"block_id": 1, "tipo_bloque_id": 1, "description": "B1", "name": "N1"}, {"block_id": 2, "tipo_bloque_id": 2, "description": "B2", "name": "N2"}]
var block_types_data = [{"tipo_bloque_id": 1, "tipo_bloque": "T1"}, {"tipo_bloque_id": 2, "tipo_bloque": "T2"}]

func test_get_all_blocks():
	assert_file_exists(Env.DATABASE_URL)
	var repo = BlockRepository.new()
	var blocks = repo.get_all_blocks()
	assert_not_null(blocks)
	

func test_get_blocks_by_block_type():
	assert_file_exists(Env.DATABASE_URL)
	var repo = BlockRepository.new()
	var blocks = repo.get_blocks_by_block_type(1)
	assert_not_null(blocks.size())
