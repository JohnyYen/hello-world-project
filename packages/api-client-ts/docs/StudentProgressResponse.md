
# StudentProgressResponse

Esquema para la respuesta de progreso del estudiante

## Properties

Name | Type
------------ | -------------
`success` | boolean
`message` | string
`data` | object
`error` | [](.md)

## Example

```typescript
import type { StudentProgressResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "success": null,
  "message": null,
  "data": null,
  "error": null,
} satisfies StudentProgressResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as StudentProgressResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


