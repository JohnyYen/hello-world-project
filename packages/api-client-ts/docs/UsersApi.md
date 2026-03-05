# UsersApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**createStudentApiV1UsersStudentsPost**](UsersApi.md#createstudentapiv1usersstudentspost) | **POST** /api/v1/users/students | Create Student |
| [**createUserApiV1UsersPost**](UsersApi.md#createuserapiv1userspost) | **POST** /api/v1/users/ | Crear un nuevo usuario |
| [**deleteStudentApiV1UsersStudentsIdDelete**](UsersApi.md#deletestudentapiv1usersstudentsiddelete) | **DELETE** /api/v1/users/students/{id} | Delete Student |
| [**deleteUserLmsCredentialsApiV1UsersLmsCredentialsUserUserIdDelete**](UsersApi.md#deleteuserlmscredentialsapiv1userslmscredentialsuseruseriddelete) | **DELETE** /api/v1/users/lms/credentials/user/{user_id} | Delete User Lms Credentials |
| [**getAllUsersApiV1UsersGet**](UsersApi.md#getallusersapiv1usersget) | **GET** /api/v1/users/ | Obtener todos los usuarios |
| [**getStudentApiV1UsersStudentsIdGet**](UsersApi.md#getstudentapiv1usersstudentsidget) | **GET** /api/v1/users/students/{id} | Get Student |
| [**getStudentProgressApiV1UsersStudentsIdProgressGet**](UsersApi.md#getstudentprogressapiv1usersstudentsidprogressget) | **GET** /api/v1/users/students/{id}/progress | Get Student Progress |
| [**getStudentReportsApiV1UsersStudentsIdReportsGet**](UsersApi.md#getstudentreportsapiv1usersstudentsidreportsget) | **GET** /api/v1/users/students/{id}/reports | Get Student Reports |
| [**getTeacherProfileApiV1UsersProfessorsMeGet**](UsersApi.md#getteacherprofileapiv1usersprofessorsmeget) | **GET** /api/v1/users/professors/me | Get Teacher Profile |
| [**getTeacherSettingsApiV1UsersProfessorsSettingsGet**](UsersApi.md#getteachersettingsapiv1usersprofessorssettingsget) | **GET** /api/v1/users/professors/settings | Get Teacher Settings |
| [**getUserApiV1UsersUserIdGet**](UsersApi.md#getuserapiv1usersuseridget) | **GET** /api/v1/users/{user_id} | Obtener un usuario por ID |
| [**getUserLmsCredentialsApiV1UsersLmsCredentialsUserUserIdGet**](UsersApi.md#getuserlmscredentialsapiv1userslmscredentialsuseruseridget) | **GET** /api/v1/users/lms/credentials/user/{user_id} | Get User Lms Credentials |
| [**listStudentsApiV1UsersStudentsGet**](UsersApi.md#liststudentsapiv1usersstudentsget) | **GET** /api/v1/users/students | List Students |
| [**registerLmsCredentialsApiV1UsersLmsCredentialsPost**](UsersApi.md#registerlmscredentialsapiv1userslmscredentialspost) | **POST** /api/v1/users/lms/credentials | Register Lms Credentials |
| [**syncLmsDataApiV1UsersLmsSyncUserIdPost**](UsersApi.md#synclmsdataapiv1userslmssyncuseridpost) | **POST** /api/v1/users/lms/sync/{user_id} | Sync Lms Data |
| [**updateStudentApiV1UsersStudentsIdPut**](UsersApi.md#updatestudentapiv1usersstudentsidput) | **PUT** /api/v1/users/students/{id} | Update Student |
| [**updateTeacherProfileApiV1UsersProfessorsMePut**](UsersApi.md#updateteacherprofileapiv1usersprofessorsmeput) | **PUT** /api/v1/users/professors/me | Update Teacher Profile |
| [**updateTeacherSettingsApiV1UsersProfessorsSettingsPut**](UsersApi.md#updateteachersettingsapiv1usersprofessorssettingsput) | **PUT** /api/v1/users/professors/settings | Update Teacher Settings |



## createStudentApiV1UsersStudentsPost

> StudentResponse createStudentApiV1UsersStudentsPost(studentCreate)

Create Student

Registrar un nuevo estudiante.  Requiere autenticación y rol de professor o admin.

### Example

```ts
import {
  Configuration,
  UsersApi,
} from '';
import type { CreateStudentApiV1UsersStudentsPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // To configure OAuth2 access token for authorization: OAuth2PasswordBearer password
    accessToken: "YOUR ACCESS TOKEN",
  });
  const api = new UsersApi(config);

  const body = {
    // StudentCreate
    studentCreate: ...,
  } satisfies CreateStudentApiV1UsersStudentsPostRequest;

  try {
    const data = await api.createStudentApiV1UsersStudentsPost(body);
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
| **studentCreate** | [StudentCreate](StudentCreate.md) |  | |

### Return type

[**StudentResponse**](StudentResponse.md)

### Authorization

[OAuth2PasswordBearer password](../README.md#OAuth2PasswordBearer-password)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## createUserApiV1UsersPost

> SingleUserResponse createUserApiV1UsersPost(userCreate)

Crear un nuevo usuario

Crea un nuevo usuario en la base de datos con la información proporcionada. - **email**: El correo electrónico del usuario (debe ser único). - **username**: El nombre de usuario (opcional, debe ser único si se proporciona). - **name**: El nombre del usuario (requerido). - **password**: La contraseña del usuario.

### Example

```ts
import {
  Configuration,
  UsersApi,
} from '';
import type { CreateUserApiV1UsersPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new UsersApi();

  const body = {
    // UserCreate
    userCreate: ...,
  } satisfies CreateUserApiV1UsersPostRequest;

  try {
    const data = await api.createUserApiV1UsersPost(body);
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

[**SingleUserResponse**](SingleUserResponse.md)

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


## deleteStudentApiV1UsersStudentsIdDelete

> any deleteStudentApiV1UsersStudentsIdDelete(id)

Delete Student

Eliminar estudiante (soft delete).  Requiere autenticación y rol de professor o admin.

### Example

```ts
import {
  Configuration,
  UsersApi,
} from '';
import type { DeleteStudentApiV1UsersStudentsIdDeleteRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // To configure OAuth2 access token for authorization: OAuth2PasswordBearer password
    accessToken: "YOUR ACCESS TOKEN",
  });
  const api = new UsersApi(config);

  const body = {
    // number
    id: 56,
  } satisfies DeleteStudentApiV1UsersStudentsIdDeleteRequest;

  try {
    const data = await api.deleteStudentApiV1UsersStudentsIdDelete(body);
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
| **id** | `number` |  | [Defaults to `undefined`] |

### Return type

**any**

### Authorization

[OAuth2PasswordBearer password](../README.md#OAuth2PasswordBearer-password)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## deleteUserLmsCredentialsApiV1UsersLmsCredentialsUserUserIdDelete

> deleteUserLmsCredentialsApiV1UsersLmsCredentialsUserUserIdDelete(userId)

Delete User Lms Credentials

Eliminar las credenciales LMS de un usuario.  Realiza un soft delete de las credenciales.

### Example

```ts
import {
  Configuration,
  UsersApi,
} from '';
import type { DeleteUserLmsCredentialsApiV1UsersLmsCredentialsUserUserIdDeleteRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new UsersApi();

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


## getAllUsersApiV1UsersGet

> UserListResponse getAllUsersApiV1UsersGet(skip, limit, includeDeleted)

Obtener todos los usuarios

Obtiene una lista paginada de todos los usuarios registrados en el sistema.  - **include_deleted**: Si es True, incluye usuarios eliminados (soft deleted).   Por defecto es False para solo mostrar usuarios activos.

### Example

```ts
import {
  Configuration,
  UsersApi,
} from '';
import type { GetAllUsersApiV1UsersGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new UsersApi();

  const body = {
    // number (optional)
    skip: 56,
    // number (optional)
    limit: 56,
    // boolean (optional)
    includeDeleted: true,
  } satisfies GetAllUsersApiV1UsersGetRequest;

  try {
    const data = await api.getAllUsersApiV1UsersGet(body);
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
| **includeDeleted** | `boolean` |  | [Optional] [Defaults to `false`] |

### Return type

[**UserListResponse**](UserListResponse.md)

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


## getStudentApiV1UsersStudentsIdGet

> StudentResponse getStudentApiV1UsersStudentsIdGet(id)

Get Student

Obtener detalle de un estudiante.  Requiere autenticación. Professor/Admin pueden ver cualquier estudiante. El propio estudiante puede ver su propio perfil.

### Example

```ts
import {
  Configuration,
  UsersApi,
} from '';
import type { GetStudentApiV1UsersStudentsIdGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // To configure OAuth2 access token for authorization: OAuth2PasswordBearer password
    accessToken: "YOUR ACCESS TOKEN",
  });
  const api = new UsersApi(config);

  const body = {
    // number
    id: 56,
  } satisfies GetStudentApiV1UsersStudentsIdGetRequest;

  try {
    const data = await api.getStudentApiV1UsersStudentsIdGet(body);
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
| **id** | `number` |  | [Defaults to `undefined`] |

### Return type

[**StudentResponse**](StudentResponse.md)

### Authorization

[OAuth2PasswordBearer password](../README.md#OAuth2PasswordBearer-password)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## getStudentProgressApiV1UsersStudentsIdProgressGet

> StudentProgressResponse getStudentProgressApiV1UsersStudentsIdProgressGet(id)

Get Student Progress

Obtener progreso del estudiante.  Requiere autenticación. Professor/Admin pueden ver cualquier estudiante. El propio estudiante puede ver su propio progreso.

### Example

```ts
import {
  Configuration,
  UsersApi,
} from '';
import type { GetStudentProgressApiV1UsersStudentsIdProgressGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // To configure OAuth2 access token for authorization: OAuth2PasswordBearer password
    accessToken: "YOUR ACCESS TOKEN",
  });
  const api = new UsersApi(config);

  const body = {
    // number
    id: 56,
  } satisfies GetStudentProgressApiV1UsersStudentsIdProgressGetRequest;

  try {
    const data = await api.getStudentProgressApiV1UsersStudentsIdProgressGet(body);
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
| **id** | `number` |  | [Defaults to `undefined`] |

### Return type

[**StudentProgressResponse**](StudentProgressResponse.md)

### Authorization

[OAuth2PasswordBearer password](../README.md#OAuth2PasswordBearer-password)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## getStudentReportsApiV1UsersStudentsIdReportsGet

> StudentReportsResponse getStudentReportsApiV1UsersStudentsIdReportsGet(id)

Get Student Reports

Obtener reportes individuales (desempeño, actividad, etc.)

### Example

```ts
import {
  Configuration,
  UsersApi,
} from '';
import type { GetStudentReportsApiV1UsersStudentsIdReportsGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new UsersApi();

  const body = {
    // number
    id: 56,
  } satisfies GetStudentReportsApiV1UsersStudentsIdReportsGetRequest;

  try {
    const data = await api.getStudentReportsApiV1UsersStudentsIdReportsGet(body);
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
| **id** | `number` |  | [Defaults to `undefined`] |

### Return type

[**StudentReportsResponse**](StudentReportsResponse.md)

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


## getTeacherProfileApiV1UsersProfessorsMeGet

> TeacherProfileResponseSchema getTeacherProfileApiV1UsersProfessorsMeGet()

Get Teacher Profile

Obtener perfil del profesor autenticado.  Requiere autenticación mediante token JWT.

### Example

```ts
import {
  Configuration,
  UsersApi,
} from '';
import type { GetTeacherProfileApiV1UsersProfessorsMeGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // To configure OAuth2 access token for authorization: OAuth2PasswordBearer password
    accessToken: "YOUR ACCESS TOKEN",
  });
  const api = new UsersApi(config);

  try {
    const data = await api.getTeacherProfileApiV1UsersProfessorsMeGet();
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**TeacherProfileResponseSchema**](TeacherProfileResponseSchema.md)

### Authorization

[OAuth2PasswordBearer password](../README.md#OAuth2PasswordBearer-password)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## getTeacherSettingsApiV1UsersProfessorsSettingsGet

> TeacherSettingsResponseSchema getTeacherSettingsApiV1UsersProfessorsSettingsGet()

Get Teacher Settings

Obtener configuraciones del dashboard del profesor.  Requiere autenticación mediante token JWT.

### Example

```ts
import {
  Configuration,
  UsersApi,
} from '';
import type { GetTeacherSettingsApiV1UsersProfessorsSettingsGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // To configure OAuth2 access token for authorization: OAuth2PasswordBearer password
    accessToken: "YOUR ACCESS TOKEN",
  });
  const api = new UsersApi(config);

  try {
    const data = await api.getTeacherSettingsApiV1UsersProfessorsSettingsGet();
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**TeacherSettingsResponseSchema**](TeacherSettingsResponseSchema.md)

### Authorization

[OAuth2PasswordBearer password](../README.md#OAuth2PasswordBearer-password)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## getUserApiV1UsersUserIdGet

> SingleUserResponse getUserApiV1UsersUserIdGet(userId)

Obtener un usuario por ID

Busca y devuelve un usuario por su ID único.

### Example

```ts
import {
  Configuration,
  UsersApi,
} from '';
import type { GetUserApiV1UsersUserIdGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new UsersApi();

  const body = {
    // number
    userId: 56,
  } satisfies GetUserApiV1UsersUserIdGetRequest;

  try {
    const data = await api.getUserApiV1UsersUserIdGet(body);
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

[**SingleUserResponse**](SingleUserResponse.md)

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


## getUserLmsCredentialsApiV1UsersLmsCredentialsUserUserIdGet

> LMSCredentialResponse getUserLmsCredentialsApiV1UsersLmsCredentialsUserUserIdGet(userId)

Get User Lms Credentials

Obtener las credenciales LMS de un usuario.  Retorna las credenciales con la contraseña oculta.

### Example

```ts
import {
  Configuration,
  UsersApi,
} from '';
import type { GetUserLmsCredentialsApiV1UsersLmsCredentialsUserUserIdGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new UsersApi();

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


## listStudentsApiV1UsersStudentsGet

> StudentListResponse listStudentsApiV1UsersStudentsGet(skip, limit, search)

List Students

Listar estudiantes (con filtros y paginación).  Requiere autenticación y rol de professor o admin.

### Example

```ts
import {
  Configuration,
  UsersApi,
} from '';
import type { ListStudentsApiV1UsersStudentsGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // To configure OAuth2 access token for authorization: OAuth2PasswordBearer password
    accessToken: "YOUR ACCESS TOKEN",
  });
  const api = new UsersApi(config);

  const body = {
    // number | Número de registros a saltar (optional)
    skip: 56,
    // number | Número de registros a devolver (optional)
    limit: 56,
    // string | Búsqueda por nombre o email (optional)
    search: search_example,
  } satisfies ListStudentsApiV1UsersStudentsGetRequest;

  try {
    const data = await api.listStudentsApiV1UsersStudentsGet(body);
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
| **search** | `string` | Búsqueda por nombre o email | [Optional] [Defaults to `undefined`] |

### Return type

[**StudentListResponse**](StudentListResponse.md)

### Authorization

[OAuth2PasswordBearer password](../README.md#OAuth2PasswordBearer-password)

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
  UsersApi,
} from '';
import type { RegisterLmsCredentialsApiV1UsersLmsCredentialsPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new UsersApi();

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


## syncLmsDataApiV1UsersLmsSyncUserIdPost

> SyncResultResponse syncLmsDataApiV1UsersLmsSyncUserIdPost(userId)

Sync Lms Data

Sincronizar datos entre LMS y la plataforma.  Importa usuarios, cursos y calificaciones desde el LMS o exporta progreso de estudiantes al LMS.

### Example

```ts
import {
  Configuration,
  UsersApi,
} from '';
import type { SyncLmsDataApiV1UsersLmsSyncUserIdPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new UsersApi();

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


## updateStudentApiV1UsersStudentsIdPut

> StudentResponse updateStudentApiV1UsersStudentsIdPut(id, studentUpdate)

Update Student

Actualizar información del estudiante.  Requiere autenticación y rol de professor o admin.

### Example

```ts
import {
  Configuration,
  UsersApi,
} from '';
import type { UpdateStudentApiV1UsersStudentsIdPutRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // To configure OAuth2 access token for authorization: OAuth2PasswordBearer password
    accessToken: "YOUR ACCESS TOKEN",
  });
  const api = new UsersApi(config);

  const body = {
    // number
    id: 56,
    // StudentUpdate
    studentUpdate: ...,
  } satisfies UpdateStudentApiV1UsersStudentsIdPutRequest;

  try {
    const data = await api.updateStudentApiV1UsersStudentsIdPut(body);
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
| **id** | `number` |  | [Defaults to `undefined`] |
| **studentUpdate** | [StudentUpdate](StudentUpdate.md) |  | |

### Return type

[**StudentResponse**](StudentResponse.md)

### Authorization

[OAuth2PasswordBearer password](../README.md#OAuth2PasswordBearer-password)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## updateTeacherProfileApiV1UsersProfessorsMePut

> TeacherUpdateResponseSchema updateTeacherProfileApiV1UsersProfessorsMePut(teacherProfileUpdate)

Update Teacher Profile

Actualizar perfil del profesor autenticado.  Requiere autenticación mediante token JWT.

### Example

```ts
import {
  Configuration,
  UsersApi,
} from '';
import type { UpdateTeacherProfileApiV1UsersProfessorsMePutRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // To configure OAuth2 access token for authorization: OAuth2PasswordBearer password
    accessToken: "YOUR ACCESS TOKEN",
  });
  const api = new UsersApi(config);

  const body = {
    // TeacherProfileUpdate
    teacherProfileUpdate: ...,
  } satisfies UpdateTeacherProfileApiV1UsersProfessorsMePutRequest;

  try {
    const data = await api.updateTeacherProfileApiV1UsersProfessorsMePut(body);
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
| **teacherProfileUpdate** | [TeacherProfileUpdate](TeacherProfileUpdate.md) |  | |

### Return type

[**TeacherUpdateResponseSchema**](TeacherUpdateResponseSchema.md)

### Authorization

[OAuth2PasswordBearer password](../README.md#OAuth2PasswordBearer-password)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## updateTeacherSettingsApiV1UsersProfessorsSettingsPut

> TeacherSettingsResponseSchema updateTeacherSettingsApiV1UsersProfessorsSettingsPut(teacherSettingsUpdate)

Update Teacher Settings

Actualizar configuraciones del dashboard del profesor.  Requiere autenticación mediante token JWT.

### Example

```ts
import {
  Configuration,
  UsersApi,
} from '';
import type { UpdateTeacherSettingsApiV1UsersProfessorsSettingsPutRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // To configure OAuth2 access token for authorization: OAuth2PasswordBearer password
    accessToken: "YOUR ACCESS TOKEN",
  });
  const api = new UsersApi(config);

  const body = {
    // TeacherSettingsUpdate
    teacherSettingsUpdate: ...,
  } satisfies UpdateTeacherSettingsApiV1UsersProfessorsSettingsPutRequest;

  try {
    const data = await api.updateTeacherSettingsApiV1UsersProfessorsSettingsPut(body);
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
| **teacherSettingsUpdate** | [TeacherSettingsUpdate](TeacherSettingsUpdate.md) |  | |

### Return type

[**TeacherSettingsResponseSchema**](TeacherSettingsResponseSchema.md)

### Authorization

[OAuth2PasswordBearer password](../README.md#OAuth2PasswordBearer-password)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

