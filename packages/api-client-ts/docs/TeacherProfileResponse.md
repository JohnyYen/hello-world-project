
# TeacherProfileResponse

Esquema para respuesta del perfil de profesor

## Properties

Name | Type
------------ | -------------
`id` | number
`username` | string
`name` | string
`lastname` | string
`email` | string
`department` | string
`contactPhone` | string
`avatarUrl` | string
`isActive` | boolean
`createdAt` | Date
`updatedAt` | Date

## Example

```typescript
import type { TeacherProfileResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "id": null,
  "username": null,
  "name": null,
  "lastname": null,
  "email": null,
  "department": null,
  "contactPhone": null,
  "avatarUrl": null,
  "isActive": null,
  "createdAt": null,
  "updatedAt": null,
} satisfies TeacherProfileResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as TeacherProfileResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


