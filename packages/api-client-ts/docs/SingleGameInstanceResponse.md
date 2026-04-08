
# SingleGameInstanceResponse

Esquema para respuesta de una sola instancia

## Properties

Name | Type
------------ | -------------
`data` | [GameInstanceDetailResponse](GameInstanceDetailResponse.md)
`message` | string
`success` | boolean

## Example

```typescript
import type { SingleGameInstanceResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "data": null,
  "message": null,
  "success": null,
} satisfies SingleGameInstanceResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as SingleGameInstanceResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


