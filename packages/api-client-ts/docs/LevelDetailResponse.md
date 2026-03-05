
# LevelDetailResponse

Esquema para respuesta detallada de nivel con segmentos

## Properties

Name | Type
------------ | -------------
`levelNumber` | number
`title` | string
`description` | string
`goal` | string
`id` | number
`gameId` | number
`createdAt` | Date
`updatedAt` | Date
`isDeleted` | boolean
`segmentsCount` | number

## Example

```typescript
import type { LevelDetailResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "levelNumber": null,
  "title": null,
  "description": null,
  "goal": null,
  "id": null,
  "gameId": null,
  "createdAt": null,
  "updatedAt": null,
  "isDeleted": null,
  "segmentsCount": null,
} satisfies LevelDetailResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as LevelDetailResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


