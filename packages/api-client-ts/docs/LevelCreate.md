
# LevelCreate

Esquema para creación de nivel

## Properties

Name | Type
------------ | -------------
`description` | string
`game_id` | number
`goal` | string
`level_number` | number
`title` | string

## Example

```typescript
import type { LevelCreate } from ''

// TODO: Update the object below with actual values
const example = {
  "description": null,
  "game_id": null,
  "goal": null,
  "level_number": null,
  "title": null,
} satisfies LevelCreate

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as LevelCreate
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


