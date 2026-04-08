
# SyncEventCreate


## Properties

Name | Type
------------ | -------------
`event_type` | string
`payload` | object
`sync_session_id` | number

## Example

```typescript
import type { SyncEventCreate } from ''

// TODO: Update the object below with actual values
const example = {
  "event_type": null,
  "payload": null,
  "sync_session_id": null,
} satisfies SyncEventCreate

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as SyncEventCreate
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


