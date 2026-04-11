# Import the seed files
var SeedBlockType = load("res://core/database/seed/seed_block_type.gd")
var SeedBlocks = load("res://core/database/seed/seed_blocks.gd")
var SeedLevels = load("res://content/level_1_cafeteria/database/seed/seed_levels.gd")
var SeedSegments = load("res://content/level_1_cafeteria/database/seed/seed_segments.gd")
var SeedSegmentBlocks = load("res://core/database/seed/seed_segment_blocks.gd")

func run_all_seeds(db):
    create_block_types(db)
    create_blocks(db)
    create_levels(db)
    create_segments(db)
    create_segment_blocks(db)
    print("All seed data inserted successfully")

func create_block_types(db):
    var seed_block_type = SeedBlockType.new()
    seed_block_type.create_block_types(db)

func create_blocks(db):
    var seed_blocks = SeedBlocks.new()
    seed_blocks.create_blocks(db)

func create_levels(db):
    var seed_levels = SeedLevels.new()
    seed_levels.create_levels(db)

func create_segments(db):
    var seed_segments = SeedSegments.new()
    seed_segments.seed_level_1(db)

func create_segment_blocks(db):
    var seed_segment_blocks = SeedSegmentBlocks.new()
    seed_segment_blocks.create_segment_blocks(db)