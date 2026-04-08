
# LevelListResponse

Esquema para listado de niveles

## Properties

Name | Type
------------ | -------------
`data` | [Array&lt;LevelResponse&gt;](LevelResponse.md)
`message` | string
`success` | boolean
`total` | number

## Example

```typescript
import type { LevelListResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "data": null,
  "message": null,
  "success": null,
  "total": null,
} satisfies LevelListResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as LevelListResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


