
# XAPIActivityDefinition

xAPI Activity definition with type, name, description.

## Properties

Name | Type
------------ | -------------
`description` | { [key: string]: string; }
`extensions` | object
`name` | { [key: string]: string; }
`type` | string

## Example

```typescript
import type { XAPIActivityDefinition } from ''

// TODO: Update the object below with actual values
const example = {
  "description": null,
  "extensions": null,
  "name": null,
  "type": null,
} satisfies XAPIActivityDefinition

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as XAPIActivityDefinition
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


