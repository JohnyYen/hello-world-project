
# StudentCreate

Esquema para crear un nuevo estudiante

## Properties

Name | Type
------------ | -------------
`email` | string
`is_active` | boolean
`lastname` | string
`name` | string
`password` | string
`username` | string

## Example

```typescript
import type { StudentCreate } from ''

// TODO: Update the object below with actual values
const example = {
  "email": null,
  "is_active": null,
  "lastname": null,
  "name": null,
  "password": null,
  "username": null,
} satisfies StudentCreate

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as StudentCreate
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


