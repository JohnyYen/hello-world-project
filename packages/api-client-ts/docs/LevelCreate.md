
# LevelCreate

Esquema para creación de nivel

## Properties

Name | Type
------------ | -------------
`levelNumber` | number
`title` | string
`description` | string
`goal` | string
`gameId` | number

## Example

```typescript
import type { LevelCreate } from ''

// TODO: Update the object below with actual values
const example = {
  "levelNumber": null,
  "title": null,
  "description": null,
  "goal": null,
  "gameId": null,
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


