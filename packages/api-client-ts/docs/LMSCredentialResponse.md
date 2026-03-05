
# LMSCredentialResponse

Schema for LMS credential response (password masked).

## Properties

Name | Type
------------ | -------------
`id` | number
`userId` | number
`lmsUrl` | string
`lmsEmail` | string
`lmsProvider` | string
`accessToken` | string
`expireAt` | Date
`createdAt` | Date
`updatedAt` | Date

## Example

```typescript
import type { LMSCredentialResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "id": null,
  "userId": null,
  "lmsUrl": null,
  "lmsEmail": null,
  "lmsProvider": null,
  "accessToken": null,
  "expireAt": null,
  "createdAt": null,
  "updatedAt": null,
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


