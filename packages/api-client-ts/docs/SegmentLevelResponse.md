
# SegmentLevelResponse

Esquema para la respuesta de un segmento de nivel

## Properties

Name | Type
------------ | -------------
`_configuration` | object
`created_at` | Date
`id` | number
`is_deleted` | boolean
`level_number_id` | number
`updated_at` | Date

## Example

```typescript
import type { SegmentLevelResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "_configuration": null,
  "created_at": null,
  "id": null,
  "is_deleted": null,
  "level_number_id": null,
  "updated_at": null,
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


