
# TeacherProfileResponse

Esquema para respuesta del perfil de profesor

## Properties

Name | Type
------------ | -------------
`avatar_url` | string
`contact_phone` | string
`created_at` | Date
`department` | string
`email` | string
`id` | number
`is_active` | boolean
`lastname` | string
`name` | string
`updated_at` | Date
`username` | string

## Example

```typescript
import type { TeacherProfileResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "avatar_url": null,
  "contact_phone": null,
  "created_at": null,
  "department": null,
  "email": null,
  "id": null,
  "is_active": null,
  "lastname": null,
  "name": null,
  "updated_at": null,
  "username": null,
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


