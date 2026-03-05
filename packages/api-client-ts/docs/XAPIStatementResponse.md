
# XAPIStatementResponse

xAPI Statement response after storage.

## Properties

Name | Type
------------ | -------------
`id` | string
`actor` | [XAPIActor](XAPIActor.md)
`verb` | [XAPIVerb](XAPIVerb.md)
`object` | [XAPIActivity](XAPIActivity.md)
`result` | [XAPIResult](XAPIResult.md)
`context` | [XAPIContextOutput](XAPIContextOutput.md)
`timestamp` | Date
`stored` | Date

## Example

```typescript
import type { XAPIStatementResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "id": null,
  "actor": null,
  "verb": null,
  "object": null,
  "result": null,
  "context": null,
  "timestamp": null,
  "stored": null,
} satisfies XAPIStatementResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as XAPIStatementResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


