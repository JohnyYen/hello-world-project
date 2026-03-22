
# XAPIStatementListResponse

List of xAPI statements with pagination.

## Properties

Name | Type
------------ | -------------
`limit` | number
`skip` | number
`statements` | [Array&lt;XAPIStatementResponse&gt;](XAPIStatementResponse.md)
`total` | number

## Example

```typescript
import type { XAPIStatementListResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "limit": null,
  "skip": null,
  "statements": null,
  "total": null,
} satisfies XAPIStatementListResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as XAPIStatementListResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


