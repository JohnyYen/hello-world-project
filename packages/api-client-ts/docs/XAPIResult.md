
# XAPIResult

xAPI Result - The result of the action (quantitative and qualitative).

## Properties

Name | Type
------------ | -------------
`score` | [XAPIScore](XAPIScore.md)
`success` | boolean
`completion` | boolean
`response` | string
`duration` | string
`extensions` | object

## Example

```typescript
import type { XAPIResult } from ''

// TODO: Update the object below with actual values
const example = {
  "score": null,
  "success": null,
  "completion": null,
  "response": null,
  "duration": null,
  "extensions": null,
} satisfies XAPIResult

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as XAPIResult
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


