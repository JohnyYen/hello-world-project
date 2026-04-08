
# XAPIResult

xAPI Result - The result of the action (quantitative and qualitative).

## Properties

Name | Type
------------ | -------------
`completion` | boolean
`duration` | string
`extensions` | object
`response` | string
`score` | [XAPIScore](XAPIScore.md)
`success` | boolean

## Example

```typescript
import type { XAPIResult } from ''

// TODO: Update the object below with actual values
const example = {
  "completion": null,
  "duration": null,
  "extensions": null,
  "response": null,
  "score": null,
  "success": null,
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


