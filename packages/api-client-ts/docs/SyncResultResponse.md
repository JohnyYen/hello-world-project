
# SyncResultResponse

Response schema for LMS sync operation.

## Properties

Name | Type
------------ | -------------
`message` | string
`next_sync_scheduled` | Date
`records_synced` | { [key: string]: number; }
`status` | string
`sync_time` | Date

## Example

```typescript
import type { SyncResultResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "message": null,
  "next_sync_scheduled": null,
  "records_synced": null,
  "status": null,
  "sync_time": null,
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


