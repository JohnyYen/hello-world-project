
# GameInstanceDetailResponse

Esquema para respuesta detallada de instancia con relaciones

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
`gameTitle` | string
`studentUsername` | string

## Example

```typescript
import type { GameInstanceDetailResponse } from ''

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
  "gameTitle": null,
  "studentUsername": null,
} satisfies GameInstanceDetailResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as GameInstanceDetailResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


