"""
Diagnostic script: xAPI statement flow from game to progress update.

The game sends xAPI statements via sync events in LEGACY format (not xAPI 1.0):
{
    "event_type": "xapi_statement",
    "payload": {
        "statement_id": "<uuid>",
        "verb_id": "http://adlnet.gov/expapi/verbs/completed",
        "verb_display": "completó",
        "object_type": "level",
        "object_id": "2",                    # Level number as string
        "object_name": "Level 2",
        "actor_id": "<users.id>",            # users.id, NOT students.id!
        "result": {
            "score_raw": 0.75,               # Same value as score_scaled
            "score_scaled": 0.75,            # Both are 0.0-1.0 scale
            "success": true,
            "completion": true,
            "duration": "PT120.5S"
        },
        "timestamp": "..."
    }
}

KNOWN FIXES APPLIED (commit cd6dba3):
  - student_id now resolved via SyncSession → GameInstance chain (students.id)
  - No longer uses payload.actor_id (which is users.id, not students.id)

REMAINING ISSUES (fixed in this session):
  1. objectives_completed: "attempted" events no longer mark as completed
  2. score extraction: uses explicit None checks instead of `or`
     (0.0 is a valid score, but `0.0 or X` returns X — wrong!)
"""

if __name__ == "__main__":
    print("=" * 60)
    print("xAPI FLOW DIAGNOSTIC")
    print("=" * 60)
    print("""
CURRENT STATE:
  - student_id: Resolved via chain (SyncSession → GameInstance → students.id) ✅
  - segment_level_id: Resolved via chain (object_id → level_number → Level → SegmentLevel)
  - objectives_completed: Only set for 'completed' verb (not 'attempted') ✅
  - efficiency_rating: Extracted from result.score_scaled or result.score_raw ✅
    (uses explicit None checks, not `or` — handles 0.0 correctly)

REMAINING RISKS:
  - SegmentLevel resolution depends on DB having matching Level + SegmentLevel rows
  - Score naming: game passes same value for score_raw and score_scaled (both 0.0-1.0)
    - This works, but semantically score_raw should be 0-100 and score_scaled 0.0-1.0
    - See game_controller.gd line 107-108: `track_level_completed(score, score, ...)`
  - The diagnostic test files (test_xapi_flow.py) previously tested for complete xAPI 1.0
    format, but the game sends legacy format — now corrected.
    """)
