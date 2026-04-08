
# XAPIActivity

xAPI Activity - The object of the action.

## Properties

Name | Type
------------ | -------------
`definition` | [XAPIActivityDefinition](XAPIActivityDefinition.md)
`id` | string
`object_type` | string

## Example

```typescript
import type { XAPIActivity } from ''

// TODO: Update the object below with actual values
const example = {
  "definition": null,
  "id": null,
  "object_type": null,
} satisfies XAPIActivity

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as XAPIActivity
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


