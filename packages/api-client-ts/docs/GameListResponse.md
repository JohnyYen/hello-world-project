
# GameListResponse

Esquema para listado de juegos

## Properties

Name | Type
------------ | -------------
`data` | [Array&lt;GameResponse&gt;](GameResponse.md)
`limit` | number
`message` | string
`skip` | number
`success` | boolean
`total` | number

## Example

```typescript
import type { GameListResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "data": null,
  "limit": null,
  "message": null,
  "skip": null,
  "success": null,
  "total": null,
} satisfies GameListResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as GameListResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


