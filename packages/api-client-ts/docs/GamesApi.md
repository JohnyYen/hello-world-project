# GamesApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**createGameApiV1GamesPost**](GamesApi.md#creategameapiv1gamespost) | **POST** /api/v1/games | Create Game |
| [**createGameInstanceApiV1GameInstancesGameIdInstancesPost**](GamesApi.md#creategameinstanceapiv1gameinstancesgameidinstancespost) | **POST** /api/v1/game-instances/{game_id}/instances | Create Game Instance |
| [**createGameLevelApiV1GamesGameIdLevelsPost**](GamesApi.md#creategamelevelapiv1gamesgameidlevelspost) | **POST** /api/v1/games/{game_id}/levels | Create Game Level |
| [**createLevelSegmentApiV1SegmentsLevelIdSegmentsPost**](GamesApi.md#createlevelsegmentapiv1segmentslevelidsegmentspost) | **POST** /api/v1/segments/{level_id}/segments | Create Level Segment |
| [**deleteGameApiV1GamesGameIdDelete**](GamesApi.md#deletegameapiv1gamesgameiddelete) | **DELETE** /api/v1/games/{game_id} | Delete Game |
| [**deleteLevelApiV1LevelsLevelIdDelete**](GamesApi.md#deletelevelapiv1levelsleveliddelete) | **DELETE** /api/v1/levels/{level_id} | Delete Level |
| [**deleteSegmentApiV1SegmentsSegmentIdDelete**](GamesApi.md#deletesegmentapiv1segmentssegmentiddelete) | **DELETE** /api/v1/segments/{segment_id} | Delete Segment |
| [**endInstanceApiV1GameInstancesInstanceIdEndPut**](GamesApi.md#endinstanceapiv1gameinstancesinstanceidendput) | **PUT** /api/v1/game-instances/{instance_id}/end | End Instance |
| [**getGameApiV1GamesGameIdGet**](GamesApi.md#getgameapiv1gamesgameidget) | **GET** /api/v1/games/{game_id} | Get Game |
| [**getGameLevelsApiV1GamesGameIdLevelsGet**](GamesApi.md#getgamelevelsapiv1gamesgameidlevelsget) | **GET** /api/v1/games/{game_id}/levels | Get Game Levels |
| [**getGamesApiV1GamesGet**](GamesApi.md#getgamesapiv1gamesget) | **GET** /api/v1/games | Get Games |
| [**getInstanceApiV1GameInstancesInstanceIdGet**](GamesApi.md#getinstanceapiv1gameinstancesinstanceidget) | **GET** /api/v1/game-instances/{instance_id} | Get Instance |
| [**getLevelApiV1LevelsLevelIdGet**](GamesApi.md#getlevelapiv1levelslevelidget) | **GET** /api/v1/levels/{level_id} | Get Level |
| [**getLevelSegmentsApiV1SegmentsLevelIdSegmentsGet**](GamesApi.md#getlevelsegmentsapiv1segmentslevelidsegmentsget) | **GET** /api/v1/segments/{level_id}/segments | Get Level Segments |
| [**listGameInstancesApiV1GameInstancesGameIdInstancesGet**](GamesApi.md#listgameinstancesapiv1gameinstancesgameidinstancesget) | **GET** /api/v1/game-instances/{game_id}/instances | List Game Instances |
| [**updateGameApiV1GamesGameIdPut**](GamesApi.md#updategameapiv1gamesgameidput) | **PUT** /api/v1/games/{game_id} | Update Game |
| [**updateLevelApiV1LevelsLevelIdPut**](GamesApi.md#updatelevelapiv1levelslevelidput) | **PUT** /api/v1/levels/{level_id} | Update Level |
| [**updateSegmentApiV1SegmentsSegmentIdPut**](GamesApi.md#updatesegmentapiv1segmentssegmentidput) | **PUT** /api/v1/segments/{segment_id} | Update Segment |



## createGameApiV1GamesPost

> GameCreateResponse createGameApiV1GamesPost(gameCreate)

Create Game

Crea un nuevo juego.  - **title**: Título del juego (requerido) - **description**: Descripción del juego (opcional) - **creator**: Creador del juego (opcional) - **subject**: Materia/asignatura (opcional) - **publication_status**: Estado de publicación (opcional)

### Example

```ts
import {
  Configuration,
  GamesApi,
} from '';
import type { CreateGameApiV1GamesPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: HTTPBearer
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new GamesApi(config);

  const body = {
    // GameCreate
    gameCreate: ...,
  } satisfies CreateGameApiV1GamesPostRequest;

  try {
    const data = await api.createGameApiV1GamesPost(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **gameCreate** | [GameCreate](GameCreate.md) |  | |

### Return type

[**GameCreateResponse**](GameCreateResponse.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **201** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## createGameInstanceApiV1GameInstancesGameIdInstancesPost

> GameInstanceCreateResponse createGameInstanceApiV1GameInstancesGameIdInstancesPost(gameId, gameInstanceCreate)

Create Game Instance

Crea una nueva instancia de juego para un estudiante.  - **game_id**: ID del juego - **student_id**: ID del estudiante (requerido) - **status**: Estado inicial (default: active)

### Example

```ts
import {
  Configuration,
  GamesApi,
} from '';
import type { CreateGameInstanceApiV1GameInstancesGameIdInstancesPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: HTTPBearer
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new GamesApi(config);

  const body = {
    // number
    gameId: 56,
    // GameInstanceCreate
    gameInstanceCreate: ...,
  } satisfies CreateGameInstanceApiV1GameInstancesGameIdInstancesPostRequest;

  try {
    const data = await api.createGameInstanceApiV1GameInstancesGameIdInstancesPost(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **gameId** | `number` |  | [Defaults to `undefined`] |
| **gameInstanceCreate** | [GameInstanceCreate](GameInstanceCreate.md) |  | |

### Return type

[**GameInstanceCreateResponse**](GameInstanceCreateResponse.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **201** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## createGameLevelApiV1GamesGameIdLevelsPost

> LevelCreateResponse createGameLevelApiV1GamesGameIdLevelsPost(gameId, levelCreate)

Create Game Level

Crea un nuevo nivel en un juego.  - **game_id**: ID del juego - **level_number**: Número del nivel (requerido) - **title**: Título del nivel (requerido) - **description**: Descripción del nivel (opcional) - **goal**: Objetivo del nivel (opcional)

### Example

```ts
import {
  Configuration,
  GamesApi,
} from '';
import type { CreateGameLevelApiV1GamesGameIdLevelsPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: HTTPBearer
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new GamesApi(config);

  const body = {
    // number
    gameId: 56,
    // LevelCreate
    levelCreate: ...,
  } satisfies CreateGameLevelApiV1GamesGameIdLevelsPostRequest;

  try {
    const data = await api.createGameLevelApiV1GamesGameIdLevelsPost(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **gameId** | `number` |  | [Defaults to `undefined`] |
| **levelCreate** | [LevelCreate](LevelCreate.md) |  | |

### Return type

[**LevelCreateResponse**](LevelCreateResponse.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **201** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## createLevelSegmentApiV1SegmentsLevelIdSegmentsPost

> SegmentLevelCreateResponse createLevelSegmentApiV1SegmentsLevelIdSegmentsPost(levelId, segmentLevelCreate)

Create Level Segment

Crea un nuevo segmento en un nivel.  - **level_id**: ID del nivel - **configuration**: Configuración JSON del segmento (opcional)

### Example

```ts
import {
  Configuration,
  GamesApi,
} from '';
import type { CreateLevelSegmentApiV1SegmentsLevelIdSegmentsPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: HTTPBearer
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new GamesApi(config);

  const body = {
    // number
    levelId: 56,
    // SegmentLevelCreate
    segmentLevelCreate: ...,
  } satisfies CreateLevelSegmentApiV1SegmentsLevelIdSegmentsPostRequest;

  try {
    const data = await api.createLevelSegmentApiV1SegmentsLevelIdSegmentsPost(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **levelId** | `number` |  | [Defaults to `undefined`] |
| **segmentLevelCreate** | [SegmentLevelCreate](SegmentLevelCreate.md) |  | |

### Return type

[**SegmentLevelCreateResponse**](SegmentLevelCreateResponse.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **201** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## deleteGameApiV1GamesGameIdDelete

> GameDeleteResponse deleteGameApiV1GamesGameIdDelete(gameId)

Delete Game

Elimina un juego (soft delete).  - **game_id**: ID del juego a eliminar

### Example

```ts
import {
  Configuration,
  GamesApi,
} from '';
import type { DeleteGameApiV1GamesGameIdDeleteRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: HTTPBearer
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new GamesApi(config);

  const body = {
    // number
    gameId: 56,
  } satisfies DeleteGameApiV1GamesGameIdDeleteRequest;

  try {
    const data = await api.deleteGameApiV1GamesGameIdDelete(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **gameId** | `number` |  | [Defaults to `undefined`] |

### Return type

[**GameDeleteResponse**](GameDeleteResponse.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## deleteLevelApiV1LevelsLevelIdDelete

> LevelDeleteResponse deleteLevelApiV1LevelsLevelIdDelete(levelId)

Delete Level

Elimina un nivel (soft delete).  - **level_id**: ID del nivel a eliminar

### Example

```ts
import {
  Configuration,
  GamesApi,
} from '';
import type { DeleteLevelApiV1LevelsLevelIdDeleteRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: HTTPBearer
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new GamesApi(config);

  const body = {
    // number
    levelId: 56,
  } satisfies DeleteLevelApiV1LevelsLevelIdDeleteRequest;

  try {
    const data = await api.deleteLevelApiV1LevelsLevelIdDelete(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **levelId** | `number` |  | [Defaults to `undefined`] |

### Return type

[**LevelDeleteResponse**](LevelDeleteResponse.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## deleteSegmentApiV1SegmentsSegmentIdDelete

> SegmentLevelDeleteResponse deleteSegmentApiV1SegmentsSegmentIdDelete(segmentId)

Delete Segment

Elimina un segmento (soft delete).  - **segment_id**: ID del segmento a eliminar

### Example

```ts
import {
  Configuration,
  GamesApi,
} from '';
import type { DeleteSegmentApiV1SegmentsSegmentIdDeleteRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: HTTPBearer
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new GamesApi(config);

  const body = {
    // number
    segmentId: 56,
  } satisfies DeleteSegmentApiV1SegmentsSegmentIdDeleteRequest;

  try {
    const data = await api.deleteSegmentApiV1SegmentsSegmentIdDelete(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **segmentId** | `number` |  | [Defaults to `undefined`] |

### Return type

[**SegmentLevelDeleteResponse**](SegmentLevelDeleteResponse.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## endInstanceApiV1GameInstancesInstanceIdEndPut

> GameInstanceEndResponse endInstanceApiV1GameInstancesInstanceIdEndPut(instanceId, gameInstanceEnd)

End Instance

Finaliza una instancia de juego.  - **instance_id**: ID de la instancia a finalizar - **status**: Estado final (default: completed)

### Example

```ts
import {
  Configuration,
  GamesApi,
} from '';
import type { EndInstanceApiV1GameInstancesInstanceIdEndPutRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: HTTPBearer
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new GamesApi(config);

  const body = {
    // number
    instanceId: 56,
    // GameInstanceEnd (optional)
    gameInstanceEnd: ...,
  } satisfies EndInstanceApiV1GameInstancesInstanceIdEndPutRequest;

  try {
    const data = await api.endInstanceApiV1GameInstancesInstanceIdEndPut(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **instanceId** | `number` |  | [Defaults to `undefined`] |
| **gameInstanceEnd** | [GameInstanceEnd](GameInstanceEnd.md) |  | [Optional] |

### Return type

[**GameInstanceEndResponse**](GameInstanceEndResponse.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## getGameApiV1GamesGameIdGet

> SingleGameResponse getGameApiV1GamesGameIdGet(gameId)

Get Game

Obtiene los detalles de un juego específico.  - **game_id**: ID del juego a obtener

### Example

```ts
import {
  Configuration,
  GamesApi,
} from '';
import type { GetGameApiV1GamesGameIdGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: HTTPBearer
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new GamesApi(config);

  const body = {
    // number
    gameId: 56,
  } satisfies GetGameApiV1GamesGameIdGetRequest;

  try {
    const data = await api.getGameApiV1GamesGameIdGet(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **gameId** | `number` |  | [Defaults to `undefined`] |

### Return type

[**SingleGameResponse**](SingleGameResponse.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## getGameLevelsApiV1GamesGameIdLevelsGet

> LevelListResponse getGameLevelsApiV1GamesGameIdLevelsGet(gameId, skip, limit)

Get Game Levels

Lista los niveles de un juego con paginación.  - **game_id**: ID del juego - **skip**: Número de registros a saltar - **limit**: Número máximo de registros a devolver

### Example

```ts
import {
  Configuration,
  GamesApi,
} from '';
import type { GetGameLevelsApiV1GamesGameIdLevelsGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: HTTPBearer
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new GamesApi(config);

  const body = {
    // number
    gameId: 56,
    // number | Número de registros a saltar (optional)
    skip: 56,
    // number | Número de registros a devolver (optional)
    limit: 56,
  } satisfies GetGameLevelsApiV1GamesGameIdLevelsGetRequest;

  try {
    const data = await api.getGameLevelsApiV1GamesGameIdLevelsGet(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **gameId** | `number` |  | [Defaults to `undefined`] |
| **skip** | `number` | Número de registros a saltar | [Optional] [Defaults to `0`] |
| **limit** | `number` | Número de registros a devolver | [Optional] [Defaults to `10`] |

### Return type

[**LevelListResponse**](LevelListResponse.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## getGamesApiV1GamesGet

> GameListResponse getGamesApiV1GamesGet(skip, limit)

Get Games

Lista todos los juegos con paginación.  - **skip**: Número de registros a saltar (para paginación) - **limit**: Número máximo de registros a devolver (1-100)

### Example

```ts
import {
  Configuration,
  GamesApi,
} from '';
import type { GetGamesApiV1GamesGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: HTTPBearer
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new GamesApi(config);

  const body = {
    // number | Número de registros a saltar (optional)
    skip: 56,
    // number | Número de registros a devolver (optional)
    limit: 56,
  } satisfies GetGamesApiV1GamesGetRequest;

  try {
    const data = await api.getGamesApiV1GamesGet(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **skip** | `number` | Número de registros a saltar | [Optional] [Defaults to `0`] |
| **limit** | `number` | Número de registros a devolver | [Optional] [Defaults to `10`] |

### Return type

[**GameListResponse**](GameListResponse.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## getInstanceApiV1GameInstancesInstanceIdGet

> SingleGameInstanceResponse getInstanceApiV1GameInstancesInstanceIdGet(instanceId)

Get Instance

Obtiene los detalles de una instancia de juego.  - **instance_id**: ID de la instancia

### Example

```ts
import {
  Configuration,
  GamesApi,
} from '';
import type { GetInstanceApiV1GameInstancesInstanceIdGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: HTTPBearer
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new GamesApi(config);

  const body = {
    // number
    instanceId: 56,
  } satisfies GetInstanceApiV1GameInstancesInstanceIdGetRequest;

  try {
    const data = await api.getInstanceApiV1GameInstancesInstanceIdGet(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **instanceId** | `number` |  | [Defaults to `undefined`] |

### Return type

[**SingleGameInstanceResponse**](SingleGameInstanceResponse.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## getLevelApiV1LevelsLevelIdGet

> SingleLevelResponse getLevelApiV1LevelsLevelIdGet(levelId)

Get Level

Obtiene los detalles de un nivel específico.  - **level_id**: ID del nivel a obtener

### Example

```ts
import {
  Configuration,
  GamesApi,
} from '';
import type { GetLevelApiV1LevelsLevelIdGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: HTTPBearer
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new GamesApi(config);

  const body = {
    // number
    levelId: 56,
  } satisfies GetLevelApiV1LevelsLevelIdGetRequest;

  try {
    const data = await api.getLevelApiV1LevelsLevelIdGet(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **levelId** | `number` |  | [Defaults to `undefined`] |

### Return type

[**SingleLevelResponse**](SingleLevelResponse.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## getLevelSegmentsApiV1SegmentsLevelIdSegmentsGet

> SegmentLevelListResponse getLevelSegmentsApiV1SegmentsLevelIdSegmentsGet(levelId, skip, limit)

Get Level Segments

Lista los segmentos de un nivel con paginación.  - **level_id**: ID del nivel - **skip**: Número de registros a saltar - **limit**: Número máximo de registros a devolver

### Example

```ts
import {
  Configuration,
  GamesApi,
} from '';
import type { GetLevelSegmentsApiV1SegmentsLevelIdSegmentsGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: HTTPBearer
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new GamesApi(config);

  const body = {
    // number
    levelId: 56,
    // number | Número de registros a saltar (optional)
    skip: 56,
    // number | Número de registros a devolver (optional)
    limit: 56,
  } satisfies GetLevelSegmentsApiV1SegmentsLevelIdSegmentsGetRequest;

  try {
    const data = await api.getLevelSegmentsApiV1SegmentsLevelIdSegmentsGet(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **levelId** | `number` |  | [Defaults to `undefined`] |
| **skip** | `number` | Número de registros a saltar | [Optional] [Defaults to `0`] |
| **limit** | `number` | Número de registros a devolver | [Optional] [Defaults to `10`] |

### Return type

[**SegmentLevelListResponse**](SegmentLevelListResponse.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## listGameInstancesApiV1GameInstancesGameIdInstancesGet

> GameInstanceListResponse listGameInstancesApiV1GameInstancesGameIdInstancesGet(gameId, skip, limit, statusFilter)

List Game Instances

Lista las instancias de un juego con paginación.  - **game_id**: ID del juego - **skip**: Número de registros a saltar - **limit**: Número máximo de registros a devolver - **status_filter**: Filtrar por estado (opcional)

### Example

```ts
import {
  Configuration,
  GamesApi,
} from '';
import type { ListGameInstancesApiV1GameInstancesGameIdInstancesGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: HTTPBearer
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new GamesApi(config);

  const body = {
    // number
    gameId: 56,
    // number | Número de registros a saltar (optional)
    skip: 56,
    // number | Número de registros a devolver (optional)
    limit: 56,
    // string | Filtrar por estado (active, completed, abandoned) (optional)
    statusFilter: statusFilter_example,
  } satisfies ListGameInstancesApiV1GameInstancesGameIdInstancesGetRequest;

  try {
    const data = await api.listGameInstancesApiV1GameInstancesGameIdInstancesGet(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **gameId** | `number` |  | [Defaults to `undefined`] |
| **skip** | `number` | Número de registros a saltar | [Optional] [Defaults to `0`] |
| **limit** | `number` | Número de registros a devolver | [Optional] [Defaults to `10`] |
| **statusFilter** | `string` | Filtrar por estado (active, completed, abandoned) | [Optional] [Defaults to `undefined`] |

### Return type

[**GameInstanceListResponse**](GameInstanceListResponse.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## updateGameApiV1GamesGameIdPut

> GameUpdateResponse updateGameApiV1GamesGameIdPut(gameId, gameUpdate)

Update Game

Actualiza un juego existente.  - **game_id**: ID del juego a actualizar - **title**: Nuevo título (opcional) - **description**: Nueva descripción (opcional) - **creator**: Nuevo creador (opcional) - **subject**: Nueva materia (opcional) - **publication_status**: Nuevo estado (opcional)

### Example

```ts
import {
  Configuration,
  GamesApi,
} from '';
import type { UpdateGameApiV1GamesGameIdPutRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: HTTPBearer
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new GamesApi(config);

  const body = {
    // number
    gameId: 56,
    // GameUpdate
    gameUpdate: ...,
  } satisfies UpdateGameApiV1GamesGameIdPutRequest;

  try {
    const data = await api.updateGameApiV1GamesGameIdPut(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **gameId** | `number` |  | [Defaults to `undefined`] |
| **gameUpdate** | [GameUpdate](GameUpdate.md) |  | |

### Return type

[**GameUpdateResponse**](GameUpdateResponse.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## updateLevelApiV1LevelsLevelIdPut

> LevelUpdateResponse updateLevelApiV1LevelsLevelIdPut(levelId, levelUpdate)

Update Level

Actualiza un nivel existente.  - **level_id**: ID del nivel a actualizar - **level_number**: Nuevo número de nivel (opcional) - **title**: Nuevo título (opcional) - **description**: Nueva descripción (opcional) - **goal**: Nuevo objetivo (opcional)

### Example

```ts
import {
  Configuration,
  GamesApi,
} from '';
import type { UpdateLevelApiV1LevelsLevelIdPutRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: HTTPBearer
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new GamesApi(config);

  const body = {
    // number
    levelId: 56,
    // LevelUpdate
    levelUpdate: ...,
  } satisfies UpdateLevelApiV1LevelsLevelIdPutRequest;

  try {
    const data = await api.updateLevelApiV1LevelsLevelIdPut(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **levelId** | `number` |  | [Defaults to `undefined`] |
| **levelUpdate** | [LevelUpdate](LevelUpdate.md) |  | |

### Return type

[**LevelUpdateResponse**](LevelUpdateResponse.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## updateSegmentApiV1SegmentsSegmentIdPut

> SegmentLevelUpdateResponse updateSegmentApiV1SegmentsSegmentIdPut(segmentId, segmentLevelUpdate)

Update Segment

Actualiza un segmento existente.  - **segment_id**: ID del segmento a actualizar - **configuration**: Nueva configuración JSON (opcional)

### Example

```ts
import {
  Configuration,
  GamesApi,
} from '';
import type { UpdateSegmentApiV1SegmentsSegmentIdPutRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: HTTPBearer
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new GamesApi(config);

  const body = {
    // number
    segmentId: 56,
    // SegmentLevelUpdate
    segmentLevelUpdate: ...,
  } satisfies UpdateSegmentApiV1SegmentsSegmentIdPutRequest;

  try {
    const data = await api.updateSegmentApiV1SegmentsSegmentIdPut(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **segmentId** | `number` |  | [Defaults to `undefined`] |
| **segmentLevelUpdate** | [SegmentLevelUpdate](SegmentLevelUpdate.md) |  | |

### Return type

[**SegmentLevelUpdateResponse**](SegmentLevelUpdateResponse.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

