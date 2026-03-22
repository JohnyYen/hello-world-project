
# GameInstanceEndResponse

Esquema para respuesta de finalización de instancia

## Properties

Name | Type
------------ | -------------
`data` | [GameInstanceResponse](GameInstanceResponse.md)
`message` | string
`success` | boolean

## Example

```typescript
import type { GameInstanceEndResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "data": null,
  "message": null,
  "success": null,
} satisfies GameInstanceEndResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as GameInstanceEndResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


