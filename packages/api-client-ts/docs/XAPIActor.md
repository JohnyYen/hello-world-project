
# XAPIActor

xAPI Actor - Who performed the action.

## Properties

Name | Type
------------ | -------------
`mbox` | string
`mboxSha1sum` | string
`account` | { [key: string]: string; }
`name` | string
`objectType` | [XAPIActorType](XAPIActorType.md)

## Example

```typescript
import type { XAPIActor } from ''

// TODO: Update the object below with actual values
const example = {
  "mbox": null,
  "mboxSha1sum": null,
  "account": null,
  "name": null,
  "objectType": null,
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


