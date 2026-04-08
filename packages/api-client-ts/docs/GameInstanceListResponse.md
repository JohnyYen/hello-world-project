
# GameInstanceListResponse

Esquema para listado de instancias de juego

## Properties

Name | Type
------------ | -------------
`data` | [Array&lt;GameInstanceResponse&gt;](GameInstanceResponse.md)
`limit` | number
`message` | string
`skip` | number
`success` | boolean
`total` | number

## Example

```typescript
import type { GameInstanceListResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "data": null,
  "limit": null,
  "message": null,
  "skip": null,
  "success": null,
  "total": null,
} satisfies GameInstanceListResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as GameInstanceListResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


