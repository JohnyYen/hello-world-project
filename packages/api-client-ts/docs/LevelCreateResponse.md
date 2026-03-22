
# LevelCreateResponse

Esquema para respuesta de creación de nivel

## Properties

Name | Type
------------ | -------------
`data` | [LevelResponse](LevelResponse.md)
`message` | string
`success` | boolean

## Example

```typescript
import type { LevelCreateResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "data": null,
  "message": null,
  "success": null,
} satisfies LevelCreateResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as LevelCreateResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


