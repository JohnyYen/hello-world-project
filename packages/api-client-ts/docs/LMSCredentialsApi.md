# LMSCredentialsApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**deleteUserLmsCredentialsApiV1UsersLmsCredentialsUserUserIdDelete**](LMSCredentialsApi.md#deleteuserlmscredentialsapiv1userslmscredentialsuseruseriddelete) | **DELETE** /api/v1/users/lms/credentials/user/{user_id} | Delete User Lms Credentials |
| [**getUserLmsCredentialsApiV1UsersLmsCredentialsUserUserIdGet**](LMSCredentialsApi.md#getuserlmscredentialsapiv1userslmscredentialsuseruseridget) | **GET** /api/v1/users/lms/credentials/user/{user_id} | Get User Lms Credentials |
| [**registerLmsCredentialsApiV1UsersLmsCredentialsPost**](LMSCredentialsApi.md#registerlmscredentialsapiv1userslmscredentialspost) | **POST** /api/v1/users/lms/credentials | Register Lms Credentials |



## deleteUserLmsCredentialsApiV1UsersLmsCredentialsUserUserIdDelete

> deleteUserLmsCredentialsApiV1UsersLmsCredentialsUserUserIdDelete(userId)

Delete User Lms Credentials

Eliminar las credenciales LMS de un usuario.  Realiza un soft delete de las credenciales.

### Example

```ts
import {
  Configuration,
  LMSCredentialsApi,
} from '';
import type { DeleteUserLmsCredentialsApiV1UsersLmsCredentialsUserUserIdDeleteRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new LMSCredentialsApi();

  const body = {
    // number
    userId: 56,
  } satisfies DeleteUserLmsCredentialsApiV1UsersLmsCredentialsUserUserIdDeleteRequest;

  try {
    const data = await api.deleteUserLmsCredentialsApiV1UsersLmsCredentialsUserUserIdDelete(body);
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

`void` (Empty response body)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **204** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## getUserLmsCredentialsApiV1UsersLmsCredentialsUserUserIdGet

> LMSCredentialResponse getUserLmsCredentialsApiV1UsersLmsCredentialsUserUserIdGet(userId)

Get User Lms Credentials

Obtener las credenciales LMS de un usuario.  Retorna las credenciales con la contraseña oculta.

### Example

```ts
import {
  Configuration,
  LMSCredentialsApi,
} from '';
import type { GetUserLmsCredentialsApiV1UsersLmsCredentialsUserUserIdGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new LMSCredentialsApi();

  const body = {
    // number
    userId: 56,
  } satisfies GetUserLmsCredentialsApiV1UsersLmsCredentialsUserUserIdGetRequest;

  try {
    const data = await api.getUserLmsCredentialsApiV1UsersLmsCredentialsUserUserIdGet(body);
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

[**LMSCredentialResponse**](LMSCredentialResponse.md)

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


## registerLmsCredentialsApiV1UsersLmsCredentialsPost

> LMSCredentialResponse registerLmsCredentialsApiV1UsersLmsCredentialsPost(lMSCredentialCreate)

Register Lms Credentials

Registrar credenciales LMS para un usuario.  - **user_id**: ID del usuario que registra las credenciales - **lms_url**: URL del LMS (ej: https://moodle.university.edu) - **lms_email**: Email de la cuenta en el LMS - **lms_password**: Contraseña de la cuenta LMS - **lms_provider**: Proveedor LMS (moodle, canvas, etc.)

### Example

```ts
import {
  Configuration,
  LMSCredentialsApi,
} from '';
import type { RegisterLmsCredentialsApiV1UsersLmsCredentialsPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new LMSCredentialsApi();

  const body = {
    // LMSCredentialCreate
    lMSCredentialCreate: ...,
  } satisfies RegisterLmsCredentialsApiV1UsersLmsCredentialsPostRequest;

  try {
    const data = await api.registerLmsCredentialsApiV1UsersLmsCredentialsPost(body);
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
| **lMSCredentialCreate** | [LMSCredentialCreate](LMSCredentialCreate.md) |  | |

### Return type

[**LMSCredentialResponse**](LMSCredentialResponse.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **201** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

