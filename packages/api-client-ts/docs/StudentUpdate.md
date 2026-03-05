
# StudentUpdate

Esquema para actualizar la información del estudiante

## Properties

Name | Type
------------ | -------------
`username` | string
`email` | string
`name` | string
`lastname` | string
`isActive` | boolean

## Example

```typescript
import type { StudentUpdate } from ''

// TODO: Update the object below with actual values
const example = {
  "username": null,
  "email": null,
  "name": null,
  "lastname": null,
  "isActive": null,
} satisfies StudentUpdate

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as StudentUpdate
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


