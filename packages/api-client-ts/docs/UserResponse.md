
# UserResponse

Esquema para respuesta de usuario

## Properties

Name | Type
------------ | -------------
`createdAt` | Date
`updatedAt` | Date
`username` | string
`email` | string
`id` | number
`name` | string
`lastname` | string
`isActive` | boolean
`role` | [UserRoleResponse](UserRoleResponse.md)

## Example

```typescript
import type { UserResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "createdAt": null,
  "updatedAt": null,
  "username": usuario,
  "email": usuario@example.com,
  "id": null,
  "name": null,
  "lastname": null,
  "isActive": null,
  "role": null,
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


