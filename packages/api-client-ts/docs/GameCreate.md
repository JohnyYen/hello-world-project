
# GameCreate

Esquema para creación de juego

## Properties

Name | Type
------------ | -------------
`title` | string
`description` | string
`creator` | string
`subject` | string
`publicationStatus` | string

## Example

```typescript
import type { GameCreate } from ''

// TODO: Update the object below with actual values
const example = {
  "title": Juego de Matemáticas,
  "description": null,
  "creator": null,
  "subject": null,
  "publicationStatus": null,
} satisfies GameCreate

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as GameCreate
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


