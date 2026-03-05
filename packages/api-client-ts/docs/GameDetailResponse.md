
# GameDetailResponse

Esquema para respuesta detallada de juego con relaciones

## Properties

Name | Type
------------ | -------------
`title` | string
`description` | string
`creator` | string
`subject` | string
`publicationStatus` | string
`id` | number
`createdAt` | Date
`updatedAt` | Date
`isDeleted` | boolean
`levelsCount` | number

## Example

```typescript
import type { GameDetailResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "title": Juego de Matemáticas,
  "description": null,
  "creator": null,
  "subject": null,
  "publicationStatus": null,
  "id": null,
  "createdAt": null,
  "updatedAt": null,
  "isDeleted": null,
  "levelsCount": null,
} satisfies GameDetailResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as GameDetailResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


