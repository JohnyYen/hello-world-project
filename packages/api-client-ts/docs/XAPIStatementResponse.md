
# XAPIStatementResponse

xAPI Statement response after storage.

## Properties

Name | Type
------------ | -------------
`actor` | [XAPIActor](XAPIActor.md)
`context` | [XAPIContextOutput](XAPIContextOutput.md)
`id` | string
`object` | [XAPIActivity](XAPIActivity.md)
`result` | [XAPIResult](XAPIResult.md)
`stored` | Date
`timestamp` | Date
`verb` | [XAPIVerb](XAPIVerb.md)

## Example

```typescript
import type { XAPIStatementResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "actor": null,
  "context": null,
  "id": null,
  "object": null,
  "result": null,
  "stored": null,
  "timestamp": null,
  "verb": null,
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


