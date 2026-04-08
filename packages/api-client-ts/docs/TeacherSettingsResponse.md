
# TeacherSettingsResponse

Esquema para respuesta de configuraciones de profesor

## Properties

Name | Type
------------ | -------------
`animations_enabled` | boolean
`auto_logout` | boolean
`color_theme` | string
`date_format` | string
`email_notifications` | boolean
`interface_language` | string
`notification_frequency` | string
`notifications_enabled` | boolean
`remember_login` | boolean
`session_duration_minutes` | number
`theme` | string
`timezone` | string

## Example

```typescript
import type { TeacherSettingsResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "animations_enabled": null,
  "auto_logout": null,
  "color_theme": null,
  "date_format": null,
  "email_notifications": null,
  "interface_language": null,
  "notification_frequency": null,
  "notifications_enabled": null,
  "remember_login": null,
  "session_duration_minutes": null,
  "theme": null,
  "timezone": null,
} satisfies TeacherSettingsResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as TeacherSettingsResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


