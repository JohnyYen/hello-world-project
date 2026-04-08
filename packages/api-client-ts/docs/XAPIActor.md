
# XAPIActor

xAPI Actor - Who performed the action.

## Properties

Name | Type
------------ | -------------
`account` | { [key: string]: string; }
`mbox` | string
`mbox_sha1sum` | string
`name` | string
`object_type` | [XAPIActorType](XAPIActorType.md)

## Example

```typescript
import type { XAPIActor } from ''

// TODO: Update the object below with actual values
const example = {
  "account": null,
  "mbox": null,
  "mbox_sha1sum": null,
  "name": null,
  "object_type": null,
} satisfies XAPIActor

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as XAPIActor
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


