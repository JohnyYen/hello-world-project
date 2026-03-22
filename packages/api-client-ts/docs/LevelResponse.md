
# LevelResponse

Esquema para respuesta de nivel

## Properties

Name | Type
------------ | -------------
`created_at` | Date
`description` | string
`game_id` | number
`goal` | string
`id` | number
`is_deleted` | boolean
`level_number` | number
`title` | string
`updated_at` | Date

## Example

```typescript
import type { LevelResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "created_at": null,
  "description": null,
  "game_id": null,
  "goal": null,
  "id": null,
  "is_deleted": null,
  "level_number": null,
  "title": null,
  "updated_at": null,
} satisfies LevelResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as LevelResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


