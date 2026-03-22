
# SegmentLevelUpdateResponse

Esquema para respuesta de actualización de segmento

## Properties

Name | Type
------------ | -------------
`data` | [SegmentLevelResponse](SegmentLevelResponse.md)
`message` | string
`success` | boolean

## Example

```typescript
import type { SegmentLevelUpdateResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "data": null,
  "message": null,
  "success": null,
} satisfies SegmentLevelUpdateResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as SegmentLevelUpdateResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


