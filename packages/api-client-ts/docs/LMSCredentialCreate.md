
# LMSCredentialCreate

Schema for creating LMS credentials.

## Properties

Name | Type
------------ | -------------
`lms_email` | string
`lms_password` | string
`lms_provider` | string
`lms_url` | string
`user_id` | number

## Example

```typescript
import type { LMSCredentialCreate } from ''

// TODO: Update the object below with actual values
const example = {
  "lms_email": null,
  "lms_password": null,
  "lms_provider": null,
  "lms_url": null,
  "user_id": null,
} satisfies LMSCredentialCreate

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as LMSCredentialCreate
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


