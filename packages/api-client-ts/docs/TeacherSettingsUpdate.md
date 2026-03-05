
# TeacherSettingsUpdate

Esquema para actualización de configuraciones de profesor

## Properties

Name | Type
------------ | -------------
`theme` | string
`notificationsEnabled` | boolean
`notificationFrequency` | string
`interfaceLanguage` | string

## Example

```typescript
import type { TeacherSettingsUpdate } from ''

// TODO: Update the object below with actual values
const example = {
  "theme": null,
  "notificationsEnabled": null,
  "notificationFrequency": null,
  "interfaceLanguage": null,
} satisfies TeacherSettingsUpdate

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as TeacherSettingsUpdate
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


