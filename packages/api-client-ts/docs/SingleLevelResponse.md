
# SingleLevelResponse

Esquema para respuesta de un solo nivel

## Properties

Name | Type
------------ | -------------
`data` | [LevelDetailResponse](LevelDetailResponse.md)
`message` | string
`success` | boolean

## Example

```typescript
import type { SingleLevelResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "data": null,
  "message": null,
  "success": null,
} satisfies SingleLevelResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as SingleLevelResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


