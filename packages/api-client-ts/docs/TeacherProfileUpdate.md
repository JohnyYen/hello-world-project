
# TeacherProfileUpdate

Esquema para actualización del perfil de profesor

## Properties

Name | Type
------------ | -------------
`name` | string
`lastname` | string
`email` | string
`department` | string
`contactPhone` | string
`avatarUrl` | string

## Example

```typescript
import type { TeacherProfileUpdate } from ''

// TODO: Update the object below with actual values
const example = {
  "name": null,
  "lastname": null,
  "email": null,
  "department": null,
  "contactPhone": null,
  "avatarUrl": null,
} satisfies TeacherProfileUpdate

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as TeacherProfileUpdate
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


