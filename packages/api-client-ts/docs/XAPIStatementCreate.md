
# XAPIStatementCreate

xAPI Statement schema for receiving statements from game client. Supports full xAPI 1.0 specification with game-specific context.

## Properties

Name | Type
------------ | -------------
`id` | string
`actor` | [XAPIActor](XAPIActor.md)
`verb` | [XAPIVerb](XAPIVerb.md)
`object` | [XAPIActivity](XAPIActivity.md)
`result` | [XAPIResult](XAPIResult.md)
`context` | [XAPIContextInput](XAPIContextInput.md)
`timestamp` | Date
`stored` | Date
`authority` | [XAPIActor](XAPIActor.md)
`version` | string
`attachments` | Array&lt;object&gt;

## Example

```typescript
import type { XAPIStatementCreate } from ''

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
  "authority": null,
  "version": null,
  "attachments": null,
} satisfies XAPIStatementCreate

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as XAPIStatementCreate
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


