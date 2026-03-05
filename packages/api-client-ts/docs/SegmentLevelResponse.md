
# SegmentLevelResponse

Esquema para la respuesta de un segmento de nivel

## Properties

Name | Type
------------ | -------------
`id` | number
`levelNumberId` | number
`_configuration` | object
`createdAt` | Date
`updatedAt` | Date
`isDeleted` | boolean

## Example

```typescript
import type { SegmentLevelResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "id": null,
  "levelNumberId": null,
  "_configuration": null,
  "createdAt": null,
  "updatedAt": null,
  "isDeleted": null,
} satisfies SegmentLevelResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as SegmentLevelResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


