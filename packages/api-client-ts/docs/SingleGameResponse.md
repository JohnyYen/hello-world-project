
# SingleGameResponse

Esquema para respuesta de un solo juego

## Properties

Name | Type
------------ | -------------
`success` | boolean
`message` | string
`data` | [GameDetailResponse](GameDetailResponse.md)

## Example

```typescript
import type { SingleGameResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "success": null,
  "message": null,
  "data": null,
} satisfies SingleGameResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as SingleGameResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


