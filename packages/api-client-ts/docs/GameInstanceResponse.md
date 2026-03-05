
# GameInstanceResponse

Esquema para la respuesta de una instancia de juego

## Properties

Name | Type
------------ | -------------
`id` | number
`gameId` | number
`studentId` | number
`status` | string
`startInstance` | Date
`createdAt` | Date
`updatedAt` | Date
`isDeleted` | boolean

## Example

```typescript
import type { GameInstanceResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "id": null,
  "gameId": null,
  "studentId": null,
  "status": null,
  "startInstance": null,
  "createdAt": null,
  "updatedAt": null,
  "isDeleted": null,
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


