
# SyncSessionSchema


## Properties

Name | Type
------------ | -------------
`end_time` | Date
`id` | number
`instance_id` | number
`is_active` | boolean
`start_time` | Date

## Example

```typescript
import type { SyncSessionSchema } from ''

// TODO: Update the object below with actual values
const example = {
  "end_time": null,
  "id": null,
  "instance_id": null,
  "is_active": null,
  "start_time": null,
} satisfies SyncSessionSchema

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as SyncSessionSchema
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


