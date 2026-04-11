func create_segment_blocks(db) -> void:
    db.insert_row("Segment_Blocks", {
        "segment_id": 1,
        "block_id": 1,  # Changed from "blokc_id" to "block_id" to match the schema
        "is_required": true,		
    })
    
    db.insert_row("Segment_Blocks", {
        "segment_id": 1,
        "block_id": 2,  # Changed from "blokc_id" to "block_id" to match the schema
        "is_required": true,		
    })
    
    db.insert_row("Segment_Blocks", {
        "segment_id": 1,
        "block_id": 3,  # Changed from "blokc_id" to "block_id" to match the schema
        "is_required": true,		
    })