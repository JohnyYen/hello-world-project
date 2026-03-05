
# FeedbackSchema


## Properties

Name | Type
------------ | -------------
`studentId` | number
`comments` | string
`rating` | number
`id` | number
`createdAt` | Date
`updatedAt` | Date

## Example

```typescript
import type { FeedbackSchema } from ''

// TODO: Update the object below with actual values
const example = {
  "studentId": null,
  "comments": null,
  "rating": null,
  "id": null,
  "createdAt": null,
  "updatedAt": null,
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


