
# UserChangePassword

Esquema para cambio de contraseña

## Properties

Name | Type
------------ | -------------
`current_password` | string
`new_password` | string

## Example

```typescript
import type { UserChangePassword } from ''

// TODO: Update the object below with actual values
const example = {
  "current_password": Current123!,
  "new_password": NewPassword123!,
} satisfies UserChangePassword

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as UserChangePassword
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


