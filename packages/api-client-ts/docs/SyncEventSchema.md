
# SyncEventSchema


## Properties

Name | Type
------------ | -------------
`event_type` | string
`id` | number
`payload` | object
`status` | string
`sync_session_id` | number
`timestamp` | Date

## Example

```typescript
import type { SyncEventSchema } from ''

// TODO: Update the object below with actual values
const example = {
  "event_type": null,
  "id": null,
  "payload": null,
  "status": null,
  "sync_session_id": null,
  "timestamp": null,
} satisfies SyncEventSchema

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as SyncEventSchema
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


