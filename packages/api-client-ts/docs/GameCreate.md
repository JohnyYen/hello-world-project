
# GameCreate

Esquema para creación de juego

## Properties

Name | Type
------------ | -------------
`creator` | string
`description` | string
`publication_status` | string
`subject` | string
`title` | string

## Example

```typescript
import type { GameCreate } from ''

// TODO: Update the object below with actual values
const example = {
  "creator": null,
  "description": null,
  "publication_status": null,
  "subject": null,
  "title": Juego de Matemáticas,
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


