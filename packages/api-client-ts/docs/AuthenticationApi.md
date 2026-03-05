# AuthenticationApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**changePasswordApiV1AuthChangePasswordPost**](AuthenticationApi.md#changepasswordapiv1authchangepasswordpost) | **POST** /api/v1/auth/change-password | Change Password |
| [**loginForAccessTokenApiV1AuthLoginPost**](AuthenticationApi.md#loginforaccesstokenapiv1authloginpost) | **POST** /api/v1/auth/login | Login For Access Token |
| [**registerUserApiV1AuthRegisterPost**](AuthenticationApi.md#registeruserapiv1authregisterpost) | **POST** /api/v1/auth/register | Register User |



## changePasswordApiV1AuthChangePasswordPost

> SingleUserResponse changePasswordApiV1AuthChangePasswordPost(userId, userChangePassword)

Change Password

Cambia la contraseña de un usuario.  - **user_id**: ID del usuario (en query parameter o body) - **current_password**: Contraseña actual para verificación - **new_password**: Nueva contraseña (mínimo 8 caracteres)

### Example

```ts
import {
  Configuration,
  AuthenticationApi,
} from '';
import type { ChangePasswordApiV1AuthChangePasswordPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new AuthenticationApi();

  const body = {
    // number
    userId: 56,
    // UserChangePassword
    userChangePassword: ...,
  } satisfies ChangePasswordApiV1AuthChangePasswordPostRequest;

  try {
    const data = await api.changePasswordApiV1AuthChangePasswordPost(body);
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
| **userChangePassword** | [UserChangePassword](UserChangePassword.md) |  | |

### Return type

[**SingleUserResponse**](SingleUserResponse.md)

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


## loginForAccessTokenApiV1AuthLoginPost

> UserLoginResponse loginForAccessTokenApiV1AuthLoginPost(userLogin)

Login For Access Token

Autentica un usuario y retorna el token de acceso JWT.  - **username**: Username del usuario (opcional) - **email**: Email del usuario (opcional) - **password**: Contraseña del usuario  Nota: Proporcionar username O email, no ambos requeridos.  Retorna el token JWT y los datos del usuario autenticado.

### Example

```ts
import {
  Configuration,
  AuthenticationApi,
} from '';
import type { LoginForAccessTokenApiV1AuthLoginPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new AuthenticationApi();

  const body = {
    // UserLogin
    userLogin: ...,
  } satisfies LoginForAccessTokenApiV1AuthLoginPostRequest;

  try {
    const data = await api.loginForAccessTokenApiV1AuthLoginPost(body);
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
| **userLogin** | [UserLogin](UserLogin.md) |  | |

### Return type

[**UserLoginResponse**](UserLoginResponse.md)

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


## registerUserApiV1AuthRegisterPost

> UserLoginResponse registerUserApiV1AuthRegisterPost(userCreate)

Register User

Registra un nuevo usuario y retorna el token de acceso JWT.  - **username**: Nombre de usuario (debe ser único) - **email**: Email del usuario (debe ser único) - **name**: Nombre del usuario (requerido) - **lastname**: Apellido del usuario (opcional) - **password**: Contraseña del usuario (será hasheada)  Retorna el token JWT y los datos del usuario creado.

### Example

```ts
import {
  Configuration,
  AuthenticationApi,
} from '';
import type { RegisterUserApiV1AuthRegisterPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new AuthenticationApi();

  const body = {
    // UserCreate
    userCreate: ...,
  } satisfies RegisterUserApiV1AuthRegisterPostRequest;

  try {
    const data = await api.registerUserApiV1AuthRegisterPost(body);
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
| **userCreate** | [UserCreate](UserCreate.md) |  | |

### Return type

[**UserLoginResponse**](UserLoginResponse.md)

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

