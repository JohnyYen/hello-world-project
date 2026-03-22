
# XAPIStatementCreate

xAPI Statement schema for receiving statements from game client. Supports full xAPI 1.0 specification with game-specific context.

## Properties

Name | Type
------------ | -------------
`actor` | [XAPIActor](XAPIActor.md)
`attachments` | Array&lt;object&gt;
`authority` | [XAPIActor](XAPIActor.md)
`context` | [XAPIContextInput](XAPIContextInput.md)
`id` | string
`object` | [XAPIActivity](XAPIActivity.md)
`result` | [XAPIResult](XAPIResult.md)
`stored` | Date
`timestamp` | Date
`verb` | [XAPIVerb](XAPIVerb.md)
`version` | string

## Example

```typescript
import type { XAPIStatementCreate } from ''

// TODO: Update the object below with actual values
const example = {
  "actor": null,
  "attachments": null,
  "authority": null,
  "context": null,
  "id": null,
  "object": null,
  "result": null,
  "stored": null,
  "timestamp": null,
  "verb": null,
  "version": null,
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


