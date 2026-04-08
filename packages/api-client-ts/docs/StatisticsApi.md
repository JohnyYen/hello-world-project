# StatisticsApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**createMetricTypeApiV1StatisticMetricTypesPost**](StatisticsApi.md#createmetrictypeapiv1statisticmetrictypespost) | **POST** /api/v1/statistic/metric-types | Create Metric Type |
| [**deleteMetricTypeApiV1StatisticMetricTypesMetricTypeIdDelete**](StatisticsApi.md#deletemetrictypeapiv1statisticmetrictypesmetrictypeiddelete) | **DELETE** /api/v1/statistic/metric-types/{metric_type_id} | Delete Metric Type |
| [**getMetricTypeApiV1StatisticMetricTypesMetricTypeIdGet**](StatisticsApi.md#getmetrictypeapiv1statisticmetrictypesmetrictypeidget) | **GET** /api/v1/statistic/metric-types/{metric_type_id} | Get Metric Type |
| [**getStatementApiV1StatisticXapiStatementsStatementIdGet**](StatisticsApi.md#getstatementapiv1statisticxapistatementsstatementidget) | **GET** /api/v1/statistic/xapi/statements/{statement_id} | Get Statement |
| [**getStatementsApiV1StatisticXapiStatementsGet**](StatisticsApi.md#getstatementsapiv1statisticxapistatementsget) | **GET** /api/v1/statistic/xapi/statements | Get Statements |
| [**getStudentFeedbackHistoryApiV1StatisticFeedbackStudentIdGet**](StatisticsApi.md#getstudentfeedbackhistoryapiv1statisticfeedbackstudentidget) | **GET** /api/v1/statistic/feedback/{student_id} | Get Student Feedback History |
| [**listMetricTypesApiV1StatisticMetricTypesGet**](StatisticsApi.md#listmetrictypesapiv1statisticmetrictypesget) | **GET** /api/v1/statistic/metric-types | List Metric Types |
| [**sendStatementsApiV1StatisticXapiStatementsPost**](StatisticsApi.md#sendstatementsapiv1statisticxapistatementspost) | **POST** /api/v1/statistic/xapi/statements | Send Statements |
| [**submitFeedbackApiV1StatisticFeedbackPost**](StatisticsApi.md#submitfeedbackapiv1statisticfeedbackpost) | **POST** /api/v1/statistic/feedback | Submit Feedback |
| [**updateMetricTypeApiV1StatisticMetricTypesMetricTypeIdPatch**](StatisticsApi.md#updatemetrictypeapiv1statisticmetrictypesmetrictypeidpatch) | **PATCH** /api/v1/statistic/metric-types/{metric_type_id} | Update Metric Type |



## createMetricTypeApiV1StatisticMetricTypesPost

> MetricTypeSchema createMetricTypeApiV1StatisticMetricTypesPost(metricTypeCreate)

Create Metric Type

Crea un nuevo tipo de métrica.

### Example

```ts
import {
  Configuration,
  StatisticsApi,
} from '';
import type { CreateMetricTypeApiV1StatisticMetricTypesPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: HTTPBearer
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new StatisticsApi(config);

  const body = {
    // MetricTypeCreate
    metricTypeCreate: ...,
  } satisfies CreateMetricTypeApiV1StatisticMetricTypesPostRequest;

  try {
    const data = await api.createMetricTypeApiV1StatisticMetricTypesPost(body);
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
| **metricTypeCreate** | [MetricTypeCreate](MetricTypeCreate.md) |  | |

### Return type

[**MetricTypeSchema**](MetricTypeSchema.md)

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


## deleteMetricTypeApiV1StatisticMetricTypesMetricTypeIdDelete

> deleteMetricTypeApiV1StatisticMetricTypesMetricTypeIdDelete(metricTypeId)

Delete Metric Type

Elimina un tipo de métrica (soft delete).

### Example

```ts
import {
  Configuration,
  StatisticsApi,
} from '';
import type { DeleteMetricTypeApiV1StatisticMetricTypesMetricTypeIdDeleteRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: HTTPBearer
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new StatisticsApi(config);

  const body = {
    // number
    metricTypeId: 56,
  } satisfies DeleteMetricTypeApiV1StatisticMetricTypesMetricTypeIdDeleteRequest;

  try {
    const data = await api.deleteMetricTypeApiV1StatisticMetricTypesMetricTypeIdDelete(body);
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
| **metricTypeId** | `number` |  | [Defaults to `undefined`] |

### Return type

`void` (Empty response body)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **204** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## getMetricTypeApiV1StatisticMetricTypesMetricTypeIdGet

> MetricTypeSchema getMetricTypeApiV1StatisticMetricTypesMetricTypeIdGet(metricTypeId)

Get Metric Type

Obtiene un tipo de métrica por su ID.

### Example

```ts
import {
  Configuration,
  StatisticsApi,
} from '';
import type { GetMetricTypeApiV1StatisticMetricTypesMetricTypeIdGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: HTTPBearer
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new StatisticsApi(config);

  const body = {
    // number
    metricTypeId: 56,
  } satisfies GetMetricTypeApiV1StatisticMetricTypesMetricTypeIdGetRequest;

  try {
    const data = await api.getMetricTypeApiV1StatisticMetricTypesMetricTypeIdGet(body);
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
| **metricTypeId** | `number` |  | [Defaults to `undefined`] |

### Return type

[**MetricTypeSchema**](MetricTypeSchema.md)

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


## getStatementApiV1StatisticXapiStatementsStatementIdGet

> XAPIStatementResponse getStatementApiV1StatisticXapiStatementsStatementIdGet(statementId)

Get Statement

Get a specific xAPI statement by ID.

### Example

```ts
import {
  Configuration,
  StatisticsApi,
} from '';
import type { GetStatementApiV1StatisticXapiStatementsStatementIdGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // To configure OAuth2 access token for authorization: OAuth2PasswordBearer password
    accessToken: "YOUR ACCESS TOKEN",
    // Configure HTTP bearer authorization: HTTPBearer
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new StatisticsApi(config);

  const body = {
    // string
    statementId: statementId_example,
  } satisfies GetStatementApiV1StatisticXapiStatementsStatementIdGetRequest;

  try {
    const data = await api.getStatementApiV1StatisticXapiStatementsStatementIdGet(body);
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
| **statementId** | `string` |  | [Defaults to `undefined`] |

### Return type

[**XAPIStatementResponse**](XAPIStatementResponse.md)

### Authorization

[OAuth2PasswordBearer password](../README.md#OAuth2PasswordBearer-password), [HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## getStatementsApiV1StatisticXapiStatementsGet

> XAPIStatementListResponse getStatementsApiV1StatisticXapiStatementsGet(skip, limit, studentId, verbId, gameId, levelId)

Get Statements

Get xAPI statements with optional filters.  Returns statements with pagination. Use filters to narrow results.

### Example

```ts
import {
  Configuration,
  StatisticsApi,
} from '';
import type { GetStatementsApiV1StatisticXapiStatementsGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // To configure OAuth2 access token for authorization: OAuth2PasswordBearer password
    accessToken: "YOUR ACCESS TOKEN",
    // Configure HTTP bearer authorization: HTTPBearer
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new StatisticsApi(config);

  const body = {
    // number | Number of records to skip (optional)
    skip: 56,
    // number | Maximum number of records to return (optional)
    limit: 56,
    // number | Filter by student ID (optional)
    studentId: 56,
    // string | Filter by verb ID (optional)
    verbId: verbId_example,
    // number | Filter by game ID (optional)
    gameId: 56,
    // number | Filter by level ID (optional)
    levelId: 56,
  } satisfies GetStatementsApiV1StatisticXapiStatementsGetRequest;

  try {
    const data = await api.getStatementsApiV1StatisticXapiStatementsGet(body);
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
| **skip** | `number` | Number of records to skip | [Optional] [Defaults to `0`] |
| **limit** | `number` | Maximum number of records to return | [Optional] [Defaults to `100`] |
| **studentId** | `number` | Filter by student ID | [Optional] [Defaults to `undefined`] |
| **verbId** | `string` | Filter by verb ID | [Optional] [Defaults to `undefined`] |
| **gameId** | `number` | Filter by game ID | [Optional] [Defaults to `undefined`] |
| **levelId** | `number` | Filter by level ID | [Optional] [Defaults to `undefined`] |

### Return type

[**XAPIStatementListResponse**](XAPIStatementListResponse.md)

### Authorization

[OAuth2PasswordBearer password](../README.md#OAuth2PasswordBearer-password), [HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## getStudentFeedbackHistoryApiV1StatisticFeedbackStudentIdGet

> Array&lt;FeedbackSchema&gt; getStudentFeedbackHistoryApiV1StatisticFeedbackStudentIdGet(studentId, skip, limit)

Get Student Feedback History

Obtener feedback histórico del estudiante.

### Example

```ts
import {
  Configuration,
  StatisticsApi,
} from '';
import type { GetStudentFeedbackHistoryApiV1StatisticFeedbackStudentIdGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: HTTPBearer
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new StatisticsApi(config);

  const body = {
    // number
    studentId: 56,
    // number (optional)
    skip: 56,
    // number (optional)
    limit: 56,
  } satisfies GetStudentFeedbackHistoryApiV1StatisticFeedbackStudentIdGetRequest;

  try {
    const data = await api.getStudentFeedbackHistoryApiV1StatisticFeedbackStudentIdGet(body);
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
| **studentId** | `number` |  | [Defaults to `undefined`] |
| **skip** | `number` |  | [Optional] [Defaults to `0`] |
| **limit** | `number` |  | [Optional] [Defaults to `100`] |

### Return type

[**Array&lt;FeedbackSchema&gt;**](FeedbackSchema.md)

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


## listMetricTypesApiV1StatisticMetricTypesGet

> Array&lt;MetricTypeSchema&gt; listMetricTypesApiV1StatisticMetricTypesGet(skip, limit)

List Metric Types

Lista todos los tipos de métricas disponibles.

### Example

```ts
import {
  Configuration,
  StatisticsApi,
} from '';
import type { ListMetricTypesApiV1StatisticMetricTypesGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: HTTPBearer
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new StatisticsApi(config);

  const body = {
    // number (optional)
    skip: 56,
    // number (optional)
    limit: 56,
  } satisfies ListMetricTypesApiV1StatisticMetricTypesGetRequest;

  try {
    const data = await api.listMetricTypesApiV1StatisticMetricTypesGet(body);
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
| **skip** | `number` |  | [Optional] [Defaults to `0`] |
| **limit** | `number` |  | [Optional] [Defaults to `100`] |

### Return type

[**Array&lt;MetricTypeSchema&gt;**](MetricTypeSchema.md)

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


## sendStatementsApiV1StatisticXapiStatementsPost

> Array&lt;XAPIStatementResponse&gt; sendStatementsApiV1StatisticXapiStatementsPost(xAPIStatementBatchCreate)

Send Statements

Receive and store xAPI statements.  Accepts a batch of xAPI statements (1-1000 per request). Supports full xAPI 1.0 specification with game-specific context.  The game client should send statements with: - actor.account.name &#x3D; student_id - verb &#x3D; standard xAPI verb - object.id &#x3D; activity ID (e.g., hello-world://segment/level_1_seg_3) - result &#x3D; quantitative data (score, success, completion) - context &#x3D; qualitative data (platform, language, extensions) - context.extensions &#x3D; game-specific data (game_id, level_id, segment_id)

### Example

```ts
import {
  Configuration,
  StatisticsApi,
} from '';
import type { SendStatementsApiV1StatisticXapiStatementsPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // To configure OAuth2 access token for authorization: OAuth2PasswordBearer password
    accessToken: "YOUR ACCESS TOKEN",
    // Configure HTTP bearer authorization: HTTPBearer
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new StatisticsApi(config);

  const body = {
    // XAPIStatementBatchCreate
    xAPIStatementBatchCreate: ...,
  } satisfies SendStatementsApiV1StatisticXapiStatementsPostRequest;

  try {
    const data = await api.sendStatementsApiV1StatisticXapiStatementsPost(body);
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
| **xAPIStatementBatchCreate** | [XAPIStatementBatchCreate](XAPIStatementBatchCreate.md) |  | |

### Return type

[**Array&lt;XAPIStatementResponse&gt;**](XAPIStatementResponse.md)

### Authorization

[OAuth2PasswordBearer password](../README.md#OAuth2PasswordBearer-password), [HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## submitFeedbackApiV1StatisticFeedbackPost

> FeedbackSchema submitFeedbackApiV1StatisticFeedbackPost(feedbackCreate)

Submit Feedback

Enviar retroalimentación de un estudiante.

### Example

```ts
import {
  Configuration,
  StatisticsApi,
} from '';
import type { SubmitFeedbackApiV1StatisticFeedbackPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: HTTPBearer
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new StatisticsApi(config);

  const body = {
    // FeedbackCreate
    feedbackCreate: ...,
  } satisfies SubmitFeedbackApiV1StatisticFeedbackPostRequest;

  try {
    const data = await api.submitFeedbackApiV1StatisticFeedbackPost(body);
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
| **feedbackCreate** | [FeedbackCreate](FeedbackCreate.md) |  | |

### Return type

[**FeedbackSchema**](FeedbackSchema.md)

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


## updateMetricTypeApiV1StatisticMetricTypesMetricTypeIdPatch

> MetricTypeSchema updateMetricTypeApiV1StatisticMetricTypesMetricTypeIdPatch(metricTypeId, metricTypeUpdate)

Update Metric Type

Actualiza un tipo de métrica existente.

### Example

```ts
import {
  Configuration,
  StatisticsApi,
} from '';
import type { UpdateMetricTypeApiV1StatisticMetricTypesMetricTypeIdPatchRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: HTTPBearer
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new StatisticsApi(config);

  const body = {
    // number
    metricTypeId: 56,
    // MetricTypeUpdate
    metricTypeUpdate: ...,
  } satisfies UpdateMetricTypeApiV1StatisticMetricTypesMetricTypeIdPatchRequest;

  try {
    const data = await api.updateMetricTypeApiV1StatisticMetricTypesMetricTypeIdPatch(body);
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
| **metricTypeId** | `number` |  | [Defaults to `undefined`] |
| **metricTypeUpdate** | [MetricTypeUpdate](MetricTypeUpdate.md) |  | |

### Return type

[**MetricTypeSchema**](MetricTypeSchema.md)

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

