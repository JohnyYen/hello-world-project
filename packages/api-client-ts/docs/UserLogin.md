
# UserLogin

Esquema para inicio de sesión

## Properties

Name | Type
------------ | -------------
`username` | string
`email` | string
`password` | string

## Example

```typescript
import type { UserLogin } from ''

// TODO: Update the object below with actual values
const example = {
  "username": null,
  "email": null,
  "password": Password123!,
} satisfies UserLogin

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as UserLogin
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


