
# XAPIActivity

xAPI Activity - The object of the action.

## Properties

Name | Type
------------ | -------------
`id` | string
`objectType` | string
`definition` | [XAPIActivityDefinition](XAPIActivityDefinition.md)

## Example

```typescript
import type { XAPIActivity } from ''

// TODO: Update the object below with actual values
const example = {
  "id": null,
  "objectType": null,
  "definition": null,
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


