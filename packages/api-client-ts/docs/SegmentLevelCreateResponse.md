
# SegmentLevelCreateResponse

Esquema para respuesta de creación de segmento

## Properties

Name | Type
------------ | -------------
`data` | [SegmentLevelResponse](SegmentLevelResponse.md)
`message` | string
`success` | boolean

## Example

```typescript
import type { SegmentLevelCreateResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "data": null,
  "message": null,
  "success": null,
} satisfies SegmentLevelCreateResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as SegmentLevelCreateResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


