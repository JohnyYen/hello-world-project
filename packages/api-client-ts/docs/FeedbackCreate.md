
# FeedbackCreate


## Properties

Name | Type
------------ | -------------
`comments` | string
`rating` | number
`student_id` | number

## Example

```typescript
import type { FeedbackCreate } from ''

// TODO: Update the object below with actual values
const example = {
  "comments": null,
  "rating": null,
  "student_id": null,
} satisfies FeedbackCreate

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as FeedbackCreate
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


