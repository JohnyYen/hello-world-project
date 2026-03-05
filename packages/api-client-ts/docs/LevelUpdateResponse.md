
# LevelUpdateResponse

Esquema para respuesta de actualización de nivel

## Properties

Name | Type
------------ | -------------
`success` | boolean
`message` | string
`data` | [LevelResponse](LevelResponse.md)

## Example

```typescript
import type { LevelUpdateResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "success": null,
  "message": null,
  "data": null,
} satisfies LevelUpdateResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as LevelUpdateResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


