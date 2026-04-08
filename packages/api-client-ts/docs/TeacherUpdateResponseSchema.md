
# TeacherUpdateResponseSchema

Respuesta para actualizaciones de profesor

## Properties

Name | Type
------------ | -------------
`data` | [TeacherProfileResponse](TeacherProfileResponse.md)
`error` | [](.md)
`message` | string
`success` | boolean

## Example

```typescript
import type { TeacherUpdateResponseSchema } from ''

// TODO: Update the object below with actual values
const example = {
  "data": null,
  "error": null,
  "message": null,
  "success": null,
} satisfies TeacherUpdateResponseSchema

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as TeacherUpdateResponseSchema
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


