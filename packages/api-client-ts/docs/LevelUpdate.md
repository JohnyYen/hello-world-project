
# LevelUpdate

Esquema para actualización de nivel

## Properties

Name | Type
------------ | -------------
`levelNumber` | number
`title` | string
`description` | string
`goal` | string

## Example

```typescript
import type { LevelUpdate } from ''

// TODO: Update the object below with actual values
const example = {
  "levelNumber": null,
  "title": null,
  "description": null,
  "goal": null,
} satisfies LevelUpdate

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as LevelUpdate
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


