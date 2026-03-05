
# SyncEventSchema


## Properties

Name | Type
------------ | -------------
`syncSessionId` | number
`eventType` | string
`payload` | object
`id` | number
`timestamp` | Date
`status` | string

## Example

```typescript
import type { SyncEventSchema } from ''

// TODO: Update the object below with actual values
const example = {
  "syncSessionId": null,
  "eventType": null,
  "payload": null,
  "id": null,
  "timestamp": null,
  "status": null,
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


