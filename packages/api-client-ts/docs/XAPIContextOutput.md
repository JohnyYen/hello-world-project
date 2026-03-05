
# XAPIContextOutput

xAPI Context - Additional context information.

## Properties

Name | Type
------------ | -------------
`registration` | string
`platform` | string
`language` | string
`instructor` | [XAPIActor](XAPIActor.md)
`team` | [XAPIActor](XAPIActor.md)
`contextActivities` | object
`extensions` | object

## Example

```typescript
import type { XAPIContextOutput } from ''

// TODO: Update the object below with actual values
const example = {
  "registration": null,
  "platform": null,
  "language": null,
  "instructor": null,
  "team": null,
  "contextActivities": null,
  "extensions": null,
} satisfies XAPIContextOutput

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as XAPIContextOutput
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


