
# XAPIContextInput

xAPI Context - Additional context information.

## Properties

Name | Type
------------ | -------------
`context_activities` | object
`extensions` | object
`instructor` | [XAPIActor](XAPIActor.md)
`language` | string
`platform` | string
`registration` | string
`team` | [XAPIActor](XAPIActor.md)

## Example

```typescript
import type { XAPIContextInput } from ''

// TODO: Update the object below with actual values
const example = {
  "context_activities": null,
  "extensions": null,
  "instructor": null,
  "language": null,
  "platform": null,
  "registration": null,
  "team": null,
} satisfies XAPIContextInput

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as XAPIContextInput
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


