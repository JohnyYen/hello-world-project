
# GameDetailResponse

Esquema para respuesta detallada de juego con relaciones

## Properties

Name | Type
------------ | -------------
`created_at` | Date
`creator` | string
`description` | string
`id` | number
`is_deleted` | boolean
`levels_count` | number
`publication_status` | string
`subject` | string
`title` | string
`updated_at` | Date

## Example

```typescript
import type { GameDetailResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "created_at": null,
  "creator": null,
  "description": null,
  "id": null,
  "is_deleted": null,
  "levels_count": null,
  "publication_status": null,
  "subject": null,
  "title": Juego de Matemáticas,
  "updated_at": null,
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


