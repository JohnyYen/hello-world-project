
# SyncResultResponse

Response schema for LMS sync operation.

## Properties

Name | Type
------------ | -------------
`status` | string
`message` | string
`recordsSynced` | { [key: string]: number; }
`syncTime` | Date
`nextSyncScheduled` | Date

## Example

```typescript
import type { SyncResultResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "status": null,
  "message": null,
  "recordsSynced": null,
  "syncTime": null,
  "nextSyncScheduled": null,
} satisfies SyncResultResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as SyncResultResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


