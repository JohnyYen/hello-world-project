
# UserLoginResponse

Respuesta de autenticación exitosa

## Properties

Name | Type
------------ | -------------
`access_token` | string
`expires_in` | number
`token_type` | string
`user` | [UserResponse](UserResponse.md)

## Example

```typescript
import type { UserLoginResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "access_token": null,
  "expires_in": null,
  "token_type": null,
  "user": null,
} satisfies UserLoginResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as UserLoginResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


