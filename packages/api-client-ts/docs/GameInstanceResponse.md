
# GameInstanceResponse

Esquema para la respuesta de una instancia de juego

## Properties

Name | Type
------------ | -------------
`created_at` | Date
`game_id` | number
`id` | number
`is_deleted` | boolean
`start_instance` | Date
`status` | string
`student_id` | number
`updated_at` | Date

## Example

```typescript
import type { GameInstanceResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "created_at": null,
  "game_id": null,
  "id": null,
  "is_deleted": null,
  "start_instance": null,
  "status": null,
  "student_id": null,
  "updated_at": null,
} satisfies GameInstanceResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as GameInstanceResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


