# xAPI Implementation for Hello World Game

## Overview

This module implements **xAPI 1.0 (Experience API)** for tracking learning experiences from the Hello World educational game. It provides a standardized way to collect, store, and query learning data with support for high-volume ingestion (10K+ statements per session).

## Features

- **xAPI 1.0 Compliant** - Full specification support with game-specific extensions
- **Batch Processing** - Accept up to 1000 statements per request
- **JWT Authentication** - Secure endpoint access
- **Optimized Queries** - Indexed fields for fast retrieval by student, game, level, verb
- **Automatic Parsing** - Extracts game-specific fields from xAPI context
- **Extensible** - Easy to add new verbs and activity types

## xAPI Statement Format

### Required Fields

```json
{
  "actor": { "account": { "homePage": "hello-world-game", "name": "student_id" } },
  "verb": { "id": "http://adlnet.gov/expapi/verbs/completed" },
  "object": { "id": "hello-world://segment/level_1_seg_3" }
}
```

### Full Example (with context and result)

```json
{
  "statements": [
    {
      "actor": {
        "account": {
          "homePage": "hello-world-game",
          "name": "123"
        }
      },
      "verb": {
        "id": "http://adlnet.gov/expapi/verbs/completed"
      },
      "object": {
        "id": "hello-world://segment/level_1_seg_3",
        "definition": {
          "type": "http://adlnet.gov/expapi/activities/lesson",
          "name": { "es": "Segmento 3 - Variables" }
        }
      },
      "result": {
        "score": { "raw": 85, "min": 0, "max": 100, "scaled": 0.85 },
        "success": true,
        "completion": true,
        "duration": "PT5M30S"
      },
      "context": {
        "platform": "Hello World Game v1.0",
        "language": "es",
        "extensions": {
          "http://hello-world-game.com/extensions/game_id": 1,
          "http://hello-world-game.com/extensions/level_id": 1,
          "http://hello-world-game.com/extensions/segment_id": 3,
          "http://hello-world-game.com/extensions/attempts": 2,
          "http://hello-world-game.com/extensions/hints_used": 1
        }
      },
      "timestamp": "2026-02-13T10:30:00Z"
    }
  ]
}
```

## Supported Verbs

| Verb ID | Usage |
|---------|-------|
| `http://adlnet.gov/expapi/verbs/initialized` | Player starts a level/segment |
| `http://adlnet.gov/expapi/verbs/progressed` | Progress in content |
| `http://adlnet.gov/expapi/verbs/attempted` | Attempted to complete something |
| `http://adlnet.gov/expapi/verbs/completed` | Completed a segment |
| `http://adlnet.gov/expapi/verbs/passed` | Passed a level |
| `http://adlnet.gov/expapi/verbs/failed` | Failed a level |
| `http://adlnet.gov/expapi/verbs/experienced` | Experienced (e.g., error) |
| `http://adlnet.gov/expapi/verbs/interacted` | Interacted (e.g., hint used) |
| `http://adlnet.gov/expapi/verbs/terminated` | Terminated game session |

## Activity Types

| Type | Description |
|------|-------------|
| `http://adlnet.gov/expapi/activities/course` | Full game/course |
| `http://adlnet.gov/expapi/activities/lesson` | Level |
| `hello-world://activity/level` | Game level |
| `hello-world://activity/segment` | Segment within a level |
| `hello-world://activity/exercise` | Exercise/puzzle |

## API Endpoints

### POST /statistic/xapi/statements

Receive and store xAPI statements.

- **Auth**: JWT Token required
- **Body**: `{ "statements": [...] }` (1-1000 items)
- **Response**: Array of stored statements with IDs

### GET /statistic/xapi/statements

Get statements with filters.

- **Auth**: JWT Token required
- **Query Parameters**:
  - `student_id` - Filter by student ID
  - `verb_id` - Filter by verb
  - `game_id` - Filter by game ID
  - `level_id` - Filter by level ID
  - `skip` - Pagination offset (default: 0)
  - `limit` - Results per page (default: 100, max: 1000)

### GET /statantic/xapi/statements/{statement_id}

Get a specific statement by ID.

- **Auth**: JWT Token required

## Game Integration

### Object ID Format

Use the following format for object IDs:
```
hello-world://segment/level_{level_id}_seg_{segment_id}
hello-world://level/{level_id}
hello-world://game/{game_id}
```

### Context Extensions

Include game-specific data in context.extensions:

| Extension | Type | Description |
|-----------|------|-------------|
| `http://hello-world-game.com/extensions/game_id` | integer | Game ID |
| `http://hello-world-game.com/extensions/level_id` | integer | Level ID |
| `http://hello-world-game.com/extensions/segment_id` | integer | Segment ID |
| `http://hello-world-game.com/extensions/attempts` | integer | Number of attempts |
| `http://hello-world-game.com/extensions/hints_used` | integer | Hints used |
| `http://hello-world-game.com/extensions/game_session` | string | Session ID |

## Database Schema

The `xapi_statements` table includes:
- Parsed fields for efficient queries (actor, verb, object, result)
- Full statement JSON storage
- Indexed fields: student_id, game_id, level_id, verb_id, timestamp

## Future Enhancements

- **Progress Derivation**: Automatically derive Progress records from xAPI statements
- **Analytics Endpoints**: Aggregated statistics endpoints
- **LRS Export**: Export statements to external Learning Record Stores
