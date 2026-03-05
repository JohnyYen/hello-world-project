
# LMSCredentialCreate

Schema for creating LMS credentials.

## Properties

Name | Type
------------ | -------------
`userId` | number
`lmsUrl` | string
`lmsEmail` | string
`lmsPassword` | string
`lmsProvider` | string

## Example

```typescript
import type { LMSCredentialCreate } from ''

// TODO: Update the object below with actual values
const example = {
  "userId": null,
  "lmsUrl": null,
  "lmsEmail": null,
  "lmsPassword": null,
  "lmsProvider": null,
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


