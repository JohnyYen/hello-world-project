# LMSIntegrationApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**syncLmsDataApiV1UsersLmsSyncUserIdPost**](LMSIntegrationApi.md#synclmsdataapiv1userslmssyncuseridpost) | **POST** /api/v1/users/lms/sync/{user_id} | Sync Lms Data |



## syncLmsDataApiV1UsersLmsSyncUserIdPost

> SyncResultResponse syncLmsDataApiV1UsersLmsSyncUserIdPost(userId)

Sync Lms Data

Sincronizar datos entre LMS y la plataforma.  Importa usuarios, cursos y calificaciones desde el LMS o exporta progreso de estudiantes al LMS.

### Example

```ts
import {
  Configuration,
  LMSIntegrationApi,
} from '';
import type { SyncLmsDataApiV1UsersLmsSyncUserIdPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: HTTPBearer
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new LMSIntegrationApi(config);

  const body = {
    // number
    userId: 56,
  } satisfies SyncLmsDataApiV1UsersLmsSyncUserIdPostRequest;

  try {
    const data = await api.syncLmsDataApiV1UsersLmsSyncUserIdPost(body);
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
| **userId** | `number` |  | [Defaults to `undefined`] |

### Return type

[**SyncResultResponse**](SyncResultResponse.md)

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

