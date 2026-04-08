
# UserResponse

Esquema para respuesta de usuario

## Properties

Name | Type
------------ | -------------
`created_at` | Date
`email` | string
`id` | number
`is_active` | boolean
`lastname` | string
`name` | string
`role` | [UserRoleResponse](UserRoleResponse.md)
`updated_at` | Date
`username` | string

## Example

```typescript
import type { UserResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "created_at": null,
  "email": usuario@example.com,
  "id": null,
  "is_active": null,
  "lastname": null,
  "name": null,
  "role": null,
  "updated_at": null,
  "username": usuario,
} satisfies UserResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as UserResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


