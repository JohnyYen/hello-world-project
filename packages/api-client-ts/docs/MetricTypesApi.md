# MetricTypesApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**createMetricTypeApiV1StatisticMetricTypesPost**](MetricTypesApi.md#createmetrictypeapiv1statisticmetrictypespost) | **POST** /api/v1/statistic/metric-types | Create Metric Type |
| [**deleteMetricTypeApiV1StatisticMetricTypesMetricTypeIdDelete**](MetricTypesApi.md#deletemetrictypeapiv1statisticmetrictypesmetrictypeiddelete) | **DELETE** /api/v1/statistic/metric-types/{metric_type_id} | Delete Metric Type |
| [**getMetricTypeApiV1StatisticMetricTypesMetricTypeIdGet**](MetricTypesApi.md#getmetrictypeapiv1statisticmetrictypesmetrictypeidget) | **GET** /api/v1/statistic/metric-types/{metric_type_id} | Get Metric Type |
| [**listMetricTypesApiV1StatisticMetricTypesGet**](MetricTypesApi.md#listmetrictypesapiv1statisticmetrictypesget) | **GET** /api/v1/statistic/metric-types | List Metric Types |
| [**updateMetricTypeApiV1StatisticMetricTypesMetricTypeIdPatch**](MetricTypesApi.md#updatemetrictypeapiv1statisticmetrictypesmetrictypeidpatch) | **PATCH** /api/v1/statistic/metric-types/{metric_type_id} | Update Metric Type |



## createMetricTypeApiV1StatisticMetricTypesPost

> MetricTypeSchema createMetricTypeApiV1StatisticMetricTypesPost(metricTypeCreate)

Create Metric Type

Crea un nuevo tipo de métrica.

### Example

```ts
import {
  Configuration,
  MetricTypesApi,
} from '';
import type { CreateMetricTypeApiV1StatisticMetricTypesPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: HTTPBearer
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new MetricTypesApi(config);

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
  MetricTypesApi,
} from '';
import type { DeleteMetricTypeApiV1StatisticMetricTypesMetricTypeIdDeleteRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: HTTPBearer
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new MetricTypesApi(config);

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
  MetricTypesApi,
} from '';
import type { GetMetricTypeApiV1StatisticMetricTypesMetricTypeIdGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: HTTPBearer
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new MetricTypesApi(config);

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


## listMetricTypesApiV1StatisticMetricTypesGet

> Array&lt;MetricTypeSchema&gt; listMetricTypesApiV1StatisticMetricTypesGet(skip, limit)

List Metric Types

Lista todos los tipos de métricas disponibles.

### Example

```ts
import {
  Configuration,
  MetricTypesApi,
} from '';
import type { ListMetricTypesApiV1StatisticMetricTypesGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: HTTPBearer
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new MetricTypesApi(config);

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


## updateMetricTypeApiV1StatisticMetricTypesMetricTypeIdPatch

> MetricTypeSchema updateMetricTypeApiV1StatisticMetricTypesMetricTypeIdPatch(metricTypeId, metricTypeUpdate)

Update Metric Type

Actualiza un tipo de métrica existente.

### Example

```ts
import {
  Configuration,
  MetricTypesApi,
} from '';
import type { UpdateMetricTypeApiV1StatisticMetricTypesMetricTypeIdPatchRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: HTTPBearer
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new MetricTypesApi(config);

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

