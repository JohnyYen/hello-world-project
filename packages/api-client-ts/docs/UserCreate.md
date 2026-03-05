
# UserCreate

Esquema para creación de usuario.  Note: El role_id NO se incluye en el registro. El sistema asigna automáticamente el rol de \'professor\' al usuario.

## Properties

Name | Type
------------ | -------------
`username` | string
`email` | string
`name` | string
`lastname` | string
`password` | string

## Example

```typescript
import type { UserCreate } from ''

// TODO: Update the object below with actual values
const example = {
  "username": usuario,
  "email": usuario@example.com,
  "name": John,
  "lastname": null,
  "password": Password123!,
} satisfies UserCreate

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as UserCreate
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


