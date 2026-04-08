
# FeedbackSchema


## Properties

Name | Type
------------ | -------------
`comments` | string
`created_at` | Date
`id` | number
`rating` | number
`student_id` | number
`updated_at` | Date

## Example

```typescript
import type { FeedbackSchema } from ''

// TODO: Update the object below with actual values
const example = {
  "comments": null,
  "created_at": null,
  "id": null,
  "rating": null,
  "student_id": null,
  "updated_at": null,
} satisfies FeedbackSchema

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as FeedbackSchema
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


