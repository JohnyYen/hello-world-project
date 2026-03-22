
# LMSCredentialResponse

Schema for LMS credential response (password masked).

## Properties

Name | Type
------------ | -------------
`access_token` | string
`created_at` | Date
`expire_at` | Date
`id` | number
`lms_email` | string
`lms_provider` | string
`lms_url` | string
`updated_at` | Date
`user_id` | number

## Example

```typescript
import type { LMSCredentialResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "access_token": null,
  "created_at": null,
  "expire_at": null,
  "id": null,
  "lms_email": null,
  "lms_provider": null,
  "lms_url": null,
  "updated_at": null,
  "user_id": null,
} satisfies LMSCredentialResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as LMSCredentialResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


