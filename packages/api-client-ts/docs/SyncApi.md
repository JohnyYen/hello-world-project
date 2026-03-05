# SyncApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**endSyncSessionApiV1SyncSyncSessionsSessionIdEndPut**](SyncApi.md#endsyncsessionapiv1syncsyncsessionssessionidendput) | **PUT** /api/v1/sync/sync-sessions/{session_id}/end | End Sync Session |
| [**getSessionsByInstanceApiV1SyncSyncSessionsInstanceIdGet**](SyncApi.md#getsessionsbyinstanceapiv1syncsyncsessionsinstanceidget) | **GET** /api/v1/sync/sync-sessions/{instance_id} | Get Sessions By Instance |
| [**listSyncEventsApiV1SyncSyncEventsSessionIdGet**](SyncApi.md#listsynceventsapiv1syncsynceventssessionidget) | **GET** /api/v1/sync/sync-events/{session_id} | List Sync Events |
| [**registerSyncEventApiV1SyncSyncEventsPost**](SyncApi.md#registersynceventapiv1syncsynceventspost) | **POST** /api/v1/sync/sync-events | Register Sync Event |
| [**startSyncSessionApiV1SyncSyncSessionsPost**](SyncApi.md#startsyncsessionapiv1syncsyncsessionspost) | **POST** /api/v1/sync/sync-sessions | Start Sync Session |



## endSyncSessionApiV1SyncSyncSessionsSessionIdEndPut

> SyncSessionSchema endSyncSessionApiV1SyncSyncSessionsSessionIdEndPut(sessionId)

End Sync Session

Finaliza la sesión.

### Example

```ts
import {
  Configuration,
  SyncApi,
} from '';
import type { EndSyncSessionApiV1SyncSyncSessionsSessionIdEndPutRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new SyncApi();

  const body = {
    // number
    sessionId: 56,
  } satisfies EndSyncSessionApiV1SyncSyncSessionsSessionIdEndPutRequest;

  try {
    const data = await api.endSyncSessionApiV1SyncSyncSessionsSessionIdEndPut(body);
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
| **sessionId** | `number` |  | [Defaults to `undefined`] |

### Return type

[**SyncSessionSchema**](SyncSessionSchema.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## getSessionsByInstanceApiV1SyncSyncSessionsInstanceIdGet

> Array&lt;SyncSessionSchema&gt; getSessionsByInstanceApiV1SyncSyncSessionsInstanceIdGet(instanceId)

Get Sessions By Instance

Obtiene sesiones de una instancia.

### Example

```ts
import {
  Configuration,
  SyncApi,
} from '';
import type { GetSessionsByInstanceApiV1SyncSyncSessionsInstanceIdGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new SyncApi();

  const body = {
    // number
    instanceId: 56,
  } satisfies GetSessionsByInstanceApiV1SyncSyncSessionsInstanceIdGetRequest;

  try {
    const data = await api.getSessionsByInstanceApiV1SyncSyncSessionsInstanceIdGet(body);
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

[**Array&lt;SyncSessionSchema&gt;**](SyncSessionSchema.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## listSyncEventsApiV1SyncSyncEventsSessionIdGet

> Array&lt;SyncEventSchema&gt; listSyncEventsApiV1SyncSyncEventsSessionIdGet(sessionId)

List Sync Events

Lista eventos asociados a una sesión.

### Example

```ts
import {
  Configuration,
  SyncApi,
} from '';
import type { ListSyncEventsApiV1SyncSyncEventsSessionIdGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new SyncApi();

  const body = {
    // number
    sessionId: 56,
  } satisfies ListSyncEventsApiV1SyncSyncEventsSessionIdGetRequest;

  try {
    const data = await api.listSyncEventsApiV1SyncSyncEventsSessionIdGet(body);
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
| **sessionId** | `number` |  | [Defaults to `undefined`] |

### Return type

[**Array&lt;SyncEventSchema&gt;**](SyncEventSchema.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## registerSyncEventApiV1SyncSyncEventsPost

> SyncEventSchema registerSyncEventApiV1SyncSyncEventsPost(syncEventCreate)

Register Sync Event

Registra un evento (acción del jugador).

### Example

```ts
import {
  Configuration,
  SyncApi,
} from '';
import type { RegisterSyncEventApiV1SyncSyncEventsPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new SyncApi();

  const body = {
    // SyncEventCreate
    syncEventCreate: ...,
  } satisfies RegisterSyncEventApiV1SyncSyncEventsPostRequest;

  try {
    const data = await api.registerSyncEventApiV1SyncSyncEventsPost(body);
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
| **syncEventCreate** | [SyncEventCreate](SyncEventCreate.md) |  | |

### Return type

[**SyncEventSchema**](SyncEventSchema.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## startSyncSessionApiV1SyncSyncSessionsPost

> SyncSessionSchema startSyncSessionApiV1SyncSyncSessionsPost(syncSessionCreate)

Start Sync Session

Inicia una sesión de sincronización.

### Example

```ts
import {
  Configuration,
  SyncApi,
} from '';
import type { StartSyncSessionApiV1SyncSyncSessionsPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new SyncApi();

  const body = {
    // SyncSessionCreate
    syncSessionCreate: ...,
  } satisfies StartSyncSessionApiV1SyncSyncSessionsPostRequest;

  try {
    const data = await api.startSyncSessionApiV1SyncSyncSessionsPost(body);
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
| **syncSessionCreate** | [SyncSessionCreate](SyncSessionCreate.md) |  | |

### Return type

[**SyncSessionSchema**](SyncSessionSchema.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

