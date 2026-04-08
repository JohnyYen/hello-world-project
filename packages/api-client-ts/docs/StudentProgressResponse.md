
# StudentProgressResponse

Esquema para la respuesta de progreso del estudiante

## Properties

Name | Type
------------ | -------------
`data` | object
`error` | [](.md)
`message` | string
`success` | boolean

## Example

```typescript
import type { StudentProgressResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "data": null,
  "error": null,
  "message": null,
  "success": null,
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


