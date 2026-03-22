
# GameInstanceCreate

Esquema para crear una nueva instancia de juego

## Properties

Name | Type
------------ | -------------
`game_id` | number
`status` | string
`student_id` | number

## Example

```typescript
import type { GameInstanceCreate } from ''

// TODO: Update the object below with actual values
const example = {
  "game_id": null,
  "status": null,
  "student_id": null,
} satisfies GameInstanceCreate

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as GameInstanceCreate
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


